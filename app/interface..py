import streamlit as st
import sqlite3
import pandas as pd
import requests


conn = sqlite3.connect("data/nutricao.db", check_same_thread=False)

st.set_page_config(page_title="NutriBot", layout="centered")

st.title("🍎 NutriBot – Assistente Nutricional")

menu = st.sidebar.selectbox("Navegar", ["Calcular TDEE", "Registrar Refeição", "Histórico"])


if menu == "Calcular TDEE":
    st.subheader("📊 Cálculo de Gasto Energético Diário")

    peso = st.number_input("Peso (kg)", 30.0, 200.0, 70.0)
    altura = st.number_input("Altura (cm)", 100.0, 250.0, 175.0)
    idade = st.number_input("Idade", 10, 100, 25)
    sexo = st.selectbox("Sexo", ["masculino", "feminino"])
    nivel = st.selectbox("Nível de atividade", ["sedentario", "leve", "moderado", "intenso", "muito_intenso"])
    objetivo = st.selectbox("Objetivo", ["manter", "emagrecer", "ganhar"])

    if st.button("Calcular"):
        payload = {
            "peso": peso,
            "altura": altura,
            "idade": idade,
            "sexo": sexo,
            "nivel_atividade": nivel,
            "objetivo": objetivo
        }
        res = requests.post("http://127.0.0.1:8000/calcular_gasto_energetico", json=payload)
        if res.status_code == 200:
            resultado = res.json()
            st.success(f"TMB: {resultado['TMB']} kcal")
            st.success(f"TDEE: {resultado['TDEE']} kcal")
            st.info(f"Meta diária ({objetivo}): {resultado['meta_calorica_diaria']} kcal")
        else:
            st.error("Erro ao calcular.")


elif menu == "Registrar Refeição":
    st.subheader("🍽️ Registrar nova refeição")

    alimento = st.text_input("Alimento")
    gramas = st.number_input("Quantidade (g)", 0.0, 1000.0, 100.0)
    calorias = st.number_input("Calorias", 0.0, 2000.0)
    proteinas = st.number_input("Proteínas", 0.0, 100.0)
    carboidratos = st.number_input("Carboidratos", 0.0, 300.0)
    gorduras = st.number_input("Gorduras", 0.0, 100.0)

    if st.button("Salvar refeição"):
        payload = {
            "alimento": alimento,
            "gramas": gramas,
            "calorias": calorias,
            "proteinas": proteinas,
            "carboidratos": carboidratos,
            "gorduras": gorduras
        }
        res = requests.post("http://127.0.0.1:8000/refeicao", json=payload)
        if res.status_code == 200:
            st.success("✅ Refeição registrada com sucesso!")
        else:
            st.error("Erro ao registrar refeição.")


elif menu == "Histórico":
    st.subheader("📅 Histórico de Refeições")
    df = pd.read_sql_query("SELECT * FROM refeicoes ORDER BY horario DESC", conn)
    st.dataframe(df)
