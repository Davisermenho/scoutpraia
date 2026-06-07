from __future__ import annotations

from collections.abc import Iterable

import streamlit as st
from sqlmodel import Session, select

from scoutpraia.core.database import create_db_and_tables, engine
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, Possession, SetSegment
from scoutpraia.models.player import Player
from scoutpraia.models.taxonomy import EventDefinition, TaxonomyVersion
from scoutpraia.services.event_service import (
    create_event,
    delete_event,
    list_events_by_match,
    update_event,
)
from scoutpraia.services.match_service import list_match_roster, list_matches, list_players
from scoutpraia.ui_labels import (
    column_label,
    event_type_label,
    team_side_label,
    zone_label,
)
from scoutpraia.utils.zones import ZONES


QUICK_EVENT_TYPES = [
    "shot_attempt",
    "goal_scored",
    "two_point_goal",
    "technical_error",
    "turnover",
    "assist",
    "defensive_stop",
    "steal",
    "block",
    "save",
    "goal_conceded",
    "shootout_goal",
]


def render() -> None:
    st.header("Marcação")
    create_db_and_tables()
    _init_state()

    with Session(engine) as session:
        matches = list_matches(session)
        if not matches:
            st.info("Nenhum jogo cadastrado. Cadastre um jogo na página Jogos.")
            return

        match = _select_match(matches)
        if match is None:
            st.info("Selecione um jogo para iniciar a marcação.")
            return

        _render_match_context(match)

        taxonomies = list(
            session.exec(select(TaxonomyVersion).order_by(TaxonomyVersion.id.desc())).all()
        )
        if not taxonomies:
            st.error("Nenhuma taxonomia disponível.")
            return

        taxonomy = _select_taxonomy(taxonomies)
        definitions = list(
            session.exec(
                select(EventDefinition).where(
                    EventDefinition.taxonomy_version_id == taxonomy.id,
                    EventDefinition.active == True,
                )
            ).all()
        )
        event_types = sorted(
            {
                definition.event_type
                for definition in definitions
                if definition.event_type and definition.event_type.strip()
            }
        )
        if not event_types:
            st.error("A taxonomia selecionada não possui eventos ativos.")
            return

        _sync_selected_event_type(event_types)
        _render_management_tools(session, match.id)

        main_col, side_col = st.columns([2, 1], gap="large")
        with main_col:
            _render_video(match)
            _render_quick_event_buttons(event_types)
            _render_event_form(
                session=session,
                match=match,
                taxonomy=taxonomy,
                event_types=event_types,
            )
        with side_col:
            _render_event_history(session, match.id, limit=20)
            _render_last_event_editor(
                session=session,
                match_id=match.id,
                taxonomy_id=taxonomy.id,
                event_types=event_types,
            )


def _init_state() -> None:
    st.session_state.setdefault("tagging_event_type", "shot_attempt")
    st.session_state.setdefault("tagging_timestamp_second", 0.0)
    st.session_state.setdefault("tagging_team_side", "team")


def _select_match(matches: list[Match]) -> Match | None:
    options = {
        _match_label(match): match
        for match in matches
    }
    selected_label = st.selectbox(
        "Jogo",
        options=list(options.keys()),
        key="tagging_match",
    )
    return options.get(selected_label)


def _select_taxonomy(taxonomies: list[TaxonomyVersion]) -> TaxonomyVersion:
    options = {
        f"{taxonomy.name} ({taxonomy.status})": taxonomy
        for taxonomy in taxonomies
    }
    default_index = 0
    selected_label = st.selectbox(
        "Taxonomia",
        options=list(options.keys()),
        index=default_index,
        key="tagging_taxonomy",
    )
    return options[selected_label]


def _render_match_context(match: Match) -> None:
    st.caption(
        "Use timestamp manual e botões rápidos. O player nativo do Streamlit não expõe "
        "controle fino do tempo real no MVP."
    )
    details = [
        f"Jogo {match.id}",
        match.competition_name or "sem competição",
    ]
    if match.phase:
        details.append(match.phase)
    st.write(" | ".join(details))


def _render_video(match: Match) -> None:
    if not match.video_path:
        st.warning("Este jogo não possui vídeo vinculado.")
        return
    st.video(match.video_path)


