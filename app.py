import streamlit as st
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

# --- CSS PARA DARK MODE E FIX DE LAYOUT ---
st.markdown("""
<style>
    .stApp { background-color: #0D0D0D !important; }
    [data-testid="stHeader"], [data-testid="stFooter"] { display: none !important; }
    
    h1, h2, h3, h4, p, li, span, b { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    .orange-text { color: #FF6B00 !important; font-weight: 800; }
    
    .content-box {
        background: #161616;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-bottom: 20px;
    }

    /* Forçar o SVG a aparecer (Filtro para garantir visibilidade se o SVG for branco) */
    .logo-container img {
        width: 280px;
        display: block;
        margin: 0 auto;
        padding: 10px;
    }

    /* BOTÃO LARANJA OCP */
    div.stButton > button {
        background-color: #FF6B00 !important;
        color: white !important;
        border: 2px solid #FF6B00 !important;
        font-weight: bold !important;
        height: 3.5em;
        width: 100%;
        border-radius: 8px !important;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background-color: #e66000 !important;
        border-color: #FFFFFF !important;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER (Logotipo) ---
# Usando st.image para o SVG para garantir que o Streamlit trate a transparência melhor
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=280)
else:
    st.markdown("<h2 style='text-align: center; color: #FF6B00;'>OpenCanvas Pro</h2>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-top: 10px;'>Cognitive <span class='orange-text'>AutoML</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; opacity: 0.7; letter-spacing: 2px;'>TRUSTED PLATFORM FOR SCIENTIFIC INTEGRITY</p>", unsafe_allow_html=True)
st.write("---")

# --- SEÇÃO PRINCIPAL (IMAGEM + TEXTO) ---
col_img, col_txt = st.columns([1.2, 1], gap="large")

with col_img:
    if os.path.exists(SHIELD_PATH):
        st.image(SHIELD_PATH, use_container_width=True)
    else:
        st.info("Aguardando 'integrity_shield.png' na pasta assets.")

with col_txt:
    st.markdown("### 🛡️ Trusted Platform & Diferenciais")
    
    # Renderização limpa dos diferenciais
    st.markdown("""
    <div class="content-box">
        <div style="margin-bottom: 18px;">
            <span style="font-size: 1.2rem;">🧠</span> <b class="orange-text">Navegação Cognitiva (E.M.I.L.I.A.):</b><br>
            <span style="font-size: 0.9rem; opacity: 0.85;">Assistente com Grafo de Conhecimento que evita "pântanos estatísticos".</span>
        </div>
        <div style="margin-bottom: 18px;">
            <span style="font-size: 1.2rem;">🔬</span> <b class="orange-text">Scientific Integrity (19+ Checks):</b><br>
            <span style="font-size: 0.9rem; opacity: 0.85;">Auditoria rigorosa de Target Leakage, Overfitting e inconsistências.</span>
        </div>
        <div style="margin-bottom: 18px;">
            <span style="font-size: 1.2rem;">📄</span> <b class="orange-text">Artefatos de Elite:</b><br>
            <span style="font-size: 0.9rem; opacity: 0.85;">Relatórios Executivos em PDF e Documentação Técnica completa.</span>
        </div>
        <div style="margin-bottom: 18px;">
            <span style="font-size: 1.2rem;">⚙️</span> <b class="orange-text">Predição em Batch:</b><br>
            <span style="font-size: 0.9rem; opacity: 0.85;">Suporte nativo para processamento em lote e exportação de modelos.</span>
        </div>
        <div style="margin-bottom: 5px;">
            <span style="font-size: 1.2rem;">🏠</span> <b class="orange-text">Soberania Local-First:</b><br>
            <span style="font-size: 0.9rem; opacity: 0.85;">Processamento na sua infraestrutura. Compliance LGPD/GDPR.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SEÇÃO DE PILARES ---
st.write("---")
st.markdown("### 🚀 Pilares de Performance")
p1, p2, p3 = st.columns(3)

with p1:
    st.markdown('<div class="content-box" style="min-height: 160px;"><h4 class="orange-text">Auditoria Gold Standard</h4>Certificado de Integridade Científica gerado para cada modelo.</div>', unsafe_allow_html=True)
with p2:
    st.markdown('<div class="content-box" style="min-height: 160px;"><h4 class="orange-text">White-Box AI</h4>Transparência total. Controle absoluto sobre cada etapa do pipeline.</div>', unsafe_allow_html=True)
with p3:
    st.markdown('<div class="content-box" style="min-height: 160px;"><h4 class="orange-text">Eficiência de Recurso</h4>Otimizado para rodar localmente, sem dependência de nuvem.</div>', unsafe_allow_html=True)

# --- FORMULÁRIO ---
st.write("---")
_, center_col, _ = st.columns([1, 1.5, 1])
with center_col:
    st.markdown("<h3 style='text-align: center;'>Não perca o 'Go-Live'</h3>", unsafe_allow_html=True)
    with st.form("waitlist_form", clear_on_submit=True):
        email = st.text_input("Seu e-mail:", placeholder="exemplo@empresa.com")
        submit = st.form_submit_button("🔔 ME AVISE QUANDO LANÇAR")
        if submit and email:
            st.balloons()
            st.success("Perfeito! Você será avisado assim que virarmos a chave.")

st.markdown("<p style='text-align: center; color: #444; margin-top: 50px; font-size: 0.8rem;'>OpenCanvas Pro © 2026 | Built for Science. Built for Trust.</p>", unsafe_allow_html=True)
