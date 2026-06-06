import streamlit as st
from sqlmodel import Session

from scoutpraia.core.database import create_db_and_tables, engine
from scoutpraia.services.match_service import (
    create_match_with_video,
    create_opponent,
    create_player,
    list_matches,
    list_opponents,
    list_players,
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
            use_container_width=True,
        )
    else:
        st.info("Nenhuma adversária cadastrada.")


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
            use_container_width=True,
        )
    else:
        st.info("Nenhuma atleta cadastrada.")


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
            use_container_width=True,
        )
    else:
        st.info("Nenhum jogo cadastrado.")


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
