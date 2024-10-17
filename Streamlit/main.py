import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configuração da conexão com o Banco de Dados
host = "localhost"
port = "5432"
database = "leitura_minuto"
username = "postgres"
password = "nis"

# Função para coletar dados
conn_str = f"postgresql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(conn_str)

@st.cache_data
def get_data():
    conn = engine.raw_connection()
    try:
        query = """ SELECT * FROM matriculas; """
        #query = """ SELECT ano, tipo_de_curso, unidade, SUM(vagas) AS total_vagas, SUM(ingressantes) AS total_ingressantes, SUM(concluintes) AS total_concluintes, SUM(matriculas_equivalentes) AS total_matriculas_equivalentes, SUM(matriculas) AS total_matriculas FROM matriculas GROUP BY ano, tipo_de_curso, unidade ORDER BY ano, tipo_de_curso, unidade; """
        df = pd.read_sql(query, con=conn)
    finally:
        conn.close()
    return df

todos_os_dados = get_data()

# Criação da interface Streamlit
st.title("Painel Leitura Minuto")

# Selecionar o Campus
campus_selecionado = st.selectbox("Selecione o Campus:", todos_os_dados["unidade"].unique())
dados = todos_os_dados[todos_os_dados["unidade"] == campus_selecionado]

# Selecionar tipo de curso
tipos_curso_selecionados = st.multiselect(
    "Selecione o(s) tipo(s) de curso:", 
    dados["tipo_de_curso"].unique(),
    default=dados["tipo_de_curso"].unique()
)
dados_filtrados = dados[dados["tipo_de_curso"].isin(tipos_curso_selecionados)]

if len(tipos_curso_selecionados) > 1:
    dados_grafico = dados_filtrados.groupby(["ano", "tipo_de_curso"]).sum().reset_index()
else:
    dados_grafico = dados_filtrados

dados_agrupados = dados_filtrados.groupby(["ano", "tipo_de_curso"]).sum().reset_index()

st.text("O Campus XXXXXX possui ....")


# Gráfico 1: Total de vagas por ano e tipo de curso
st.subheader("Total de Vagas")
st.bar_chart(dados_agrupados, x="ano", y="vagas", color="tipo_de_curso")

# Gráfico 2: Total de ingressantes por ano e tipo de curso
st.subheader("Total de Ingressantes")
st.line_chart(dados_agrupados, x="ano", y="ingressantes", color="tipo_de_curso")

# Gráfico 3: Total de concluintes por ano e tipo de curso
st.subheader("Total de Concluintes")
st.area_chart(dados_agrupados, x="ano", y="concluintes", color="tipo_de_curso")

# Gráfico 4: Total de concluintes por ano e turno
st.subheader("Total de Concluintes por Turno")
st.area_chart(dados_agrupados, x="ano", y="concluintes", color="turno_do_curso")

# Download 
st.dataframe(dados_filtrados)


# Agrupar por curso e somar os ingressantes
cursos_populares = dados_filtrados.groupby("subeixo_tecnologico")["ingressantes"].sum().sort_values(ascending=False)

# Mostrar o curso mais popular
curso_mais_popular = cursos_populares.index[0]
st.write(f"O curso mais popular é: {curso_mais_popular}")

# Mostrar um gráfico de barras dos cursos mais populares
st.bar_chart(cursos_populares.head(10)) # Mostrar top 10 cursos

# Agrupar por turno e calcular estatísticas
dados_por_turno = dados_filtrados.groupby("turno_do_curso").agg(
    total_vagas = ("vagas", "sum"),
    total_ingressantes = ("ingressantes", "sum"),
    total_concluintes = ("concluintes", "sum")
)

# Mostrar tabela com as estatísticas por turno
st.subheader("Análise por Turno")
st.dataframe(dados_por_turno)

# Criar gráficos para visualizar as diferenças entre os turnos
st.subheader("Comparação entre Turnos")
st.bar_chart(dados_por_turno, y=["total_vagas", "total_ingressantes", "total_concluintes"])