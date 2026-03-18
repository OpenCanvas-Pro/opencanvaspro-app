import streamlit as st
import time
import base64
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="OpenCanvas Pro | Cognitive AutoML",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FUNÇÕES AUXILIARES ---
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- CSS CUSTOMIZADO (ESTILO COCKPIT / DARK MODE / NEON ORANGE) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=JetBrains+Mono:wght@500&display=swap');
    
    :root {{
        --ocp-orange: #FF6B00;
        --ocp-bg: #0D0D0D;
        --ocp-card: #161616;
    }}

    .stApp {{
        background-color: var(--ocp-bg);
        color: white;
        font-family: 'Inter', sans-serif;
    }}

    /* Esconder Elementos Padrão */
    #MainMenu, footer, header {{ visibility: hidden; }}

    /* Grid de Integridade */
    .shield-container {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
        gap: 12px;
        margin-top: 20px;
    }}

    .check-card {{
        background: var(--ocp-card);
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }}

    .check-card:hover {{
        border-color: var(--ocp-orange);
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(255, 107, 0, 0.2);
    }}

    .check-icon {{
        font-size: 1.2rem;
        margin-bottom: 8px;
    }}

    .check-label {{
        font-size: 0.75rem;
        font-weight: 600;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* Estilo do Botão Principal */
    .stButton>button {{
        background: linear-gradient(90deg, #FF6B00 0%, #FF8533 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        font-weight: 800;
        border-radius: 5px;
        width: 100%;
        transition: all 0.3s;
    }}

    .stButton>button:hover {{
        box-shadow: 0 0 20px rgba(255, 107, 0, 0.4);
        transform: scale(1.02);
    }}

    .emilia-box {{
        background: rgba(255, 107, 0, 0.05);
        border-left: 4px solid var(--ocp-orange);
        padding: 20px;
        border-radius: 0 10px 10px 0;
    }}
</style>
""", unsafe_allow_html=True)

# --- HEADER / LOGO ---
col_logo, col_empty = st.columns([1, 4])
with col_logo:
    try:
        st.image("Cor_Preto_Logo_OCP.png", use_container_width=True)
    except:
        st.title("🍊 OCP")

# --- HERO SECTION ---
st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-bottom: 0;'>Cognitive AutoML</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FF6B00; font-weight: 700; font-size: 1.2rem;'>THE TRUSTED PLATFORM FOR SCIENTIFIC INTEGRITY</p>", unsafe_allow_html=True)

st.write("---")

# --- CONTEÚDO PRINCIPAL (EMILIA + SHIELD) ---
c1, c2 = st.columns([1, 1.8], gap="large")

with c1:
    try:
        st.image("Emilia_hires.jpg", caption="E.M.I.L.I.A. - Your Cognitive Advisor", use_container_width=True)
    except:
        st.info("Imagem da E.M.I.L.I.A. carregando...")
        
    st.markdown("""
    <div class="emilia-box">
        <h4 style='color: #FF6B00; margin-top:0;'>Mensagem da E.M.I.L.I.A.</h4>
        <p style='font-size: 0.9rem; line-height: 1.4;'>
            "Bem-vindo ao cockpit. Enquanto você foca no problema de negócio, 
            eu monitoro 19 dimensões de integridade científica em tempo real. 
            Nenhum viés ou vazamento de dados passará pelo meu escudo."
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("### 🛡️ Scientific Integrity Shield (v1.0 Preview)")
    st.markdown("<p style='color: #666;'>A OpenCanvas Pro valida automaticamente cada etapa do seu experimento.</p>", unsafe_allow_html=True)
    
    # Matriz dos 19 Checks
    checks = [
        ("⚖️", "Class Imbalance"), ("🚰", "Data Leakage"), ("❓", "Missing Values"),
        ("👥", "Duplicate Rows"), ("📊", "Outlier Risk"), ("🔠", "Cardinality"),
        ("🆔", "ID-Like Risk"), ("🔢", "Encoding Risk"), ("📉", "Data Drift"),
        ("🎯", "Metric Validity"), ("🧠", "Overfitting"), ("🏗️", "Model Stability"),
        ("🔗", "Multicollinearity"), ("🔔", "Normality"), ("🧪", "Stress Test"),
        ("📏", "Threshold Quality"), ("🛑", "Constant Columns"), ("🔀", "Unknown-like"),
        ("💰", "Monetary Values")
    ]
    
    shield_html = '<div class="shield-container">'
    for icon, name in checks:
        shield_html += f"""
        <div class="check-card">
            <div class="check-icon">{icon}</div>
            <div class="check-label">{name}</div>
        </div>
        """
    shield_html += '</div>'
    st.markdown(shield_html, unsafe_allow_html=True)

# --- ESPAÇADOR ---
st.write("")
st.write("")

# --- WAITLIST FORM (MODERNIZADO) ---
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns([1, 1.5, 1])
with col_f2:
    st.markdown("<h3 style='text-align: center;'>Junte-se à Revolução Local-First</h3>", unsafe_allow_html=True)
    with st.form("waitlist_form"):
        email = st.text_input("Seu melhor e-mail corporativo:", placeholder="exemplo@empresa.com")
        submit = st.form_submit_button("🚀 SOLICITAR ACESSO ANTECIPADO")
        
        if submit:
            if email and "@" in email:
                st.toast("E-mail registrado com sucesso!", icon="🔥")
                st.balloons()
                st.success(f"Confirmado! **{email}** está na lista prioritária para a v1.0.")
            else:
                st.error("Por favor, insira um e-mail válido.")

# --- FOOTER ---
st.markdown("<br><p style='text-align: center; color: #444; font-size: 0.8rem;'>OpenCanvas Pro &copy; 2026 | Built for Science. Built for Trust.</p>", unsafe_allow_html=True)
