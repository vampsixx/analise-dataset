import streamlit as st
from controller.AcidenteController import AcidenteController

def tela_analise():
    with st.sidebar:
        st.title("Navegação")
        if st.button("⬅️ Voltar à Tela Inicial"):
            st.session_state["tela"] = "inicial"
            st.rerun()
        st.info("Carregue as planilhas para análise. Um banco de dados será criado para cada ano.")

    st.title("📊 Área de Análise de Acidentes")

    st.header("1. Carregamento dos Dados")
    st.info("O nome de cada planilha deve conter o ano dos dados (ex: 'dados_2022.csv').")

    if "uploads" not in st.session_state:
        st.session_state["uploads"] = [None]

    novos_uploads = []
    controller = AcidenteController()

    for i, file in enumerate(st.session_state["uploads"]):
        uploaded_file = st.file_uploader(
            f"Planilha {i+1}",
            type=["csv", "xlsx"],
            key=f"upload_{i}"
        )
        novos_uploads.append(uploaded_file)

        if uploaded_file is not None:
            with st.expander(f"Analisando Planilha: {uploaded_file.name}", expanded=True):
                try:
                    
                    df_pa, db_path = controller.processar_planilha(uploaded_file)
                    
                    st.success(f"Sucesso! Dados salvos em '{db_path}'.")
                    st.write("Amostra dos dados carregados (UF=PA):")
                    st.dataframe(df_pa.head()) 

                except Exception as e:
                    st.error(e)

    if len(st.session_state["uploads"]) > 0 and st.session_state["uploads"][-1] is not None:
        if len(st.session_state["uploads"]) < 3:
            novos_uploads.append(None)

    st.session_state["uploads"] = novos_uploads

    st.markdown("---")

    st.header("2. Visualização dos Dados Salvos")
    
    bancos_de_dados = controller.listar_bancos_de_dados()

    if not bancos_de_dados:
        st.warning("Nenhum banco de dados encontrado. Carregue uma planilha para começar.")
    else:
        st.subheader("Bancos de Dados Disponíveis:")
        
        num_cols = 3
        cols = st.columns(num_cols)
        for i, nome_banco in enumerate(bancos_de_dados):
            with cols[i % num_cols]:
                if st.button(f"Ver dados de {nome_banco}", key=nome_banco, use_container_width=True):
                    st.session_state['df_visualizar'] = controller.listar_dados_por_banco(nome_banco)
                    st.session_state['banco_visualizar'] = nome_banco

    if 'df_visualizar' in st.session_state:
        st.subheader(f"Visualizando dados de: {st.session_state['banco_visualizar']}")
        df_view = st.session_state['df_visualizar']
        if df_view.empty:
            st.warning("Não há dados para exibir para a UF='PA' neste banco de dados.")
        else:
            st.dataframe(df_view)