def _render_quick_event_buttons(event_types: list[str]) -> None:
    st.subheader("Botões rápidos")
    quick_types = [event_type for event_type in QUICK_EVENT_TYPES if event_type in event_types]
    if not quick_types:
        st.info("Nenhum evento rápido disponível para esta taxonomia.")
        return

    button_columns = st.columns(3)
    for index, event_type in enumerate(quick_types):
        with button_columns[index % 3]:
            if st.button(
                event_type_label(event_type),
                key=f"quick_event_{event_type}",
                width="stretch",
            ):
                st.session_state["tagging_event_type"] = event_type


def _render_management_tools(session: Session, match_id: int) -> None:
    with st.expander("Sets e posses", expanded=False):
        left_col, right_col = st.columns(2)
        with left_col:
            with st.form("create_set_form"):
                st.markdown("**Novo set**")
                set_number = st.number_input("Número do set", min_value=1, value=1)
                start_second = st.number_input(
                    "Início do set (s)",
                    min_value=0.0,
                    value=0.0,
                    step=0.1,
                )
                end_second = st.number_input(
                    "Fim do set (s)",
                    min_value=0.0,
                    value=0.0,
                    step=0.1,
                )
                submitted = st.form_submit_button("Salvar set")
                if submitted:
                    set_segment = SetSegment(
                        match_id=match_id,
                        set_number=int(set_number),
                        start_second=start_second or None,
                        end_second=end_second or None,
                    )
                    session.add(set_segment)
                    session.commit()
                    session.refresh(set_segment)
                    st.success(f"Set {set_segment.set_number} salvo.")
        with right_col:
            set_options = _set_options(session, match_id)
            with st.form("create_possession_form"):
                st.markdown("**Nova posse**")
                possession_team_side = st.radio(
                    "Equipe da posse",
                    options=["team", "opponent"],
                    horizontal=True,
                    key="new_possession_team_side",
                    format_func=team_side_label,
                )
                selected_set_label = st.selectbox(
                    "Set da posse",
                    options=list(set_options.keys()),
                    key="new_possession_set",
                )
                start_second = st.number_input(
                    "Início da posse (s)",
                    min_value=0.0,
                    value=0.0,
                    step=0.1,
                    key="new_possession_start",
                )
                end_second = st.number_input(
                    "Fim da posse (s)",
                    min_value=0.0,
                    value=0.0,
                    step=0.1,
                    key="new_possession_end",
                )
                result = st.text_input("Resultado da posse", key="new_possession_result")
                points_scored = st.number_input(
                    "Pontos feitos",
                    min_value=0,
                    max_value=2,
                    value=0,
                    key="new_possession_points_scored",
                )
                points_conceded = st.number_input(
                    "Pontos sofridos",
                    min_value=0,
                    max_value=2,
                    value=0,
                    key="new_possession_points_conceded",
                )
                submitted = st.form_submit_button("Salvar posse")
                if submitted:
                    possession = Possession(
                        match_id=match_id,
                        set_id=set_options[selected_set_label],
                        team_side=possession_team_side,
                        start_second=start_second or None,
                        end_second=end_second or None,
                        result=result or None,
                        points_scored=int(points_scored),
                        points_conceded=int(points_conceded),
                    )
                    session.add(possession)
                    session.commit()
                    session.refresh(possession)
                    st.success(f"Posse {possession.id} salva.")


