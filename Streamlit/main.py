import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

# Funções do painel
from funcoes_chat import responder_pergunta
from bancodedados.conexao import get_data

# Carrega todos os dados
query = """SELECT * FROM situacao_matricula;"""
todos_os_dados = get_data(query)

st.title("Monitoramento de Matrículas")

# Filtros
campus_selecionado = st.selectbox("Selecione o Campus:", todos_os_dados["unidade"].unique())

turno_opcoes = ["Todos"] + sorted(todos_os_dados["turno_do_curso"].dropna().unique())
turno_selecionado = st.selectbox("Selecione o Turno do Curso:", turno_opcoes)

tipo_curso_opcoes = ["Todos"] + sorted(todos_os_dados["tipo_de_curso"].dropna().unique())
tipo_curso_selecionado = st.selectbox("Selecione o Tipo de Curso:", tipo_curso_opcoes)

dados_filtrados = todos_os_dados[todos_os_dados["unidade"] == campus_selecionado]

if turno_selecionado != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["turno_do_curso"] == turno_selecionado]

if tipo_curso_selecionado != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["tipo_de_curso"] == tipo_curso_selecionado]

if not dados_filtrados.empty:
    situacoes_relevantes = ["Concluintes", "Em curso", "Evadidos"]
    dados_situacao = dados_filtrados[dados_filtrados["situacao"].isin(situacoes_relevantes)]
    
    dados_por_ano = dados_situacao.groupby(["ano", "situacao"])["matriculas"].sum().reset_index()

    chart = alt.Chart(dados_por_ano).mark_line().encode(
        x='ano:O',
        y='matriculas:Q',
        color='situacao:N',
        tooltip=['ano', 'situacao', 'matriculas']
    ).properties(
        title=f"Quantidade de Matrículas por Situação ao Longo dos Anos para o {campus_selecionado}"
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.write("Nenhum dado disponível para os filtros selecionados.")

logo_path = "logo_IF.jpg"  
logo = Image.open(logo_path)

# Chat com dados
st.subheader("Converse com os dados")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": f"Olá! Como posso ajudar você com os dados do {campus_selecionado}?"}]

for msg in st.session_state["messages"]:
    if msg["role"] == "assistant":
        col1, col2 = st.columns([0.05, 0.9])
        with col1:
            st.image(logo, width=30)
        with col2:
            st.write(msg["content"])
    else:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Entrada do usuário
if user_input := st.chat_input("Faça uma pergunta sobre os dados:"):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    resposta = responder_pergunta(user_input, dados_filtrados, campus_selecionado)
    st.session_state["messages"].append({"role": "assistant", "content": resposta})

    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.image(logo, width=40)
    with col2:
        st.write(resposta)
