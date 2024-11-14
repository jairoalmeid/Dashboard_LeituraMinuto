import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from bancodedados.config import host, port, database, username, password 


# O arquivo config está oculto no GitIgnore, você deve criar esse arquivo e inserir o host, port, database, username e password do seu Banco de Dados.
conn_str = f"postgresql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(conn_str)

@st.cache_data
def get_data(query):
    conn = engine.raw_connection()
    try:
        df = pd.read_sql(query, con=conn)
    finally:
        conn.close()
    return df

