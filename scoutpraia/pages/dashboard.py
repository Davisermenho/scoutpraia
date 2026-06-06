from __future__ import annotations

import pandas as pd
import streamlit as st
from sqlmodel import Session, select

from scoutpraia.core.database import create_db_and_tables, engine
from scoutpraia.models.event import Event
from scoutpraia.models.report import Report
from scoutpraia.services.match_service import list_matches
from scoutpraia.services.report_service import build_collective_report_payload


def render() -> None:
    st.header("Dashboard")
    create_db_and_tables()

    with Session(engine) as session:
        matches = list_matches(session)
        total_events = len(session.exec(select(Event)).all())
        total_reports = len(session.exec(select(Report)).all())

        metric_cols = st.columns(4)
        metric_cols[0].metric("Jogos cadastrados", len(matches))
        metric_cols[1].metric("Eventos salvos", total_events)
        metric_cols[2].metric("Relatórios gerados", total_reports)
        metric_cols[3].metric(
            "Jogos com vídeo",
            sum(1 for match in matches if match.video_path),
        )

        st.subheader("Atalhos operacionais")
        st.markdown(
            "- Cadastre jogo e vídeo em `Jogos`.\n"
            "- Marque eventos em `Marcação` com timestamp manual.\n"
            "- Gere HTML em `Relatórios`.\n"
            "- Revise histórico e tendências em `Adversárias`."
        )

        if not matches:
            st.info("Nenhum jogo cadastrado ainda. O dashboard exibe estado vazio sem erro.")
            return

        st.subheader("Jogos recentes")
        st.dataframe(
            [
                {
                    "id": match.id,
                    "data": match.match_date,
                    "competição": match.competition_name,
                    "fase": match.phase,
                    "placar": _score_label(match.final_score_team, match.final_score_opponent),
                    "vídeo": "sim" if match.video_path else "não",
                }
                for match in matches[:5]
            ],
            use_container_width=True,
        )

        st.subheader("Resumo de KPIs recentes")
        kpi_rows = []
        for match in matches[:3]:
            try:
                payload = build_collective_report_payload(session, match.id)
            except ValueError:
                continue
            kpis = payload["kpis"]
            kpi_rows.append(
                {
                    "jogo": match.id,
                    "competição": match.competition_name,
                    "pontos": kpis["points_total"],
                    "gols": kpis["goals_total"],
                    "pontos_por_posse": kpis["points_per_possession"],
                    "conversão": kpis["offensive_conversion_rate"],
                    "erro_técnico_posse": kpis["technical_error_rate"],
                }
            )
        if kpi_rows:
            st.dataframe(pd.DataFrame(kpi_rows), use_container_width=True)
        else:
            st.info("Ainda não há eventos suficientes para KPI coletivo recente.")


def _score_label(score_team: int | None, score_opponent: int | None) -> str:
    if score_team is None and score_opponent is None:
        return "sem placar"
    return f"{score_team if score_team is not None else '-'} x {score_opponent if score_opponent is not None else '-'}"
