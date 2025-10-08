import streamlit as st 

nome = st.text_input("digite o seu nome:")
if nome:
st.write(nome.lower())
