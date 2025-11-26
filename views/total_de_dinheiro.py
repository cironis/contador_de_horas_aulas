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
    st.title("Visualizar total")

    seletor_periodo = st.date_input("Selecione o período:", value=(date.today().replace(day=1),date.today()))
    data_inicio, data_fim = seletor_periodo

    merged_df = horas_df.merge(alunos_df, on="aluno", how="left", suffixes=('','_aluno'))
    filtro_periodo = (merged_df["data_da_aula"] >= data_inicio.strftime("%Y-%m-%d")) & (merged_df["data_da_aula"] <= data_fim.strftime("%Y-%m-%d"))
    merged_df = merged_df.loc[filtro_periodo]
    merged_df["quantidade_de_horas"] =merged_df["quantidade_de_horas"].astype(float)
    merged_df["hora_aula"] = merged_df["hora_aula"].astype(float)
    merged_df["valor_total"] = merged_df["quantidade_de_horas"] * merged_df["hora_aula"]

    resumo_professor = merged_df.groupby("professor")[["quantidade_de_horas","valor_total"]].sum().reset_index()

    total_geral_horas = resumo_professor["quantidade_de_horas"].sum()
    total_geral_valor = resumo_professor["valor_total"].sum()
    resumo_professor = resumo_professor.append({
                            "professor": "Total Geral",
                            "quantidade_de_horas": total_geral_horas,
                            "valor_total": total_geral_valor
                        }, ignore_index=True)

    st.dataframe(
        resumo_professor,
        hide_index=True,
        column_config={
            "valor_total": st.column_config.NumberColumn(
                "Valor total",
                format="R$ %.2f",  # 2 casas decimais com R$
            ),
        },
    )

else:
    st.error("Senha incorreta. Acesso negado.")