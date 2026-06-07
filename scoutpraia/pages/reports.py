from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
from sqlmodel import Session, select

from scoutpraia.core.database import create_db_and_tables, engine
from scoutpraia.models.event import Event
from scoutpraia.models.player import Player
from scoutpraia.models.report import Report
from scoutpraia.services.match_service import list_matches
from scoutpraia.services.report_service import (
    build_collective_report_payload,
    build_individual_report_payload,
    build_opponent_report_payload,
    generate_collective_report,
    generate_individual_report,
    generate_opponent_report,
)
from scoutpraia.ui_labels import column_label, display_value_label, kpi_label, report_type_label


def render() -> None:
    st.header("Relatórios")
    create_db_and_tables()

    with Session(engine) as session:
        matches = list_matches(session)
        if not matches:
            st.info("Nenhum jogo cadastrado. Cadastre um jogo antes de gerar relatórios.")
            return

        match_options = {
            _match_label(match): match.id
            for match in matches
        }
        selected_match_label = st.selectbox(
            "Jogo",
            options=list(match_options.keys()),
            key="reports_match",
        )
        match_id = match_options[selected_match_label]

        _render_kpi_preview(session, match_id)
        _render_report_generation(session, match_id)
        _render_existing_reports(session, match_id)


def _render_kpi_preview(session: Session, match_id: int) -> None:
    st.subheader("Prévia de KPIs")
    try:
        collective_payload = build_collective_report_payload(session, match_id)
        opponent_payload = build_opponent_report_payload(session, match_id)
    except ValueError as exc:
        st.info(str(exc))
        return

    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown("**Coletivo**")
        st.dataframe(
            _kpi_preview_rows(collective_payload["kpis"]),
            width="stretch",
        )
        _render_collective_nested_kpis(collective_payload["kpis"])
        warnings = collective_payload["kpis"].get("critical_warnings", [])
        if warnings:
            st.warning(" | ".join(warnings))
    with right_col:
        st.markdown("**Adversária**")
        st.dataframe(
            _kpi_preview_rows(opponent_payload["kpis"]),
            width="stretch",
        )
        warnings = opponent_payload["kpis"].get("critical_warnings", [])
        if warnings:
            st.warning(" | ".join(warnings))


def _render_report_generation(session: Session, match_id: int) -> None:
    st.subheader("Gerar relatórios")
    team_players = _players_with_team_events(session, match_id)
    player_options = {
        (
            f"{player.name} (#{player.shirt_number})"
            if player.shirt_number is not None
            else player.name
        ): player.id
        for player in team_players
    }

    collective_col, individual_col, opponent_col = st.columns(3)

    with collective_col:
        if st.button("Gerar coletivo", width="stretch"):
            try:
                report = generate_collective_report(session, match_id=match_id)
                st.success(f"Relatório coletivo gerado: {report.file_path}")
            except ValueError as exc:
                st.error(str(exc))

    with individual_col:
        selected_player_label = st.selectbox(
            "Atleta",
            options=list(player_options.keys()) if player_options else ["Sem atleta com evento"],
            key="report_player",
        )
        if st.button("Gerar individual", width="stretch"):
            if not player_options:
                st.info("Nenhuma atleta com evento disponível para relatório individual.")
            else:
                try:
                    report = generate_individual_report(
                        session,
                        match_id=match_id,
                        player_id=player_options[selected_player_label],
                    )
                    st.success(f"Relatório individual gerado: {report.file_path}")
                except ValueError as exc:
                    st.error(str(exc))

    with opponent_col:
        if st.button("Gerar adversária", width="stretch"):
            try:
                report = generate_opponent_report(session, match_id=match_id)
                st.success(f"Relatório de adversária gerado: {report.file_path}")
            except ValueError as exc:
                st.error(str(exc))


def _render_existing_reports(session: Session, match_id: int) -> None:
    st.subheader("Arquivos gerados")
    reports = list(
        session.exec(
            select(Report)
            .where(Report.match_id == match_id)
            .order_by(Report.generated_at.desc(), Report.id.desc())
        ).all()
    )
    if not reports:
        st.info("Nenhum relatório gerado para este jogo.")
        return

    st.caption(f"{len(reports)} relatório(s) gerado(s) para este jogo.")

    for report in reports:
        path = Path(report.file_path)
        report_label = report_type_label(report.report_type)
        st.markdown(f"**{report_label}** — `{report.file_path}`")
        cols = st.columns([1, 1, 2])
        with cols[0]:
            if path.exists():
                st.download_button(
                    label=f"Download {report_label}",
                    data=path.read_text(encoding="utf-8"),
                    file_name=path.name,
                    mime="text/html",
                    key=f"download_report_{report.id}",
                    width="stretch",
                )
        with cols[1]:
            if path.exists() and hasattr(st, "link_button"):
                st.link_button(
                    "Abrir HTML",
                    f"file://{path.resolve()}",
                    width="stretch",
                )
        with cols[2]:
            st.caption(
                f"Gerado em {report.generated_at.isoformat()} | arquivo {'presente' if path.exists() else 'ausente'}"
            )


def _players_with_team_events(session: Session, match_id: int) -> list[Player]:
    player_ids = [
        player_id
        for player_id in session.exec(
            select(Event.player_id)
            .where(Event.match_id == match_id, Event.team_side == "team")
            .distinct()
        ).all()
        if player_id is not None
    ]
    if not player_ids:
        return []
    return list(
        session.exec(
            select(Player)
            .where(Player.id.in_(player_ids))
            .order_by(Player.name)
        ).all()
    )


def _match_label(match) -> str:
    return f"Jogo {match.id} — {match.competition_name or 'sem competição'}"


def _display_value(value: object) -> object:
    if value is None:
        return "n/d"
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if isinstance(value, (list, tuple, set)):
        return json.dumps(list(value), ensure_ascii=False)
    return display_value_label(value)


def _kpi_preview_rows(kpis: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, value in kpis.items():
        if key == "critical_warnings" or isinstance(value, dict):
            continue
        rows.append(
            {
                column_label("metric"): kpi_label(key),
                column_label("value"): _display_text(value),
            }
        )
    return rows


def _render_collective_nested_kpis(kpis: dict[str, object]) -> None:
    set_performance = kpis.get("set_performance")
    if not isinstance(set_performance, dict) or not set_performance:
        return

    rows = []
    for set_number, values in set_performance.items():
        if not isinstance(values, dict):
            rows.append(
                {
                    column_label("set"): str(set_number),
                    column_label("value"): _display_text(values),
                }
            )
            continue
        rows.append(
            {
                column_label("set"): str(set_number),
                **{
                    kpi_label(metric): _display_text(metric_value)
                    for metric, metric_value in values.items()
                },
            }
        )

    st.caption("Detalhe por set")
    st.dataframe(rows, width="stretch")


def _display_text(value: object) -> str:
    return str(_display_value(value))
