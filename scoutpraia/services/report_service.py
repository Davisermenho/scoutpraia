from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlmodel import Session, select

from scoutpraia.core.config import settings
from scoutpraia.core.paths import ensure_storage_dirs, safe_join, safe_slug
from scoutpraia.models.clip import Clip
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, Possession, SetSegment
from scoutpraia.models.opponent import Opponent
from scoutpraia.models.player import Player
from scoutpraia.models.report import Report
from scoutpraia.models.taxonomy import EventDefinition, TaxonomyVersion
from scoutpraia.services.analytics_service import (
    collective_kpis,
    individual_kpis,
    opponent_kpis,
)
from scoutpraia.services.validation_service import validate_taxonomy_for_final_report
from scoutpraia.utils.datetime import utc_now
from scoutpraia.utils.timecode import seconds_to_timecode


TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
TEMPLATE_BY_TYPE = {
    "collective": "report_collective.html",
    "individual": "report_individual.html",
    "opponent": "report_opponent.html",
}


def render_report(template_dir: Path, template_name: str, payload: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_name)
    return template.render(**payload)


def build_collective_report_payload(
    session: Session,
    match_id: int,
    taxonomy_version_id: int | None = None,
    require_approved_taxonomy: bool = False,
) -> dict[str, object]:
    context = _build_match_report_context(
        session=session,
        match_id=match_id,
        taxonomy_version_id=taxonomy_version_id,
        require_approved_taxonomy=require_approved_taxonomy,
    )
    team_events = [event for event in context["events"] if event.team_side == "team"]
    return {
        **_base_payload(context, "collective"),
        "summary": {
            "team_events_total": len(team_events),
            "clips_total": len(context["clip_links"]),
            "players_with_events": len(
                {
                    event.player_id
                    for event in team_events
                    if event.player_id is not None
                }
            ),
        },
        "kpis": collective_kpis(
            context["events_frame"],
            possessions=context["possessions_frame"],
            set_segments=context["set_segments_frame"],
            taxonomy_status=context["taxonomy"].status,
            event_definitions=context["event_definitions_frame"],
        ),
        "clips": context["clip_links"],
    }


def build_individual_report_payload(
    session: Session,
    match_id: int,
    player_id: int,
    taxonomy_version_id: int | None = None,
    require_approved_taxonomy: bool = False,
) -> dict[str, object]:
    context = _build_match_report_context(
        session=session,
        match_id=match_id,
        taxonomy_version_id=taxonomy_version_id,
        require_approved_taxonomy=require_approved_taxonomy,
    )
    player = session.get(Player, player_id)
    if player is None:
        raise ValueError(f"Atleta não encontrada: {player_id}")

    kpis_by_player = individual_kpis(
        context["events_frame"],
        taxonomy_status=context["taxonomy"].status,
        event_definitions=context["event_definitions_frame"],
    )
    if player_id not in kpis_by_player:
        raise ValueError(
            f"Atleta {player_id} não possui eventos suficientes para relatório individual."
        )

    player_events = [
        event
        for event in context["events"]
        if event.team_side == "team" and event.player_id == player_id
    ]
    return {
        **_base_payload(context, "individual"),
        "player": {
            "id": player.id,
            "name": player.name,
            "shirt_number": player.shirt_number,
            "primary_role": player.primary_role,
        },
        "player_name": player.name,
        "summary": {
            "player_events_total": len(player_events),
            "clips_total": len(
                [clip for clip in context["clip_links"] if clip["player_id"] == player_id]
            ),
        },
        "kpis": kpis_by_player[player_id],
        "clips": [
            clip for clip in context["clip_links"] if clip["player_id"] == player_id
        ],
    }


def build_opponent_report_payload(
    session: Session,
    match_id: int,
    taxonomy_version_id: int | None = None,
    require_approved_taxonomy: bool = False,
) -> dict[str, object]:
    context = _build_match_report_context(
        session=session,
        match_id=match_id,
        taxonomy_version_id=taxonomy_version_id,
        require_approved_taxonomy=require_approved_taxonomy,
    )
    opponent_events = [
        event for event in context["events"] if event.team_side == "opponent"
    ]
    return {
        **_base_payload(context, "opponent"),
        "opponent_name": context["opponent_name"],
        "summary": {
            "opponent_events_total": len(opponent_events),
            "clips_total": len(
                [
                    clip
                    for clip in context["clip_links"]
                    if clip["team_side"] == "opponent"
                ]
            ),
        },
        "kpis": opponent_kpis(
            context["events_frame"],
            possessions=context["possessions_frame"],
            taxonomy_status=context["taxonomy"].status,
            event_definitions=context["event_definitions_frame"],
        ),
        "clips": [
            clip
            for clip in context["clip_links"]
            if clip["team_side"] == "opponent"
        ],
    }


