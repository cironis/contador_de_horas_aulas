import streamlit as st
from datetime import date
from auxiliar.google_sheets import get_sheet_data,append_sheet_data
from auxiliar.download_as_image import df_to_image_bytes


password = st.secrets["PASSWORD"]
password_parametro = st.query_params.get("password",None)

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if password == password_parametro:
    st.session_state["autenticado"] = True

autenticado = st.session_state["autenticado"] 

if "base_alunos" not in st.session_state:
    st.session_state["base_alunos"] = get_sheet_data("base_alunos")

base_alunos = st.session_state["base_alunos"]

alunos_df = st.session_state["base_alunos"]
if "base_de_horas" not in st.session_state:
    st.session_state["base_de_horas"] = get_sheet_data("base_de_horas")

horas_df = st.session_state["base_de_horas"]

if autenticado:
    st.title("Visualizar total de dinheiro por professor")

    seletor_periodo = st.date_input("Selecione o período:", value=(date.today().replace(day=1),date.today()))
    data_inicio, data_fim = seletor_periodo

    merged_df = horas_df.merge(alunos_df, on="aluno", how="left")

    st.dataframe(merged_df)

else:
    st.error("Senha incorreta. Acesso negado.")