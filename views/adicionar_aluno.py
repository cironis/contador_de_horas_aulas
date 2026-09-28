import streamlit as st
import pandas as pd
from auxiliar.google_sheets import get_base_alunos,set_sheet_data

if "base_alunos" not in st.session_state:
    st.session_state["base_alunos"] = get_base_alunos()

alunos_df = st.session_state["base_alunos"]

st.title("Adicionar Alunos")

base_alunos = st.data_editor(
    alunos_df,
    num_rows="dynamic",
    column_config={
        "aluno": st.column_config.TextColumn("Nome do Aluno"),
        "hora_aula": st.column_config.NumberColumn(
            "Hora Aula",
            help="Valor da hora-aula",
            format="R$ %.2f",
        ),
        "professor": st.column_config.SelectboxColumn(
            "Professor", 
            options=["Patricia","Ciro"],
            required=True),
        "percentual_recebido": st.column_config.NumberColumn(
            "% Recebido",
            help="Quanto do valor cobrado fica com o professor (0 a 100). "
                 "Ex.: 70 = o aluno paga o valor cheio e 30% é repassado para a clínica.",
            min_value=0,
            max_value=100,
            step=1,
            default=100,
            format="%d%%",
        ),
    },
)

atualizar_botao = st.button("Atualizar base de alunos")

if atualizar_botao:
    base_alunos["percentual_recebido"] = base_alunos["percentual_recebido"].fillna(100)
    set_sheet_data("base_alunos",base_alunos)
    st.session_state["base_alunos"] = base_alunos
    st.success("Base de alunos atualizada com sucesso!")
    st.balloons()
