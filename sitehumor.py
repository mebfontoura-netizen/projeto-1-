import streamlit as st
import pandas as pd
import datetime
import random
import os

# ---------- CONFIG ----------
st.set_page_config(page_title="AstroMood — Diário Cósmico", page_icon="🌙", layout="centered")
DATA_FILE = "astromood_data.csv"

# ---------- DATA STRUCTURES ----------
SIGNOS = [
    "Áries ♈", "Touro ♉", "Gêmeos ♊", "Câncer ♋", "Leão ♌", "Virgem ♍",
    "Libra ♎", "Escorpião ♏", "Sagitário ♐", "Capricórnio ♑", "Aquário ♒", "Peixes ♓"
]

SIGN_COLORS = {
    s: color for s, color in zip(SIGNOS, [
        "#FF6B6B", "#FFD166", "#F5CBA7", "#9AD3BC", "#FFD2A6", "#C6D8FF",
        "#E7DAFF", "#E19AFF", "#F6B8B8", "#B8D8D8", "#BEE7E6", "#D3C0F9"
    ])
}

MOODS = {
    "Feliz 😄": 3,
    "Tranquilo 🌿": 2,
    "Neutro 😐": 1,
    "Ansioso 😟": 0,
    "Triste 😢": -1,
}

HOROSCOPES = {
    "Áries ♈": "Hoje é dia de agir com coragem. Pequenas decisões te levam a grandes surpresas.",
    "Touro ♉": "A estabilidade aparece quando você se permite desacelerar e valorizar o presente.",
    "Gêmeos ♊": "Comunique-se — uma conversa pode clarear o que estava confuso.",
    "Câncer ♋": "Cuide do seu lar e das suas emoções; um pequeno gesto traz conforto.",
    "Leão ♌": "Brilhe! Seu entusiasmo atrai oportunidades sociais importantes.",
    "Virgem ♍": "Organize uma pequena rotina: ela trará bem-estar e foco.",
    "Libra ♎": "Busque equilíbrio nas relações — ouvir pode ser tão poderoso quanto falar.",
    "Escorpião ♏": "Intensidade emocional favorece transformações profundas. Confie no processo.",
    "Sagitário ♐": "Aventure-se em uma leitura ou saída curta — será renovador.",
    "Capricórnio ♑": "Planeje com cuidado: metas bem definidas te aproximam do objetivo.",
    "Aquário ♒": "Ideias inovadoras surgem quando você troca experiências com outras pessoas.",
    "Peixes ♓": "Deixe a criatividade fluir — arte e música serão grandes aliados hoje.",
}

MUSICAS = {
    "Feliz 😄": [
        ("Happy - Pharrell Williams", "https://www.youtube.com/watch?v=ZbZSe6N_BXs"),
        ("Good as Hell - Lizzo", "https://www.youtube.com/watch?v=vuq-VAiW9kw"),
    ],
    "Tranquilo 🌿": [
        ("Better Together - Jack Johnson", "https://www.youtube.com/watch?v=u57d4_b_YgI"),
        ("Banana Pancakes - Jack Johnson", "https://www.youtube.com/watch?v=OkyrIRyrRdY"),
    ],
    "Neutro 😐": [
        ("Someone You Loved - Lewis Capaldi", "https://www.youtube.com/watch?v=zABLecsR5UE"),
    ],
    "Ansioso 😟": [
        ("Weightless - Marconi Union", "https://www.youtube.com/watch?v=UfcAVejslrU"),
    ],
    "Triste 😢": [
        ("Someone Like You - Adele", "https://www.youtube.com/watch?v=hLQl3WQQoQ0"),
    ],
}

# ---------- HELPERS ----------

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=["date"]) 
        return df
    else:
        return pd.DataFrame(columns=["date", "sign", "mood", "mood_val", "note"])

def save_entry(sign, mood, mood_val, note):
    df = load_data()
    new = pd.DataFrame([{
        "date": datetime.date.today(),
        "sign": sign,
        "mood": mood,
        "mood_val": mood_val,
        "note": note
    }])
    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# ---------- LAYOUT ----------
