import streamlit as st
from auxiliar.athentication import esta_autenticado, tela_de_login, botao_sair

st.set_page_config(layout="wide")

# --- PAGE SETUP ---
horas_page = st.Page(
    "views/adicionar_horas.py",
    title="Adicionar Horas",
    icon=":material/punch_clock:",
    default=True,
)

aluno_page = st.Page(
    "views/adicionar_aluno.py",
    title="Adicionar Alunos",
    icon=":material/child_care:",
)

total_page = st.Page(
    "views/total_de_dinheiro.py",
    title="Total de Dinheiro",
    icon=":material/money:",
)

editar_horas_page = st.Page(
    "views/editar_planilha.py",
    title="Editar Planilha de Horas",
    icon=":material/warning:",
)

# --- NAVIGATION SETUP ---
if esta_autenticado():
    pg = st.navigation(
        {
            "Controle de horas": [horas_page,total_page],
            "Configurações": [aluno_page,editar_horas_page],
        }
    )
    botao_sair()
else:
    pg = st.navigation([st.Page(tela_de_login, title="Login", icon=":material/lock:")], position="hidden")

# --- SHARED ON ALL PAGES ---
st.sidebar.caption("Version 1.2.0")


# --- RUN NAVIGATION ---
pg.run()