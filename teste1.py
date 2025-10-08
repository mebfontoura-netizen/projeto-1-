import streamlit as st 

nome = input_box("digite o seu nome:")
if nome:
st.write(nome.lower())
