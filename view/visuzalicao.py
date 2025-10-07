import streamlit as st

def tela_visualizacao():
    with st.sidebar:
        st.title("Navegação")
        if st.button("⬅️ Voltar à Tela Inicial"):
            st.session_state["tela"] = "inicial"
            st.rerun()

        if st.button("⬅️ Voltar à Tela de Análise"):
            st.session_state["tela"] = "analise"
            st.rerun()
       
        st.info("Visualize gráficos e relatórios baseados nos dados carregados.")

    st.title("📈 Área de Visualização de Dados")

    st.markdown(
        """
        Aqui você poderá visualizar gráficos e relatórios gerados a partir dos dados de acidentes
        carregados anteriormente. Selecione o banco de dados desejado para começar a análise.
        """
    )

