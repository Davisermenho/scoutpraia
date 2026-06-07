import streamlit as st
from sqlmodel import Session

from scoutpraia.core.database import create_db_and_tables, engine
from scoutpraia.services.match_service import (
    add_player_to_match,
    create_match_with_video,
    create_opponent,
    create_player,
    delete_match,
    delete_opponent,
    delete_player,
    list_match_roster,
    list_matches,
    list_opponents,
    list_players,
    remove_player_from_match,
    update_match_with_video,
    update_opponent,
    update_player,
)


def _render_opponents(session: Session) -> None:
    st.subheader("Adversárias")
    with st.form("create_opponent"):
        name = st.text_input("Nome da adversária")
        category = st.text_input("Categoria")
        notes = st.text_area("Observações")
        submitted = st.form_submit_button("Cadastrar adversária")
        if submitted:
            try:
                create_opponent(session, name=name, category=category, notes=notes)
                st.success("Adversária cadastrada.")
            except ValueError as exc:
                st.error(str(exc))

    opponents = list_opponents(session)
    if opponents:
        st.dataframe(
            [
                {
                    "id": opponent.id,
                    "name": opponent.name,
                    "category": opponent.category,
                    "notes": opponent.notes,
                }
                for opponent in opponents
            ],
            width="stretch",
        )
    else:
        st.info("Nenhuma adversária cadastrada.")

    if opponents:
        selected_label = st.selectbox(
            "Editar adversária",
            options=[f"{opponent.name} (id {opponent.id})" for opponent in opponents],
            key="edit_opponent_select",
        )
        selected_opponent = next(
            opponent
            for opponent in opponents
            if f"{opponent.name} (id {opponent.id})" == selected_label
        )
        with st.form("update_opponent_form"):
            name = st.text_input("Nome da adversária", value=selected_opponent.name)
            category = st.text_input(
                "Categoria da adversária", value=selected_opponent.category or ""
            )
            notes = st.text_area(
                "Observações da adversária", value=selected_opponent.notes or ""
            )
            submitted = st.form_submit_button("Atualizar adversária")
            if submitted:
                try:
                    update_opponent(
                        session,
                        selected_opponent.id,
                        name=name,
                        category=category,
                        notes=notes,
                    )
                    st.success("Adversária atualizada.")
                except ValueError as exc:
                    st.error(str(exc))
        if st.button("Excluir adversária", key="delete_opponent_button", type="secondary"):
            try:
                if delete_opponent(session, selected_opponent.id):
                    st.success("Adversária excluída.")
            except ValueError as exc:
                st.error(str(exc))


def _render_players(session: Session) -> None:
    st.subheader("Atletas")
    with st.form("create_player"):
        name = st.text_input("Nome da atleta")
        shirt_number = st.number_input("Número", min_value=0, max_value=999, value=0)
        primary_role = st.text_input("Função principal")
        secondary_role = st.text_input("Função secundária")
        submitted = st.form_submit_button("Cadastrar atleta")
        if submitted:
            try:
                create_player(
                    session,
                    name=name,
                    shirt_number=int(shirt_number) if shirt_number else None,
                    primary_role=primary_role,
                    secondary_role=secondary_role,
                )
                st.success("Atleta cadastrada.")
            except ValueError as exc:
                st.error(str(exc))

    players = list_players(session)
    if players:
        st.dataframe(
            [
                {
                    "id": player.id,
                    "name": player.name,
                    "shirt_number": player.shirt_number,
                    "primary_role": player.primary_role,
                    "secondary_role": player.secondary_role,
                    "active": player.active,
                }
                for player in players
            ],
            width="stretch",
        )
    else:
        st.info("Nenhuma atleta cadastrada.")

    if players:
        selected_label = st.selectbox(
            "Editar atleta",
            options=[
                f"{player.name} (id {player.id})"
                for player in players
            ],
            key="edit_player_select",
        )
        selected_player = next(
            player
            for player in players
            if f"{player.name} (id {player.id})" == selected_label
        )
        with st.form("update_player_form"):
            name = st.text_input("Nome da atleta", value=selected_player.name)
            shirt_number = st.number_input(
                "Número da atleta",
                min_value=0,
                max_value=999,
                value=selected_player.shirt_number or 0,
            )
            primary_role = st.text_input(
                "Função principal da atleta",
                value=selected_player.primary_role or "",
            )
            secondary_role = st.text_input(
                "Função secundária da atleta",
                value=selected_player.secondary_role or "",
            )
            active = st.checkbox("Ativa", value=selected_player.active)
            submitted = st.form_submit_button("Atualizar atleta")
            if submitted:
                try:
                    update_player(
                        session,
                        selected_player.id,
                        name=name,
                        shirt_number=int(shirt_number) if shirt_number else None,
                        primary_role=primary_role,
                        secondary_role=secondary_role,
                        active=active,
                    )
                    st.success("Atleta atualizada.")
                except ValueError as exc:
                    st.error(str(exc))
        if st.button("Excluir atleta", key="delete_player_button", type="secondary"):
            try:
                if delete_player(session, selected_player.id):
                    st.success("Atleta excluída.")
            except ValueError as exc:
                st.error(str(exc))


