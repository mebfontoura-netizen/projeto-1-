import streamlit as st
import pandas as pd
import datetime
import os

# ---------- CONFIGURAÇÃO ----------
st.set_page_config(page_title="Meu Planner Diário", page_icon="📝", layout="centered")

# ---------- TÍTULO E IMAGEM DECORATIVA ----------
st.title("🩷 Meu Planner Diário 🩷")
st.image(
    "https://i.imgur.com/jv3x8mV.png",  # imagem válida e bonita
    caption="Organize seu dia com estilo e tranquilidade 🌸",
    use_container_width=True,
)

# ---------- DEFINIÇÃO DO ARQUIVO DE DADOS ----------
DATA_FILE = "planner_data.csv"

# ---------- CARREGAR OU CRIAR DADOS ----------
if os.path.exists(DATA_FILE):
    data = pd.read_csv(DATA_FILE)
else:
    data = pd.DataFrame(columns=["tipo", "texto", "feito", "data"])

# ---------- MENU LATERAL ----------
view = st.sidebar.radio(
    "Escolha uma seção:",
    ["Visão Geral", "Checklist", "Lista de Compras", "Tarefas", "Humor"]
)

# ---------- FUNÇÃO DE SALVAR ----------
def salvar_dados():
    data.to_csv(DATA_FILE, index=False)

# ---------- VISÃO GERAL ----------
if view == "Visão Geral":
    st.subheader("📅 Visão Geral do Dia")
    hoje = datetime.date.today()
    st.write(f"Data de hoje: **{hoje.strftime('%d/%m/%Y')}**")

    tarefas = data[data["tipo"] == "Tarefa"]
    concluidas = tarefas["feito"].sum() if not tarefas.empty else 0
    total = len(tarefas)

    if total > 0:
        progresso = (concluidas / total) * 100
        st.progress(progresso / 100)
        st.write(f"✅ {concluidas} de {total} tarefas concluídas ({progresso:.0f}%)")
    else:
        st.info("Nenhuma tarefa adicionada ainda!")

# ---------- CHECKLIST ----------
elif view == "Checklist":
    st.subheader("📝 Checklist")

    nova = st.text_input("Adicionar novo item:")
    if st.button("Adicionar"):
        if nova.strip():
            data.loc[len(data)] = ["Checklist", nova, False, datetime.date.today()]
            salvar_dados()
            st.success("Item adicionado!")

    for i, row in data[data["tipo"] == "Checklist"].iterrows():
        feito = st.checkbox(row["texto"], value=row["feito"], key=f"check_{i}")
        if feito != row["feito"]:
            data.at[i, "feito"] = feito
            salvar_dados()

# ---------- LISTA DE COMPRAS ----------
elif view == "Lista de Compras":
    st.subheader("🛒 Lista de Compras")

    item = st.text_input("Adicionar item à lista:")
    if st.button("Adicionar item"):
        if item.strip():
            data.loc[len(data)] = ["Compras", item, False, datetime.date.today()]
            salvar_dados()
            st.success("Item adicionado à lista!")

    for i, row in data[data["tipo"] == "Compras"].iterrows():
        feito = st.checkbox(row["texto"], value=row["feito"], key=f"compras_{i}")
        if feito != row["feito"]:
            data.at[i, "feito"] = feito
            salvar_dados()

# ---------- TAREFAS ----------
elif view == "Tarefas":
    st.subheader("📋 Tarefas do Dia")

    tarefa = st.text_input("Adicionar nova tarefa:")
    if st.button("Adicionar tarefa"):
        if tarefa.strip():
            data.loc[len(data)] = ["Tarefa", tarefa, False, datetime.date.today()]
            salvar_dados()
            st.success("Tarefa adicionada!")

    for i, row in data[data["tipo"] == "Tarefa"].iterrows():
        feito = st.checkbox(row["texto"], value=row["feito"], key=f"tarefa_{i}")
        if feito != row["feito"]:
            data.at[i, "feito"] = feito
            salvar_dados()

# ---------- HUMOR ----------
elif view == "Humor":
    st.subheader("💖 Como você está se sentindo hoje?")

    humor = st.radio(
        "Escolha seu humor:",
        ["😊 Feliz", "😐 Neutro", "😔 Triste", "😡 Irritado", "😴 Cansado"]
    )

    comentario = st.text_area("Quer desabafar um pouquinho?")
    if st.button("Salvar humor"):
        data.loc[len(data)] = ["Humor", f"{humor} - {comentario}", True, datetime.date.today()]
        salvar_dados()
        st.success("Humor registrado com sucesso! 💕")

# ---------- RODAPÉ ----------
st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido com 💖 em Streamlit por Maria Eduarda Fontoura")