def generate_collective_report(
    session: Session,
    match_id: int,
    taxonomy_version_id: int | None = None,
    output_dir: str | Path | None = None,
    require_approved_taxonomy: bool = False,
) -> Report:
    payload = build_collective_report_payload(
        session=session,
        match_id=match_id,
        taxonomy_version_id=taxonomy_version_id,
        require_approved_taxonomy=require_approved_taxonomy,
    )
    return _persist_report(
        session=session,
        match_id=match_id,
        report_type="collective",
        payload=payload,
        output_dir=output_dir,
    )


def generate_individual_report(
    session: Session,
    match_id: int,
    player_id: int,
    taxonomy_version_id: int | None = None,
    output_dir: str | Path | None = None,
    require_approved_taxonomy: bool = False,
) -> Report:
    payload = build_individual_report_payload(
        session=session,
        match_id=match_id,
        player_id=player_id,
        taxonomy_version_id=taxonomy_version_id,
        require_approved_taxonomy=require_approved_taxonomy,
    )
    return _persist_report(
        session=session,
        match_id=match_id,
        report_type="individual",
        payload=payload,
        output_dir=output_dir,
        subject_slug=safe_slug(payload["player_name"]),
    )


def generate_opponent_report(
    session: Session,
    match_id: int,
    taxonomy_version_id: int | None = None,
    output_dir: str | Path | None = None,
    require_approved_taxonomy: bool = False,
) -> Report:
    payload = build_opponent_report_payload(
        session=session,
        match_id=match_id,
        taxonomy_version_id=taxonomy_version_id,
        require_approved_taxonomy=require_approved_taxonomy,
    )
    return _persist_report(
        session=session,
        match_id=match_id,
        report_type="opponent",
        payload=payload,
        output_dir=output_dir,
        subject_slug=safe_slug(payload["opponent_name"]),
    )


def _persist_report(
    session: Session,
    match_id: int,
    report_type: str,
    payload: dict[str, object],
    output_dir: str | Path | None = None,
    subject_slug: str | None = None,
) -> Report:
    report_dir = Path(output_dir) if output_dir is not None else settings.report_dir
    ensure_storage_dirs()
    report_dir.mkdir(parents=True, exist_ok=True)

    filename = _report_filename(
        match_id=match_id,
        report_type=report_type,
        generated_at=str(payload["generated_at"]),
        subject_slug=subject_slug,
    )
    report_path = safe_join(report_dir, filename)

    final_payload = _payload_with_report_paths(payload, report_path)
    final_payload["report_file"] = str(report_path)
    final_payload["report_file_name"] = report_path.name

    rendered = render_report(
        TEMPLATE_DIR,
        TEMPLATE_BY_TYPE[report_type],
        final_payload,
    )
    report_path.write_text(rendered, encoding="utf-8")

    persisted_report = Report(
        match_id=match_id,
        report_type=report_type,
        file_path=str(report_path),
        payload_json=json.dumps(
            final_payload,
            ensure_ascii=False,
            sort_keys=True,
        ),
    )
    session.add(persisted_report)
    session.commit()
    session.refresh(persisted_report)
    return persisted_report


