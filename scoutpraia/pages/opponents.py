from __future__ import annotations

import pandas as pd
import streamlit as st
from sqlmodel import Session, select

from scoutpraia.core.database import create_db_and_tables, engine
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, Possession
from scoutpraia.services.analytics_service import opponent_kpis
from scoutpraia.services.match_service import (
    create_opponent,
    delete_opponent,
    list_opponents,
    update_opponent,
)
from scoutpraia.services.taxonomy_service import EVENT_DEFINITIONS


def render() -> None:
    st.header("Adversárias")
    create_db_and_tables()

    with Session(engine) as session:
        opponents = list_opponents(session)
        _render_create_opponent(session)
        if not opponents:
            st.info("Nenhuma adversária cadastrada.")
            return

        st.subheader("Cadastro e revisão")
        selected_label, selected_opponent = _select_opponent(opponents)
        _render_edit_delete_opponent(session, selected_opponent)

        st.subheader("Histórico de jogos")
        matches = list(
            session.exec(
                select(Match)
                .where(Match.opponent_id == selected_opponent.id)
                .order_by(Match.match_date, Match.id)
            ).all()
        )
        if matches:
            st.dataframe(
                [
                    {
                        "id": match.id,
                        "data": match.match_date,
                        "competição": match.competition_name,
                        "fase": match.phase,
                        "placar": _score_label(
                            match.final_score_team, match.final_score_opponent
                        ),
                        "vídeo": "sim" if match.video_path else "não",
                    }
                    for match in matches
                ],
                use_container_width=True,
            )
        else:
            st.info("Nenhum jogo encontrado para esta adversária.")

        st.subheader("Tendências calculadas")
        trends = _opponent_trends(session, selected_opponent.id)
        if trends is None:
            st.info("Ainda não há eventos suficientes para tendências desta adversária.")
        else:
            cols = st.columns(3)
            cols[0].metric("Lado preferencial", trends["preferred_attack_side"] or "n/d")
            cols[1].metric(
                "Erro sob pressão",
                trends["pressure_error_rate"]
                if trends["pressure_error_rate"] is not None
                else "n/d",
            )
            cols[2].metric(
                "Eficiência shoot-out",
                trends["shootout_efficiency"]
                if trends["shootout_efficiency"] is not None
                else "n/d",
            )
            st.dataframe(
                pd.DataFrame(
                    [
                        {"métrica": key, "valor": _display_value(value)}
                        for key, value in trends.items()
                        if key != "critical_warnings"
                    ]
                ),
                use_container_width=True,
            )
            if trends.get("critical_warnings"):
                st.warning(" | ".join(trends["critical_warnings"]))

        st.subheader("Plano de jogo manual")
        st.caption(f"Adversária selecionada: {selected_label}")
        with st.form("opponent_plan_form"):
            notes = st.text_area(
                "Plano / observações",
                value=selected_opponent.notes or "",
                height=160,
            )
            submitted = st.form_submit_button("Salvar plano")
            if submitted:
                updated = update_opponent(
                    session,
                    selected_opponent.id,
                    name=selected_opponent.name,
                    category=selected_opponent.category,
                    notes=notes,
                )
                st.success(f"Plano salvo para {updated.name}.")


def _render_create_opponent(session: Session) -> None:
    with st.form("opponents_create_form"):
        st.subheader("Nova adversária")
        name = st.text_input("Nome")
        category = st.text_input("Categoria")
        notes = st.text_area("Observações iniciais")
        submitted = st.form_submit_button("Cadastrar adversária")
        if submitted:
            try:
                opponent = create_opponent(
                    session, name=name, category=category, notes=notes
                )
                st.success(f"Adversária cadastrada: {opponent.name}.")
            except ValueError as exc:
                st.error(str(exc))


def _select_opponent(opponents):
    options = {f"{opponent.name} (id {opponent.id})": opponent for opponent in opponents}
    selected_label = st.selectbox("Adversária", options=list(options.keys()))
    return selected_label, options[selected_label]


def _render_edit_delete_opponent(session: Session, opponent) -> None:
    with st.form("opponents_edit_form"):
        name = st.text_input("Nome da adversária", value=opponent.name)
        category = st.text_input("Categoria da adversária", value=opponent.category or "")
        notes = st.text_area("Observações da adversária", value=opponent.notes or "")
        submitted = st.form_submit_button("Atualizar adversária")
        if submitted:
            try:
                updated = update_opponent(
                    session,
                    opponent.id,
                    name=name,
                    category=category,
                    notes=notes,
                )
                st.success(f"Adversária atualizada: {updated.name}.")
            except ValueError as exc:
                st.error(str(exc))

    if st.button("Excluir adversária selecionada", type="secondary"):
        try:
            removed = delete_opponent(session, opponent.id)
            if removed:
                st.success(f"Adversária {opponent.name} excluída.")
        except ValueError as exc:
            st.error(str(exc))


def _opponent_trends(session: Session, opponent_id: int) -> dict[str, object] | None:
    matches = list(
        session.exec(select(Match).where(Match.opponent_id == opponent_id)).all()
    )
    match_ids = [match.id for match in matches if match.id is not None]
    if not match_ids:
        return None
    events = list(
        session.exec(select(Event).where(Event.match_id.in_(match_ids))).all()
    )
    possessions = list(
        session.exec(select(Possession).where(Possession.match_id.in_(match_ids))).all()
    )
    if not events:
        return None
    return opponent_kpis(
        pd.DataFrame([event.model_dump() for event in events]),
        possessions=pd.DataFrame([possession.model_dump() for possession in possessions]),
        taxonomy_status="draft",
        event_definitions=pd.DataFrame(EVENT_DEFINITIONS),
    )


def _score_label(score_team: int | None, score_opponent: int | None) -> str:
    if score_team is None and score_opponent is None:
        return "sem placar"
    return f"{score_team if score_team is not None else '-'} x {score_opponent if score_opponent is not None else '-'}"


def _display_value(value: object) -> object:
    if isinstance(value, dict):
        return str(value)
    return value
