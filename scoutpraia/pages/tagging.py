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
from scoutpraia.services.match_service import (
    delete_possession,
    delete_set_segment,
    list_match_roster,
    list_matches,
    list_players,
    update_possession,
    update_set_segment,
)
from scoutpraia.ui_labels import (
    column_label,
    event_type_label,
    team_side_label,
    zone_label,
)
from scoutpraia.utils.timecode import format_seconds_for_input, timecode_to_seconds
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
TIME_INPUT_HELP = "Aceita segundos, MM:SS ou HH:MM:SS. Exemplos: 145, 02:25, 01:02:25, 02:25.4."


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
            _render_event_editor(
                session=session,
                match_id=match.id,
                taxonomy_id=taxonomy.id,
                event_types=event_types,
            )


def _init_state() -> None:
    st.session_state.setdefault("tagging_event_type", "shot_attempt")
    st.session_state.setdefault("tagging_timestamp_second", 0.0)
    st.session_state.setdefault(
        "tagging_timestamp_input",
        format_seconds_for_input(st.session_state["tagging_timestamp_second"]),
    )
    st.session_state.setdefault("tagging_team_side", "team")
    st.session_state.setdefault("tagging_set", None)
    st.session_state.setdefault("tagging_player", None)
    st.session_state.setdefault("tagging_secondary_player", None)
    st.session_state.setdefault("tagging_zone", None)
    st.session_state.setdefault("tagging_possession", None)
    st.session_state.setdefault("tagging_points", 0)
    st.session_state.setdefault("tagging_event_subtype", "")
    st.session_state.setdefault("tagging_outcome", "")
    st.session_state.setdefault("tagging_notes", "")
    st.session_state.setdefault("edit_event_id", None)
    st.session_state.setdefault("pending_new_set_state", None)
    st.session_state.setdefault("pending_new_possession_state", None)
    st.session_state.setdefault("management_success_message", None)


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
        success_message = st.session_state.pop("management_success_message", None)
        if success_message:
            st.success(success_message)
        left_col, right_col = st.columns(2)
        with left_col:
            next_set_number = _next_set_number(session, match_id)
            _sync_new_set_form_state(next_set_number)
            with st.form("create_set_form"):
                st.markdown("**Novo set**")
                set_number = st.number_input(
                    "Número do set",
                    min_value=1,
                    key="new_set_number",
                )
                start_input = st.text_input(
                    "Início do set",
                    key="new_set_start",
                    help=TIME_INPUT_HELP,
                )
                _render_time_input_preview(start_input)
                end_input = st.text_input(
                    "Fim do set",
                    key="new_set_end",
                    help=TIME_INPUT_HELP,
                )
                _render_time_input_preview(end_input)
                submitted = st.form_submit_button("Salvar set")
                if submitted:
                    try:
                        start_second = _parse_time_input(start_input, "Início do set")
                        end_second = _parse_time_input(end_input, "Fim do set")
                        set_segment = SetSegment(
                            match_id=match_id,
                            set_number=int(set_number),
                            start_second=start_second,
                            end_second=end_second,
                        )
                        session.add(set_segment)
                        session.commit()
                        session.refresh(set_segment)
                        st.session_state["pending_new_set_state"] = {
                            "new_set_number": int(set_segment.set_number) + 1,
                            "new_set_start": format_seconds_for_input(0.0),
                            "new_set_end": format_seconds_for_input(0.0),
                        }
                        st.session_state["management_success_message"] = (
                            f"Set {set_segment.set_number} salvo."
                        )
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))
            set_options = _set_options(session, match_id)
            editable_set_ids = [
                set_id for set_id in set_options.values() if set_id is not None
            ]
            if editable_set_ids:
                selected_set_id = st.selectbox(
                    "Set para editar ou excluir",
                    options=editable_set_ids,
                    index=len(editable_set_ids) - 1,
                    format_func=lambda set_id: _set_editor_label(
                        session.get(SetSegment, set_id)
                    ),
                    key="edit_set_id",
                )
                selected_set = session.get(SetSegment, selected_set_id)
                if selected_set is not None:
                    with st.form("edit_set_form"):
                        st.markdown("**Editar set selecionado**")
                        set_number = st.number_input(
                            "Número do set selecionado",
                            min_value=1,
                            value=int(selected_set.set_number),
                        )
                        start_input = st.text_input(
                            "Início do set selecionado",
                            value=format_seconds_for_input(selected_set.start_second),
                            help=TIME_INPUT_HELP,
                        )
                        _render_time_input_preview(start_input)
                        end_input = st.text_input(
                            "Fim do set selecionado",
                            value=format_seconds_for_input(selected_set.end_second),
                            help=TIME_INPUT_HELP,
                        )
                        _render_time_input_preview(end_input)
                        submitted = st.form_submit_button("Atualizar set selecionado")
                        if submitted:
                            try:
                                start_second = _parse_time_input(
                                    start_input, "Início do set selecionado"
                                )
                                end_second = _parse_time_input(
                                    end_input, "Fim do set selecionado"
                                )
                                updated = update_set_segment(
                                    session,
                                    selected_set.id,
                                    set_number=int(set_number),
                                    start_second=start_second,
                                    end_second=end_second,
                                )
                                st.success(f"Set {updated.set_number} atualizado.")
                            except ValueError as exc:
                                st.error(str(exc))

                    if st.button(
                        "Excluir set selecionado",
                        key="delete_selected_set",
                        type="secondary",
                    ):
                        try:
                            deleted = delete_set_segment(session, selected_set.id)
                            if deleted:
                                st.success(f"Set {selected_set.id} excluído.")
                        except ValueError as exc:
                            st.error(str(exc))
        with right_col:
            set_options = _set_options(session, match_id)
            _sync_new_possession_form_state(set_options)
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
                start_input = st.text_input(
                    "Início da posse",
                    key="new_possession_start",
                    help=TIME_INPUT_HELP,
                )
                _render_time_input_preview(start_input)
                end_input = st.text_input(
                    "Fim da posse",
                    key="new_possession_end",
                    help=TIME_INPUT_HELP,
                )
                _render_time_input_preview(end_input)
                result = st.text_input("Resultado da posse", key="new_possession_result")
                points_scored = st.number_input(
                    "Pontos feitos",
                    min_value=0,
                    max_value=2,
                    key="new_possession_points_scored",
                )
                points_conceded = st.number_input(
                    "Pontos sofridos",
                    min_value=0,
                    max_value=2,
                    key="new_possession_points_conceded",
                )
                submitted = st.form_submit_button("Salvar posse")
                if submitted:
                    try:
                        start_second = _parse_time_input(start_input, "Início da posse")
                        end_second = _parse_time_input(end_input, "Fim da posse")
                        possession = Possession(
                            match_id=match_id,
                            set_id=set_options[selected_set_label],
                            team_side=possession_team_side,
                            start_second=start_second,
                            end_second=end_second,
                            result=result or None,
                            points_scored=int(points_scored),
                            points_conceded=int(points_conceded),
                        )
                        session.add(possession)
                        session.commit()
                        session.refresh(possession)
                        st.session_state["pending_new_possession_state"] = {
                            "new_possession_team_side": possession_team_side,
                            "new_possession_set": selected_set_label,
                            "new_possession_start": format_seconds_for_input(0.0),
                            "new_possession_end": format_seconds_for_input(0.0),
                            "new_possession_result": "",
                            "new_possession_points_scored": 0,
                            "new_possession_points_conceded": 0,
                        }
                        st.session_state["management_success_message"] = (
                            f"Posse {possession.id} salva."
                        )
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))
            possession_options = _possession_options(session, match_id, None)
            editable_possession_ids = [
                possession_id
                for possession_id in possession_options.values()
                if possession_id is not None
            ]
            if editable_possession_ids:
                selected_possession_id = st.selectbox(
                    "Posse para editar ou excluir",
                    options=editable_possession_ids,
                    index=len(editable_possession_ids) - 1,
                    format_func=lambda possession_id: _possession_editor_label(
                        session, session.get(Possession, possession_id)
                    ),
                    key="edit_possession_id",
                )
                selected_possession = session.get(Possession, selected_possession_id)
                if selected_possession is not None:
                    selected_set_labels = list(set_options.keys())
                    selected_set_label = next(
                        (
                            label
                            for label, set_id in set_options.items()
                            if set_id == selected_possession.set_id
                        ),
                        "Sem set",
                    )
                    with st.form("edit_possession_form"):
                        st.markdown("**Editar posse selecionada**")
                        possession_team_side = st.radio(
                            "Equipe da posse selecionada",
                            options=["team", "opponent"],
                            horizontal=True,
                            index=0 if selected_possession.team_side == "team" else 1,
                            format_func=team_side_label,
                        )
                        selected_set_label = st.selectbox(
                            "Set da posse selecionada",
                            options=selected_set_labels,
                            index=_option_index(selected_set_labels, selected_set_label),
                        )
                        start_input = st.text_input(
                            "Início da posse selecionada",
                            value=format_seconds_for_input(selected_possession.start_second),
                            help=TIME_INPUT_HELP,
                        )
                        _render_time_input_preview(start_input)
                        end_input = st.text_input(
                            "Fim da posse selecionada",
                            value=format_seconds_for_input(selected_possession.end_second),
                            help=TIME_INPUT_HELP,
                        )
                        _render_time_input_preview(end_input)
                        result = st.text_input(
                            "Resultado da posse selecionada",
                            value=selected_possession.result or "",
                        )
                        points_scored = st.number_input(
                            "Pontos feitos da posse",
                            min_value=0,
                            max_value=2,
                            value=int(selected_possession.points_scored),
                        )
                        points_conceded = st.number_input(
                            "Pontos sofridos da posse",
                            min_value=0,
                            max_value=2,
                            value=int(selected_possession.points_conceded),
                        )
                        submitted = st.form_submit_button("Atualizar posse selecionada")
                        if submitted:
                            try:
                                start_second = _parse_time_input(
                                    start_input, "Início da posse selecionada"
                                )
                                end_second = _parse_time_input(
                                    end_input, "Fim da posse selecionada"
                                )
                                updated = update_possession(
                                    session,
                                    selected_possession.id,
                                    set_id=set_options[selected_set_label],
                                    team_side=possession_team_side,
                                    start_second=start_second,
                                    end_second=end_second,
                                    result=result,
                                    points_scored=int(points_scored),
                                    points_conceded=int(points_conceded),
                                )
                                st.success(f"Posse {updated.id} atualizada.")
                            except ValueError as exc:
                                st.error(str(exc))

                    if st.button(
                        "Excluir posse selecionada",
                        key="delete_selected_possession",
                        type="secondary",
                    ):
                        try:
                            deleted = delete_possession(session, selected_possession.id)
                            if deleted:
                                st.success(f"Posse {selected_possession.id} excluída.")
                        except ValueError as exc:
                            st.error(str(exc))


