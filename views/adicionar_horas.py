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

alunos_df = st.session_state["base_alunos"]

@st.dialog("Visualizar Horas",width = "medium")
def visualizar_horas_aluno(aluno: str):

    horas_df = get_sheet_data("base_de_horas")
    horas_aluno = horas_df.loc[horas_df["aluno"] == aluno]

    seletor_periodo = st.date_input("Selecione o período:", value=(date.today().replace(day=1),date.today()))
    data_inicio, data_fim = seletor_periodo
    filtro_periodo = (horas_aluno["data_da_aula"] >= data_inicio.strftime("%Y-%m-%d")) & (horas_aluno["data_da_aula"] <= data_fim.strftime("%Y-%m-%d"))
    
    horas_aluno = horas_aluno.loc[filtro_periodo]
    horas_aluno["quantidade_de_horas"] = horas_aluno["quantidade_de_horas"].astype(float)
    horas_aluno = horas_aluno.sort_values(by="data_da_aula",ascending=True)
    
    total_horas = horas_aluno["quantidade_de_horas"].sum()
    
    valor_aluno = alunos_df.loc[alunos_df["aluno"] == aluno, "hora_aula"].values[0]

    total_horas = float(total_horas)
    valor_aluno = float(valor_aluno)

    valor_total = total_horas * valor_aluno

    st.subheader(f"Horas do aluno {aluno}:")

    col1,col2,col3= st.columns(3)
    col1.metric("Total de horas no período:", f"{total_horas} horas")
    col2.metric("Valor total no período:", f"R$ {valor_total:.2f}")
    col3.metric("Valor da hora-aula:", f"R$ {valor_aluno:.2f}")

    st.subheader("Detalhamento das horas:")
    
    colunas = ["data_da_aula","quantidade_de_horas"]
    relatorio_detalhado_df = horas_aluno[colunas]
    relatorio_detalhado_df = relatorio_detalhado_df.rename(columns={
        "data_da_aula": "Data da Aula",
        "quantidade_de_horas": "Quantidade de Horas",
    })

    st.dataframe(relatorio_detalhado_df,hide_index=True)

    titulo_da_tabela = (
    f"Aluno: {aluno}\n"
    f"Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}\n"
    f"Total de horas: {total_horas} horas"
    )

    img_bytes = df_to_image_bytes(relatorio_detalhado_df,title=titulo_da_tabela)

    st.download_button(
        label="Baixar tabela",
        data=img_bytes,
        file_name="tabela.png",
        mime="image/png",
    )

    st.caption("Link para edição no Google Sheets: https://docs.google.com/spreadsheets/d/133kYKvfehQQeJTQ86Z2IM3SmgIBNmd0ZQfhvPFgqFGY/")

professor_parametro = st.query_params.get("professor",None)

if professor_parametro == "ciro":
    index = 1
else:
    index = 0


if autenticado:
    st.title("Adicionar Horas")

    col1,col2,col3 = st.columns(3)

    professor = col1.selectbox("Selecione o professor:", ["Patricia","Ciro"],index=index)

    alunos_filtrados = alunos_df.loc[alunos_df["professor"] == professor]
    alunos = alunos_filtrados["aluno"].tolist()

    aluno = col2.selectbox("Selecione o aluno:", alunos)

    data_aula = col1.date_input("Data da atividade:", value=date.today())
    quantidade_horas = col2.number_input("Quantidade de horas:", step=0.5)

    botao_adicionar_horas = col1.button("Adicionar horas",type="primary")
    visualizar_aluno = st.button("Visualizar horas do aluno",type="secondary")

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
else:
    st.error("Senha incorreta. Acesso negado.")