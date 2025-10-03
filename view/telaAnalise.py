import streamlit as st
import pandas as pd

def tela_analise():
    st.title("📊 Área de Análise de Acidentes")

    # Inicializa lista de uploads se não existir
    if "uploads" not in st.session_state:
        st.session_state["uploads"] = [None]  # começa com 1 campo

    st.markdown("### Faça upload das planilhas (até 4 arquivos)")

   