def _render_matches(session: Session) -> None:
    st.header("Jogos")
    opponents = list_opponents(session)
    opponent_options = {f"{opponent.name} (id {opponent.id})": opponent.id for opponent in opponents}

    with st.form("create_match"):
        match_date = st.date_input("Data do jogo", value=None)
        competition_name = st.text_input("Competição")
        phase = st.text_input("Fase")
        selected_opponent = st.selectbox(
            "Adversária",
            options=list(opponent_options.keys()),
            index=0 if opponent_options else None,
            placeholder="Cadastre uma adversária antes",
        )
        video_path = st.text_input("Caminho local do vídeo")
        notes = st.text_area("Contexto/observações")
        submitted = st.form_submit_button("Cadastrar jogo e ler metadados")

        if submitted:
            if not selected_opponent:
                st.error("Cadastre uma adversária antes de criar o jogo.")
                return
            try:
                match = create_match_with_video(
                    session,
                    video_path=video_path,
                    match_date=match_date,
                    opponent_id=opponent_options[selected_opponent],
                    competition_name=competition_name,
                    phase=phase,
                    notes=notes,
                )
                st.success(
                    "Jogo cadastrado com metadados: "
                    f"{match.duration_seconds}s, "
                    f"{match.video_width}x{match.video_height}, "
                    f"{match.video_fps} fps, codec {match.video_codec}."
                )
            except (FileNotFoundError, ValueError) as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Falha ao ler metadados do vídeo: {exc}")

    matches = list_matches(session)
    if matches:
        st.dataframe(
            [
                {
                    "id": match.id,
                    "date": match.match_date,
                    "opponent_id": match.opponent_id,
                    "competition": match.competition_name,
                    "phase": match.phase,
                    "video_path": match.video_path,
                    "duration_seconds": match.duration_seconds,
                    "resolution": (
                        f"{match.video_width}x{match.video_height}"
                        if match.video_width and match.video_height
                        else None
                    ),
                    "fps": match.video_fps,
                    "codec": match.video_codec,
                }
                for match in matches
            ],
            width="stretch",
        )
    else:
        st.info("Nenhum jogo cadastrado.")

    if matches and opponent_options:
        match_options = {
            f"Jogo {match.id} — {match.competition_name or 'sem competição'}": match
            for match in matches
        }
        selected_match_label = st.selectbox(
            "Editar jogo",
            options=list(match_options.keys()),
            key="edit_match_select",
        )
        selected_match = match_options[selected_match_label]
        reverse_opponent_options = {
            value: key for key, value in opponent_options.items()
        }
        with st.form("update_match_form"):
            match_date = st.date_input(
                "Data do jogo (edição)",
                value=selected_match.match_date,
            )
            competition_name = st.text_input(
                "Competição (edição)",
                value=selected_match.competition_name or "",
            )
            phase = st.text_input("Fase (edição)", value=selected_match.phase or "")
            selected_opponent = st.selectbox(
                "Adversária (edição)",
                options=list(opponent_options.keys()),
                index=_option_index(
                    list(opponent_options.keys()),
                    reverse_opponent_options.get(selected_match.opponent_id, ""),
                ),
            )
            video_path = st.text_input(
                "Caminho local do vídeo (edição)",
                value=selected_match.video_path or "",
            )
            notes = st.text_area(
                "Contexto/observações (edição)",
                value=selected_match.notes or "",
            )
            final_score_team = st.number_input(
                "Placar equipe",
                min_value=0,
                max_value=99,
                value=selected_match.final_score_team or 0,
            )
            final_score_opponent = st.number_input(
                "Placar adversária",
                min_value=0,
                max_value=99,
                value=selected_match.final_score_opponent or 0,
            )
            submitted = st.form_submit_button("Atualizar jogo e reler metadados")
            if submitted:
                try:
                    update_match_with_video(
                        session,
                        selected_match.id,
                        video_path=video_path,
                        match_date=match_date,
                        opponent_id=opponent_options[selected_opponent],
                        competition_name=competition_name,
                        phase=phase,
                        notes=notes,
                        final_score_team=int(final_score_team),
                        final_score_opponent=int(final_score_opponent),
                    )
                    st.success("Jogo atualizado.")
                except (FileNotFoundError, ValueError) as exc:
                    st.error(str(exc))
        if st.button("Excluir jogo", key="delete_match_button", type="secondary"):
            try:
                if delete_match(session, selected_match.id):
                    st.success("Jogo excluído.")
            except ValueError as exc:
                st.error(str(exc))

    _render_match_roster(session, matches)