def _build_match_report_context(
    session: Session,
    match_id: int,
    taxonomy_version_id: int | None,
    require_approved_taxonomy: bool,
) -> dict[str, object]:
    match = session.get(Match, match_id)
    if match is None:
        raise ValueError(f"Jogo não encontrado: {match_id}")

    events = list(
        session.exec(
            select(Event)
            .where(Event.match_id == match_id)
            .order_by(Event.timestamp_second, Event.id)
        ).all()
    )
    if not events:
        raise ValueError(f"Jogo {match_id} não possui eventos para relatório.")

    resolved_taxonomy_id = _resolve_taxonomy_version_id(events, taxonomy_version_id)
    taxonomy = session.get(TaxonomyVersion, resolved_taxonomy_id)
    if taxonomy is None:
        raise ValueError(f"Taxonomia não encontrada: {resolved_taxonomy_id}")
    if require_approved_taxonomy:
        validate_taxonomy_for_final_report(session, taxonomy.id)

    filtered_events = [
        event for event in events if event.taxonomy_version_id == resolved_taxonomy_id
    ]
    if not filtered_events:
        raise ValueError(
            f"Jogo {match_id} não possui eventos para a taxonomia {resolved_taxonomy_id}."
        )

    possessions = list(
        session.exec(
            select(Possession)
            .where(Possession.match_id == match_id)
            .order_by(Possession.start_second, Possession.id)
        ).all()
    )
    set_segments = list(
        session.exec(
            select(SetSegment)
            .where(SetSegment.match_id == match_id)
            .order_by(SetSegment.set_number, SetSegment.id)
        ).all()
    )
    event_definitions = list(
        session.exec(
            select(EventDefinition).where(
                EventDefinition.taxonomy_version_id == taxonomy.id,
                EventDefinition.active == True,
            )
        ).all()
    )
    clips = list(
        session.exec(select(Clip).where(Clip.match_id == match_id).order_by(Clip.id)).all()
    )
    event_by_id = {event.id: event for event in filtered_events if event.id is not None}

    clip_links = [
        clip_link
        for clip_link in (
            _build_clip_link(clip, event_by_id) for clip in clips
        )
        if clip_link is not None
    ]

    opponent = session.get(Opponent, match.opponent_id) if match.opponent_id else None

    return {
        "match": match,
        "opponent": opponent,
        "opponent_name": opponent.name if opponent is not None else "Adversária não cadastrada",
        "taxonomy": taxonomy,
        "events": filtered_events,
        "events_frame": _to_frame(filtered_events),
        "possessions_frame": _to_frame(possessions),
        "set_segments_frame": _to_frame(set_segments),
        "event_definitions_frame": _to_frame(event_definitions),
        "clip_links": clip_links,
    }


def _base_payload(
    context: dict[str, object],
    report_type: str,
) -> dict[str, object]:
    match = context["match"]
    taxonomy = context["taxonomy"]
    match_date = match.match_date.isoformat() if match.match_date is not None else None
    generated_at = utc_now().isoformat()
    return {
        "report_type": report_type,
        "generated_at": generated_at,
        "match": {
            "id": match.id,
            "competition_name": match.competition_name,
            "phase": match.phase,
            "match_date": match_date,
            "final_score_team": match.final_score_team,
            "final_score_opponent": match.final_score_opponent,
            "notes": match.notes,
        },
        "taxonomy_version": taxonomy.name,
        "taxonomy_status": taxonomy.status,
        "critical_warnings": [],
        "opponent_name": context["opponent_name"],
    }


def _resolve_taxonomy_version_id(
    events: list[Event],
    explicit_taxonomy_version_id: int | None,
) -> int:
    if explicit_taxonomy_version_id is not None:
        return explicit_taxonomy_version_id

    taxonomy_ids = sorted({event.taxonomy_version_id for event in events})
    if len(taxonomy_ids) != 1:
        raise ValueError(
            "O jogo possui múltiplas versões de taxonomia; informe taxonomy_version_id."
        )
    return taxonomy_ids[0]


def _to_frame(rows: list[object]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame([row.model_dump() for row in rows])


def _build_clip_link(
    clip: Clip,
    event_by_id: dict[int, Event],
) -> dict[str, object] | None:
    if clip.event_id is None:
        return None
    event = event_by_id.get(clip.event_id)
    if event is None:
        return None

    clip_path = Path(clip.clip_path)
    if not clip_path.exists():
        return None

    return {
        "clip_id": clip.id,
        "event_id": event.id,
        "player_id": clip.player_id,
        "label": clip.label,
        "team_side": event.team_side,
        "timestamp": seconds_to_timecode(event.timestamp_second),
        "clip_path": str(clip_path),
    }


def _report_filename(
    match_id: int,
    report_type: str,
    generated_at: str,
    subject_slug: str | None = None,
) -> str:
    timestamp_slug = safe_slug(generated_at.replace("+00:00", "utc"))
    subject_part = f"_{subject_slug}" if subject_slug else ""
    return f"match-{match_id}_{report_type}{subject_part}_{timestamp_slug}.html"


def _payload_with_report_paths(
    payload: dict[str, object],
    report_path: Path,
) -> dict[str, object]:
    final_payload = dict(payload)
    clips = []
    for clip in payload.get("clips", []):
        clip_payload = dict(clip)
        clip_path = Path(str(clip_payload.pop("clip_path")))
        clip_payload["relative_path"] = os.path.relpath(
            clip_path.resolve(),
            start=report_path.parent.resolve(),
        ).replace(os.sep, "/")
        clips.append(clip_payload)
    final_payload["clips"] = clips
    return final_payload
