import streamlit as st

def tela_inicial():
    st.title("🚦 Sistema de Análise de Acidentes de Trânsito")
    st.markdown("""
    Bem-vindo ao sistema!  
    Aqui você poderá carregar planilhas de acidentes de trânsito e gerar estatísticas
    para auxiliar na análise dos dados.
    """)

    if st.button("👉 Iniciar Análise"):
        st.session_state["tela"] = "analise"
