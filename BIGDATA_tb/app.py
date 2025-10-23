import streamlit as st  # construir dashboards
from streamlit_option_menu import option_menu  # menu de navegação
import pandas as pd  # manipulação de dados
import plotly.express as px  # construir graficos
st.set_page_config(page_title="Projeto Big Data - Análise de Acidentes de Trânsito no Pará",
                   page_icon=":car:", layout="wide")
with st.sidebar:
    selected = option_menu(
        menu_title="Projeto Big Data",
        options=["Home", "Analise de dados", "Visualização de Dados", "Acidentes por município",
                 "Classificações", "Período"],
        icons=["house", "bar-chart", "bar-chart", "map", "list", "calendar"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important"},
            "icon": {"color": "#541a83e6", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#8A87871F",
            },
            "nav-link-selected": {"background-color": "#8A87871F"},
        },
    )
# Carregar dados
    arquivos_anos = {
        "2023": "datatran2023.csv",
        "2024": "datatran2024.csv",
        "2025": "datatran2025.csv"
    }
    anos = list(arquivos_anos.keys())
    ano_selecionado = st.selectbox("Selecione o ano", anos)
    arquivo_selecionado = arquivos_anos[ano_selecionado]
    df = pd.read_csv(arquivo_selecionado, sep=';',
                     encoding='latin1', low_memory=False)
    multselected_anos = st.multiselect(
        "Selecione os anos para análise comparativa", anos, default=anos)
    # Define uma paleta de cores personalizada
    rocket_palette = [
        "#160141", "#260446", "#3A0453", "#66135C", "#792860", "#A53950", "#a54848", "#A06444", "#9E7E42", "#AC973C"
    ]
# Página inicial
if selected == "Home":
    st.header("👥Cliente e Contexto")
    st.subheader(
        "Informações sobre o cliente, fonte de dados, ferramentas utilizadas e entre outros.")
    st.markdown("Fonte dos dados: [Detran-PA](https://www.detran.pa.gov.br/)")
    st.text("Desenvolvido por: Kemmily Riany, Letícia Keller, Matheus Gaia, Raphael Valentin e João Paulo")
    st.write("Este projeto tem como objetivo analisar os dados de acidentes de trânsito no estado do Pará entre os anos de 2023 e 2025. E fornecendo métodos para visualização de dados do usuario, "
             "buscamos identificar padrões e tendências que possam contribuir para a melhoria da segurança viária na região. Os dados foram coletados a partir de registros oficiais de acidentes de trânsito fornecidos pelo Detran-PA,"
             " abrangendo informações detalhadas sobre os incidentes, incluindo localização, causas, condições climáticas e características dos envolvidos. Segue então duas análises principais: visualização de dados e análise de dados. E ainda, disponibilizamos análises específicas como acidentes por município, classificações e período.")
    st.text("As ferramentas utilizadas incluem Streamlit para a criação da interface web, Pandas para manipulação de dados, Plotly e Matplotlib para visualizações gráficas, SQLite como banco de dados .")
    st.markdown(
        "## Selecione uma opção no menu lateral para explorar diferentes análises correspondentes aos anos de 2023-2025.")

elif selected == "Analise de dados":
    st.title("Análise do Trânsito no Pará")
    st.markdown(
        "*Sua ferramenta para transformar dados de trânsito em ações de segurança.*")
    st.markdown("---")

    st.markdown(
        """
        Bem-vindo ao sistema! Esta plataforma foi desenvolvida para auxiliar na análise de
        acidentes de trânsito no estado do Pará, permitindo a geração de relatórios e
        visualizações que podem apoiar a tomada de decisões para um trânsito mais seguro.
        """
    )
    with st.expander(" Como funciona?"):
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

    if st.button(" Começar a Análise"):
        st.session_state["tela"] = "analise"
        st.rerun()

elif selected == "Visualização de Dados":
    st.header("Visualização de Dados")