def _render_event_form(
    session: Session,
    match: Match,
    taxonomy: TaxonomyVersion,
    event_types: list[str],
) -> None:
    st.subheader("Registrar evento")
    players = _players_for_match(session, match.id)
    player_options = _player_options(players)
    set_options = _set_options(session, match.id)
    selected_set_label = st.selectbox(
        "Set",
        options=list(set_options.keys()),
        key="tagging_set",
    )
    selected_set_id = set_options[selected_set_label]

    possession_options = _possession_options(session, match.id, selected_set_id)
    with st.form("create_event_form"):
        timestamp_second = st.number_input(
            "Timestamp manual (s)",
            min_value=0.0,
            value=float(st.session_state.get("tagging_timestamp_second", 0.0)),
            step=0.1,
        )
        event_type = st.selectbox(
            "Evento",
            options=event_types,
            index=event_types.index(st.session_state["tagging_event_type"]),
            format_func=event_type_label,
        )
        team_side = st.radio(
            "Lado",
            options=["team", "opponent"],
            horizontal=True,
            index=0 if st.session_state.get("tagging_team_side") == "team" else 1,
            format_func=team_side_label,
        )
        player_label = st.selectbox(
            "Atleta",
            options=list(player_options.keys()),
        )
        secondary_player_label = st.selectbox(
            "Atleta secundária",
            options=list(player_options.keys()),
            key="secondary_player_label",
        )
        zone_label = st.selectbox(
            "Zona",
            options=["Sem zona"] + sorted(ZONES),
            format_func=_zone_option_label,
        )
        possession_label = st.selectbox(
            "Posse",
            options=list(possession_options.keys()),
        )
        points_value = st.selectbox("Pontos", options=[0, 1, 2], index=0)
        event_subtype = st.text_input("Subtipo")
        outcome = st.text_input("Desfecho")
        notes = st.text_area("Notas")
        submitted = st.form_submit_button("Salvar evento")

        if submitted:
            try:
                created = create_event(
                    session,
                    Event(
                        match_id=match.id,
                        set_id=selected_set_id,
                        possession_id=possession_options[possession_label],
                        taxonomy_version_id=taxonomy.id,
                        event_type=event_type,
                        event_subtype=event_subtype or None,
                        player_id=player_options[player_label],
                        secondary_player_id=player_options[secondary_player_label],
                        team_side=team_side,
                        timestamp_second=float(timestamp_second),
                        outcome=outcome or None,
                        zone=None if zone_label == "Sem zona" else zone_label,
                        points_value=int(points_value),
                        notes=notes or None,
                    ),
                )
                st.session_state["tagging_event_type"] = created.event_type
                st.session_state["tagging_timestamp_second"] = float(created.timestamp_second)
                st.session_state["tagging_team_side"] = created.team_side
                st.success(f"Evento {created.id} salvo.")
            except ValueError as exc:
                st.error(str(exc))


def _render_event_history(session: Session, match_id: int, limit: int) -> None:
    st.subheader("Histórico recente")
    events = list_events_by_match(session, match_id)
    if not events:
        st.info("Nenhum evento salvo para este jogo.")
        return

    players_by_id = {
        player.id: player
        for player in list_players(session, active_only=False)
    }
    st.dataframe(
        [
            {
                column_label("id"): event.id,
                column_label("timestamp"): round(event.timestamp_second, 1),
                column_label("event_type"): event_type_label(event.event_type),
                column_label("player"): players_by_id[event.player_id].name
                if event.player_id in players_by_id
                else None,
                column_label("team_side"): team_side_label(event.team_side),
                column_label("zone"): _zone_option_label(event.zone),
                column_label("points_value"): event.points_value,
            }
            for event in events[-limit:]
        ],
        width="stretch",
    )


