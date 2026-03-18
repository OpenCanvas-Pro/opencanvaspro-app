import streamlit as st
import base64
import os

# 1. A PRIMEIRA LINHA DEVE SER ESTA (E APENAS UMA VEZ):
st.set_page_config(
    page_title="OpenCanvas Pro | Cognitive AutoML",
    page_icon="32.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FUNÇÃO PARA CARREGAR IMAGEM LOCAL COM SEGURANÇA ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

img_logo_b64 = get_base64_image("Cor_Preto_Logo_OCP.png")
img_emilia_b64 = get_base64_image("Emilia_hires.jpg")

# --- CSS TOTALMENTE INJETADO (FORÇANDO DARK MODE) ---
st.markdown(f"""
<style>
    /* Forçar fundo preto em tudo */
    .stApp {{
        background-color: #0D0D0D !important;
        color: #FFFFFF !important;
    }}
    
    /* Esconder elementos nativos que poluem o visual */
    header, footer, #MainMenu {{visibility: hidden;}}
    
    .main-title {{
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0px;
        color: white;
    }}
    
    .highlight-text {{
        text-align: center;
        color: #FF6B00;
        font-weight: 700;
        font-size: 1.2rem;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }}

    /* Grid de Integridade */
    .shield-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 10px;
        padding: 10px;
    }}

    .check-card {{
        background: #161616;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        transition: 0.3s;
    }}

    .check-card:hover {{
        border-color: #FF6B00;
        box-shadow: 0 0 10px rgba(255, 107, 0, 0.3);
    }}

    .check-label {{
        font-size: 0.7rem;
        color: #AAA;
        text-transform: uppercase;
        margin-top: 5px;
    }}

    .emilia-quote {{
        background: rgba(255, 107, 0, 0.1);
        border-left: 4px solid #FF6B00;
        padding: 15px;
        font-style: italic;
        font-size: 0.95rem;
        border-radius: 0 10px 10px 0;
    }}
</style>
""", unsafe_allow_html=True)

# --- CONTEÚDO ---

# Logo customizado via HTML para garantir centralização e cor
if img_logo_b64:
    st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{img_logo_b64}" width="200"></div>', unsafe_allow_html=True)
else:
    st.markdown("<h2 style='text-align: center; color: #FF6B00;'>OpenCanvas Pro</h2>", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>Cognitive AutoML</h1>", unsafe_allow_html=True)
st.markdown("<p class='highlight-text'>TRUSTED PLATFORM FOR SCIENTIFIC INTEGRITY</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    if img_emilia_b64:
        st.markdown(f'<img src="data:image/jpeg;base64,{img_emilia_b64}" style="width:100%; border-radius: 15px; border: 1px solid #333;">', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="emilia-quote">
        "Meu escudo de 19 camadas garante que sua IA seja construída sobre ciência, não sobre ruído."
        <br><b>— E.M.I.L.I.A.</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🛡️ Scientific Integrity Shield")
    
    checks = [
        ("⚖️", "Class Imbalance"), ("🚰", "Data Leakage"), ("❓", "Missing Values"),
        ("👥", "Duplicate Rows"), ("📊", "Outlier Risk"), ("🔠", "Cardinality"),
        ("🆔", "ID-Like Risk"), ("🔢", "Encoding Risk"), ("📉", "Data Drift"),
        ("🎯", "Metric Validity"), ("🧠", "Overfitting"), ("🏗️", "Model Stability"),
        ("🔗", "Multicollinearity"), ("🔔", "Normality"), ("🧪", "Stress Test"),
        ("📏", "Threshold Quality"), ("🛑", "Constant Columns"), ("🔀", "Unknown-like"),
        ("💰", "Monetary Values")
    ]
    
    grid_html = '<div class="shield-grid">'
    for icon, label in checks:
        grid_html += f"""
        <div class="check-card">
            <div style="font-size: 1.5rem;">{icon}</div>
            <div class="check-label">{label}</div>
        </div>
        """
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

# --- FORMULÁRIO ---
st.markdown("<br><hr style='border-color: #333;'><br>", unsafe_allow_html=True)
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    st.markdown("<h3 style='text-align: center;'>Solicitar Acesso Antecipado</h3>", unsafe_allow_html=True)
    with st.form("waitlist"):
        email = st.text_input("E-mail:", placeholder="seu@email.com")
        btn = st.form_submit_button("RESERVAR MEU LUGAR NA v1.0")
        if btn and email:
            st.balloons()
            st.success("Pronto! Você será avisado em breve.")

st.markdown("<p style='text-align: center; color: #444; margin-top: 50px;'>OpenCanvas Pro © 2026 | Local-First Cognitive Intelligence</p>", unsafe_allow_html=True)
