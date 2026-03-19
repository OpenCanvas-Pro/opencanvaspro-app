import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. Configuração de Elite
st.set_page_config(
    page_title="OpenCanvas Pro | Cognitive AutoML",
    page_icon="32.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DEFINIÇÃO DE PATHS ---
ASSETS_DIR = "assets"
LOGO_PATH = os.path.join(ASSETS_DIR, "Cor_sobre_preto.svg")
SHIELD_PATH = os.path.join(ASSETS_DIR, "integrity_shield.png")

# --- CSS PARA DARK MODE REAL E CORREÇÕES VISUAIS ---
st.markdown("""
<style>
    .stApp { background-color: #0D0D0D !important; }
    [data-testid="stHeader"], [data-testid="stFooter"] { display: none !important; }
    
    h1, h2, h3, p, li, span, b { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    .orange-text { color: #FF6B00 !important; font-weight: 800; }
    
    .content-box {
        background: #161616;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333;
        margin-bottom: 15px;
    }

    /* Forçar o SVG a ser visível e responsivo */
    .logo-container svg {
        width: 100% !important;
        height: auto !important;
        max-width: 280px;
        display: block;
        margin: 0 auto;
    }

    /* Estilização do Botão de Envio */
    div.stButton > button {
        background-color: #FF6B00 !important;
        color: white !important;
        border: 2px solid #FF6B00 !important;
        font-weight: bold !important;
        height: 3.5em;
        width: 100%;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }

    /* Efeito ao passar o mouse (Hover) */
    div.stButton > button:hover {
        background-color: #e66000 !important; /* Um laranja levemente mais escuro */
        border-color: #FFFFFF !important;
        color: white !important;
        transform: scale(1.02);
    }

    /* Efeito ao clicar (Active/Focus) */
    div.stButton > button:active, div.stButton > button:focus {
        background-color: #FF6B00 !important;
        color: white !important;
        box-shadow: 0 0 15px rgba(255, 107, 0, 0.4) !important;
    }

# --- HEADER (Logotipo SVG com injeção direta de classe) ---
if os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "r") as f:
        svg_content = f.read()
    # Injetamos o SVG dentro de uma div com a classe que definimos no CSS acima
    st.markdown(f'<div class="logo-container">{svg_content}</div>', unsafe_allow_html=True)
else:
    st.markdown("<h2 style='text-align: center; color: #FF6B00; padding-top: 20px;'>OpenCanvas Pro</h2>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-top: 5px;'>Cognitive <span class='orange-text'>AutoML</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; opacity: 0.7; letter-spacing: 2px;'>TRUSTED PLATFORM FOR SCIENTIFIC INTEGRITY</p>", unsafe_allow_html=True)
st.write("---")

# --- SEÇÃO PRINCIPAL (IMAGEM + TEXTO) ---
col_img, col_txt = st.columns([1.2, 1], gap="large")

with col_img:
    if os.path.exists(SHIELD_PATH):
        st.image(SHIELD_PATH, use_container_width=True)
    else:
        st.error(f"⚠️ Verifique se '{SHIELD_PATH}' está no GitHub.")

with col_txt:
    st.markdown("### 🛡️ Trusted Platform & Diferenciais")
    
    # Abrimos uma única box para todos os itens para manter o alinhamento
    items = [
        ("🧠", "Navegação Cognitiva (E.M.I.L.I.A.)", "Assistente com Grafo de Conhecimento que funciona como um GPS para evitar pântanos estatísticos."),
        ("🔬", "Scientific Integrity (19+ Checks)", "Auditoria rigorosa de Target Leakage, Overfitting e inconsistências semânticas."),
        ("📄", "Artefatos de Elite", "Geração de Relatórios Executivos em PDF e Documentação Técnica completa."),
        ("⚙️", "Predição em Batch", "Suporte nativo para processamento em lote e exportação de modelos otimizados."),
        ("🏠", "Soberania Local-First", "Processamento na sua infraestrutura. Compliance nativa LGPD/GDPR.")
    ]
    
    html_diferenciais = '<div class="content-box">'
    for icon, title, desc in items:
        html_diferenciais += f"""
        <div style="margin-bottom: 15px;">
            <span style="font-size: 1.1rem;">{icon}</span> <b class="orange-text">{title}:</b><br>
            <span style="font-size: 0.9rem; opacity: 0.8;">{desc}</span>
        </div>
        """
    html_diferenciais += '</div>'
    st.markdown(html_diferenciais, unsafe_allow_html=True)

# --- SEÇÃO DE PILARES (RENDERIZADA DEPOIS DA LINHA) ---
st.write("---")
st.markdown("### 🚀 Pilares de Performance")
p1, p2, p3 = st.columns(3)

pilares = [
    ("Auditoria Gold Standard", "Certificado de Integridade Científica gerado para cada modelo, pronto para compliance."),
    ("White-Box AI", "Transparência total. Controle absoluto sobre cada etapa do pipeline, do pré ao deploy."),
    ("Eficiência de Recurso", "Otimizado para rodar localmente, eliminando a dependência de créditos abusivos.")
]

for col, (title, desc) in zip([p1, p2, p3], pilares):
    col.markdown(f"""
    <div class="content-box" style="min-height: 180px;">
        <h4 class="orange-text">{title}</h4>
        <p style="font-size: 0.9rem; opacity: 0.9;">{desc}</p>
    </div>
    """, unsafe_allow_html=True)

# --- FORMULÁRIO FINAL ---
st.write("---")
_, center_col, _ = st.columns([1, 1.5, 1])

with center_col:
    st.markdown("<h3 style='text-align: center;'>Não perca o 'Go-Live'</h3>", unsafe_allow_html=True)
    with st.form("waitlist_form", clear_on_submit=True):
        email_input = st.text_input("E-mail:", placeholder="seu@email.com")
        submit = st.form_submit_button("🔔 ME AVISE QUANDO LANÇAR")
        
        if submit:
            if email_input and "@" in email_input:
                # Aqui você inserirá sua função enviar_lead(email_input) no futuro
                st.balloons()
                st.success("Perfeito! Você será avisado em breve.")
            else:
                st.warning("E-mail inválido.")

st.markdown("<p style='text-align: center; color: #444; margin-top: 40px; font-size: 0.8rem;'>OpenCanvas Pro © 2026 | Built for Science. Built for Trust.</p>", unsafe_allow_html=True)
