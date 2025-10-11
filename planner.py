import streamlit as st
import pandas as pd
import datetime
import uuid
import json
from pathlib import Path

# ---------- CONFIG ----------
st.set_page_config(page_title="Meu Planner Diário", page_icon="🗓️", layout="wide")
DATA_FILE = Path("planner_data.json")

# ---------- FUNÇÕES ----------
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

# ---------- DADOS ----------
data = ensure_structure(load_data())

# ---------- LAYOUT ----------
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🗓️ Meu Planner Diário")
    st.caption("Um planner simples com checklist, lista de compras, tarefas, humor e notas.")
with col2:
    st.image("https://images.unsplash.com/photo-1508780709619-79562169bc64?q=80&w=400&auto=format&fit=crop", width=180)

st.markdown("---")

# ---------- SIDEBAR ----------
st.sidebar.title("Navegação")
view = st.sidebar.radio("Escolha uma seção:", ["Visão Geral", "Checklist", "Lista de Compras", "Tarefas", "Humor"])
