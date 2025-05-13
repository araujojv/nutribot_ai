import streamlit as st
import sqlite3
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="NutriBot", layout="centered")
st.title("🍎 NutriBot – Assistente Nutricional")

# Simular login com ID de usuário
st.sidebar.subheader("👤 Login do Usuário")
usuario_id = st.sidebar.number_input("ID do usuário", min_value=1, step=1)

menu = st.sidebar.selectbox("Navegar", ["Calcular TDEE", "Registrar Refeição", "Histórico"])

# ============================ CALCULAR TDEE ============================
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

# ============================ REGISTRAR REFEIÇÃO ============================
elif menu == "Registrar Refeição":
    st.subheader("🍽️ Registrar nova refeição")

    if not usuario_id:
        st.warning("⚠️ Por favor, insira seu ID de usuário no menu lateral.")
    else:
        try:
            alimentos = requests.get("http://127.0.0.1:8000/alimentos").json()
        except:
            alimentos = []
            st.error("❌ Erro ao carregar lista de alimentos")

        nome = st.selectbox("Selecione o alimento", alimentos)
        gramas = st.number_input("Quantidade (g)", 0.0, 1000.0, 100.0)

        if st.button("Buscar e salvar"):
            entrada = [{"alimento": nome, "gramas": gramas}]
            res = requests.post("http://127.0.0.1:8000/calcular_refeicao", json=entrada)

            if res.status_code == 200:
                dados = res.json()
                if "detalhes" in dados and dados["detalhes"]:
                    item = dados["detalhes"][0]
                    if "erro" in item:
                        st.error(f"Erro: {item['erro']}")
                    else:
                        st.success("Refeição encontrada:")
                        st.json(item)

                        # Vincula o usuário
                        item["usuario_id"] = usuario_id

                        save = requests.post("http://127.0.0.1:8000/refeicao", json=item)
                        if save.status_code == 200:
                            st.success("✅ Refeição registrada com sucesso!")
                        else:
                            st.error("Erro ao registrar no banco.")
            else:
                st.error("Erro ao buscar dados.")

# ============================ HISTÓRICO ============================
elif menu == "Histórico":
    st.subheader("📅 Histórico de Refeições")

    if not usuario_id:
        st.warning("⚠️ Por favor, insira seu ID de usuário no menu lateral.")
    else:
        try:
            res = requests.get(f"http://127.0.0.1:8000/refeicao/{usuario_id}")
            if res.status_code == 200:
                df = pd.DataFrame(res.json())
                if not df.empty:
                    st.dataframe(df)

                    st.subheader("📈 Comparativo Nutricional")
                    nutrientes = df.melt(
                        id_vars=["alimento"],
                        value_vars=["calorias", "proteinas", "carboidratos", "gorduras"],
                        var_name="Nutriente",
                        value_name="Valor"
                    )

                    fig = px.bar(nutrientes, x="alimento", y="Valor", color="Nutriente", barmode="group")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Nenhuma refeição registrada ainda.")
            else:
                st.error("Erro ao buscar histórico.")
        except:
            st.error("Erro ao conectar com a API.")
