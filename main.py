import pandas as pd
import plotly.express as px
import streamlit as st




if __name__ == '__main__':
    st.set_page_config(page_title="Finance Trends 2020–2025", layout="wide") # Configuração da página


    df = pd.read_csv("Finance_Trends.csv").dropna() # Carregamento dos dados


    df.dropna(inplace=True) # limpeza dos dados
    df['Stock_Marktet'].replace({'Yes': 1, 'No': 0}, inplace=True) # Conversão de yes/no para 1/0

    st.title("Keagle Finance Trends Dashboard") #titulo do dashboard
    st.markdown("Análise interativa do perfil e comportamento de investidores entre 2020 e 2025.")

    # Filtros interativos
    st.sidebar.header("🎛️ Filtros")
    gender_filter = st.sidebar.selectbox("Gênero", options=["Todos"] + list(df["gender"].dropna().unique()))
    age_range = st.sidebar.slider("Faixa Etária", int(df["age"].min()), int(df["age"].max()), (25, 45))
    duration_filter = st.sidebar.multiselect("Duração do Investimento", options=df["Duration"].dropna().unique())
    objective_filter = st.sidebar.multiselect("Objetivo de Poupança",
                                              options=df["What are your savings objectives?"].dropna().unique())

    # Aplicar filtros
    filtered_df = df.copy()
    if gender_filter != "Todos":
        filtered_df = filtered_df[filtered_df["gender"] == gender_filter]
    filtered_df = filtered_df[(filtered_df["age"] >= age_range[0]) & (filtered_df["age"] <= age_range[1])]
    if duration_filter:
        filtered_df = filtered_df[filtered_df["Duration"].isin(duration_filter)]
    if objective_filter:
        filtered_df = filtered_df[filtered_df["What are your savings objectives?"].isin(objective_filter)]

        # Aba 1 - Perfil
    st.header("1. Perfil dos Investidores")
    col1, col2 = st.columns(2)
    with col1:
        fig_gender = px.pie(filtered_df, names="gender", title="Distribuição por Gênero")
        st.plotly_chart(fig_gender, use_container_width=True)
    with col2:
        fig_age = px.histogram(filtered_df, x="age", nbins=10, title="Distribuição por Idade")
        st.plotly_chart(fig_age, use_container_width=True)

    # Aba 2 – Preferências de Investimento
    st.header("2. Preferências de Investimento")
    invest_cols = ["Mutual_Funds", "Equity_Market", "Debentures", "Government_Bonds",
                   "Fixed_Deposits", "PPF", "Gold", "Stock_Marktet"]
    df_pref = filtered_df[invest_cols].mean().reset_index()
    df_pref.columns = ["Avenue", "Average"]
    fig_pref = px.bar(df_pref, x="Avenue", y="Average", title="Popularidade dos Tipos de Investimento")
    st.plotly_chart(fig_pref, use_container_width=True)

    # Aba 3 – Objetivos e Fatores
    st.header("3. Objetivos e Fatores")
    col3, col4 = st.columns(2)
    with col3:
        obj_counts = filtered_df["What are your savings objectives?"].value_counts().reset_index()
        obj_counts.columns = ["Objective", "Count"]
        fig_obj = px.bar(obj_counts, x="Objective", y="Count", title="Objetivos de Poupança")
        st.plotly_chart(fig_obj, use_container_width=True)
    with col4:
        factor_counts = filtered_df["Factor"].value_counts().reset_index()
        factor_counts.columns = ["Factor", "Count"]
        fig_factor = px.bar(factor_counts, x="Factor", y="Count", title="Fatores que Influenciam a Decisão")
        st.plotly_chart(fig_factor, use_container_width=True)

    # Aba 4 – Fontes de Informação
    st.header("4. Fontes de Informação")
    source_counts = filtered_df["Source"].value_counts().reset_index()
    source_counts.columns = ["Source", "Count"]
    fig_source = px.bar(source_counts, x="Source", y="Count", title="Fontes de Informação Mais Utilizadas")
    st.plotly_chart(fig_source, use_container_width=True)
