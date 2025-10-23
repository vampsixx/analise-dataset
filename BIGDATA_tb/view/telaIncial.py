import streamlit as st

def tela_inicial():
        with st.sidebar:
            st.title("Navegação")
            if st.button("➡️ Análise de Dados"):
                st.session_state["tela"] = "analise"
                st.rerun() 
            if st.button("➡️ Visualização de Dados"):
                st.session_state["tela"] = "visualizacao"
                st.rerun()

        st.title("Análise do Trânsito no Pará")
        st.markdown("*Sua ferramenta para transformar dados de trânsito em ações de segurança.*")

        st.markdown("---")

        st.markdown(
        """
        Bem-vindo ao sistema! Esta plataforma foi desenvolvida para auxiliar na análise de
        acidentes de trânsito no estado do Pará, permitindo a geração de relatórios e
        visualizações que podem apoiar a tomada de decisões para um trânsito mais seguro.
        """
    )
        with st.expander("📈 Como funciona?"):
            st.info(
                """
                1.  **Carregue os Dados:** Na tela de análise, você poderá carregar até 3 planilhas
                    (.csv ou .xlsx) contendo os registros de acidentes.
                2.  **Visualize os Gráficos:** O sistema irá processar os dados e gerar
                    gráficos interativos sobre as principais causas, locais e características dos acidentes.
                3.  **Obtenha Insights:** Com base nas análises, identifique os pontos críticos e
                    planeje ações preventivas, como melhorias na via ou aumento da fiscalização.
                """
            )

        st.markdown("") 

        if st.button("🚀 Começar a Análise"):
            st.session_state["tela"] = "analise"
            st.rerun()