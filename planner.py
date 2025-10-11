import streamlit as st
import pandas as pd
import datetime
import os

# ---------- CONFIG ----------
st.set_page_config(page_title="Meu Planner Diário", page_icon="💖", layout="centered")

DATA_FILE = "planner_data.csv"

# ---------- FUNÇÕES DE DADOS ----------
def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["tipo", "item", "feito"])

def salvar_dados(df):
    df.to_csv(DATA_FILE, index=False)

df = carregar_dados()

# ---------- CABEÇALHO ----------
st.title("💗 Meu Planner Diário 💗")
st.image(
    "https://ca.pinterest.com/pin/225250418855358335/",  # banner rosa decorativo
    caption="Organize seu dia com estilo e leveza 🌸",
    use_container_width=True
)

st.markdown("**Por Maria Eduarda Fontoura ✨**")

# ---------- SIDEBAR ----------
view = st.sidebar.radio("Escolha uma seção:", ["Visão Geral", "Checklist", "Lista de Compras", "Tarefas", "Humor"])

# ---------- VISÃO GERAL ----------
if view == "Visão Geral":
    st.header("📅 Resumo do Dia")
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    st.subheader(f"Data: {hoje}")

    humor = st.selectbox("Como está seu humor hoje?", ["😀 Feliz", "😐 Neutra", "😢 Triste", "😡 Irritada", "😴 Cansada"])
    st.write(f"💭 Seu humor de hoje: {humor}")

# ---------- CHECKLIST ----------
elif view == "Checklist":
    st.header("✅ Checklist Diário")
    novo_item = st.text_input("Adicionar novo item:")
    if st.button("Adicionar"):
        if novo_item:
            df = df._append({"tipo": "checklist", "item": novo_item, "feito": False}, ignore_index=True)
            salvar_dados(df)

    checklist = df[df["tipo"] == "checklist"]
    for i, row in checklist.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            done = st.checkbox(row["item"], value=row["feito"], key=f"check_{i}")
        with col2:
            if st.button("🗑️", key=f"del_check_{i}"):
                df = df.drop(i)
                salvar_dados(df)
                st.experimental_rerun()
        df.loc[i, "feito"] = done
    salvar_dados(df)

# ---------- LISTA DE COMPRAS ----------
elif view == "Lista de Compras":
    st.header("🛒 Lista de Compras")
    novo_item = st.text_input("Adicionar produto:")
    if st.button("Adicionar produto"):
        if novo_item:
            df = df._append({"tipo": "compras", "item": novo_item, "feito": False}, ignore_index=True)
            salvar_dados(df)

    compras = df[df["tipo"] == "compras"]
    for i, row in compras.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"🛍️ {row['item']}")
        with col2:
            if st.button("🗑️", key=f"del_compras_{i}"):
                df = df.drop(i)
                salvar_dados(df)
                st.experimental_rerun()

# ---------- TAREFAS ----------
elif view == "Tarefas":
    st.header("📝 Suas Tarefas")
    nova_tarefa = st.text_input("Adicionar tarefa:")
    if st.button("Adicionar tarefa"):
        if nova_tarefa:
            df = df._append({"tipo": "tarefas", "item": nova_tarefa, "feito": False}, ignore_index=True)
            salvar_dados(df)

    tarefas = df[df["tipo"] == "tarefas"]
    for i, row in tarefas.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            done = st.checkbox(row["item"], value=row["feito"], key=f"task_{i}")
        with col2:
            if st.button("🗑️", key=f"del_task_{i}"):
                df = df.drop(i)
                salvar_dados(df)
                st.experimental_rerun()
        df.loc[i, "feito"] = done
    salvar_dados(df)

# ---------- HUMOR ----------
elif view == "Humor":
    st.header("🌈 Como está se sentindo hoje?")
    humor = st.select_slider(
        "Escolha seu humor:",
        options=["😢", "😐", "🙂", "😄", "🤩"],
        value="🙂"
    )
    st.write(f"Seu humor de hoje: {humor}")
    st.balloons()

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Feito com 💖 por Maria Eduarda Fontoura")

