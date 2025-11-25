import streamlit as st
from datetime import date
from auxiliar.google_sheets import get_sheet_data,append_sheet_data

if "base_alunos" not in st.session_state:
    st.session_state["base_alunos"] = get_sheet_data("base_alunos")

alunos_df = st.session_state["base_alunos"]

@st.dialog("Visualizar Horas do Aluno",width = "medium")
def visualizar_horas_aluno(aluno: str):
    horas_df = get_sheet_data("base_de_horas")
    horas_aluno = horas_df.loc[horas_df["aluno"] == aluno]
    
    colunas = ["data_da_aula","quantidade_de_horas","data_atualizacao"]
    
    st.subheader(f"Horas do aluno {aluno}:")
    col1,col2,col3 = st.columns(3)

    seletor_periodo = col1.date_input("Selecione o período:", value=(date.today().replace(day=1),date.today()))
    data_inicio, data_fim = seletor_periodo
    filtro_periodo = (horas_aluno["data_da_aula"] >= data_inicio.strftime("%Y-%m-%d")) & (horas_aluno["data_da_aula"] <= data_fim.strftime("%Y-%m-%d"))
    
    horas_aluno = horas_aluno.loc[filtro_periodo]
    horas_aluno["quantidade_de_horas"] = horas_aluno["quantidade_de_horas"].astype(float)
    horas_aluno = horas_aluno.sort_values(by="data_da_aula",ascending=True)
    
    total_horas = horas_aluno["quantidade_de_horas"].sum()
    col2.metric("Total de horas no período:", f"{total_horas} horas")

    valor_aluno = alunos_df.loc[alunos_df["aluno"] == aluno, "hora_aula"].values[0]

    total_horas = float(total_horas)
    valor_aluno = float(valor_aluno)

    valor_total = total_horas * valor_aluno

    col3.metric("Valor total no período:", f"R$ {valor_total:.2f}")

    st.subheader("Detalhamento das horas:")
    st.dataframe(horas_aluno[colunas],hide_index=True)

professor_parametro = st.query_params.get("professor",None)

if professor_parametro == "patricia":
    index = 0
else:
    index = 1



st.title("Adicionar Horas")

col1,col2,col3 = st.columns(3)

professor = col1.selectbox("Selecione o professor:", ["Patricia","Ciro"],index=0)

alunos_filtrados = alunos_df.loc[alunos_df["professor"] == professor]
alunos = alunos_filtrados["aluno"].tolist()

aluno = col2.selectbox("Selecione o aluno:", alunos)

data_aula = col1.date_input("Data da atividade:", value=date.today())
quantidade_horas = col2.number_input("Quantidade de horas:", step=0.5)

botao_adicionar_horas = col1.button("Adicionar horas")
visualizar_aluno = col3.button("Visualizar horas do aluno")

if botao_adicionar_horas:
    nova_linha = {
        "data_da_aula": data_aula.strftime("%Y-%m-%d"),
        "quantidade_de_horas": quantidade_horas,
        "aluno": aluno,
        "professor": professor,
        "data_atualizacao": date.today().strftime("%Y-%m-%d"),
    }
    
    append_sheet_data("base_de_horas", [list(nova_linha.values())])
    st.success(f"Foram adicionadas {quantidade_horas} horas para o aluno {aluno} do professor {professor}.")
    st.balloons()

if visualizar_aluno:
    visualizar_horas_aluno(aluno)