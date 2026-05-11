import streamlit as st
import pandas as pd
import json
import plotly.express as px
import os

st.set_page_config(page_title="DevSecOps Analytics", layout="wide")
st.title("🛡️ Painel de Segurança - DevSecOps Lab")

# Tenta ler o arquivo gerado pelo pipeline (certifique-se de ter baixado o artefato)
sbom_path = 'public/sbom.json'

if os.path.exists(sbom_path):
    with open(sbom_path) as f:
        data = json.load(f)
    
    # Extrair componentes do SBOM (CycloneDX)
    components = data.get('components', [])
    df = pd.json_normalize(components)

    # Métricas Principais
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Dependências", len(df))
    col2.metric("Linguagem Base", "Python")
    col3.metric("Status", "Análise Concluída")

    st.divider()

    # Gráfico de Tipos de Componentes
    st.subheader("📦 Distribuição de Pacotes")
    if 'type' in df.columns:
        fig = px.pie(df, names='type', title="Tipos de Bibliotecas")
        st.plotly_chart(fig)

    # Tabela de Dependências para busca
    st.subheader("🔍 Inventário de Software (SBOM)")
    st.dataframe(df[['name', 'version', 'purl']].dropna(), use_container_width=True)

else:
    st.error(f"Arquivo {sbom_path} não encontrado. Baixe o artefato do GitHub e coloque na pasta 'public/'.")
