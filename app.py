import os
import streamlit as st

# =========================================================
# OpenCanvas Pro — Landing Page
# VERSION: 1.1.0
# Status: Public Preview
# =========================================================

ASSETS_DIR = "assets"
PAGE_ICON_PATH = os.path.join(ASSETS_DIR, "32.png")
LOGO_PATH = os.path.join(ASSETS_DIR, "Cor_sobre_preto.svg")
SHIELD_PATH = os.path.join(ASSETS_DIR, "integrity_shield.png")

st.set_page_config(
    page_title="OpenCanvas Pro | Cognitive AutoML",
    page_icon=PAGE_ICON_PATH if os.path.exists(PAGE_ICON_PATH) else "🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        :root {
            --ocp-bg: #0D0D0D;
            --ocp-card: #161616;
            --ocp-border: #2B2B2B;
            --ocp-orange: #FF6B00;
            --ocp-orange-2: #FF8A33;
            --ocp-white: #FFFFFF;
            --ocp-muted: #D9D9D9;
            --ocp-soft: #BDBDBD;
        }

        .stApp {
            background: var(--ocp-bg) !important;
        }

        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        footer {
            display: none !important;
        }

        .block-container {
            padding-top: 1.4rem !important;
            padding-bottom: 2rem !important;
            max-width: 1500px !important;
        }

        h1, h2, h3, h4, h5, h6, p, li, span, label, div {
            font-family: "Inter", sans-serif !important;
        }

        .ocp-section-rule {
            border-top: 1px solid rgba(255,255,255,0.06);
            margin: 1.0rem 0 1.25rem 0;
        }

        .hero-logo-wrap {
            margin-top: 5.5rem;
            margin-left: 0.6rem;
        }

        .hero-title {
            text-align: center;
            font-size: 3.2rem;
            font-weight: 800;
            color: var(--ocp-white);
            margin: 0 0 0.2rem 0;
            letter-spacing: -0.03em;
        }

        .hero-title .accent {
            color: var(--ocp-orange) !important;
        }

        .hero-kicker {
            text-align: center;
            color: rgba(255,255,255,0.72) !important;
            letter-spacing: 2px;
            font-size: 1.02rem;
            margin-bottom: 0.25rem;
        }

        .hero-subcopy {
            text-align: center;
            color: var(--ocp-soft) !important;
            font-size: 0.98rem;
            max-width: 900px;
            margin: 0.25rem auto 0.45rem auto;
            line-height: 1.65;
        }

        .startup-chip {
            display: inline-block;
            margin: 0.75rem auto 0 auto;
            padding: 0.4rem 0.75rem;
            border: 1px solid rgba(255,107,0,0.35);
            border-radius: 999px;
            background: rgba(255,107,0,0.08);
            color: #FFD0B0 !important;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.03em;
        }

        .section-title {
            color: var(--ocp-white) !important;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }

        .section-title .accent {
            color: var(--ocp-orange) !important;
        }

        .section-subtitle {
            color: var(--ocp-soft) !important;
            font-size: 1rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        }

        .content-box {
            background: linear-gradient(180deg, rgba(22,22,22,0.98) 0%, rgba(18,18,18,0.98) 100%);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid var(--ocp-border);
            box-shadow: 0 0 0 1px rgba(255,255,255,0.02) inset;
            height: 100%;
        }

        .content-box h4 {
            color: var(--ocp-white) !important;
            margin-top: 0;
            margin-bottom: 0.45rem;
            font-size: 1.35rem;
            font-weight: 800;
        }

        .content-box p,
        .content-box span,
        .content-box li,
        .pillar-body {
            color: var(--ocp-muted) !important;
            opacity: 1 !important;
            line-height: 1.65;
            font-size: 0.98rem;
        }

        .orange-text {
            color: var(--ocp-orange) !important;
            font-weight: 800 !important;
        }

        .mini-kicker {
            color: var(--ocp-orange) !important;
            font-size: 0.9rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }

        .benefit-item {
            margin-bottom: 1rem;
        }

        .benefit-item:last-child {
            margin-bottom: 0;
        }

        .benefit-label {
            color: var(--ocp-orange) !important;
            font-size: 1rem;
            font-weight: 800;
        }

        .benefit-desc {
            color: var(--ocp-muted) !important;
            font-size: 0.95rem;
            line-height: 1.55;
            margin-top: 0.18rem;
        }

        .pillar-card {
            min-height: 190px;
        }

        .waitlist-wrap {
            max-width: 860px;
            margin: 0 auto;
        }

        .waitlist-title {
            text-align: center;
            color: var(--ocp-white) !important;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }

        .waitlist-subtitle {
            text-align: center;
            color: var(--ocp-soft) !important;
            max-width: 760px;
            margin: 0 auto 1rem auto;
            line-height: 1.65;
            font-size: 0.98rem;
        }

        div.stButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(90deg, var(--ocp-orange) 0%, var(--ocp-orange-2) 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            border-radius: 10px !important;
            min-height: 3.2rem !important;
            font-weight: 800 !important;
            width: 100% !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 8px 20px rgba(255,107,0,0.18);
        }

        div.stButton > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            transform: translateY(-1px);
            border-color: rgba(255,255,255,0.28) !important;
            box-shadow: 0 10px 24px rgba(255,107,0,0.28);
        }

        div.stButton > button p,
        div[data-testid="stFormSubmitButton"] > button p {
            color: #FFFFFF !important;
            font-weight: 800 !important;
        }

        .footer-wrap {
            margin-top: 1.5rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255,255,255,0.06);
            text-align: center;
        }

        .footer-main {
            color: var(--ocp-white) !important;
            font-size: 0.95rem;
            font-weight: 700;
        }

        .footer-sub {
            color: var(--ocp-soft) !important;
            font-size: 0.82rem;
            margin-top: 0.35rem;
            line-height: 1.6;
        }

        .footer-highlight {
            color: var(--ocp-orange) !important;
            font-weight: 800;
        }

        .stImage img {
            border-radius: 14px;
        }

        @media (max-width: 900px) {
            .hero-logo-wrap {
                margin-top: 0.5rem;
                margin-left: 0;
            }
            .hero-title {
                font-size: 2.45rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HERO
# =========================================================
hero_left, hero_center = st.columns([1, 5], gap="small")

with hero_left:
    st.markdown('<div class="hero-logo-wrap">', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=185)
    else:
        st.markdown(
            "<h3 style='color:#FF6B00; margin-top: 90px;'>OpenCanvas Pro</h3>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with hero_center:
    st.markdown(
        '''
        <div style="padding-top: 4.8rem;">
            <div class="hero-title">Cognitive <span class="accent">AutoML</span></div>
            <div class="hero-kicker">TRUSTED PLATFORM FOR SCIENTIFIC INTEGRITY</div>
            <div class="hero-subcopy">
                A OpenCanvas Pro é uma startup brasileira em nascimento, construída para transformar
                automação em confiança: unindo AutoML, governança, integridade científica e auditoria
                técnica para equipes que precisam de clareza — não apenas métricas bonitas.
            </div>
            <div style="text-align:center;">
                <span class="startup-chip">Startup em nascimento • opencanvaspro.com • CNPJ 64.918.004/0001-36</span>
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)

# =========================================================
# MAIN VALUE SECTION
# =========================================================
col_img, col_txt = st.columns([1.2, 1], gap="large")

with col_img:
    if os.path.exists(SHIELD_PATH):
        st.image(SHIELD_PATH, use_container_width=True)
    else:
        st.info("Aguardando 'integrity_shield.png' na pasta assets.")

with col_txt:
    st.markdown('<div class="section-title">Trusted Platform & <span class="accent">Diferenciais</span></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Não somos apenas mais uma interface para treinar modelos. Estamos desenhando uma nova categoria de software: uma plataforma de AutoML cognitiva, auditável e orientada à confiança.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="content-box">
            <div class="benefit-item">
                <div class="benefit-label">🧠 Cognitive Navigation (E.M.I.L.I.A.)</div>
                <div class="benefit-desc">Assistente contextual com grafo de conhecimento para orientar estratégias de treino, identificar riscos e evitar “pântanos estatísticos”.</div>
            </div>
            <div class="benefit-item">
                <div class="benefit-label">🔬 Scientific Integrity Shield™</div>
                <div class="benefit-desc">19+ validações avançadas para leakage, overfitting, inconsistências, desequilíbrio, colunas problemáticas e falhas silenciosas de modelagem.</div>
            </div>
            <div class="benefit-item">
                <div class="benefit-label">📄 Executive-Grade Artifacts</div>
                <div class="benefit-desc">Relatórios executivos, contratos de auditoria, documentação técnica e rastreabilidade para ambientes que exigem governança real.</div>
            </div>
            <div class="benefit-item">
                <div class="benefit-label">⚙️ Batch Prediction & Model Export</div>
                <div class="benefit-desc">Pipeline pronto para inferência em lote, exportação de modelos e operacionalização local-first com menor fricção.</div>
            </div>
            <div class="benefit-item">
                <div class="benefit-label">🏠 Local-First AI Sovereignty</div>
                <div class="benefit-desc">Processamento na infraestrutura do cliente, com foco em LGPD/GDPR, compliance, transparência e soberania sobre dados e artefatos.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# PILLARS
# =========================================================
st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">🚀 Pilares de <span class="accent">Performance</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Cada pilar foi desenhado para reduzir fricção, aumentar confiança e tornar o uso de Machine Learning mais seguro para times técnicos e executivos.</div>',
    unsafe_allow_html=True,
)

p1, p2, p3 = st.columns(3, gap="medium")

with p1:
    st.markdown(
        """
        <div class="content-box pillar-card">
            <div class="mini-kicker">Trust by Design</div>
            <h4>Auditoria Gold Standard</h4>
            <div class="pillar-body">
                Cada execução pode gerar trilha de auditoria, histórico de transformação, contratos técnicos e certificado de integridade científica para decisões com respaldo.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with p2:
    st.markdown(
        """
        <div class="content-box pillar-card">
            <div class="mini-kicker">White-Box ML</div>
            <h4>Transparência Operacional</h4>
            <div class="pillar-body">
                Controle explícito sobre dados, etapas de preparação, checks, métricas e artefatos. Nada de caixa-preta disfarçada de conveniência.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with p3:
    st.markdown(
        """
        <div class="content-box pillar-card">
            <div class="mini-kicker">Local-First Efficiency</div>
            <h4>Eficiência de Recurso</h4>
            <div class="pillar-body">
                Arquitetura orientada a performance local, redução de fricção operacional e menor dependência de nuvem para workloads sensíveis.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# WAITLIST
# =========================================================
st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="waitlist-wrap">', unsafe_allow_html=True)
st.markdown('<div class="waitlist-title">Entre cedo no radar da OpenCanvas Pro</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="waitlist-subtitle">
        Estamos abrindo terreno para o lançamento oficial. Cadastre seu e-mail para acompanhar a evolução da plataforma, os previews técnicos e o início do acesso antecipado.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("waitlist_form", clear_on_submit=True):
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        email = st.text_input("Seu e-mail:", placeholder="exemplo@empresa.com")
        submitted = st.form_submit_button("🔔 QUERO SER AVISADO NO LANÇAMENTO")
        if submitted:
            if email and "@" in email:
                st.success("Interesse registrado nesta prévia pública. Em breve abriremos a lista oficial de acesso antecipado.")
            else:
                st.warning("Por favor, informe um e-mail válido.")

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer-wrap">
        <div class="footer-main">OpenCanvas Pro © 2026 • <span class="footer-highlight">Cognitive AutoML Trusted Platform</span></div>
        <div class="footer-sub">
            Startup brasileira em nascimento • CNPJ 64.918.004/0001-36 • opencanvaspro.com<br>
            Built for Science. Built for Trust. Powered by E.M.I.L.I.A.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)