elif selected == "Acidentes por município":
    st.header("Análise de Acidentes por Município")
    st.write("Esta seção apresenta uma análise dos acidentes de trânsito no Pará, categorizados pelos municípios com mais acidentes registrados.")

    # Filtrar apenas registros do estado do Pará (uf == 'PA').
    # Trata tanto 'uf' quanto 'UF', se presente.
    if 'uf' in df.columns:
        df = df[df['uf'] == 'PA']
    elif 'UF' in df.columns:
        df = df[df['UF'] == 'PA']
    top_municipios = df['municipio'].value_counts().nlargest(10)
    df_grafico = pd.DataFrame(
        {'municipio': top_municipios.index, 'acidentes': top_municipios.values})

    fig = px.bar(df_grafico, x='municipio', y='acidentes', title=f"10 Municípios Com Mais Acidentes no Pará ({ano_selecionado})",
                 color='municipio', color_discrete_sequence=rocket_palette,
                 category_orders={
                     'municipio': df_grafico['municipio'].tolist()},
                 template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

elif selected == "Classificações":
    st.header("Análise de Acidentes por Classificação")
    st.write("Esta seção apresenta uma análise dos acidentes de trânsito no Pará, categorizados por diferentes classificações como tipo de acidente, gravidade e condição da via.")
    st.subheader("Acidentes por Tipo")
    if 'uf' in df.columns:
        df = df[df['uf'] == 'PA']
    elif 'UF' in df.columns:
        df = df[df['UF'] == 'PA']
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)

    with col1:
        # Verifica se a coluna existe
        if 'tipo_acidente' in df.columns:
            # Agrupa os dados por tipo de acidente
            tipo = df['tipo_acidente'].value_counts().reset_index()
            tipo.columns = ['Tipo de Acidente', 'Número de Acidentes']
            tipo = tipo.sort_values(by='Número de Acidentes', ascending=False)

            # Gráfico de barras
            fig_tipo = px.bar(
                tipo,
                x='Tipo de Acidente',
                y='Número de Acidentes',
                title=f"Tipos de Acidentes no Pará ({ano_selecionado})",
                color='Tipo de Acidente',
                color_discrete_sequence=rocket_palette,
            )

            fig_tipo.update_layout(template='plotly_dark')

            st.plotly_chart(fig_tipo)
        else:
            st.warning("Coluna 'tipo_acidente' não encontrada no arquivo.")
    # Verifica se a coluna existe
    with col2:
        if 'classificacao_acidente' in df.columns:
            # Agrupa os dados por classificação
            classificacao = df['classificacao_acidente'].value_counts(
            ).reset_index()
            classificacao.columns = ['Classificação', 'Número de Acidentes']

            # Gráfico de pizza
            fig_classificacao = px.pie(
                classificacao,
                names='Classificação',
                values='Número de Acidentes',
                title=f"Classificação de Acidentes no Pará por gravidade ({ano_selecionado})",
                color='Classificação',
                color_discrete_sequence=rocket_palette,
                hole=0.3  # pizza com buraco no centro
            )

            fig_classificacao.update_traces(
                textposition='inside', textinfo='percent+label')
            fig_classificacao.update_layout(template='plotly_dark')
            fig_classificacao.update_layout(xaxis_tickangle=-45)

            st.plotly_chart(fig_classificacao, use_container_width=True)
        else:
            st.warning(
                "Coluna 'classificacao_acidente' não encontrada no arquivo.")

    with col3:
        if 'tipo_pista' in df.columns:
            tipo_pista = df['tipo_pista'].value_counts().reset_index()
            tipo_pista.columns = ['Tipo de Pista', 'Número de Acidentes']

            fig_tipo_pista = px.bar(
                tipo_pista,
                x='Tipo de Pista',
                y='Número de Acidentes',
                title=f"Tipo de Pista nos Acidentes no Pará ({ano_selecionado})",
                color='Tipo de Pista',
                color_discrete_sequence=rocket_palette,
            )

            fig_tipo_pista.update_layout(template='plotly_dark')

            st.plotly_chart(fig_tipo_pista)
        else:
            st.warning("Coluna 'tipo_pista' não encontrada no arquivo.")

elif selected == "Período":
    df = pd.read_csv("acidentes_para.csv")
    st.header("Análise de Acidentes por Período")
    st.write("Esta seção apresenta uma análise dos acidentes de trânsito no Pará, categorizados por diferentes períodos incluindo dia, mês e ano, além de interferências do clima.")
    st.subheader("Acidentes por Ano")