def _render_event_form(
    session: Session,
    match: Match,
    taxonomy: TaxonomyVersion,
    event_types: list[str],
) -> None:
    st.subheader("Registrar evento")
    _sync_event_form_state(session, match.id)
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
    if st.session_state.get("tagging_possession") not in possession_options:
        st.session_state["tagging_possession"] = _default_possession_label(possession_options)

    st.caption("Ajuste rápido do timestamp")
    time_buttons = st.columns(4)
    quick_time_buttons = [
        ("-1s", -1.0),
        ("-0.5s", -0.5),
        ("+0.5s", 0.5),
        ("+1s", 1.0),
    ]
    for column, (label, delta) in zip(time_buttons, quick_time_buttons, strict=True):
        with column:
            if st.button(label, key=f"shift_timestamp_{label}"):
                _shift_tagging_timestamp(delta)

    with st.form("create_event_form"):
        timestamp_input = st.text_input(
            "Timestamp do vídeo",
            key="tagging_timestamp_input",
            help=TIME_INPUT_HELP,
        )
        _render_time_input_preview(timestamp_input)
        event_type = st.selectbox(
            "Evento",
            options=event_types,
            key="tagging_event_type",
            format_func=event_type_label,
        )
        team_side = st.radio(
            "Lado",
            options=["team", "opponent"],
            horizontal=True,
            key="tagging_team_side",
            format_func=team_side_label,
        )
        player_label = st.selectbox(
            "Atleta",
            options=list(player_options.keys()),
            key="tagging_player",
        )
        secondary_player_label = st.selectbox(
            "Atleta secundária",
            options=list(player_options.keys()),
            key="tagging_secondary_player",
        )
        zone_label = st.selectbox(
            "Zona",
            options=["Sem zona"] + sorted(ZONES),
            key="tagging_zone",
            format_func=_zone_option_label,
        )
        possession_label = st.selectbox(
            "Posse",
            options=list(possession_options.keys()),
            key="tagging_possession",
        )
        points_value = st.selectbox("Pontos", options=[0, 1, 2], key="tagging_points")
        event_subtype = st.text_input("Subtipo", key="tagging_event_subtype")
        outcome = st.text_input("Desfecho", key="tagging_outcome")
        notes = st.text_area("Notas", key="tagging_notes")
        submitted = st.form_submit_button("Salvar evento")

        if submitted:
            try:
                timestamp_second = _parse_time_input(timestamp_input, "Timestamp do vídeo")
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
                st.session_state["tagging_timestamp_second"] = float(created.timestamp_second)
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


