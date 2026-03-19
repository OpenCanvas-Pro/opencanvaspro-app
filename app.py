import base64
import mimetypes
import os
import smtplib
from textwrap import dedent
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# OpenCanvas Pro — Landing Page
# VERSION: 1.1.2
# Status: Public Preview
# =========================================================

ASSETS_DIR = "assets"
PAGE_ICON_PATH = os.path.join(ASSETS_DIR, "32.png")
LOGO_PATH = os.path.join(ASSETS_DIR, "Cor_sobre_preto.svg")
SHIELD_PATH = os.path.join(ASSETS_DIR, "integrity_shield.png")
LINKEDIN_URL = "https://www.linkedin.com/company/opencanvaspro"
X_URL = "https://x.com/opencanvaspro"
GITHUB_URL = "https://github.com/OpenCanvas-Pro"


def file_to_data_uri(path: str) -> str:
    mime_type, _ = mimetypes.guess_type(path)
    mime_type = mime_type or "application/octet-stream"
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def lucide_icon(name: str) -> str:
    icons = {
        "brain": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9.5 2a3.5 3.5 0 0 0-2.847 5.534A4 4 0 0 0 6 15.5V16a3 3 0 0 0 5.24 2"/><path d="M14.5 2a3.5 3.5 0 0 1 2.847 5.534A4 4 0 0 1 18 15.5V16a3 3 0 0 1-5.24 2"/><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M9 12H6"/><path d="M18 12h-3"/><path d="M12 12h.01"/></svg>',
        "bell-ring": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.674C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/><path d="M4 2C2.8 3.7 2 5.7 2 8"/><path d="M22 8a9.9 9.9 0 0 0-2-6"/></svg>',
        "send": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.536 21.686a.5.5 0 0 0 .937-.025l6.5-19a.5.5 0 0 0-.63-.63l-19 6.5a.5.5 0 0 0-.025.937l7.876 3.438a2 2 0 0 1 1.02 1.02z"/><path d="m21.854 2.147-10.94 10.939"/></svg>',
        "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/></svg>',
        "file-text": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>',
        "rocket": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.5 16.5c-1.5 1.5-2 4.5-2 4.5s3-.5 4.5-2c1-1 1.5-2 1.5-2s-1-.5-2-1.5-1.5-2-1.5-2-1 1.5-2.5 3Z"/><path d="m12 15-3-3a19.8 19.8 0 0 1 8-8l3 3a19.8 19.8 0 0 1-8 8Z"/><path d="M9 12 4 7a19.8 19.8 0 0 1 8-3l3 3"/><path d="M12 15l5 5a19.8 19.8 0 0 0 3-8l-3-3"/></svg>',
        "sliders": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="10" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="8" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="12" y2="3"/><line x1="2" x2="6" y1="14" y2="14"/><line x1="10" x2="14" y1="8" y2="8"/><line x1="18" x2="22" y1="16" y2="16"/></svg>',
        "building": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M8 10h.01"/><path d="M16 10h.01"/><path d="M8 14h.01"/><path d="M16 14h.01"/></svg>',
    }
    return icons[name]


def social_icon(name: str) -> str:
    icons = {
        "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.94 8.5H3.56V19h3.38zM5.25 3A1.97 1.97 0 1 0 5.3 6.94 1.97 1.97 0 0 0 5.25 3M20.44 11.12c0-2.93-1.56-4.3-3.65-4.3a3.16 3.16 0 0 0-2.87 1.58h-.05V8.5H10.5c.04.62 0 10.5 0 10.5h3.38v-5.86c0-.31.02-.62.12-.84.25-.62.82-1.27 1.77-1.27 1.25 0 1.75.96 1.75 2.37V19H21z"/></svg>',
        "x": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.9 2H22l-6.77 7.74L23.2 22h-6.26l-4.9-7.39L5.58 22H2.47l7.24-8.27L1.8 2h6.42l4.43 6.75zm-1.1 18h1.73L7.3 3.9H5.45z"/></svg>',
        "github": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5a12 12 0 0 0-3.79 23.39c.6.11.82-.26.82-.58v-2.03c-3.34.73-4.04-1.42-4.04-1.42-.55-1.38-1.33-1.75-1.33-1.75-1.09-.74.08-.72.08-.72 1.2.08 1.84 1.24 1.84 1.24 1.08 1.83 2.82 1.3 3.5.99.11-.78.42-1.3.76-1.6-2.67-.31-5.47-1.33-5.47-5.92 0-1.31.47-2.38 1.24-3.22-.12-.31-.54-1.56.12-3.26 0 0 1.01-.32 3.3 1.23A11.5 11.5 0 0 1 12 6.32c1.02 0 2.05.14 3.01.41 2.29-1.55 3.29-1.23 3.29-1.23.67 1.7.25 2.95.13 3.26.77.84 1.24 1.91 1.24 3.22 0 4.6-2.8 5.6-5.48 5.91.43.37.82 1.1.82 2.22v3.2c0 .32.22.7.83.58A12 12 0 0 0 12 .5"/></svg>',
    }
    return icons[name]


