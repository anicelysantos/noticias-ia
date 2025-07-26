import streamlit as st
import pandas as pd
from streamlit_timeline import timeline
from datetime import datetime
import json

st.set_page_config(layout="wide")

# Título e autoria alinhados à esquerda
st.markdown("""
    <div style="text-align: left;">
        <h1>NoticIAs</h1>
        <h4 style="margin-top: -10px; color: grey;">Projeto desenvolvido por Anicely Santos com curadoria de notícias do IP.Rec.</h4>
    </div>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    return pd.read_csv("noticias.csv", parse_dates=["Data"])

df = carregar_dados()

# Filtros horizontais
col1, col2, col3, col4 = st.columns(4)

with col1:
    anos = sorted(df['Data'].dt.year.dropna().unique())
    ano = st.selectbox("Ano", ["Todos"] + list(anos))

with col2:
    meses = sorted(df['Data'].dt.month.dropna().unique())
    nome_meses = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
                  7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
    mes = st.selectbox("Mês", ["Todos"] + [nome_meses[m] for m in meses])

with col3:
    categorias = sorted(df['Categoria'].dropna().unique())
    categoria = st.selectbox("Categoria", ["Todas"] + categorias)

with col4:
    tipos = sorted(df['Tipo'].dropna().unique())
    tipo = st.selectbox("Tipo", ["Todos"] + tipos)

# Aplicando filtros
df_filtrado = df.copy()

if ano != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Data'].dt.year == int(ano)]
if mes != "Todos":
    mes_num = list(nome_meses.keys())[list(nome_meses.values()).index(mes)]
    df_filtrado = df_filtrado[df_filtrado['Data'].dt.month == mes_num]
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado['Categoria'] == categoria]
if tipo != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Tipo'] == tipo]

#quantidade de noticias achadas pelo filtro
st.markdown(f"### {len(df_filtrado)} notícia(s) encontrada(s)")

# Montando eventos da timeline
eventos = []
for _, row in df_filtrado.iterrows():
    imagem_html = f"<img src='{row['Imagem']}' style='width:80px; height:auto; float:left; margin-right:10px;'/>" if pd.notna(row["Imagem"]) else ""
    resumo_html = f"<p style='margin-top:5px;'>{row['Resumo']}</p>" if pd.notna(row.get("Resumo", "")) else ""
    conteudo = f"""
        <div style='display: flex; align-items: flex-start;'>
            {imagem_html}
            <div>
                <small>{row['Fonte']}</small><br>
                {resumo_html}
                <a href="{row['Link']}" target="_blank">Ler mais</a>
            </div>
        </div>
    """
    eventos.append({
        "start_date": {"year": row["Data"].year, "month": row["Data"].month},
        "text": {"headline":  row["Titulo"], "text": conteudo},
        "group": row.get("Categoria", "Outros")
    })

timeline_data = {
    "title": {"text": {"headline": "NoticIAs", "text": "Linha do tempo de notícias sobre IA"}},
    "events": eventos
}

timeline(json.dumps(timeline_data), height=600)
