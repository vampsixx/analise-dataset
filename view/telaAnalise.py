import streamlit as st
from controller.AcidenteController import AcidenteController
import os

def tela_analise():
    with st.sidebar:
        st.title("Navegação")
        if st.button("⬅️ Voltar à Tela Inicial"):
            st.session_state["tela"] = "inicial"
            st.rerun()
        if st.button("➡️ Visualização de Dados"):
            st.session_state["tela"] = "visualizacao"
            st.rerun()

        st.info("Carregue as planilhas para análise. Um banco de dados será criado para cada ano.")

    st.title("📊 Área de Análise de Acidentes")
    st.header("1. Carregamento dos Dados")
    st.info("O nome de cada planilha deve conter o ano dos dados (ex: 'dados_2022.csv').")

    if 'confirmation_state' not in st.session_state:
        st.session_state.confirmation_state = {}

    if "uploads" not in st.session_state:
        st.session_state["uploads"] = [None]

    novos_uploads = []
    controller = AcidenteController()

    for i, file in enumerate(st.session_state.get("uploads", [None])):
        uploaded_file = st.file_uploader(
            f"Planilha {i+1}",
            type=["csv", "xlsx"],
            key=f"upload_{i}"
        )
        novos_uploads.append(uploaded_file)

        if uploaded_file is not None:
            st.markdown("---")
            ano = controller.extrair_ano_do_nome(uploaded_file.name)
            
            if not ano:
                st.error(f"Não foi possível extrair um ano (4 dígitos) do nome do arquivo '{uploaded_file.name}'.")
                continue

            db_path_esperado = f"data/acidentes_{ano}.db"
            db_existe = os.path.exists(db_path_esperado)

            def processar():
                with st.spinner(f"Processando e salvando dados de {ano}..."):
                    try:
                        df_pa, db_path = controller.processar_planilha(uploaded_file)
                        st.success(f"Sucesso! Dados para o ano de {ano} foram salvos em '{db_path}'.")
                        with st.expander("Ver amostra dos dados carregados"):
                            st.dataframe(df_pa.head())
                    except Exception as e:
                        st.error(e)
            
            if db_existe and st.session_state.confirmation_state.get(i) is None:
                st.warning(f"⚠️ Já existem dados para o ano de {ano}. Deseja sobrescrevê-los com o arquivo '{uploaded_file.name}'?")
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("Sim, sobrescrever", key=f"overwrite_{i}"):
                        st.session_state.confirmation_state[i] = 'overwrite'
                        st.rerun() 
                with col2:
                    if st.button("Não, cancelar", key=f"cancel_{i}"):
                        st.session_state.confirmation_state[i] = 'cancel'
                        st.rerun() 
            elif st.session_state.confirmation_state.get(i) == 'overwrite':
                processar()
                st.session_state.confirmation_state[i] = 'done' 
            
            elif st.session_state.confirmation_state.get(i) == 'cancel':
                st.info(f"Operação para o arquivo '{uploaded_file.name}' cancelada.")
                st.session_state.confirmation_state[i] = 'done' 

     
            elif not db_existe:
                 processar()


    for i in list(st.session_state.confirmation_state.keys()):
        if i >= len(novos_uploads) or novos_uploads[i] is None:
            del st.session_state.confirmation_state[i]


    if len(st.session_state.get("uploads", [])) > 0 and st.session_state["uploads"][-1] is not None:
        if len(st.session_state["uploads"]) < 3:
            novos_uploads.append(None)

    st.session_state["uploads"] = novos_uploads