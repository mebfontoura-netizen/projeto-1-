import streamlit as st
import pandas as pd
import datetime
import uuid
import json
from pathlib import Path

# ---------- CONFIG ----------
st.set_page_config(page_title="Meu Planner Diário", page_icon="🗓️", layout="wide")
DATA_FILE = Path("planner_data.json")

# ---------- UTILIDADES ----------

def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_structure(d):
    d.setdefault("checklists", [])
    d.setdefault("shopping", [])
    d.setdefault("tasks", [])
    d.setdefault("mood_log", [])
    d.setdefault("notes", [])
    return d


def new_item(text):
    return {"id": str(uuid.uuid4()), "text": text, "done": False, "created": datetime.datetime.now().isoformat()}


# ---------- INÍCIO ----------

data = load_data()
data = ensure_structure(data)

# ---------- LAYOUT ----------

# Top banner with decorative image
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Meu Planner Diário")
    st.caption("Checklist, lista de compras, tarefas, humor e notas — tudo num só lugar.")
with col2:
    st.image("https://images.unsplash.com/photo-1508780709619-79562169bc64?q=80&w=400&auto=format&fit=crop&ixlib=rb-4.0.3&s=0d3e6e2a9f9b6e6d43a4b5c9b4b0c2a8", width=160)

st.markdown("---")

# Sidebar for navigation
st.sidebar.title("Navegação")
view = st.sidebar.radio("Ir para:", ["Visão Geral", "Checklist", "Lista de Compras", "Tarefas", "Humor", "Notas", "Importar/Exportar"]) 

# Quick stats on sidebar
total_tasks = len(data["tasks"]) if data.get("tasks") else 0
completed_tasks = sum(1 for t in data.get("tasks", []) if t.get("done"))
st.sidebar.markdown(f"**Tarefas:** {completed_tasks}/{total_tasks}")
st.sidebar.markdown(f"**Itens na compra:** {len(data.get('shopping', []))}")

st.sidebar.markdown("---")
if st.sidebar.button("Limpar dados (apagar tudo)"):
    if st.sidebar.checkbox("Confirmo que quero apagar todos os dados"):
        data = ensure_structure({})
        save_data(data)
        st.sidebar.success("Dados apagados. Recarregue a página.")

# ---------- VIEWS ----------

if view == "Visão Geral":
    st.header("Visão Geral do Dia")
    today = datetime.date.today().isoformat()
    st.subheader(f"Hoje — {today}")

    with st.expander("Checklist rápido"):
        for cl in data.get("checklists", []):
            checked = st.checkbox(cl["text"], value=cl.get("done", False), key=f"cl_{cl['id']}")
            if checked != cl.get("done", False):
                cl["done"] = checked
                save_data(data)

    st.subheader("Últimos registros de humor")
    moods = data.get("mood_log", [])[-5:][::-1]
    if moods:
        for m in moods:
            ts = m.get("timestamp", "")
            st.write(f"{m.get('emoji','')}  — {m.get('note','')}  \t  *{ts.split('T')[0]}*")
    else:
        st.info("Nenhum registro de humor ainda — vá na aba 'Humor' para adicionar um.")

elif view == "Checklist":
    st.header("Checklist")
    new_text = st.text_input("Adicionar item na checklist", key="new_check_text")
    if st.button("Adicionar item", key="add_check") and new_text.strip():
        item = new_item(new_text.strip())
        data["checklists"].append(item)
        save_data(data)
        st.experime
