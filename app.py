import streamlit as st

st.set_page_config(page_title="OpenCanvas Pro", page_icon="🍊")

# Centralizando
c1, c2, c3 = st.columns([1,2,1])

with c2:
    st.image("assets/logo_laranja_neural.png") # (Se já tiver a imagem)
    st.title("OpenCanvas Pro")
    st.markdown("### A Revolução do AutoML Local-First")
    
    st.info("Estamos preparando algo incrível para o Agronegócio e Big Data.")
    
    st.write("---")
    st.write("**Em breve disponível para:**")
    st.write("✅ FATEC Bebedouro")
    st.write("✅ Pesquisadores de Data Science")
    
    st.text_input("Entre na lista de espera (E-mail):")
    st.button("Avise-me quando lançar 🚀")