def _render_match_roster(session: Session, matches: list) -> None:
    st.subheader("Elenco disponível do jogo")
    players = list_players(session)
    if not matches or not players:
        st.info("Cadastre pelo menos um jogo e uma atleta para associar elenco.")
        return

    match_options = {
        f"Jogo {match.id} — {match.competition_name or 'sem competição'}": match.id
        for match in matches
    }
    player_options = {
        f"{player.name} (#{player.shirt_number})"
        if player.shirt_number is not None
        else player.name: player.id
        for player in players
    }

    selected_match_label = st.selectbox(
        "Jogo para associar elenco",
        options=list(match_options.keys()),
        key="roster_match",
    )
    selected_player_labels = st.multiselect(
        "Atletas disponíveis",
        options=list(player_options.keys()),
        key="roster_players",
    )

    if st.button("Adicionar atletas ao elenco", key="add_roster_players"):
        match_id = match_options[selected_match_label]
        for player_label in selected_player_labels:
            add_player_to_match(
                session,
                match_id=match_id,
                player_id=player_options[player_label],
            )
        st.success("Atletas associadas ao jogo.")

    selected_match_id = match_options[selected_match_label]
    roster = list_match_roster(session, selected_match_id)
    players_by_id = {player.id: player for player in players}
    if roster:
        st.dataframe(
            [
                {
                    "match_id": entry.match_id,
                    "player_id": entry.player_id,
                    "name": players_by_id[entry.player_id].name
                    if entry.player_id in players_by_id
                    else None,
                    "available": entry.available,
                    "starter": entry.starter,
                }
                for entry in roster
            ],
            width="stretch",
        )
        removable_player_label = st.selectbox(
            "Remover atleta do elenco",
            options=[
                (
                    f"{players_by_id[entry.player_id].name} (#{players_by_id[entry.player_id].shirt_number})"
                    if entry.player_id in players_by_id
                    and players_by_id[entry.player_id].shirt_number is not None
                    else players_by_id[entry.player_id].name
                )
                for entry in roster
                if entry.player_id in players_by_id
            ],
            key="remove_roster_player_select",
        )
        removable_player_id = player_options[removable_player_label]
        if st.button("Remover atleta do elenco", key="remove_roster_player_button"):
            removed = remove_player_from_match(
                session,
                match_id=selected_match_id,
                player_id=removable_player_id,
            )
            if removed:
                st.success("Atleta removida do elenco.")
    else:
        st.info("Nenhuma atleta associada a este jogo.")


def render() -> None:
    create_db_and_tables()
    with Session(engine) as session:
        tab_matches, tab_opponents, tab_players = st.tabs(
            ["Jogos", "Adversárias", "Atletas"]
        )
        with tab_matches:
            _render_matches(session)
        with tab_opponents:
            _render_opponents(session)
        with tab_players:
            _render_players(session)


def _option_index(options: list[str], target: str) -> int:
    if target in options:
        return options.index(target)
    return 0