def send_waitlist_email(user_email: str) -> tuple[bool, str]:
    try:
        host = st.secrets["EMAIL_HOST"]
        port = int(st.secrets["EMAIL_PORT"])
        username = st.secrets["EMAIL_USERNAME"]
        password = st.secrets["EMAIL_PASSWORD"]
        waitlist_to = st.secrets.get("WAITLIST_TO", "contato@opencanvaspro.com")

        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = waitlist_to
        msg["Subject"] = "Novo cadastro na waitlist — OpenCanvas Pro"

        body = f"""
Novo interesse registrado na waitlist da OpenCanvas Pro.

E-mail informado: {user_email}

Origem: landing pública
Produto: OpenCanvas Pro — Cognitive AutoML
Site: opencanvaspro.com
CNPJ: 64.918.004/0001-36
"""
        msg.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP(host, port, timeout=10)
        server.starttls()
        server.login(username, password)
        server.sendmail(username, waitlist_to, msg.as_string())
        server.quit()

        return True, "Interesse registrado com sucesso."
    except Exception as e:
        return False, str(e)


st.set_page_config(
    page_title="OpenCanvas Pro | Cognitive AutoML",
    page_icon=PAGE_ICON_PATH if os.path.exists(PAGE_ICON_PATH) else "🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# SEO & META TAGS (POWER MODE)
# =========================================================
def inject_seo_tags():
    seo_script = dedent(
        """
        <script>
        const metaTags = [
          { name: "description", content: "A plataforma de AutoML que une Integridade Científica e Navegação Cognitiva. Desenvolvida para modelos de alta confiança." },
          { name: "keywords", content: "AutoML, Machine Learning, Integridade Científica, Data Science, AI, OpenCanvas" },
          { name: "author", content: "OpenCanvas Pro" },
          { property: "og:type", content: "website" },
          { property: "og:url", content: "https://opencanvaspro.com/" },
          { property: "og:title", content: "OpenCanvas Pro | Cognitive AutoML" },
          { property: "og:description", content: "Garanta a integridade científica dos seus modelos de IA com a plataforma Cognitive AutoML." },
          { property: "og:image", content: "https://opencanvaspro.com/assets/integrity_shield.png" },
          { property: "twitter:card", content: "summary_large_image" },
          { property: "twitter:url", content: "https://opencanvaspro.com/" },
          { property: "twitter:title", content: "OpenCanvas Pro | Cognitive AutoML" },
          { property: "twitter:description", content: "Trusted Platform for Scientific Integrity em Machine Learning." },
          { property: "twitter:image", content: "https://opencanvaspro.com/assets/integrity_shield.png" }
        ];

        document.title = "OpenCanvas Pro | Cognitive AutoML Trusted Platform";

        metaTags.forEach((attrs) => {
          const selector = attrs.name
            ? `meta[name="${attrs.name}"]`
            : `meta[property="${attrs.property}"]`;

          let tag = parent.document.head.querySelector(selector);
          if (!tag) {
            tag = parent.document.createElement("meta");
            parent.document.head.appendChild(tag);
          }

          Object.entries(attrs).forEach(([key, value]) => tag.setAttribute(key, value));
        });
        </script>
        """
    ).strip()
    components.html(seo_script, height=0)

inject_seo_tags()

# =========================================================

logo_uri = file_to_data_uri(LOGO_PATH) if os.path.exists(LOGO_PATH) else ""
shield_uri = file_to_data_uri(SHIELD_PATH) if os.path.exists(SHIELD_PATH) else ""

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
            padding-top: 0.30rem !important;
            padding-bottom: 2rem !important;
            max-width: 1500px !important;
        }

        h1, h2, h3, h4, h5, h6, p, li, span, label, div {
            font-family: "Inter", sans-serif !important;
        }

        .ocp-section-rule {
            border-top: 1px solid rgba(255,255,255,0.06);
            margin: 1.15rem 0 1.35rem 0;
        }

        .hero-logo-wrap {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 180px;
            padding-top: 0.55rem;
        }

        .hero-logo-img {
            width: 170px;
            height: auto;
            display: block;
        }

        .hero-copy-wrap {
            padding-top: 0.1rem;
        }

        .hero-title {
            text-align: center;
            font-size: 3.2rem;
            font-weight: 800;
            color: var(--ocp-white);
            margin: 0 0 0.2rem 0;
            letter-spacing: -0.03em;
            line-height: 1.08;
        }

        .hero-title .accent {
            color: var(--ocp-orange) !important;
        }

        .hero-kicker {
            text-align: center;
            color: rgba(255,255,255,0.72) !important;
            letter-spacing: 2px;
            font-size: 1.02rem;
            margin-bottom: 0.38rem;
        }

        .hero-subcopy {
            text-align: center;
            color: var(--ocp-soft) !important;
            font-size: 0.98rem;
            max-width: 900px;
            margin: 0.25rem auto 0 auto;
            line-height: 1.68;
        }

        .hero-highlight {
            text-align: center;
            color: var(--ocp-orange) !important;
            font-size: 0.98rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            margin-top: 0.75rem;
        }

        .section-title {
            color: var(--ocp-white) !important;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.28rem;
            line-height: 1.15;
        }

        .section-title .accent {
            color: var(--ocp-orange) !important;
        }

        .section-subtitle {
            color: var(--ocp-soft) !important;
            font-size: 1rem;
            line-height: 1.62;
            margin-bottom: 1rem;
            max-width: none;
        }

        .feature-intro {
            margin-bottom: 0.7rem;
            text-align: center;
            width: 100%;
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
            display: flex;
            align-items: center;
            gap: 0.6rem;
            line-height: 1.35;
        }

        .benefit-label-icon {
            width: 18px;
            height: 18px;
            flex: 0 0 18px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: var(--ocp-orange);
        }

        .benefit-label-icon svg {
            width: 18px;
            height: 18px;
        }

        .benefit-desc {
            color: var(--ocp-muted) !important;
            font-size: 0.95rem;
            line-height: 1.55;
            margin-top: 0.18rem;
        }

        .feature-row {
            align-items: stretch;
        }

        .feature-media-wrap {
            width: 100%;
            height: 100%;
            min-height: 440px;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--ocp-border);
            box-shadow: 0 0 0 1px rgba(255,255,255,0.02) inset;
            background: #101010;

            display: flex;
            align-items: center;
            justify-content: center;
        }

        .feature-media {
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
        }

        .feature-card {
            min-height: 100px;
        }

        .feature-card .content-box {
            height: 100%;
        }

        .feature-card-shell {
            display: flex;
            align-items: stretch;
            gap: 22px;
            height: 100%;
        }

        .feature-visual {
            flex: 0 0 52%;
            min-width: 0;
        }

        .feature-copy {
            flex: 0 0 48%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .pillar-card {
            min-height: 255px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease, background 0.22s ease;
        }

        .pillar-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255,107,0,0.38);
            box-shadow: 0 14px 30px rgba(255,107,0,0.12), 0 0 0 1px rgba(255,107,0,0.08) inset;
            background: linear-gradient(180deg, rgba(28,20,14,0.98) 0%, rgba(20,16,12,0.98) 100%);
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

        .waitlist-title .accent {
            color: var(--ocp-orange) !important;
        }

        .waitlist-subtitle {
            text-align: center;
            color: var(--ocp-soft) !important;
            max-width: 760px;
            margin: 0 auto 1rem auto;
            line-height: 1.65;
            font-size: 0.98rem;
        }

        .waitlist-cta-row {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            width: 100%;
        }

        .waitlist-input-icon,
        .waitlist-cta-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--ocp-orange);
            flex: 0 0 22px;
        }

        .waitlist-input-icon {
            margin-top: 2rem;
        }

        .waitlist-cta-icon {
            margin-top: 0.7rem;
        }

        .waitlist-input-icon svg,
        .waitlist-cta-icon svg {
            width: 22px;
            height: 22px;
        }

        .waitlist-cta-button {
            flex: 1 1 auto;
        }

        .social-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.85rem;
            margin-top: 0.9rem;
        }

        .social-link {
            width: 42px;
            height: 42px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(255,255,255,0.02);
            color: var(--ocp-soft) !important;
            text-decoration: none;
            transition: transform 0.22s ease, border-color 0.22s ease, color 0.22s ease, background 0.22s ease;
        }

        .social-link:hover {
            transform: translateY(-2px);
            border-color: rgba(255,107,0,0.5);
            background: rgba(255,107,0,0.08);
            color: var(--ocp-orange) !important;
        }

        .social-link svg {
            width: 18px;
            height: 18px;
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
            transform: none !important;
            background: #0D0D0D !important;
            color: var(--ocp-orange) !important;
            border-color: var(--ocp-orange) !important;
            box-shadow: none !important;
        }

        div.stButton > button p,
        div[data-testid="stFormSubmitButton"] > button p {
            color: #FFFFFF !important;
            font-weight: 800 !important;
        }

        div.stButton > button:hover p,
        div[data-testid="stFormSubmitButton"] > button:hover p {
            color: var(--ocp-orange) !important;
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

        .footer-sub a {
            color: var(--ocp-orange) !important;
            text-decoration: none;
            font-weight: 700;
        }

        .footer-sub a:hover {
            color: var(--ocp-orange-2) !important;
            text-decoration: underline;
        }

        .footer-highlight {
            color: var(--ocp-orange) !important;
            font-weight: 800;
        }

        @media (max-width: 900px) {
            .hero-logo-wrap {
                min-height: auto;
                padding-top: 0.15rem;
                margin-bottom: 0.5rem;
            }

            .hero-logo-img {
                width: 145px;
            }

            .hero-title {
                font-size: 2.45rem;
            }

            .feature-media-wrap,
            .feature-card {
                height: auto;
                min-height: auto;
            }

            .feature-card-shell {
                flex-direction: column;
            }

            .feature-visual {
                min-width: 0;
            }

            .feature-media-wrap {
                min-height: 220px;
            }

            .feature-media {
                height: auto;
                max-height: 220px;
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
    if logo_uri:
        st.markdown(
            f'''
            <div class="hero-logo-wrap">
                <img src="{logo_uri}" class="hero-logo-img" alt="OpenCanvas Pro Logo" />
            </div>
            ''',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='hero-logo-wrap'><h3 style='color:#FF6B00;'>OpenCanvas Pro</h3></div>",
            unsafe_allow_html=True,
        )

with hero_center:
    st.markdown(
        '''
        <div class="hero-copy-wrap">
            <div class="hero-title">OpenCanvas <span class="accent">Pro - Cognitive AutoML</span></div>
            <div class="hero-kicker">TRUSTED PLATFORM FOR SCIENTIFIC INTEGRITY</div>
            <div class="hero-subcopy">
                A OpenCanvas Pro é uma startup brasileira em nascimento, construída para transformar
                automação em confiança: unindo AutoML, governança, integridade científica e auditoria
                técnica para equipes que precisam de clareza — não apenas métricas bonitas.
            </div>
        </div>

        <div class="hero-highlight">
            Projetado para times que não podem errar decisões baseadas em dados
        </div>

        ''',
        unsafe_allow_html=True,
    )

        

st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)

        

# =========================================================
# MAIN VALUE SECTION
# =========================================================
st.markdown(
    '''
    <div class="feature-intro">
        <div class="section-title">Trusted Platform & <span class="accent">Diferenciais</span></div>
        <div class="section-subtitle">
            Não somos apenas mais uma interface para treinar modelos. Estamos desenhando uma nova categoria de software:
            uma plataforma de AutoML cognitiva, auditável e orientada à confiança.
        </div>
    </div>
    ''',
    unsafe_allow_html=True,
)

feature_visual_html = (
    dedent(
        f"""
        <div class="feature-visual">
            <div class="feature-media-wrap">
                <img src="{shield_uri}" class="feature-media" alt="Scientific Integrity Shield" />
            </div>
        </div>
        """
    ).strip()
    if shield_uri
    else dedent(
        """
        <div class="feature-visual">
            <div class="feature-media-wrap">
                <div class="benefit-desc">Aguardando 'integrity_shield.png' na pasta assets.</div>
            </div>
        </div>
        """
    ).strip()
)

st.markdown(
    dedent(
        f"""
    <div class="feature-card">
        <div class="content-box">
            <div class="feature-card-shell">
                {feature_visual_html}
                <div class="feature-copy">
                    <div class="benefit-item">
                        <div class="benefit-label"><span class="benefit-label-icon">{lucide_icon("brain")}</span> Cognitive Navigation (E.M.I.L.I.A.)</div>
                        <div class="benefit-desc">Assistente contextual com grafo de conhecimento para orientar estratégias de treino, identificar riscos e evitar “pântanos estatísticos”.</div>
                    </div>
                    <div class="benefit-item">
                        <div class="benefit-label"><span class="benefit-label-icon">{lucide_icon("shield")}</span> Scientific Integrity Shield™</div>
                        <div class="benefit-desc">19+ validações avançadas para leakage, overfitting, inconsistências, desequilíbrio, colunas problemáticas e falhas silenciosas de modelagem.</div>
                    </div>
                    <div class="benefit-item">
                        <div class="benefit-label"><span class="benefit-label-icon">{lucide_icon("file-text")}</span> Executive-Grade Artifacts</div>
                        <div class="benefit-desc">Relatórios executivos, contratos de auditoria, documentação técnica e rastreabilidade para ambientes que exigem governança real.</div>
                    </div>
                    <div class="benefit-item">
                        <div class="benefit-label"><span class="benefit-label-icon">{lucide_icon("sliders")}</span> Batch Prediction & Model Export</div>
                        <div class="benefit-desc">Pipeline pronto para inferência em lote, exportação de modelos e operacionalização local-first com menor fricção.</div>
                    </div>
                    <div class="benefit-item">
                        <div class="benefit-label"><span class="benefit-label-icon">{lucide_icon("building")}</span> Local-First AI Sovereignty</div>
                        <div class="benefit-desc">Processamento na infraestrutura do cliente, com foco em LGPD/GDPR, compliance, transparência e soberania sobre dados e artefatos.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    ).strip(),
    unsafe_allow_html=True,
)

# =========================================================
# PILLARS
# =========================================================
st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="section-title"><span class="benefit-label-icon">{lucide_icon("rocket")}</span> Pilares de <span class="accent">Performance</span></div>',
    unsafe_allow_html=True,
)
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
st.markdown('<div class="waitlist-title">Entre cedo no radar da OpenCanvas <span class="accent" style="color:#FF6B00;">Pro</span></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="waitlist-subtitle">
        Estamos abrindo terreno para o lançamento oficial. Cadastre seu e-mail para acompanhar a evolução da plataforma, os previews técnicos e novidades.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("waitlist_form", clear_on_submit=True):
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        input_icon_col, input_field_col = st.columns([0.08, 0.92], gap="small")
        with input_icon_col:
            st.markdown(
                f'<div class="waitlist-input-icon">{lucide_icon("send")}</div>',
                unsafe_allow_html=True,
            )
        with input_field_col:
            email = st.text_input("Seu e-mail:", placeholder="exemplo@empresa.com")

        cta_icon_col, cta_button_col = st.columns([0.08, 0.92], gap="small")
        with cta_icon_col:
            st.markdown(
                f'<div class="waitlist-cta-icon">{lucide_icon("bell-ring")}</div>',
                unsafe_allow_html=True,
            )
        with cta_button_col:
            submitted = st.form_submit_button("QUERO SER AVISADO NO LANÇAMENTO")

        if submitted:
            if email and "@" in email:
                ok, msg = send_waitlist_email(email)
                if ok:
                    st.success("Interesse registrado com sucesso. Em breve entraremos em contato.")
                else:
                    st.error(f"Não foi possível registrar agora: {msg}")
            else:
                st.warning("Por favor, informe um e-mail válido.")

st.markdown(
    dedent(
        f"""
        <div class="social-row">
            <a class="social-link" href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                {social_icon("linkedin")}
            </a>
            <a class="social-link" href="{X_URL}" target="_blank" rel="noopener noreferrer" aria-label="X">
                {social_icon("x")}
            </a>
            <a class="social-link" href="{GITHUB_URL}" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
                {social_icon("github")}
            </a>
        </div>
        """
    ).strip(),
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer-wrap">
        <div class="footer-main">OpenCanvas <span class="accent" style="color:#FF6B00;">Pro</span> © 2026 • <span class="footer-highlight">Cognitive AutoML Trusted Platform</span></div>
        <div class="footer-sub">
            Plataforma em early-stage • CNPJ 64.918.004/0001-36 • opencanvaspro.com<br>
            Built for Science. Built for Trust. Powered by E.M.I.L.I.A. • <a href="mailto:contato@opencanvaspro.com">contato@opencanvaspro.com</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
