import streamlit as st
import pandas as pd
import datetime
import os

# ---------- CONFIG ----------
st.set_page_config(page_title="Meu Planner Diário", page_icon="💖", layout="centered")

DATA_FILE = "planner_data.csv"
GOALS_FILE = "goals_data.csv" # Novo arquivo para rastreamento de metas

# ---------- FUNÇÕES DE DADOS ----------
def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["tipo", "item", "feito"])

def salvar_dados(df):
    df.to_csv(DATA_FILE, index=False)

def carregar_metas():
    if os.path.exists(GOALS_FILE):
        return pd.read_csv(GOALS_FILE)
    else:
        # Colunas: meta, valor_atual, valor_total, data_limite
        return pd.DataFrame(columns=["meta", "valor_atual", "valor_total", "data_limite"])

def salvar_metas(df_goals):
    df_goals.to_csv(GOALS_FILE, index=False)

df = carregar_dados()
df_goals = carregar_metas()

# ---------- CABEÇALHO ----------
st.title("💗 Meu Planner Diário 💗")
st.image(
    "https://files.manuscdn.com/user_upload_by_module/session_file/310419663032198608/GkDzDVfHFzjxfuPg.jpg",  # Imagem de banner rosa decorativo (substituída por uma URL de imagem válida)
    caption="Organize seu dia com estilo e leveza 🌸",
    use_container_width=True
)

st.markdown("**Por Maria Eduarda Fontoura ✨**")

# ---------- SIDEBAR ----------
# Opção "Rastreador de Hábitos" substituída por "Painel de Metas"
view = st.sidebar.radio("Escolha uma seção:", ["Visão Geral", "Painel de Metas", "Lista de Compras", "Tarefas", "Humor"])

# ---------- VISÃO GERAL ----------
if view == "Visão Geral":
    st.header("📅 Resumo do Dia")
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    st.subheader(f"Data: {hoje}")

    humor = st.selectbox("Como está seu humor hoje?", ["😀 Feliz", "😐 Neutra", "😢 Triste", "😡 Irritada", "😴 Cansada"])
    st.write(f"💭 Seu humor de hoje: {humor}")

# ---------- PAINEL DE METAS (Substitui Rastreador de Hábitos) ----------
elif view == "Painel de Metas":
    st.header("🏆 Painel de Metas")
    
    with st.expander("Adicionar Nova Meta"):
        nova_meta = st.text_input("Nome da Meta (ex: Economizar R$ 500):")
        valor_total = st.number_input("Valor Total da Meta:", min_value=1.0, value=100.0, step=1.0)
        valor_atual = st.number_input("Valor Atual (Progresso Inicial):", min_value=0.0, value=0.0, step=1.0)
        data_limite = st.date_input("Data Limite (Opcional):", min_value=datetime.date.today(), value=datetime.date.today() + datetime.timedelta(days=30))
        
        if st.button("Salvar Meta"):
            if nova_meta and valor_total > 0 and valor_atual <= valor_total:
                nova_linha = pd.DataFrame([{
                    "meta": nova_meta, 
                    "valor_atual": valor_atual, 
                    "valor_total": valor_total, 
                    "data_limite": data_limite.strftime("%Y-%m-%d")
                }])
                global df_goals
                df_goals = pd.concat([df_goals, nova_linha], ignore_index=True)
                salvar_metas(df_goals)
                st.success(f"Meta '{nova_meta}' adicionada com sucesso!")
                st.experimental_rerun()
            else:
                st.error("Por favor, preencha todos os campos corretamente.")

    st.markdown("---")
    st.subheader("Suas Metas em Progresso")
    
    if df_goals.empty:
        st.info("Nenhuma meta adicionada ainda. Use o campo acima para começar!")
    
    for i, row in df_goals.iterrows():
        meta = row["meta"]
        valor_atual = row["valor_atual"]
        valor_total = row["valor_total"]
        data_limite = row["data_limite"]
        
        progresso = valor_atual / valor_total
        progresso_porcentagem = f"{progresso * 100:.1f}%"
        
        st.markdown(f"**{meta}** (Meta: {valor_total:.2f})")
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.progress(progresso, text=f"Progresso: {valor_atual:.2f} / {valor_total:.2f}")
        
        with col2:
            # Botão para atualizar o progresso
            novo_progresso = st.number_input("Atualizar:", min_value=0.0, max_value=valor_total, value=valor_atual, step=1.0, key=f"update_{i}")
            if novo_progresso != valor_atual:
                df_goals.loc[i, "valor_atual"] = novo_progresso
                salvar_metas(df_goals)
                st.experimental_rerun()
        
        with col3:
            # Botão para remover a meta
            if st.button("🗑️", key=f"del_goal_{i}"):
                df_goals = df_goals.drop(i)
                salvar_metas(df_goals)
                st.experimental_rerun()
        
        if progresso >= 1.0:
            st.balloons()
            st.success(f"🎉 Meta '{meta}' concluída! Parabéns!")
        elif data_limite and datetime.datetime.strptime(data_limite, "%Y-%m-%d").date() < datetime.date.today():
            st.warning(f"⚠️ Data limite ({data_limite}) para a meta '{meta}' expirou.")
        else:
            st.caption(f"Data Limite: {data_limite}")

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
            # Acessar por índice para evitar erro de SettingWithCopyWarning
            done = st.checkbox(row["item"], value=row["feito"], key=f"task_{i}")
        with col2:
            if st.button("🗑️", key=f"del_task_{i}"):
                df = df.drop(i)
                salvar_dados(df)
                st.experimental_rerun()
        # Atualizar o DataFrame principal 'df'
        if done != row["feito"]:
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