st.markdown("<div style='text-align:center'><h1>🪐 AstroMood — Diário Cósmico</h1></div>", unsafe_allow_html=True)
st.write("Registre seu humor e receba mensagens e músicas de acordo com seu signo e energia do dia ✨")
st.markdown("---")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configurações")
    sign_choice = st.selectbox("Seu signo", SIGNOS, index=6)
    st.markdown("---")
    st.write("📁 **Histórico**")
    if st.button("Baixar histórico (CSV)"):
        df = load_data()
        if not df.empty:
            st.download_button("Clique para baixar", df.to_csv(index=False), file_name="astromood_history.csv", mime="text/csv")
        else:
            st.info("Ainda não há registros.")
    if st.button("🗑️ Limpar histórico"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.success("Histórico apagado.")
        else:
            st.info("Nenhum histórico encontrado.")

# --- Entrada principal ---
st.subheader(f"🌞 Olá, {sign_choice}")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### Como você está hoje?")
    mood = st.radio("Escolha seu humor", list(MOODS.keys()))
    note = st.text_area("Quer escrever algo sobre seu dia? (opcional)", max_chars=500)
    if st.button("💾 Salvar humor de hoje"):
        mood_val = MOODS[mood]
        save_entry(sign_choice, mood, mood_val, note)
        st.success("Salvo com sucesso! 🌟")
        st.balloons()

with col2:
    color = SIGN_COLORS.get(sign_choice, "#FFFFFF")
    st.markdown(f"<div style='background:{color}; padding:12px; border-radius:8px'>", unsafe_allow_html=True)
    st.markdown(f"### 🔮 Horóscopo — {sign_choice}")
    st.write(HOROSCOPES.get(sign_choice, "Hoje há boas energias — fique atenta às pequenas oportunidades."))
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------- VISUALIZAÇÕES ----------
st.header("📊 Seu histórico de humor")
df = load_data()
if df.empty:
    st.info("Ainda não há registros. Salve seu humor para começar!")
else:
    df_sign = df[df["sign"] == sign_choice].copy()
    if df_sign.empty:
        st.info("Nenhum registro para este signo ainda.")
    else:
        df_sign["date"] = pd.to_datetime(df_sign["date"]).dt.date
        series = df_sign.groupby("date")["mood_val"].mean()
        st.line_chart(series)
        st.markdown("#### Últimos registros")
        st.dataframe(df_sign.sort_values("date", ascending=False).reset_index(drop=True))

# ---------- RECOMENDAÇÕES ----------
st.markdown("---")
st.header("🌟 Recomendações cósmicas para você")
if df.empty:
    st.info("Salve seu humor para receber recomendações.")
else:
    last = df[df["sign"] == sign_choice].sort_values("date", ascending=False).head(1)
    if last.empty:
        st.info("Registre seu humor para ver recomendações.")
    else:
        last_mood = last.iloc[0]["mood"]
        st.markdown(f"**Humor recente:** {last_mood}")
        sugest = MUSICAS.get(last_mood, [])
        if sugest:
            song = random.choice(sugest)
            st.markdown(f"🎵 **Música sugerida:** [{song[0]}]({song[1]})")
        CARE = {
            "Feliz 😄": "Compartilhe sua alegria com alguém querido 💛",
            "Tranquilo 🌿": "Medite por 5 minutos ou aprecie um pôr do sol 🌅",
            "Neutro 😐": "Escreva 3 coisas boas que aconteceram hoje ✍️",
            "Ansioso 😟": "Respire fundo e ouça uma música calma 🎧",
            "Triste 😢": "Procure conforto em algo que te traz paz 💙",
        }
        st.markdown(f"💡 **Dica de autocuidado:** {CARE.get(last_mood, '')}")

st.markdown("---")

# ---------- HUMOR + IMAGENS ----------
st.header("🖼️ Humor visual do dia")
humor = st.selectbox("Como você se sente agora?", ["😊 Feliz", "😔 Triste", "😤 Estressada", "😌 Calma"])

if humor == "😊 Feliz":
    st.image("https://i.imgur.com/7aZzZQz.png", caption="Alegria no ar!")
elif humor == "😔 Triste":
    st.image("https://i.imgur.com/x0Vt4Hk.png", caption="Dias nublados também passam 💙")
elif humor == "😤 Estressada":
    st.image("https://i.imgur.com/W2dKh3g.png", caption="Respira fundo 💨")
else:
    st.image("https://i.imgur.com/6Zb7WcE.png", caption="Paz interior 🌿")

st.markdown("---")
st.markdown("✨ Feito com amor — by Maria Eduarda 🌙")

