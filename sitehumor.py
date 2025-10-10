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

# cores por signo (sutil)
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

# Horóscopos de exemplo (podem ser ampliados ou substituídos por chamadas a API)
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

# Sugestões de músicas por humor (pequeno exemplo)
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
    new = pd.DataFrame([{"date": datetime.date.today(), "sign": sign, "mood": mood, "mood_val": mood_val, "note": note}])
    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


# ---------- LAYOUT ----------
st.markdown("<div style='text-align:center'><h1>🪐 AstroMood — Diário Cósmico</h1></div>", unsafe_allow_html=True)
st.write("Um lugar para registrar seu humor diário e receber mensagens astrológicas para acompanhar suas emoções.")
st.markdown("---")

# --- SIDEBAR: configurações e histórico ---
with st.sidebar:
    st.header("Configurações")
    st.write("Escolha seu signo e algumas preferências.")
    sign_choice = st.selectbox("Seu signo", SIGNOS, index=6)
    st.markdown("---")
    st.write("**Exportar / Histórico**")
    if st.button("Baixar histórico (CSV)"):
        df = load_data()
        if not df.empty:
            st.download_button("Clique para baixar", df.to_csv(index=False), file_name="astromood_history.csv", mime="text/csv")
        else:
            st.info("Ainda não há registros para baixar.")
    if st.button("Limpar histórico (apagar arquivo)"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.success("Histórico apagado.")
        else:
            st.info("Nenhum histórico encontrado.")

# --- Entrada principal ---
st.subheader(f"Olá — signo selecionado: {sign_choice}")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### Como você está hoje?")
    mood = st.radio("Escolha seu humor", list(MOODS.keys()))
    note = st.text_area("Conte um pouco sobre o seu dia (opcional)", max_chars=500)
    if st.button("💾 Salvar meu humor de hoje"):
        mood_val = MOODS[mood]
        save_entry(sign_choice, mood, mood_val, note)
        st.success("Salvo! Seu humor foi registrado — volte sempre 🌟")
        # mostrar horóscopo e recomendação imediata
        st.balloons()

with col2:
    # cartão com horóscopo
    color = SIGN_COLORS.get(sign_choice, "#FFFFFF")
    st.markdown(f"<div style='background:{color}; padding:12px; border-radius:8px'>", unsafe_allow_html=True)
    st.markdown(f"### 🔮 Horóscopo de hoje — {sign_choice}")
    st.write(HOROSCOPES.get(sign_choice, "Hoje há boas energias — fique atento(a) às pequenas oportunidades."))
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------- VISUALIZAÇÕES ----------
st.header("Seu histórico de humor")
df = load_data()
if df.empty:
    st.info("Ainda não há registros. Salve seu humor para começar a ver gráficos e estatísticas!")
else:
    # filtrar por signo
    df_sign = df[df["sign"] == sign_choice].copy()
    if df_sign.empty:
        st.info("Você não tem registros para este signo — comece salvando seu humor hoje.")
    else:
        # transformar date para datetime e agrupar por dia (últimos 30 dias)
        df_sign["date"] = pd.to_datetime(df_sign["date"]).dt.date
        last_n = 30
        today = datetime.date.today()
        start = today - datetime.timedelta(days=last_n - 1)
        df_period = df_sign[df_sign["date"] >= start]

        if df_period.empty:
            st.info(f"Nenhum registro nos últimos {last_n} dias. Mostrando todo o histórico do signo.")
            df_period = df_sign

        # criar série diária (preencher dias sem registro com NaN)
        idx = pd.date_range(start=df_period["date"].min(), end=df_period["date"].max(), freq="D")
        series = df_period.groupby("date")["mood_val"].mean().reindex(idx.date, fill_value=None)
        series.index = pd.to_datetime(series.index)

        # plot simples
        st.line_chart(series)

        st.markdown("#### Últimos registros")
        st.dataframe(df_sign.sort_values("date", ascending=False).reset_index(drop=True))

        # estatísticas rápidas
        st.markdown("#### Estatísticas")
        avg = df_period["mood_val"].mean()
        st.write(f"Média do humor nos últimos {len(df_period)} registros: **{avg:.2f}**")

# ---------- RECOMENDAÇÕES ----------
st.markdown("---")
st.header("Recomendações para hoje")
if df.empty:
    st.info("Você pode salvar seu humor para receber recomendações personalizadas.")
else:
    # usar último registro do usuário para sugerir música e uma ação
    last = df[df["sign"] == sign_choice].sort_values("date", ascending=False).head(1)
    if last.empty:
        st.info("Salve seu humor hoje para ver recomendações personalizadas!")
    else:
        last_mood = last.iloc[0]["mood"]
        st.markdown(f"**Humor registrado mais recente:** {last_mood}")
        # sugerir música aleatória
        sugest = MUSICAS.get(last_mood, [])
        if sugest:
            song = random.choice(sugest)
            st.markdown(f"🎵 **Sugestão de música:** [{song[0]}]({song[1]})")
        # sugestão de autocuidado baseada no humor
        CARE = {
            "Feliz 😄": "Compartilhe sua alegria: mande uma mensagem para alguém que gosta de você.",
            "Tranquilo 🌿": "Aproveite para meditar 5 minutos ou caminhar ao ar livre.",
            "Neutro 😐": "Tente escrever 3 coisas pelas quais você é grata hoje.",
            "Ansioso 😟": "Respire 4-4-4 (inspira 4s, segura 4s, expira 4s) por 2 minutos.",
            "Triste 😢": "Se possível, converse com alguém de confiança ou escreva como se sentiu.",
        }
        st.markdown(f"💡 **Sugestão de cuidado:** {CARE.get(last_mood, '')}")

st.markdown("---")
st.markdown("Feito com ❤️ — quer que eu adicione integração com a API do Spotify ou um horóscopo em tempo real (aztro)?")

# ---------- END ----------
