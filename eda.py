import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 EDA Automática", layout="wide")

st.title("📊 EDA Automática de Planilhas")
st.write("Upload de planilhas, diagnóstico de colunas e análise exploratória automática.")

uploaded_file = st.file_uploader(
    "Faça upload do arquivo (.csv ou .xlsx)",
    type=["csv", "xlsx"]
)

if uploaded_file:

    # =============================
    # Leitura do arquivo
    # =============================
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.subheader('🔍 Prévia dos dados')
    st.dataframe(df.head())

    st.subheader("🧠 Diagnóstico das Colunas")

    col_info = []

    for col in df.columns:
        col_info.append({
            "Coluna":col,
            "Tipo Detectado": str(df[col].dtype),
            "% Nulos": round((df[col].isna().sum() / df.shape[0]) * 100,2),
            'Valores Únicos': df[col].nunique()
        })
    
    col_info_df = pd.DataFrame(col_info)
    st.dataframe(col_info_df)

    st.divider()

    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    cat_cols = [col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])]


    st.subheader("📈 Análise Exploratória – Variáveis Numéricas")

    for col in numeric_cols:
        st.markdown(f'### 🔢 {col}')

        series = df[col].dropna()

        if series.empty:
            st.warning('Coluna sem valores numéricos válidos.')
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        li = q1 - 1.5 * iqr
        ls = q3 + 1.5 * iqr
        media = series.mean()
        mediana = series.median()
        desvio = series.std()

        outliers = series[(series < li) | (series > ls)]

        col1, col2, col3 = st.columns(3)

        col1.metric('Q1', round(q1,2))
        col2.metric('Q3', round(q3))
        col3.metric('IQR', round(iqr))

        col1.metric("Limite Inferior", round(li, 2))
        col2.metric("Limite Superior", round(ls, 2))
        col3.metric("Outliers", outliers.count())

        col1.metric("Média", round(media, 2))
        col2.metric("Mediana", round(mediana, 2))
        col3.metric("Desvio Padrão", round(desvio, 2))

        fig, ax = plt.subplots(1, 2, figsize=(12, 4))

        ax[0].hist(series, bins=30)
        ax[0].set_title("Histograma")

        ax[1].boxplot(series, vert=False)
        ax[1].axvline(li, linestyle="--")
        ax[1].axvline(ls, linestyle="--")
        ax[1].set_title("Boxplot")

        st.pyplot(fig)
        st.divider()

    st.subheader("📊 Análise Exploratória – Variáveis Categóricas")

    for col in cat_cols:
        st.markdown(f'### 🔤 {col}')

        series = df[col].dropna().astype(str)

        if series.empty:
            st.warning("Coluna sem valores válidos.")
            continue
        
        vc = series.value_counts()
        n_categories = vc.shape[0]

        st.write(f"Categorias únicas: **{n_categories}**")

        if n_categories <=5:
            plot_data = vc
            st.dataframe(vc)
        else:
            top5 = vc.head(4)
            outros = vc.iloc[4:].sum()
            plot_data = pd.concat([top5, pd.Series({"outros":outros})])

        fig, ax = plt.subplots(figsize=(8, 4))
        plot_data.plot(kind="bar", ax=ax)
        ax.set_title(f"Distribuição por {col}")
        ax.set_ylabel("Quantidade")

        st.pyplot(fig)
        st.divider()

    st.success("✅ Análise finalizada com sucesso!")