def _render_event_editor(
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
    filter_set_options = _set_filter_options(session, match_id)
    inverse_set_options = {value: label for label, value in set_options.items()}
    possession_options = _possession_options(session, match_id, None)
    inverse_possession_options = {
        value: label for label, value in possession_options.items()
    }

    st.subheader("Localizar evento")
    filter_col_a, filter_col_b = st.columns(2)
    with filter_col_a:
        filter_set_label = st.selectbox(
            "Filtrar por set",
            options=list(filter_set_options.keys()),
            key="edit_event_filter_set",
        )
        filter_team_side = st.selectbox(
            "Filtrar por lado",
            options=["Todos", "Equipe", "Adversária"],
            key="edit_event_filter_side",
        )
    with filter_col_b:
        filter_event_type = st.selectbox(
            "Filtrar por tipo de evento",
            options=["Todos"] + event_types,
            format_func=lambda value: "Todos" if value == "Todos" else event_type_label(value),
            key="edit_event_filter_type",
        )
        filter_search = st.text_input(
            "Buscar evento",
            key="edit_event_filter_search",
            help="Busca por id, nome do evento, atleta ou notas.",
        )

    filtered_events = _filter_events_for_editor(
        events=events,
        players=players,
        filter_set_id=filter_set_options[filter_set_label],
        filter_team_side=filter_team_side,
        filter_event_type=filter_event_type,
        filter_search=filter_search,
    )
    event_label_by_id = {
        event.id: _event_editor_label(event, players_by_id={player.id: player for player in players})
        for event in filtered_events
        if event.id is not None
    }
    event_ids = [event.id for event in filtered_events if event.id is not None]
    if not event_ids:
        st.info("Nenhum evento corresponde aos filtros atuais.")
        return
    if st.session_state.get("edit_event_id") not in event_ids:
        st.session_state["edit_event_id"] = event_ids[-1]

    current_event_index = event_ids.index(st.session_state["edit_event_id"])
    nav_prev_col, nav_next_col = st.columns(2)
    with nav_prev_col:
        if st.button(
            "Evento anterior",
            key="edit_event_prev",
            disabled=current_event_index == 0,
        ):
            st.session_state["edit_event_id"] = event_ids[current_event_index - 1]
    with nav_next_col:
        if st.button(
            "Próximo evento",
            key="edit_event_next",
            disabled=current_event_index == len(event_ids) - 1,
        ):
            st.session_state["edit_event_id"] = event_ids[current_event_index + 1]

    current_event_index = event_ids.index(st.session_state["edit_event_id"])
    st.caption(f"Evento filtrado {current_event_index + 1} de {len(event_ids)}.")
    selected_event_id = st.selectbox(
        "Evento para editar ou excluir",
        options=event_ids,
        format_func=lambda event_id: event_label_by_id[event_id],
        key="edit_event_id",
    )
    selected_event = next(event for event in filtered_events if event.id == selected_event_id)
    st.subheader("Editar ou excluir evento selecionado")

    with st.form("edit_last_event_form"):
        timestamp_input = st.text_input(
            "Timestamp do evento",
            value=format_seconds_for_input(selected_event.timestamp_second),
            help=TIME_INPUT_HELP,
        )
        _render_time_input_preview(timestamp_input)
        event_type = st.selectbox(
            "Evento do registro",
            options=event_types,
            index=event_types.index(selected_event.event_type),
            format_func=event_type_label,
        )
        team_side = st.radio(
            "Lado do evento",
            options=["team", "opponent"],
            horizontal=True,
            index=0 if selected_event.team_side == "team" else 1,
            format_func=team_side_label,
        )
        player_label = st.selectbox(
            "Atleta do evento",
            options=list(player_options.keys()),
            index=_option_index(
                list(player_options.keys()),
                inverse_player_options.get(selected_event.player_id, "Sem atleta"),
            ),
        )
        secondary_player_label = st.selectbox(
            "Atleta secundária do evento",
            options=list(player_options.keys()),
            index=_option_index(
                list(player_options.keys()),
                inverse_player_options.get(
                    selected_event.secondary_player_id,
                    "Sem atleta",
                ),
            ),
        )
        zone_label = st.selectbox(
            "Zona do evento",
            options=["Sem zona"] + sorted(ZONES),
            index=_option_index(
                ["Sem zona"] + sorted(ZONES),
                selected_event.zone or "Sem zona",
            ),
            format_func=_zone_option_label,
        )
        set_label = st.selectbox(
            "Set do evento",
            options=list(set_options.keys()),
            index=_option_index(
                list(set_options.keys()),
                inverse_set_options.get(selected_event.set_id, "Sem set"),
            ),
        )
        possession_label = st.selectbox(
            "Posse do evento",
            options=list(possession_options.keys()),
            index=_option_index(
                list(possession_options.keys()),
                inverse_possession_options.get(
                    selected_event.possession_id,
                    "Sem posse",
                ),
            ),
        )
        points_value = st.selectbox(
            "Pontos do evento",
            options=[0, 1, 2],
            index=[0, 1, 2].index(int(selected_event.points_value)),
        )
        event_subtype = st.text_input("Subtipo do evento", value=selected_event.event_subtype or "")
        outcome = st.text_input("Desfecho do evento", value=selected_event.outcome or "")
        notes = st.text_area("Notas do evento", value=selected_event.notes or "")
        update_submitted = st.form_submit_button("Atualizar evento selecionado")
        if update_submitted:
            try:
                timestamp_second = _parse_time_input(timestamp_input, "Timestamp do evento")
                updated = update_event(
                    session,
                    selected_event.id,
                    set_id=set_options[set_label],
                    possession_id=possession_options[possession_label],
                    taxonomy_version_id=taxonomy_id,
                    event_type=event_type,
                    player_id=player_options[player_label],
                    secondary_player_id=player_options[secondary_player_label],
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

    if st.button("Excluir evento selecionado", key="delete_selected_event", type="secondary"):
        deleted = delete_event(session, selected_event.id)
        if deleted:
            st.success(f"Evento {selected_event.id} excluído.")
        else:
            st.error("Falha ao excluir o evento selecionado.")


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


def _set_filter_options(session: Session, match_id: int) -> dict[str, int | None]:
    set_options = _set_options(session, match_id)
    return {"Todos": None, **{label: value for label, value in set_options.items() if value is not None}}


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


def _sync_new_set_form_state(next_set_number: int) -> None:
    pending_state = st.session_state.pop("pending_new_set_state", None)
    if pending_state:
        for key, value in pending_state.items():
            st.session_state[key] = value
    st.session_state.setdefault("new_set_number", next_set_number)
    st.session_state.setdefault("new_set_start", format_seconds_for_input(0.0))
    st.session_state.setdefault("new_set_end", format_seconds_for_input(0.0))
    if st.session_state.get("new_set_number") in {None, 0}:
        st.session_state["new_set_number"] = next_set_number


def _sync_new_possession_form_state(set_options: dict[str, int | None]) -> None:
    pending_state = st.session_state.pop("pending_new_possession_state", None)
    if pending_state:
        for key, value in pending_state.items():
            st.session_state[key] = value
    st.session_state.setdefault("new_possession_team_side", "team")
    st.session_state.setdefault("new_possession_start", format_seconds_for_input(0.0))
    st.session_state.setdefault("new_possession_end", format_seconds_for_input(0.0))
    st.session_state.setdefault("new_possession_result", "")
    st.session_state.setdefault("new_possession_points_scored", 0)
    st.session_state.setdefault("new_possession_points_conceded", 0)
    if st.session_state.get("new_possession_set") not in set_options:
        st.session_state["new_possession_set"] = _default_set_label(set_options)


def _sync_event_form_state(session: Session, match_id: int) -> None:
    players = _players_for_match(session, match_id)
    player_options = _player_options(players)
    set_options = _set_options(session, match_id)
    if st.session_state.get("tagging_set") not in set_options:
        st.session_state["tagging_set"] = _default_set_label(set_options)

    if st.session_state.get("tagging_player") not in player_options:
        st.session_state["tagging_player"] = "Sem atleta"
    if st.session_state.get("tagging_secondary_player") not in player_options:
        st.session_state["tagging_secondary_player"] = "Sem atleta"

    zone_options = ["Sem zona"] + sorted(ZONES)
    if st.session_state.get("tagging_zone") not in zone_options:
        st.session_state["tagging_zone"] = "Sem zona"
    if st.session_state.get("tagging_points") not in {0, 1, 2}:
        st.session_state["tagging_points"] = 0

    selected_set_id = set_options[st.session_state["tagging_set"]]
    possession_options = _possession_options(session, match_id, selected_set_id)
    if st.session_state.get("tagging_possession") not in possession_options:
        st.session_state["tagging_possession"] = _default_possession_label(possession_options)

    if not st.session_state.get("tagging_timestamp_input"):
        st.session_state["tagging_timestamp_input"] = format_seconds_for_input(
            st.session_state["tagging_timestamp_second"]
        )


def _shift_tagging_timestamp(delta: float) -> None:
    try:
        current_value = timecode_to_seconds(st.session_state.get("tagging_timestamp_input", "0"))
    except ValueError:
        current_value = float(st.session_state.get("tagging_timestamp_second", 0.0))
    shifted = max(0.0, current_value + delta)
    st.session_state["tagging_timestamp_second"] = shifted
    st.session_state["tagging_timestamp_input"] = format_seconds_for_input(shifted)


def _zone_option_label(value: str | None) -> str:
    if value in {None, "Sem zona"}:
        return "Sem zona"
    return zone_label(value)


def _event_editor_label(event: Event, players_by_id: dict[int | None, Player] | None = None) -> str:
    event_id = event.id if event.id is not None else "?"
    player_label = ""
    if players_by_id is not None and event.player_id in players_by_id:
        player_label = f" — {players_by_id[event.player_id].name}"
    return (
        f"Evento {event_id} — {format_seconds_for_input(event.timestamp_second)} — "
        f"{event_type_label(event.event_type)}{player_label}"
    )


def _default_set_label(set_options: dict[str, int | None]) -> str:
    labels = list(set_options.keys())
    if len(labels) > 1:
        return labels[-1]
    return "Sem set"


def _default_possession_label(possession_options: dict[str, int | None]) -> str:
    labels = list(possession_options.keys())
    if len(labels) > 1:
        return labels[-1]
    return "Sem posse"


def _next_set_number(session: Session, match_id: int) -> int:
    sets = list(
        session.exec(
            select(SetSegment)
            .where(SetSegment.match_id == match_id)
            .order_by(SetSegment.set_number, SetSegment.id)
        ).all()
    )
    return max((set_segment.set_number for set_segment in sets), default=0) + 1


def _set_editor_label(set_segment: SetSegment | None) -> str:
    if set_segment is None or set_segment.id is None:
        return "Set indisponível"
    start_label = format_seconds_for_input(set_segment.start_second)
    end_label = format_seconds_for_input(set_segment.end_second)
    return (
        f"Set {set_segment.set_number} (id {set_segment.id}) — "
        f"{start_label or '--'} até {end_label or '--'}"
    )


def _possession_editor_label(session: Session, possession: Possession | None) -> str:
    if possession is None or possession.id is None:
        return "Posse indisponível"
    set_label = "Sem set"
    if possession.set_id is not None:
        set_segment = session.get(SetSegment, possession.set_id)
        if set_segment is not None and set_segment.id is not None:
            set_label = f"Set {set_segment.set_number} (id {set_segment.id})"
    start_label = format_seconds_for_input(possession.start_second)
    end_label = format_seconds_for_input(possession.end_second)
    return (
        f"Posse {possession.id} — {team_side_label(possession.team_side)} — "
        f"{set_label} — {start_label or '--'} até {end_label or '--'}"
    )


def _filter_events_for_editor(
    *,
    events: list[Event],
    players: list[Player],
    filter_set_id: int | None,
    filter_team_side: str,
    filter_event_type: str,
    filter_search: str,
) -> list[Event]:
    players_by_id = {player.id: player for player in players}
    normalized_search = filter_search.strip().lower()
    filtered: list[Event] = []
    for event in events:
        if filter_set_id is not None and event.set_id != filter_set_id:
            continue
        if filter_team_side == "Equipe" and event.team_side != "team":
            continue
        if filter_team_side == "Adversária" and event.team_side != "opponent":
            continue
        if filter_event_type != "Todos" and event.event_type != filter_event_type:
            continue
        if normalized_search:
            player_name = ""
            if event.player_id in players_by_id:
                player_name = players_by_id[event.player_id].name.lower()
            haystack = " ".join(
                [
                    str(event.id or ""),
                    event.event_type.lower(),
                    event_type_label(event.event_type).lower(),
                    player_name,
                    (event.notes or "").lower(),
                ]
            )
            if normalized_search not in haystack:
                continue
        filtered.append(event)
    return filtered


def _parse_time_input(raw_value: str, field_label: str) -> float:
    try:
        return timecode_to_seconds(raw_value)
    except ValueError as exc:
        raise ValueError(f"{field_label}: {exc}") from exc


def _render_time_input_preview(raw_value: str) -> None:
    try:
        parsed = timecode_to_seconds(raw_value)
        st.caption(f"Convertido internamente para {parsed:.1f} s")
    except ValueError:
        st.caption("Formato aceito: segundos, MM:SS ou HH:MM:SS.")


def _match_label(match: Match) -> str:
    return f"Jogo {match.id} — {match.competition_name or 'sem competição'}"
