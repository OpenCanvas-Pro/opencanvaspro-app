import streamlit as st
import base64
import os

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

# --- CSS PARA DARK MODE E TIPOGRAFIA ---
st.markdown("""
<style>
    .stApp { background-color: #0D0D0D !important; }
    [data-testid="stHeader"], [data-testid="stFooter"] { display: none !important; }
    
    h1, h2, h3, p, li { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    .orange-text { color: #FF6B00 !important; font-weight: 800; }
    
    .content-box {
        background: #161616;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-bottom: 20px;
        color: #FFFFFF !important;
    }

    .content-box p, .content-box li, .content-box b, .content-box span {
        color: #FFFFFF !important;
    }

    .stButton>button {
        background: #FF6B00 !important;
        color: white !important; /* Corrigido de orange para white para leitura */
        border: none !important;
        font-weight: bold !important;
        height: 3em;
        width: 100%;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(255, 107, 0, 0.4);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER (Logotipo SVG) ---
if os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "r") as f:
        svg_content = f.read()
    st.markdown(f'''
        <div style="text-align: center; margin: 0 auto; padding-top: 20px;">
            <div style="width: 250px; margin: 0 auto;">
                {svg_content}
            </div>
        </div>
        <style>svg {{ width: 100%; height: auto; }}</style>
    ''', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-top: 10px;'>Cognitive <span class='orange-text'>AutoML</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; opacity: 0.8;'>A PRÓXIMA GERAÇÃO DE IA LOCAL-FIRST</p>", unsafe_allow_html=True)
st.write("---")

# --- SEÇÃO PRINCIPAL (IMAGEM + TEXTO) ---
col_img, col_txt = st.columns([1.3, 1], gap="large")

with col_img:
    if os.path.exists(SHIELD_PATH):
        st.image(SHIELD_PATH, use_container_width=True)
    else:
        st.error(f"⚠️ Erro: Arquivo '{SHIELD_PATH}' não encontrado.")

with col_txt:
    st.markdown("### 🛡️ Trusted Platform & Diferenciais")
    st.markdown("""
    <div class="content-box">
        <p style="margin-bottom: 20px; opacity: 0.9;">
            A <b>OpenCanvas Pro</b> opera como um "sistema imunológico" para seus dados e um gerador de ativos de elite:
        </p>

        <div style="margin-bottom: 18px;">
            <span style="font-size: 1.2rem;">🧠</span> <b class="orange-text">Navegação Cognitiva (E.M.I.L.I.A.):</b><br>
            <span style="font-size: 0.9rem; opacity: 0.85;">
                Assistente com Grafo de Conhecimento que funciona como um GPS para evitar "pântanos estatísticos".
            </span>
        </div>
        
        <div style="margin-bottom: 18px;">
            <span style="font-size: 1.2rem;">🔬</span> <b class="orange-text">Scientific Integrity (19+ Checks):</b><br>
            <span style="font-size: 0.9rem; opacity: 0.85;">
                Auditoria rigorosa de <b>Target Leakage, Overfitting e Data Poisoning</b>.
            </span>
        </div>

        <div style="margin-bottom: 18px;">
            <span style="font-size: 1.2rem;">📄</span> <b class="orange-text">Artefatos de Elite:</b><br>
            <span style="font-size: 0.9rem; opacity: 0.85;">
                Geração automática de <b>Relatórios Executivos em PDF</b> e Documentação Técnica completa.
            </span>
        </div>

        <div style="margin-bottom: 18px;">
            <span style="font-size: 1.2rem;">⚙️</span> <b class="orange-text">Predição em Batch:</b><br>
            <span style="font-size: 0.9rem; opacity: 0.85;">
                Suporte nativo para processamento em lote e exportação de modelos otimizados.
            </span>
        </div>
        
        <div style="margin-bottom: 5px;">
            <span style="font-size: 1.2rem;">🏠</span> <b class="orange-text">Soberania Local-First:</b><br>
            <span style="font-size: 0.9rem; opacity: 0.85;">
                Processamento na sua infraestrutura. Compliance nativa <b>LGPD/GDPR.</b>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SEÇÃO DE PILARES ---
st.markdown("### 🚀 Nossos Pilares de Performance")
p1, p2, p3 = st.columns(3)

with p1:
    st.markdown("""<div class="content-box" style="min-height: 200px;">
        <h4 class="orange-text">Auditoria Gold Standard</h4>
        Certificado de Integridade Científica gerado para cada modelo, pronto para auditorias de compliance.
    </div>""", unsafe_allow_html=True)

with p2:
    st.markdown("""<div class="content-box" style="min-height: 200px;">
        <h4 class="orange-text">White-Box AI</h4>
        Transparência total. Controle absoluto sobre cada etapa do pipeline, do pré ao deploy.
    </div>""", unsafe_allow_html=True)

with p3:
    st.markdown("""<div class="content-box" style="min-height: 200px;">
        <h4 class="orange-text">Eficiência de Recurso</h4>
        Otimizado para rodar localmente, eliminando a dependência de créditos abusivos de nuvem.
    </div>""", unsafe_allow_html=True)

# --- WAITLIST ---
st.write("---")
_, center_col, _ = st.columns([1, 1.5, 1])

with center_col: # CORRIGIDO: Agora usamos a coluna central que foi definida
    st.markdown("<h3 style='text-align: center;'>Não perca o 'Go-Live'</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.9rem; opacity: 0.7;'>Estamos finalizando os ajustes da v1.0. Deixe seu e-mail para receber o convite.</p>", unsafe_allow_html=True)
    
    with st.form("waitlist_final"):
        email = st.text_input("E-mail:", placeholder="exemplo@empresa.com")
        submit = st.form_submit_button("🔔 ME AVISE QUANDO LANÇAR")
        
        if submit and email:
            if "@" in email:
                st.balloons()
                st.success("Perfeito! Você será um dos primeiros a saber.")
            else:
                st.error("Por favor, insira um e-mail válido.")

st.markdown("<p style='text-align: center; color: #444; margin-top: 50px; font-size: 0.8rem;'>OpenCanvas Pro © 2026 | Built for Science. Built for Trust.</p>", unsafe_allow_html=True)
