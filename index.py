import streamlit as st
from view.telaIncial import tela_inicial
from view.telaAnalise import tela_analise
from view.visuzalicao import tela_visualizacao


st.set_page_config(
    page_title="Análise de Trânsito PA",
    page_icon="🚦",
    layout="centered"
)

def main():
    if "tela" not in st.session_state:
        st.session_state["tela"] = "inicial"

    if st.session_state["tela"] == "inicial":
        tela_inicial()
    elif st.session_state["tela"] == "analise":
        tela_analise()
    elif st.session_state["tela"] == "visualizacao":
        tela_visualizacao()
        

if __name__ == "__main__":
    main()