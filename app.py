import streamlit as st

from scoutpraia.core.database import create_db_and_tables
from scoutpraia.core.paths import ensure_storage_dirs


def main() -> None:
    st.set_page_config(page_title="ScoutPraia", layout="wide")
    ensure_storage_dirs()
    create_db_and_tables()

    st.title("ScoutPraia")
    st.caption("MVP local para análise de vídeos de handebol de praia.")

    page = st.sidebar.radio(
        "Navegação",
        ["Dashboard", "Jogos", "Marcação", "Relatórios", "Adversárias"],
    )

    if page == "Dashboard":
        from scoutpraia.pages.dashboard import render
    elif page == "Jogos":
        from scoutpraia.pages.matches import render
    elif page == "Marcação":
        from scoutpraia.pages.tagging import render
    elif page == "Relatórios":
        from scoutpraia.pages.reports import render
    else:
        from scoutpraia.pages.opponents import render

    render()


if __name__ == "__main__":
    main()
