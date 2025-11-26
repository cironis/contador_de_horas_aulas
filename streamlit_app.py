import streamlit as st

st.set_page_config(layout="wide")

# --- PAGE SETUP ---
horas_page = st.Page(
    "views/adicionar_horas.py",
    title="Adicionar Horas",
    icon=":material/thumb_up:",
    default=True,
)

aluno_page = st.Page(
    "views/adicionar_aluno.py",
    title="Adicionar Alunos",
    icon=":material/thumb_up:",
)

total_page = st.Page(
    "views\total_de_dinheiro.py",
    title="Total de Dinheiro",
    icon=":material/money:",
)
# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Controle de horas": [horas_page,total_page],
        "Configurações": [aluno_page],
    }
)

# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")


# --- RUN NAVIGATION ---
pg.run()