def _render_last_event_editor(
    session: Session,
    match_id: int,
    taxonomy_id: int,
    event_types: list[str],
) -> None:
    events = list_events_by_match(session, match_id)
    if not events:
        return

    players = _players_for_match(session, match_id)
    player_options = _player_options(players)
    inverse_player_options = {value: label for label, value in player_options.items()}
    set_options = _set_options(session, match_id)
    inverse_set_options = {value: label for label, value in set_options.items()}
    last_event = events[-1]
    st.subheader("Editar ou excluir último evento")

    with st.form("edit_last_event_form"):
        timestamp_second = st.number_input(
            "Timestamp do último evento (s)",
            min_value=0.0,
            value=float(last_event.timestamp_second),
            step=0.1,
        )
        event_type = st.selectbox(
            "Evento do último registro",
            options=event_types,
            index=event_types.index(last_event.event_type),
            format_func=event_type_label,
        )
        team_side = st.radio(
            "Lado do último evento",
            options=["team", "opponent"],
            horizontal=True,
            index=0 if last_event.team_side == "team" else 1,
            format_func=team_side_label,
        )
        player_label = st.selectbox(
            "Atleta do último evento",
            options=list(player_options.keys()),
            index=_option_index(
                list(player_options.keys()),
                inverse_player_options.get(last_event.player_id, "Sem atleta"),
            ),
        )
        zone_label = st.selectbox(
            "Zona do último evento",
            options=["Sem zona"] + sorted(ZONES),
            index=_option_index(
                ["Sem zona"] + sorted(ZONES),
                last_event.zone or "Sem zona",
            ),
            format_func=_zone_option_label,
        )
        set_label = st.selectbox(
            "Set do último evento",
            options=list(set_options.keys()),
            index=_option_index(
                list(set_options.keys()),
                inverse_set_options.get(last_event.set_id, "Sem set"),
            ),
        )
        points_value = st.selectbox(
            "Pontos do último evento",
            options=[0, 1, 2],
            index=[0, 1, 2].index(int(last_event.points_value)),
        )
        event_subtype = st.text_input("Subtipo do último evento", value=last_event.event_subtype or "")
        outcome = st.text_input("Desfecho do último evento", value=last_event.outcome or "")
        notes = st.text_area("Notas do último evento", value=last_event.notes or "")
        update_submitted = st.form_submit_button("Atualizar último evento")
        if update_submitted:
            try:
                updated = update_event(
                    session,
                    last_event.id,
                    set_id=set_options[set_label],
                    taxonomy_version_id=taxonomy_id,
                    event_type=event_type,
                    player_id=player_options[player_label],
                    team_side=team_side,
                    timestamp_second=float(timestamp_second),
                    zone=None if zone_label == "Sem zona" else zone_label,
                    points_value=int(points_value),
                    event_subtype=event_subtype or None,
                    outcome=outcome or None,
                    notes=notes or None,
                )
                st.success(f"Evento {updated.id} atualizado.")
            except ValueError as exc:
                st.error(str(exc))

    if st.button("Excluir último evento", key="delete_last_event", type="secondary"):
        deleted = delete_event(session, last_event.id)
        if deleted:
            st.success(f"Evento {last_event.id} excluído.")
        else:
            st.error("Falha ao excluir o último evento.")


def _players_for_match(session: Session, match_id: int) -> list[Player]:
    roster_entries = list_match_roster(session, match_id)
    players_by_id = {player.id: player for player in list_players(session, active_only=False)}
    players = [
        players_by_id[entry.player_id]
        for entry in roster_entries
        if entry.player_id in players_by_id
    ]
    if players:
        return players
    return list_players(session, active_only=False)


def _player_options(players: Iterable[Player]) -> dict[str, int | None]:
    options: dict[str, int | None] = {"Sem atleta": None}
    for player in players:
        label = (
            f"{player.name} (#{player.shirt_number})"
            if player.shirt_number is not None
            else player.name
        )
        options[label] = player.id
    return options


def _set_options(session: Session, match_id: int) -> dict[str, int | None]:
    sets = list(
        session.exec(
            select(SetSegment)
            .where(SetSegment.match_id == match_id)
            .order_by(SetSegment.set_number, SetSegment.id)
        ).all()
    )
    options: dict[str, int | None] = {"Sem set": None}
    for set_segment in sets:
        options[f"Set {set_segment.set_number} (id {set_segment.id})"] = set_segment.id
    return options


def _possession_options(
    session: Session,
    match_id: int,
    set_id: int | None,
) -> dict[str, int | None]:
    statement = select(Possession).where(Possession.match_id == match_id)
    if set_id is not None:
        statement = statement.where(Possession.set_id == set_id)
    possessions = list(
        session.exec(statement.order_by(Possession.id)).all()
    )
    options: dict[str, int | None] = {"Sem posse": None}
    for possession in possessions:
        options[
            f"Posse {possession.id} — {team_side_label(possession.team_side)}"
        ] = possession.id
    return options


def _option_index(options: list[str], target: str) -> int:
    if target in options:
        return options.index(target)
    return 0


def _sync_selected_event_type(event_types: list[str]) -> None:
    if st.session_state["tagging_event_type"] not in event_types:
        st.session_state["tagging_event_type"] = event_types[0]


def _zone_option_label(value: str | None) -> str:
    if value in {None, "Sem zona"}:
        return "Sem zona"
    return zone_label(value)


def _match_label(match: Match) -> str:
    return f"Jogo {match.id} — {match.competition_name or 'sem competição'}"
