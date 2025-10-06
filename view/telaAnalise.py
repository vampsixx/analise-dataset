import streamlit as st
from controller.AcidenteController import AcidenteController

def tela_analise():
    st.title("📊 Área de Análise de Acidentes")

    if "uploads" not in st.session_state:
        st.session_state["uploads"] = [None]

    novos_uploads = []
    controller = AcidenteController()

    for i, file in enumerate(st.session_state["uploads"]):
        uploaded_file = st.file_uploader(f"Planilha {i+1}", type=["csv", "xlsx"], key=f"upload_{i}")
        novos_uploads.append(uploaded_file)

        if uploaded_file is not None:
            st.success(f"Arquivo {uploaded_file.name} carregado!")

            # Processa e salva no banco
            try:
                df_pa = controller.processar_planilha(uploaded_file)
                st.subheader(f"Pré-visualização - {uploaded_file.name} (UF=PA)")
                st.dataframe(df_pa.head())
            except Exception as e:
                st.error(e)

            # Se não atingiu o limite, adiciona novo campo
            if i == len(st.session_state["uploads"]) - 1 and len(st.session_state["uploads"]) < 4:
                novos_uploads.append(None)

    st.session_state["uploads"] = novos_uploads

    # Mostrar dados já salvos no banco
    if st.button("📥 Ver todos os dados do banco (UF=PA)"):
        df_db = controller.listar_pa()
        st.dataframe(df_db.head(50))
