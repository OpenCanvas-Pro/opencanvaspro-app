import base64
import html as html_lib
import mimetypes
import os
import re
import smtplib
from textwrap import dedent
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Final, TypeAlias, TypedDict, cast
from urllib.parse import quote

import streamlit as st
from translations import I18N, LANG_LABELS

# =========================================================
# OpenCanvas Pro — Landing Page
# VERSION: 2.0.0
# Status: Public Preview
# =========================================================

ASSETS_DIR = "assets"
PAGE_ICON_PATH = os.path.join(ASSETS_DIR, "32.png")
LOGO_PATH = os.path.join(ASSETS_DIR, "Cor_sobre_preto.svg")
SHIELD_PATH = os.path.join(ASSETS_DIR, "integrity_shield.png")
EMILIA_PATH = os.path.join(ASSETS_DIR, "Emilia_hires.png")
NEO4J_PATH = os.path.join(ASSETS_DIR, "Neo4j Logo_FullColor_RGB_TransBG.svg")
DESAFIX_BANNER_PATH = os.path.join(ASSETS_DIR, "Banner_Desafio_2026_empresa_acelerada.png")
MATURITY_HTML_PATH = "maturidade_ia_opencanvas_v4.3.html"
SNIS_MAP_HTML_PATH = os.path.join(ASSETS_DIR, "snis_map.html")
SNIS_MAP_HEIGHT = 720
LINKEDIN_URL = "https://www.linkedin.com/company/opencanvaspro"
X_URL = "https://x.com/opencanvaspro"
GITHUB_URL = "https://github.com/OpenCanvas-Pro/opencanvaspro-app"
YOUTUBE_URL = "https://www.youtube.com/@OpenCanvasPro"
CONTACT_EMAIL = "contato@opencanvaspro.com"

FooterLink: TypeAlias = dict[str, str]
RoadmapFooterItem: TypeAlias = str | FooterLink


class RoadmapItem(TypedDict, total=False):
    level: str
    title: str
    desc: str
    features: list[str]
    footer_label: str
    footer_items: list[RoadmapFooterItem]
    status: str
    future: bool
    active: bool

@st.cache_data(show_spinner=False)
def file_to_data_uri(path: str) -> str:
    mime_type, _ = mimetypes.guess_type(path)
    mime_type = mime_type or "application/octet-stream"
    if path == NEO4J_PATH and path.endswith(".svg"):
        with open(path, "r", encoding="utf-8") as f:
            svg = f.read()
        svg = svg.replace(".st0{fill:#231F20;}", ".st0{fill:#FFFFFF;}")
        svg = svg.replace(".st1{fill:#014063;}", ".st1{fill:#4EA1F2;}")
        encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    else:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def lucide_icon(name: str) -> str:
    icons: Final[dict[str, str]] = {
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


def material_icon(name: str) -> str:
    icons: Final[dict[str, str]] = {
        "rocket-launch": "rocket_launch",
    }
    return icons[name]


def tr(lang: str, key: str) -> str:
    return I18N.get(lang, I18N["pt"]).get(key, I18N["pt"].get(key, ""))


def get_mailto_link(plan_name: str, lang: str) -> str:
    if lang == "pt":
        subject = quote(f"Interesse na versão {plan_name} - OpenCanvas Pro")
        body = quote(
            f"Olá, equipe OpenCanvas Pro.\n\n"
            f"Tenho interesse em saber mais sobre a versão {plan_name}.\n\n"
            f"Gostaria de receber informações sobre recursos, disponibilidade, implantação e próximos passos.\n\n"
            f"Nome:\n"
            f"Empresa:\n"
            f"Telefone:\n"
            f"Mensagem:\n"
        )
    else:
        subject = quote(f"Interest in {plan_name} version - OpenCanvas Pro")
        body = quote(
            f"Hello, OpenCanvas Pro team.\n\n"
            f"I am interested in learning more about the {plan_name} version.\n\n"
            f"I would like to receive information about features, availability, deployment, and next steps.\n\n"
            f"Name:\n"
            f"Company:\n"
            f"Phone:\n"
            f"Message:\n"
        )
    return f"mailto:{CONTACT_EMAIL}?subject={subject}&body={body}"


def maturity_replacements(lang: str) -> list[tuple[str, str]]:
    if lang == "en":
        return [
            ("Cognição Assistida", "Assisted Cognition"),
            ("Hoje: Level 4 — Cognição Assistida → Próximo marco: Level 5 — Agentic Autonomy", "Today: Level 4 — Assisted Cognition → Next milestone: Level 5 — Agentic Autonomy"),
            ("Level 4 — Cognição Assistida", "Level 4 — Assisted Cognition"),
            ("Level 5 — Autonomia Agêntica", "Level 5 — Agentic Autonomy"),
            ("Roadmap de Soberania Tecnológica", "Technology Sovereignty Roadmap"),
            ("Nível 1", "Level 1"),
            ("Nível 2", "Level 2"),
            ("Nível 3", "Level 3"),
            ("Nível 4", "Level 4"),
            ("Nível 5", "Level 5"),
            ("Automação Simples", "Simple Automation"),
            ("Execução de tarefas repetitivas baseada em regras estáticas.", "Execution of repetitive tasks based on static rules."),
            ("Inteligência Estatística", "Statistical Intelligence"),
            ("Aprendizado de padrões históricos sem noção de contexto.", "Learning historical patterns without a sense of context."),
            ("IA Assistiva", "Assistive AI"),
            ("Interface guiada para acelerar fluxos através da facilidade de uso.", "Guided interface to accelerate workflows through ease of use."),
            ("Cognição & Integridade", "Cognition & Integrity"),
            ("Interpreta contexto, integra sinais de qualidade e justifica recomendações com base em evidência estatística.", "Interprets context, integrates quality signals and justifies recommendations based on statistical evidence."),
            ("Autonomia Agêntica", "Agentic Autonomy"),
            ("Execução de objetivos complexos com correção dinâmica de estratégia.", "Execution of complex goals with dynamic strategy correction."),
            ("Plataformas atuais", "Current platforms"),
            ("Diferencial OpenCanvas", "OpenCanvas differentiator"),
            ("Mercado", "Market"),
            ("Scripts de Ingestão (Python)", "Ingestion scripts (Python)"),
            ("ETL Linear", "Linear ETL"),
            ("Modelos Preditivos", "Predictive models"),
            ("Classificação & Regressão", "Classification & regression"),
            ("Copilotos de Código", "Code copilots"),
            ("AutoML No-Code", "No-code AutoML"),
            ("Agentes Multi-step", "Multi-step agents"),
            ("Auto-remediação baseada em feedback de desempenho", "Performance-feedback self-remediation"),
            ("Evolução contínua orientada por contexto", "Continuous context-driven evolution"),
            ("ETL Manual / Python", "Manual ETL / Python"),
            ("Jupyter Notebooks", "Jupyter notebooks"),
            ("RPA Tradicional", "Traditional RPA"),
            ("AutoML Tradicional (H2O, AutoGluon)", "Traditional AutoML (H2O, AutoGluon)"),
            ("Notebooks de Ciência de Dados", "Data science notebooks"),
            ("AWS SageMaker Canvas", "AWS SageMaker Canvas"),
            ("Google Vertex AI", "Google Vertex AI"),
            ("MS Azure ML Studio", "MS Azure ML Studio"),
            ("Teoria acadêmica", "Academic theory"),
            ("Agentes Genéricos (Experimental)", "Generic agents (experimental)"),
            ("Pesquisa de Fronteira", "Frontier research"),
            ("Foco em Missão Crítica, Governança Executiva e Transparência Total.", "Mission-critical focus, executive governance and full transparency."),
            ("Hoje:", "Today:"),
            ("Próximo marco:", "Next milestone:"),
            ("A maioria das plataformas para no nível 3.", "Most platforms stop at level 3."),
            ("Roadmap de Soberania Tecnológica", "Technology Sovereignty Roadmap"),
            ("Auditoria Gold Standard", "Gold Standard Auditing"),
            ("Transparência Operacional", "Operational Transparency"),
            ("Eficiência de Recurso", "Resource Efficiency"),
            ("Trust by Design", "Trust by Design"),
            ("White-Box ML", "White-Box ML"),
            ("Local-First Efficiency", "Local-First Efficiency"),
            ("CURRENT STATE", "CURRENT STATE"),
            ("LAB STAGE", "LAB STAGE"),
            ("NÍVEL 1", "LEVEL 1"),
            ("NÍVEL 2", "LEVEL 2"),
            ("NÍVEL 3", "LEVEL 3"),
            ("NÍVEL 4", "LEVEL 4"),
            ("NÍVEL 5", "LEVEL 5"),
            ("Hoje: <b>Nível 4 — Cognição Assistida</b> → Próximo marco: <b>Nível 5 — Autonomia Agêntica</b>", "Today: <b>Level 4 — Assisted Cognition</b> → Next milestone: <b>Level 5 — Agentic Autonomy</b>"),
            ("Este roadmap já está operacional dentro do pipeline <b>Bronze → Silver → Gold</b> da plataforma.", "This roadmap is already operational within the platform's <b>Bronze → Silver → Gold</b> pipeline."),
            ("“Modelos não são aceitos — são auditados.”", "“Models are not accepted — they are audited.”"),
            ("OpenCanvas <b>Pro</b>™ | <b>Don’t just build models. Trust them.</b> | v4.0 Strategic Roadmap", "OpenCanvas <b>Pro</b>™ | <b>Don’t just build models. Trust them.</b> | v4.0 Strategic Roadmap"),
            ("Plataformas atuais", "Current platforms"),
            ("Diferencial OpenCanvas", "OpenCanvas differentiator"),
            ("Mercado", "Market"),
        ]
    if lang == "fr":
        return [
            ("Cognição Assistida", "Cognition assistée"),
            ("Hoje: Level 4 — Cognição Assistida → Próximo marco: Level 5 — Agentic Autonomy", "Aujourd'hui : Niveau 4 — Cognition assistée → Prochaine étape : Niveau 5 — Autonomie agentique"),
            ("Level 4 — Cognição Assistida", "Niveau 4 — Cognition assistée"),
            ("Level 5 — Autonomia Agêntica", "Niveau 5 — Autonomie agentique"),
            ("Roadmap de Soberania Tecnológica", "Feuille de route de souveraineté technologique"),
            ("Nível 1", "Niveau 1"),
            ("Nível 2", "Niveau 2"),
            ("Nível 3", "Niveau 3"),
            ("Nível 4", "Niveau 4"),
            ("Nível 5", "Niveau 5"),
            ("Automação Simples", "Automatisation simple"),
            ("Execução de tarefas repetitivas baseada em regras estáticas.", "Exécution de tâches répétitives fondée sur des règles statiques."),
            ("Inteligência Estatística", "Intelligence statistique"),
            ("Aprendizado de padrões históricos sem noção de contexto.", "Apprentissage de motifs historiques sans notion de contexte."),
            ("IA Assistiva", "IA assistive"),
            ("Interface guiada para acelerar fluxos através da facilidade de uso.", "Interface guidée pour accélérer les flux grâce à la simplicité d'usage."),
            ("Cognição & Integridade", "Cognition et intégrité"),
            ("Interpreta contexto, integra sinais de qualidade e justifica recomendações com base em evidência estatística.", "Interprète le contexte, intègre les signaux de qualité et justifie les recommandations sur base de preuves statistiques."),
            ("Autonomia Agêntica", "Autonomie agentique"),
            ("Execução de objetivos complexos com correção dinâmica de estratégia.", "Exécution d'objectifs complexes avec correction dynamique de stratégie."),
            ("Plataformas atuais", "Plateformes actuelles"),
            ("Diferencial OpenCanvas", "Différenciant OpenCanvas"),
            ("Mercado", "Marché"),
            ("Scripts de Ingestão (Python)", "Scripts d'ingestion (Python)"),
            ("ETL Linear", "ETL linéaire"),
            ("Modelos Preditivos", "Modèles prédictifs"),
            ("Classificação & Regressão", "Classification et régression"),
            ("Copilotos de Código", "Copilotes de code"),
            ("AutoML No-Code", "AutoML sans code"),
            ("Agentes Multi-step", "Agents multi-étapes"),
            ("Auto-remediação baseada em feedback de desempenho", "Auto-remédiation basée sur le feedback de performance"),
            ("Evolução contínua orientada por contexto", "Évolution continue guidée par le contexte"),
            ("ETL Manual / Python", "ETL manuel / Python"),
            ("Jupyter Notebooks", "Notebooks Jupyter"),
            ("RPA Tradicional", "RPA traditionnelle"),
            ("AutoML Tradicional (H2O, AutoGluon)", "AutoML traditionnel (H2O, AutoGluon)"),
            ("Notebooks de Ciência de Dados", "Notebooks de science des données"),
            ("AWS SageMaker Canvas", "AWS SageMaker Canvas"),
            ("Google Vertex AI", "Google Vertex AI"),
            ("MS Azure ML Studio", "MS Azure ML Studio"),
            ("Teoria acadêmica", "Théorie académique"),
            ("Agentes Genéricos (Experimental)", "Agents génériques (expérimental)"),
            ("Pesquisa de Fronteira", "Recherche de pointe"),
            ("Foco em Missão Crítica, Governança Executiva e Transparência Total.", "Priorité à la mission critique, à la gouvernance exécutive et à la transparence totale."),
            ("Hoje:", "Aujourd'hui :"),
            ("Próximo marco:", "Prochaine étape :"),
            ("A maioria das plataformas para no nível 3.", "La plupart des plateformes s'arrêtent au niveau 3."),
            ("Roadmap de Soberania Tecnológica", "Feuille de route de souveraineté technologique"),
            ("Auditoria Gold Standard", "Audit Gold Standard"),
            ("Transparência Operacional", "Transparence Opérationnelle"),
            ("Eficiência de Recurso", "Efficacité des ressources"),
            ("Trust by Design", "Trust by Design"),
            ("White-Box ML", "White-Box ML"),
            ("Local-First Efficiency", "Efficacité local-first"),
            ("CURRENT STATE", "ÉTAT ACTUEL"),
            ("LAB STAGE", "PHASE DE LABO"),
            ("NÍVEL 1", "NIVEAU 1"),
            ("NÍVEL 2", "NIVEAU 2"),
            ("NÍVEL 3", "NIVEAU 3"),
            ("NÍVEL 4", "NIVEAU 4"),
            ("NÍVEL 5", "NIVEAU 5"),
            ("Hoje: <b>Nível 4 — Cognição Assistida</b> → Próximo marco: <b>Nível 5 — Autonomia Agêntica</b>", "Aujourd'hui : <b>Niveau 4 — Cognition assistée</b> → Prochaine étape : <b>Niveau 5 — Autonomie agentique</b>"),
            ("Este roadmap já está operacional dentro do pipeline <b>Bronze → Silver → Gold</b> da plataforma.", "Cette feuille de route est déjà opérationnelle dans le pipeline <b>Bronze → Silver → Gold</b> de la plateforme."),
            ("“Modelos não são aceitos — são auditados.”", "« Les modèles ne sont pas acceptés - ils sont audités. »"),
            ("OpenCanvas <b>Pro</b>™ | <b>Don’t just build models. Trust them.</b> | v4.0 Strategic Roadmap", "OpenCanvas <b>Pro</b>™ | <b>Ne vous contentez pas de construire des modèles. Faites-leur confiance.</b> | v4.0 Strategic Roadmap"),
            ("Plataformas atuais", "Plateformes actuelles"),
            ("Diferencial OpenCanvas", "Différenciant OpenCanvas"),
            ("Mercado", "Marché"),
        ]
    if lang == "de":
        return [
            ("Cognição Assistida", "Assistierte Kognition"),
            ("Hoje: Level 4 — Cognição Assistida → Próximo marco: Level 5 — Agentic Autonomy", "Heute: Level 4 — Assistierte Kognition → Nächster Meilenstein: Level 5 — Agentische Autonomie"),
            ("Level 4 — Cognição Assistida", "Stufe 4 — Assistierte Kognition"),
            ("Level 5 — Autonomia Agêntica", "Stufe 5 — Agentische Autonomie"),
            ("Roadmap de Soberania Tecnológica", "Technologie-Souveränitäts-Roadmap"),
            ("Nível 1", "Stufe 1"),
            ("Nível 2", "Stufe 2"),
            ("Nível 3", "Stufe 3"),
            ("Nível 4", "Stufe 4"),
            ("Nível 5", "Stufe 5"),
            ("Automação Simples", "Einfache Automatisierung"),
            ("Execução de tarefas repetitivas baseada em regras estáticas.", "Ausführung sich wiederholender Aufgaben auf Basis statischer Regeln."),
            ("Inteligência Estatística", "Statistische Intelligenz"),
            ("Aprendizado de padrões históricos sem noção de contexto.", "Lernen historischer Muster ohne Kontextgefühl."),
            ("IA Assistiva", "Assistive KI"),
            ("Interface guiada para acelerar fluxos através da facilidade de uso.", "Geführte Oberfläche, die Workflows durch einfache Bedienung beschleunigt."),
            ("Cognição & Integridade", "Kognition & Integrität"),
            ("Interpreta contexto, integra sinais de qualidade e justifica recomendações com base em evidência estatística.", "Interpretation von Kontext, Integration von Qualitätssignalen und Begründung von Empfehlungen auf Basis statistischer Evidenz."),
            ("Autonomia Agêntica", "Agentische Autonomie"),
            ("Execução de objetivos complexos com correção dinâmica de estratégia.", "Ausführung komplexer Ziele mit dynamischer Strategiekorrektur."),
            ("Plataformas atuais", "Aktuelle Plattformen"),
            ("Diferencial OpenCanvas", "OpenCanvas-Differenzierung"),
            ("Mercado", "Markt"),
            ("Scripts de Ingestão (Python)", "Ingestionsskripte (Python)"),
            ("ETL Linear", "Lineares ETL"),
            ("Modelos Preditivos", "Prädiktive Modelle"),
            ("Classificação & Regressão", "Klassifikation & Regression"),
            ("Copilotos de Código", "Code-Copiloten"),
            ("AutoML No-Code", "No-Code AutoML"),
            ("Agentes Multi-step", "Mehrstufige Agenten"),
            ("Auto-remediação baseada em feedback de desempenho", "Performance-Feedback-basierte Selbstheilung"),
            ("Evolução contínua orientada por contexto", "Kontinuierliche, kontextgetriebene Entwicklung"),
            ("ETL Manual / Python", "Manuelles ETL / Python"),
            ("Jupyter Notebooks", "Jupyter-Notebooks"),
            ("RPA Tradicional", "Traditionelles RPA"),
            ("AutoML Tradicional (H2O, AutoGluon)", "Traditionelles AutoML (H2O, AutoGluon)"),
            ("Notebooks de Ciência de Dados", "Data-Science-Notebooks"),
            ("AWS SageMaker Canvas", "AWS SageMaker Canvas"),
            ("Google Vertex AI", "Google Vertex AI"),
            ("MS Azure ML Studio", "MS Azure ML Studio"),
            ("Teoria acadêmica", "Akademische Theorie"),
            ("Agentes Genéricos (Experimental)", "Generische Agenten (experimentell)"),
            ("Pesquisa de Fronteira", "Spitzenforschung"),
            ("Foco em Missão Crítica, Governança Executiva e Transparência Total.", "Fokus auf mission-kritische Systeme, Executive Governance und volle Transparenz."),
            ("Hoje:", "Heute:"),
            ("Próximo marco:", "Nächster Meilenstein:"),
            ("A maioria das plataformas para no nível 3.", "Die meisten Plattformen hören bei Stufe 3 auf."),
            ("Roadmap de Soberania Tecnológica", "Technologie-Souveränitäts-Roadmap"),
            ("Auditoria Gold Standard", "Gold-Standard-Auditierung"),
            ("Transparência Operacional", "Operative Transparenz"),
            ("Eficiência de Recurso", "Ressourceneffizienz"),
            ("Trust by Design", "Trust by Design"),
            ("White-Box ML", "White-Box ML"),
            ("Local-First Efficiency", "Local-First-Effizienz"),
            ("CURRENT STATE", "AKTUELLER STATUS"),
            ("LAB STAGE", "LABORPHASE"),
            ("NÍVEL 1", "STUFE 1"),
            ("NÍVEL 2", "STUFE 2"),
            ("NÍVEL 3", "STUFE 3"),
            ("NÍVEL 4", "STUFE 4"),
            ("NÍVEL 5", "STUFE 5"),
            ("Hoje: <b>Nível 4 — Cognição Assistida</b> → Próximo marco: <b>Nível 5 — Autonomia Agêntica</b>", "Heute: <b>Stufe 4 — Assistierte Kognition</b> → Nächster Meilenstein: <b>Stufe 5 — Agentische Autonomie</b>"),
            ("Este roadmap já está operacional dentro do pipeline <b>Bronze → Silver → Gold</b> da plataforma.", "Diese Roadmap ist bereits innerhalb der <b>Bronze → Silver → Gold</b>-Pipeline der Plattform operational."),
            ("“Modelos não são aceitos — são auditados.”", "„Modelle werden nicht akzeptiert - sie werden auditiert.“"),
            ("OpenCanvas <b>Pro</b>™ | <b>Don’t just build models. Trust them.</b> | v4.0 Strategic Roadmap", "OpenCanvas <b>Pro</b>™ | <b>Baue nicht nur Modelle. Vertraue ihnen.</b> | v4.0 Strategic Roadmap"),
            ("Plataformas atuais", "Aktuelle Plattformen"),
            ("Diferencial OpenCanvas", "OpenCanvas-Differenzierung"),
            ("Mercado", "Markt"),
        ]
    if lang == "es":
        return [
            ("Cognição Assistida", "Cognición asistida"),
            ("Hoje: Level 4 — Cognição Assistida → Próximo marco: Level 5 — Agentic Autonomy", "Hoy: Level 4 — Cognición asistida → Próximo hito: Level 5 — Autonomía agéntica"),
            ("Level 4 — Cognição Assistida", "Level 4 — Cognición asistida"),
            ("Level 5 — Autonomia Agêntica", "Level 5 — Autonomía agéntica"),
            ("Roadmap de Soberania Tecnológica", "Hoja de ruta de soberanía tecnológica"),
            ("Nível 1", "Nivel 1"),
            ("Nível 2", "Nivel 2"),
            ("Nível 3", "Nivel 3"),
            ("Nível 4", "Nivel 4"),
            ("Nível 5", "Nivel 5"),
            ("Automação Simples", "Automatización simple"),
            ("Execução de tarefas repetitivas baseada em regras estáticas.", "Ejecución de tareas repetitivas basada en reglas estáticas."),
            ("Inteligência Estatística", "Inteligencia estadística"),
            ("Aprendizado de padrões históricos sem noção de contexto.", "Aprendizaje de patrones históricos sin noción de contexto."),
            ("IA Assistiva", "IA asistiva"),
            ("Interface guiada para acelerar fluxos através da facilidade de uso.", "Interfaz guiada para acelerar flujos a través de la facilidad de uso."),
            ("Cognição & Integridade", "Cognición e integridad"),
            ("Interpreta contexto, integra sinais de qualidade e justifica recomendações com base em evidência estatística.", "Interpreta el contexto, integra señales de calidad y justifica recomendaciones con base en evidencia estadística."),
            ("Autonomia Agêntica", "Autonomía agéntica"),
            ("Execução de objetivos complexos com correção dinâmica de estratégia.", "Ejecución de objetivos complejos con corrección dinámica de estrategia."),
            ("Plataformas atuais", "Plataformas actuales"),
            ("Diferencial OpenCanvas", "Diferencial OpenCanvas"),
            ("Mercado", "Mercado"),
            ("Scripts de Ingestão (Python)", "Scripts de ingesta (Python)"),
            ("ETL Linear", "ETL lineal"),
            ("Modelos Preditivos", "Modelos predictivos"),
            ("Classificação & Regressão", "Clasificación y regresión"),
            ("Copilotos de Código", "Copilotos de código"),
            ("AutoML No-Code", "AutoML sin código"),
            ("Agentes Multi-step", "Agentes multinivel"),
            ("Auto-remediação baseada em feedback de desempenho", "Auto-remediación basada en feedback de rendimiento"),
            ("Evolução contínua orientada por contexto", "Evolución continua guiada por contexto"),
            ("ETL Manual / Python", "ETL manual / Python"),
            ("Jupyter Notebooks", "Cuadernos de Jupyter"),
            ("RPA Tradicional", "RPA tradicional"),
            ("AutoML Tradicional (H2O, AutoGluon)", "AutoML tradicional (H2O, AutoGluon)"),
            ("Notebooks de Ciência de Dados", "Cuadernos de ciencia de datos"),
            ("AWS SageMaker Canvas", "AWS SageMaker Canvas"),
            ("Google Vertex AI", "Google Vertex AI"),
            ("MS Azure ML Studio", "MS Azure ML Studio"),
            ("Teoria acadêmica", "Teoría académica"),
            ("Agentes Genéricos (Experimental)", "Agentes genéricos (experimental)"),
            ("Pesquisa de Fronteira", "Investigación de frontera"),
            ("Foco em Missão Crítica, Governança Executiva e Transparência Total.", "Enfoque en misión crítica, gobernanza ejecutiva y transparencia total."),
            ("Hoje:", "Hoy:"),
            ("Próximo marco:", "Próximo hito:"),
            ("A maioria das plataformas para no nível 3.", "La mayoría de las plataformas se detienen en el nivel 3."),
            ("Roadmap de Soberania Tecnológica", "Hoja de ruta de soberanía tecnológica"),
            ("Auditoria Gold Standard", "Auditoría Gold Standard"),
            ("Transparência Operacional", "Transparencia Operativa"),
            ("Eficiência de Recurso", "Eficiencia de Recursos"),
            ("Trust by Design", "Trust by Design"),
            ("White-Box ML", "White-Box ML"),
            ("Local-First Efficiency", "Local-First Efficiency"),
            ("CURRENT STATE", "ESTADO ACTUAL"),
            ("LAB STAGE", "FASE DE LABORATORIO"),
            ("NÍVEL 1", "NIVEL 1"),
            ("NÍVEL 2", "NIVEL 2"),
            ("NÍVEL 3", "NIVEL 3"),
            ("NÍVEL 4", "NIVEL 4"),
            ("NÍVEL 5", "NIVEL 5"),
            ("Hoje: <b>Nível 4 — Cognição Assistida</b> → Próximo marco: <b>Nível 5 — Autonomia Agêntica</b>", "Hoy: <b>Nivel 4 — Cognición asistida</b> → Próximo hito: <b>Nivel 5 — Autonomía agéntica</b>"),
            ("Este roadmap já está operacional dentro do pipeline <b>Bronze → Silver → Gold</b> da plataforma.", "Esta hoja de ruta ya está operativa dentro del pipeline <b>Bronze → Silver → Gold</b> de la plataforma."),
            ("“Modelos não são aceitos — são auditados.”", "“Los modelos no se aceptan — se auditan.”"),
            ("OpenCanvas <b>Pro</b>™ | <b>Don’t just build models. Trust them.</b> | v4.0 Strategic Roadmap", "OpenCanvas <b>Pro</b>™ | <b>No solo construyas modelos. Confía en ellos.</b> | v4.0 Strategic Roadmap"),
            ("Plataformas atuais", "Plataformas actuales"),
            ("Diferencial OpenCanvas", "Diferencial OpenCanvas"),
            ("Mercado", "Mercado"),
        ]
    if lang == "hi":
        return [
            ("Roadmap de Soberania Tecnológica", "प्रौद्योगिक संप्रभुता रोडमैप"),
            ("Nível 1", "स्तर 1"),
            ("Nível 2", "स्तर 2"),
            ("Nível 3", "स्तर 3"),
            ("Nível 4", "स्तर 4"),
            ("Nível 5", "स्तर 5"),
            ("Automação Simples", "सरल स्वचालन"),
            ("Execução de tarefas repetitivas baseada em regras estáticas.", "स्थिर नियमों पर आधारित दोहराए जाने वाले कार्यों का निष्पादन।"),
            ("Inteligência Estatística", "सांख्यिकीय बुद्धिमत्ता"),
            ("Aprendizado de padrões históricos sem noção de contexto.", "संदर्भ की समझ के बिना ऐतिहासिक पैटर्नों से सीखना।"),
            ("IA Assistiva", "सहायक AI"),
            ("Interface guiada para acelerar fluxos através da facilidade de uso.", "प्रयोग में आसानी के माध्यम से वर्कफ़्लो तेज़ करने वाला निर्देशित इंटरफ़ेस।"),
            ("Cognição & Integridade", "संज्ञान और अखंडता"),
            ("Interpreta contexto, integra sinais de qualidade e justifica recomendações com base em evidência estatística.", "संदर्भ की व्याख्या करता है, गुणवत्ता संकेतों को जोड़ता है और सांख्यिकीय साक्ष्य के आधार पर सिफ़ारिशों को उचित ठहराता है।"),
            ("Autonomia Agêntica", "एजेंटिक स्वायत्तता"),
            ("Execução de objetivos complexos com correção dinâmica de estratégia.", "गतिशील रणनीति सुधार के साथ जटिल लक्ष्यों का निष्पादन।"),
            ("Plataformas atuais", "वर्तमान प्लेटफ़ॉर्म"),
            ("Diferencial OpenCanvas", "OpenCanvas का अंतर"),
            ("Mercado", "बाज़ार"),
            ("Scripts de Ingestão (Python)", "इनजेशन स्क्रिप्ट्स (Python)"),
            ("ETL Linear", "रेखीय ETL"),
            ("Modelos Preditivos", "पूर्वानुमान मॉडल"),
            ("Classificação & Regressão", "वर्गीकरण और रिग्रेशन"),
            ("Copilotos de Código", "कोड कोपायलट"),
            ("AutoML No-Code", "नो-कोड AutoML"),
            ("Agentes Multi-step", "बहु-चरणीय एजेंट"),
            ("Auto-remediação baseada em feedback de desempenho", "प्रदर्शन फ़ीडबैक-आधारित स्व-उपचार"),
            ("Evolução contínua orientada por contexto", "संदर्भ-आधारित सतत विकास"),
            ("ETL Manual / Python", "मैनुअल ETL / Python"),
            ("Jupyter Notebooks", "Jupyter नोटबुक"),
            ("RPA Tradicional", "पारंपरिक RPA"),
            ("AutoML Tradicional (H2O, AutoGluon)", "पारंपरिक AutoML (H2O, AutoGluon)"),
            ("Notebooks de Ciência de Dados", "डेटा साइंस नोटबुक"),
            ("AWS SageMaker Canvas", "AWS SageMaker Canvas"),
            ("Google Vertex AI", "Google Vertex AI"),
            ("MS Azure ML Studio", "MS Azure ML Studio"),
            ("Teoria acadêmica", "शैक्षणिक सिद्धांत"),
            ("Agentes Genéricos (Experimental)", "सामान्य एजेंट (प्रायोगिक)"),
            ("Pesquisa de Fronteira", "अत्याधुनिक अनुसंधान"),
            ("Foco em Missão Crítica, Governança Executiva e Transparência Total.", "मिशन-क्रिटिकल उपयोग, कार्यकारी शासन और पूर्ण पारदर्शिता पर ध्यान।"),
            ("Hoje: <b>Nível 4 — Cognição Assistida</b> → Próximo marco: <b>Nível 5 — Autonomia Agêntica</b>", "आज: <b>स्तर 4 — सहायक संज्ञान</b> → अगला चरण: <b>स्तर 5 — एजेंटिक स्वायत्तता</b>"),
            ("Hoje: Nível 4 — Cognição Assistida → Próximo marco: Nível 5 — Autonomia Agêntica", "आज: स्तर 4 — सहायक संज्ञान → अगला चरण: स्तर 5 — एजेंटिक स्वायत्तता"),
            ("Today: Level 4 — Cognição Assistida → Next milestone: Level 5 — Agentic Autonomy", "आज: स्तर 4 — सहायक संज्ञान → अगला चरण: स्तर 5 — एजेंटिक स्वायत्तता"),
            ("Cognição Assistida", "सहायक संज्ञान"),
            ("Today:", "आज:"),
            ("Próximo marco:", "अगला चरण:"),
            ("A maioria das plataformas para no nível 3.", "अधिकांश प्लेटफ़ॉर्म स्तर 3 तक ही सीमित रहती हैं।"),
            ("A maioria das plataformas para no nível 3", "अधिकांश प्लेटफ़ॉर्म स्तर 3 तक ही सीमित रहती हैं"),
            ("Cognitive Navigation (E.M.I.L.I.A.™)", "संज्ञानात्मक नेविगेशन (E.M.I.L.I.A.™)"),
            ("Knowledge Graphs (Alexandr.I.A.)", "ज्ञान-ग्राफ़ (Alexandr.I.A.)"),
            ("Scientific Integrity Shield", "वैज्ञानिक अखंडता शील्ड"),
            ("Diagnóstico Proativo / White Box ML", "प्रोएक्टिव डायग्नोसिस / White-Box ML"),
            ("Auditoria Gold Standard", "गोल्ड-स्टैंडर्ड ऑडिटिंग"),
            ("Sovereignty & Model Export", "संप्रभुता और मॉडल निर्यात"),
            ("100% No Code", "100% नो-कोड"),
            ("Nível 4 — Cognição Assistida", "स्तर 4 — सहायक संज्ञान"),
            ("Nível 5 — Autonomia Agêntica", "स्तर 5 — एजेंटिक स्वायत्तता"),
            ("Este roadmap já está operacional dentro do pipeline <b>Bronze → Silver → Gold</b> da plataforma.", "यह रोडमैप प्लेटफ़ॉर्म की <b>Bronze → Silver → Gold</b> पाइपलाइन में पहले से ही कार्यरत है।"),
            ("Este roadmap já está operacional dentro do pipeline Bronze → Silver → Gold da plataforma.", "यह रोडमैप प्लेटफ़ॉर्म की Bronze → Silver → Gold पाइपलाइन में पहले से ही कार्यरत है।"),
            ("“Modelos não são aceitos — são auditados.”", "“मॉडल स्वीकार नहीं किए जाते — उनका ऑडिट किया जाता है।”"),
            ("OpenCanvas <b>Pro</b>™ | <b>Don’t just build models. Trust them.</b> | v4.0 Strategic Roadmap", "OpenCanvas <b>Pro</b>™ | <b>केवल मॉडल न बनाइए। उन पर भरोसा कीजिए।</b> | v4.0 Strategic Roadmap"),
            ("Current State", "वर्तमान स्थिति"),
            ("Lab Stage", "प्रयोगशाला चरण"),
        ]
    return []


def apply_replacements(text: str, replacements: list[tuple[str, str]]) -> str:
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def load_embeddable_html(path: str) -> str:
    if not os.path.exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def make_snis_logo_clickable(html_content: str) -> str:
    pattern = re.compile(
        r"(<style>#opencanvas-map-logo svg\{width:100%;height:100%;display:block;\}</style>)"
        r"(<div id='opencanvas-map-logo'[^>]*>.*?</svg></div>)",
        re.DOTALL,
    )
    replacement = (
        r"\1"
        r"<a href='https://www.opencanvaspro.com' target='_blank' rel='noopener noreferrer' "
        r"aria-label='OpenCanvas Pro' "
        r"style='position: fixed; top: 16px; right: 24px; z-index: 10000; display:block; "
        r"width: 138px; height: 138px; cursor:pointer; text-decoration:none;'>"
        r"\2"
        r"</a>"
    )
    return pattern.sub(replacement, html_content, count=1)


def get_query_param_str(name: str, default: str = "") -> str:
    value = st.query_params.get(name, default)
    return value if isinstance(value, str) else default


def load_maturity_section(lang: str) -> str:
    html = load_embeddable_html(MATURITY_HTML_PATH)
    if not html:
        return ""

    html = html.replace(
        "</head>",
        dedent(
            """
            <style>
                html, body {
                    overflow: hidden !important;
                }
            </style>
            </head>
            """
        ).strip(),
    )

    replacements = {
        "../assets/app/horizontal_logo_branco_transparencia.svg": file_to_data_uri(LOGO_PATH) if os.path.exists(LOGO_PATH) else "",
        "../assets/app/emilia_logo.png": file_to_data_uri(EMILIA_PATH) if os.path.exists(EMILIA_PATH) else "",
        "padding: 40px 20px;": "padding: 6px 0 0 0;",
        "justify-content: center;": "justify-content: flex-start;",
        "margin-top: 40px;": "margin-top: 0;",
        "margin-bottom: 20px;": "margin-bottom: 10px;",
    }

    for old, new in replacements.items():
        if new:
            html = html.replace(old, new)

    html = html.replace(
        '<img src="../assets/app/horizontal_logo_branco_transparencia.svg" class="logo">',
        ""
    )

    html = apply_replacements(html, maturity_replacements(lang))

    return html


ROADMAP_LEVELS: list[RoadmapItem] = [
    {
        "level": "Nível 1",
        "title": "Automação Simples",
        "desc": "Execução de tarefas repetitivas baseada em regras estáticas.",
        "features": [
            "Scripts de Ingestão (Python)",
            "ETL Linear",
        ],
        "footer_label": "Plataformas atuais",
        "footer_items": [
            "ETL Manual / Python",
            "Jupyter Notebooks",
            "RPA Tradicional",
        ],
    },
    {
        "level": "Nível 2",
        "title": "Inteligência Estatística",
        "desc": "Aprendizado de padrões históricos sem noção de contexto.",
        "features": [
            "Modelos Preditivos",
            "Classificação & Regressão",
        ],
        "footer_label": "Plataformas atuais",
        "footer_items": [
            "AutoML Tradicional (H2O, AutoGluon)",
            "Notebooks de Ciência de Dados",
        ],
    },
    {
        "level": "Nível 3",
        "title": "IA Assistiva",
        "desc": "Interface guiada para acelerar fluxos através da facilidade de uso.",
        "features": [
            "Copilotos de Código",
            "AutoML No-Code",
        ],
        "footer_label": "Plataformas atuais",
        "footer_items": [
            "AWS SageMaker Canvas",
            "Google Vertex AI",
            "MS Azure ML Studio",
        ],
    },
    {
        "level": "Nível 4",
        "title": "Cognição & Integridade",
        "desc": "Interpreta contexto, integra sinais de qualidade e justifica recomendações com base em evidência estatística.",
        "features": [
            "<b>Cognitive Navigation (E.M.I.L.I.A.™)</b>",
            "<b>Knowledge Graphs (Alexandr.I.A.)</b>",
            "Scientific Integrity Shield",
            "Diagnóstico Proativo / White Box ML",
            "Auditoria Gold Standard",
            "Sovereignty & Model Export",
            "100% No Code",
        ],
        "footer_label": "Diferencial OpenCanvas",
        "footer_items": [
            "Foco em Missão Crítica, Governança Executiva e Transparência Total.",
        ],
        "status": "CURRENT STATE",
        "active": True,
    },
    {
        "level": "Nível 5",
        "title": "Autonomia Agêntica",
        "desc": "Execução de objetivos complexos com correção dinâmica de estratégia.",
        "features": [
            "Agentes Multi-step",
            "Auto-remediação baseada em feedback de desempenho",
            "Evolução contínua orientada por contexto",
        ],
        "footer_label": "Mercado",
        "footer_items": [
            "Teoria acadêmica",
            "Agentes Genéricos (Experimental)",
            "Pesquisa de Fronteira",
        ],
        "status": "LAB STAGE",
        "future": True,
    },
]


def roadmap_t(lang: str, text: str) -> str:
    if lang == "pt":
        return text
    for old, new in maturity_replacements(lang):
        if old == text:
            return new
    return text


def roadmap_t_html(lang: str, text: str) -> str:
    if lang == "pt":
        return text
    return apply_replacements(text, maturity_replacements(lang))


def render_native_roadmap(
    lang: str,
    title_text: str | None = None,
    subtitle_text: str | None = None,
    items: list[RoadmapItem] | None = None,
    cols: int = 5,
    show_footer: bool = True,
) -> str:
    roadmap_items = items if items is not None else ROADMAP_LEVELS
    roadmap_title = title_text if title_text is not None else roadmap_t(lang, "Roadmap de Soberania Tecnológica")
    roadmap_subtitle = f'<div class="section-subtitle" style="text-align:center; margin: -2.8rem auto 3.8rem auto;">{html_lib.escape(subtitle_text)}</div>' if subtitle_text else ""
    cards_html = []
    for item in roadmap_items:
        level = item.get("level", "")
        title = item.get("title", "")
        desc = item.get("desc", "")
        status = item.get("status", "")
        features_list = item.get("features", [])
        footer_label = item.get("footer_label", "")

        card_classes = "roadmap-card"
        if item.get("active"):
            card_classes += " active"

        badge_html = ""
        price_html = ""
        
        if status:
            if show_footer:
                badge_class = "roadmap-status-badge"
                if item.get("future"):
                    badge_class += " future"
                badge_html = f'<div class="{badge_class}">{html_lib.escape(roadmap_t(lang, status))}</div>'
            else:
                price_html = f'<div class="roadmap-card-price">{html_lib.escape(roadmap_t(lang, status))}</div>'

        features = []
        for feature in features_list:
            translated_feature = roadmap_t_html(lang, feature)
            features.append(f"<li>{translated_feature}</li>")

        footer_els = []
        for fi in item.get("footer_items", []):
            if isinstance(fi, dict):
                label = roadmap_t(lang, fi.get("label", ""))
                link = fi.get("link", "#")
                if not show_footer:
                    footer_els.append(f'<a href="{link}" class="map-open-link" style="width:100%; margin-top:10px; text-decoration:none; display:flex;">{html_lib.escape(label)}</a>')
                else:
                    footer_els.append(f'<div class="roadmap-market-content">{html_lib.escape(label)}</div>')
            else:
                label = roadmap_t(lang, fi)
                if not show_footer:
                    footer_els.append(f'<div class="map-open-link" style="width:100%; margin-top:10px; cursor:default;">{html_lib.escape(label)}</div>')
                else:
                    footer_els.append(f'<div class="roadmap-market-content">{html_lib.escape(label)}</div>')
        footer_items = "".join(footer_els)

        card_item = (
            f'<div class="{card_classes}">'
            f'{badge_html}'
            f'<div class="roadmap-level-tag">{html_lib.escape(roadmap_t(lang, level))}</div>'
            f'<div class="roadmap-card-title">{html_lib.escape(roadmap_t(lang, title))}</div>'
            f'{price_html}'
            f'<div class="roadmap-card-desc">{html_lib.escape(roadmap_t(lang, desc))}</div>'
            f'<ul class="roadmap-features">{"".join(features)}</ul>'
            f'<div class="roadmap-card-footer">'
            f'<div class="roadmap-market-divider">{html_lib.escape(roadmap_t(lang, footer_label))}</div>'
            f'{footer_items}'
            f'</div>'
            f'</div>'
        )
        cards_html.append(card_item)

    footer_html = ""
    if show_footer:
        trajectory = roadmap_t_html(
            lang,
            "Hoje: <b>Nível 4 — Cognição Assistida</b> → Próximo marco: <b>Nível 5 — Autonomia Agêntica</b>",
        )
        pipeline_note = roadmap_t_html(
            lang,
            "Este roadmap já está operacional dentro do pipeline <b>Bronze → Silver → Gold</b> da plataforma.",
        )
        quote = roadmap_t_html(lang, "“Modelos não são aceitos — são auditados.”")
        footer_note = roadmap_t_html(
            lang,
            "OpenCanvas <b>Pro</b>™ | <b>Don’t just build models. Trust them.</b> | v4.0 Strategic Roadmap",
        )
        emilia_src = file_to_data_uri(EMILIA_PATH) if os.path.exists(EMILIA_PATH) else ""
        emilia_html = (
            f'<div class="roadmap-emilia-row"><div class="roadmap-emilia-badge">'
            f'<img src="{emilia_src}" alt="E.M.I.L.I.A. - Engine for Machine Learning Integrity and Auditing">'
            f'</div></div>'
            if emilia_src else ""
        )
        footer_html = (
            f'<div class="roadmap-native-footer">'
            f'<div class="roadmap-market-break">{html_lib.escape(roadmap_t(lang, "A maioria das plataformas para no nível 3."))}</div>'
            f'<div class="roadmap-trajectory">{trajectory}</div>'
            f'<div class="roadmap-pipeline-note">{pipeline_note}</div>'
            f'<blockquote class="roadmap-highlight-quote">{quote}</blockquote>'
            f'{emilia_html}'
            f'<div class="roadmap-footer-note">{footer_note}</div>'
            f'</div>'
        )

    return (
        f'<div class="roadmap-native" style="--roadmap-cols: {cols};">'
        f'<div class="ocp-section-rule"></div>'
        f'<div class="roadmap-native-header">{html_lib.escape(roadmap_title)}</div>'
        f'{roadmap_subtitle}'
        f'<div class="roadmap-native-grid">{"".join(cards_html)}</div>'
        f'{footer_html}'
        f'</div>'
    )


def render_responsive_roadmap_iframe(html_content: str, frame_id: str = "ocp-roadmap-frame") -> str:
    embedded_script = dedent(
        f"""
        <script>
        (function() {{
            function publishHeight() {{
                const body = document.body;
                const doc = document.documentElement;
                const height = Math.max(
                    body ? body.scrollHeight : 0,
                    body ? body.offsetHeight : 0,
                    doc ? doc.scrollHeight : 0,
                    doc ? doc.offsetHeight : 0
                );
                parent.postMessage({{
                    type: "ocp-roadmap-height",
                    frameId: "{frame_id}",
                    height: height
                }}, "*");
            }}

            window.addEventListener("load", function() {{
                publishHeight();
                setTimeout(publishHeight, 200);
                setTimeout(publishHeight, 800);
            }});

            window.addEventListener("resize", publishHeight);

            if (document.fonts && document.fonts.ready) {{
                document.fonts.ready.then(function() {{
                    publishHeight();
                    setTimeout(publishHeight, 300);
                }});
            }}

            const observer = new ResizeObserver(function() {{
                publishHeight();
            }});
            observer.observe(document.documentElement);
            observer.observe(document.body);
        }})();
        </script>
        """
    ).strip()

    if "</body>" in html_content:
        html_content = html_content.replace("</body>", embedded_script + "\n</body>")
    else:
        html_content = html_content + embedded_script

    escaped_srcdoc = html_lib.escape(html_content, quote=True)

    return dedent(
        f"""
        <div class="ocp-roadmap-embed">
          <iframe
            id="{frame_id}"
            title="OpenCanvas Pro Roadmap"
            srcdoc="{escaped_srcdoc}"
            loading="lazy"
          ></iframe>
        </div>
        <script>
        (function() {{
            const frameId = "{frame_id}";
            const iframe = document.getElementById(frameId);
            if (!iframe) return;

            function fallbackHeight() {{
                const width = window.innerWidth;
                if (width <= 480) return 5000;
                if (width <= 700) return 4100;
                if (width <= 900) return 3100;
                if (width <= 1100) return 2200;
                return 1180;
            }}

            function applyHeight(height) {{
                const resolved = Math.max(Number(height) || 0, fallbackHeight());
                iframe.style.height = resolved + "px";
            }}

            window.addEventListener("message", function(event) {{
                const data = event.data || {{}};
                if (data.type === "ocp-roadmap-height" && data.frameId === frameId) {{
                    applyHeight(data.height);
                }}
            }});

            iframe.addEventListener("load", function() {{
                applyHeight(fallbackHeight());
                try {{
                    const doc = iframe.contentWindow && iframe.contentWindow.document;
                    if (doc) {{
                        const measured = Math.max(
                            doc.body ? doc.body.scrollHeight : 0,
                            doc.documentElement ? doc.documentElement.scrollHeight : 0
                        );
                        applyHeight(measured);
                    }}
                }} catch (e) {{
                    applyHeight(fallbackHeight());
                }}
            }});

            applyHeight(fallbackHeight());
            window.addEventListener("resize", function() {{
                applyHeight(fallbackHeight());
            }});
        }})();
        </script>
        """
    ).strip()


def build_view_url(view: str | None = None, lang: str | None = None) -> str:
    params = []
    if view:
        params.append(f"view={view}")
    if lang:
        params.append(f"lang={lang}")
    return "/?" + "&".join(params) if params else "/"


def social_icon(name: str) -> str:
    icons: Final[dict[str, str]] = {
        "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.94 8.5H3.56V19h3.38zM5.25 3A1.97 1.97 0 1 0 5.3 6.94 1.97 1.97 0 0 0 5.25 3M20.44 11.12c0-2.93-1.56-4.3-3.65-4.3a3.16 3.16 0 0 0-2.87 1.58h-.05V8.5H10.5c.04.62 0 10.5 0 10.5h3.38v-5.86c0-.31.02-.62.12-.84.25-.62.82-1.27 1.77-1.27 1.25 0 1.75.96 1.75 2.37V19H21z"/></svg>',
        "x": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.9 2H22l-6.77 7.74L23.2 22h-6.26l-4.9-7.39L5.58 22H2.47l7.24-8.27L1.8 2h6.42l4.43 6.75zm-1.1 18h1.73L7.3 3.9H5.45z"/></svg>',
        "github": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5a12 12 0 0 0-3.79 23.39c.6.11.82-.26.82-.58v-2.03c-3.34.73-4.04-1.42-4.04-1.42-.55-1.38-1.33-1.75-1.33-1.75-1.09-.74.08-.72.08-.72 1.2.08 1.84 1.24 1.84 1.24 1.08 1.83 2.82 1.3 3.5.99.11-.78.42-1.3.76-1.6-2.67-.31-5.47-1.33-5.47-5.92 0-1.31.47-2.38 1.24-3.22-.12-.31-.54-1.56.12-3.26 0 0 1.01-.32 3.3 1.23A11.5 11.5 0 0 1 12 6.32c1.02 0 2.05.14 3.01.41 2.29-1.55 3.29-1.23 3.29-1.23.67 1.7.25 2.95.13 3.26.77.84 1.24 1.91 1.24 3.22 0 4.6-2.8 5.6-5.48 5.91.43.37.82 1.1.82 2.22v3.2c0 .32.22.7.83.58A12 12 0 0 0 12 .5"/></svg>',
        "youtube": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.4 3.5 12 3.5 12 3.5s-7.4 0-9.4.6A3 3 0 0 0 .5 6.2 31.5 31.5 0 0 0 0 12a31.5 31.5 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c2 .6 9.4.6 9.4.6s7.4 0 9.4-.6a3 3 0 0 0 2.1-2.1A31.5 31.5 0 0 0 24 12a31.5 31.5 0 0 0-.5-5.8ZM9.6 15.6V8.4l6.3 3.6-6.3 3.6Z"/></svg>',
    }
    return icons[name]


def send_waitlist_email(user_email: str, lang: str = "pt") -> tuple[bool, str]:
    try:
        host = st.secrets["EMAIL_HOST"]
        port = int(st.secrets["EMAIL_PORT"])
        username = st.secrets["EMAIL_USERNAME"]
        password = st.secrets["EMAIL_PASSWORD"]
        waitlist_to = st.secrets.get("WAITLIST_TO", "opencanvaspro@gmail.com")

        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = waitlist_to
        msg["Subject"] = tr(lang, "email_subject")

        body = f"""
{tr(lang, "email_body")}

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
def inject_seo_tags(lang: str = "pt"):
    seo_script = dedent(
        """
        <script>
        const metaTags = [
          { name: "description", content: "__DESCRIPTION__" },
          { name: "keywords", content: "__KEYWORDS__" },
          { name: "author", content: "OpenCanvas Pro" },
          { name: "robots", content: "index,follow" },
          { name: "theme-color", content: "#0D0D0D" },
          { property: "og:type", content: "website" },
          { property: "og:site_name", content: "OpenCanvas Pro" },
          { property: "og:url", content: "https://opencanvaspro.com/" },
          { property: "og:title", content: "__TITLE__" },
          { property: "og:description", content: "__OG_DESCRIPTION__" },
          { property: "og:image", content: "https://opencanvaspro.com/assets/integrity_shield.png" },
          { property: "twitter:card", content: "summary_large_image" },
          { property: "twitter:url", content: "https://opencanvaspro.com/" },
          { property: "twitter:title", content: "__TITLE__" },
          { property: "twitter:description", content: "__TWITTER_DESCRIPTION__" },
          { property: "twitter:image", content: "https://opencanvaspro.com/assets/integrity_shield.png" }
        ];

        document.title = "__DOCUMENT_TITLE__";
        const canonicalHref = "https://opencanvaspro.com/";

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

        let canonical = parent.document.head.querySelector('link[rel="canonical"]');
        if (!canonical) {
          canonical = parent.document.createElement("link");
          canonical.setAttribute("rel", "canonical");
          parent.document.head.appendChild(canonical);
        }
        canonical.setAttribute("href", canonicalHref);
        </script>
        """
    ).strip()
    seo_script = seo_script.replace("__DESCRIPTION__", tr(lang, "page_description"))
    seo_script = seo_script.replace("__KEYWORDS__", {
        "pt": "AutoML, Machine Learning, Integridade Científica, Data Science, AI, OpenCanvas",
        "en": "AutoML, Machine Learning, Scientific Integrity, Data Science, AI, OpenCanvas",
        "es": "AutoML, Machine Learning, Integridad Científica, Ciencia de Datos, IA, OpenCanvas",
    }.get(lang, "AutoML, Machine Learning"))
    seo_script = seo_script.replace("__TITLE__", tr(lang, "page_title"))
    seo_script = seo_script.replace("__OG_DESCRIPTION__", {
        "pt": "Garanta a integridade científica dos seus modelos de IA com a plataforma Cognitive AutoML.",
        "en": "Ensure the scientific integrity of your AI models with the Cognitive AutoML platform.",
        "es": "Asegura la integridad científica de tus modelos de IA con la plataforma Cognitive AutoMLOps.",
    }.get(lang, tr(lang, "page_title")))
    seo_script = seo_script.replace("__TWITTER_DESCRIPTION__", {
        "pt": "Trusted Platform for Scientific Integrity em Machine Learning.",
        "en": "Trusted Platform for Scientific Integrity in Machine Learning.",
        "es": "Plataforma de confianza para la integridad científica en Machine Learning.",
    }.get(lang, tr(lang, "page_title")))
    seo_script = seo_script.replace("__DOCUMENT_TITLE__", {
        "pt": "OpenCanvas Pro | Cognitive AutoMLOps Trusted Platform",
        "en": "OpenCanvas Pro | Cognitive AutoMLOps Trusted Platform",
        "es": "OpenCanvas Pro | Plataforma de Confianza Cognitive AutoMLOps",
    }.get(lang, tr(lang, "page_title")))
    st.html(seo_script, unsafe_allow_javascript=True)

# =========================================================

logo_uri = file_to_data_uri(LOGO_PATH) if os.path.exists(LOGO_PATH) else ""
shield_uri = file_to_data_uri(SHIELD_PATH) if os.path.exists(SHIELD_PATH) else ""
neo4j_uri = file_to_data_uri(NEO4J_PATH) if os.path.exists(NEO4J_PATH) else ""
desafix_uri = file_to_data_uri(DESAFIX_BANNER_PATH) if os.path.exists(DESAFIX_BANNER_PATH) else ""

requested_lang = get_query_param_str("lang", "pt")
if requested_lang not in LANG_LABELS:
    requested_lang = "pt"
map_only_view = get_query_param_str("view") == "snis-map"

if "ui_lang" not in st.session_state:
    st.session_state.ui_lang = requested_lang
elif map_only_view:
    st.session_state.ui_lang = requested_lang

def format_lang_label(code: str) -> str:
    return LANG_LABELS.get(code, code)


if not map_only_view:
    lang_bar_left, lang_bar_right = st.columns([9, 1], vertical_alignment="center")
    with lang_bar_right:
        st.selectbox(
            "Language",
            options=list(LANG_LABELS.keys()),
            format_func=format_lang_label,
            key="ui_lang",
            label_visibility="collapsed",
        )

lang = cast(str, st.session_state.ui_lang)
inject_seo_tags(lang)
snis_map_html = make_snis_logo_clickable(load_embeddable_html(SNIS_MAP_HTML_PATH))
main_view_url = build_view_url(lang=lang)
map_view_url = build_view_url(view="snis-map", lang=lang)

st.markdown(
    """
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0,0");
        @import url("https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap");
        @import url("https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700;800&display=swap");

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
            padding-top: 0.9rem !important;
            padding-bottom: 4.5rem !important;
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            max-width: 1360px !important;
        }

        h1, h2, h3, h4, h5, h6, p, li, span, label, div {
            font-family: "Lato", "Noto Sans Devanagari", sans-serif !important;
        }

        .material-symbols-outlined {
            font-family: "Material Symbols Outlined" !important;
        }

        .ocp-section-rule {
            border-top: 1px solid rgba(255,255,255,0.06);
            margin: 4.5rem 0 4.5rem 0;
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
            padding-top: 0.25rem;
            padding-bottom: 1.15rem;
            max-width: none;
            width: 100%;
            margin: 0 auto;
        }

        .hero-title-row {
            display: grid;
            grid-template-columns: 132px 1fr;
            align-items: center;
            width: 100%;
            column-gap: 1rem;
            margin-bottom: 1.15rem;
        }

        .hero-title-logo {
            width: 124px;
            height: auto;
            flex: 0 0 124px;
            display: block;
            justify-self: start;
        }

        .hero-title-spacer {
            width: 124px;
            flex: 0 0 124px;
            opacity: 0;
            justify-self: end;
        }

        .hero-title {
            text-align: left;
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--ocp-white);
            margin: 0;
            letter-spacing: -0.015em;
            line-height: 1.12;
        }

        .hero-title .accent {
            color: var(--ocp-orange) !important;
        }

        .hero-title .white {
            color: var(--ocp-white) !important;
        }

        .hero-subcopy {
            text-align: center;
            color: var(--ocp-white) !important;
            font-size: 3.3rem;
            max-width: 940px;
            margin: 0 auto;
            line-height: 1.2;
            font-weight: 900;
            letter-spacing: -0.03em;
            word-break: normal;
            overflow-wrap: normal;
            hyphens: none;
        }

        .hero-highlight {
            text-align: center;
            color: var(--ocp-soft) !important;
            font-size: 1.1rem;
            font-weight: 600;
            letter-spacing: 0;
            line-height: 1.62;
            margin: 1.2rem auto 0 auto;
            max-width: 820px;
        }

        .hero-pipeline-line {
            text-align: center;
            color: var(--ocp-orange) !important;
            font-size: 1.02rem;
            font-weight: 700;
            line-height: 1.7;
            max-width: 860px;
            margin: 1.15rem auto 0 auto;
        }

        .section-title {
            color: var(--ocp-white) !important;
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 0.55rem;
            line-height: 1.18;
        }

        .section-title .accent {
            color: var(--ocp-orange) !important;
        }

        .section-subtitle {
            color: var(--ocp-soft) !important;
            font-size: 1.03rem;
            line-height: 1.7;
            margin-bottom: 1.4rem;
            max-width: 1120px;
        }

        .feature-intro {
            margin-bottom: 1.15rem;
            text-align: left;
            width: 100%;
        }

        .feature-intro .section-subtitle.feature-subtitle-wide {
            max-width: none;
            width: 100%;
        }

        .content-box {
            background: linear-gradient(180deg, rgba(22,22,22,0.98) 0%, rgba(18,18,18,0.98) 100%);
            padding: 28px;
            border-radius: 20px;
            border: 1px solid var(--ocp-border);
            box-shadow: 0 0 0 1px rgba(255,255,255,0.02) inset;
            height: 100%;
        }

        .content-box h4 {
            color: var(--ocp-white) !important;
            margin-top: 0;
            margin-bottom: 0.5rem;
            font-size: 1.35rem;
            font-weight: 800;
            line-height: 1.2;
        }

        .content-box p,
        .content-box span,
        .content-box li,
        .pillar-body {
            color: var(--ocp-muted) !important;
            opacity: 1 !important;
            line-height: 1.7;
            font-size: 1rem;
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

        .section-shell-soft {
            background: linear-gradient(180deg, rgba(18,18,18,0.84) 0%, rgba(14,14,14,0.84) 100%);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 20px 48px rgba(0,0,0,0.2);
        }

        .capability-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(220px, 1fr));
            gap: 24px;
        }

        .capability-card {
            background: linear-gradient(180deg, rgba(24,24,24,0.98) 0%, rgba(17,17,17,0.98) 100%);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 20px;
            padding: 28px;
            min-height: 245px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.18);
            transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
            word-break: normal;
            overflow-wrap: normal;
            hyphens: none;
        }

        .capability-topline {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            margin-bottom: 0.95rem;
        }

        .capability-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255,107,0,0.34);
            box-shadow: 0 18px 34px rgba(255,107,0,0.08), 0 0 0 1px rgba(255,107,0,0.05) inset;
        }

        .capability-index {
            color: var(--ocp-orange) !important;
            font-size: 0.88rem;
            font-weight: 800;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            line-height: 1;
        }

        .capability-icon {
            width: 22px;
            height: 22px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: var(--ocp-orange) !important;
            font-family: "Material Symbols Outlined" !important;
            font-weight: 400;
            font-style: normal;
            font-size: 22px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            white-space: nowrap;
            direction: ltr;
            font-variation-settings: "FILL" 0, "wght" 400, "GRAD" 0, "opsz" 24;
            -webkit-font-smoothing: antialiased;
            text-rendering: optimizeLegibility;
            -moz-osx-font-smoothing: grayscale;
        }

        .capability-title {
            color: var(--ocp-white) !important;
            font-size: 1.35rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 0.8rem;
            word-break: normal;
            overflow-wrap: normal;
            hyphens: none;
        }

        .capability-desc {
            color: var(--ocp-muted) !important;
            font-size: 0.98rem;
            line-height: 1.65;
            word-break: normal;
            overflow-wrap: normal;
            hyphens: none;
        }

        .audit-shell {
            background: linear-gradient(180deg, rgba(16,16,16,0.98) 0%, rgba(12,12,12,0.98) 100%);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 24px;
            padding: 48px 30px 40px 30px;
            box-shadow: 0 18px 42px rgba(0,0,0,0.18);
        }

        .audit-flow {
            display: flex;
            align-items: flex-start;
            justify-content: center;
            width: 100%;
            gap: 10px;
            flex-wrap: nowrap;
            margin: 2.2rem 0 2.5rem 0;
            padding: 2rem 0.5rem 1.2rem 0.5rem;
            box-sizing: border-box;
            position: relative;
            z-index: 5;
            overflow-x: auto;
            scrollbar-width: none;
            -ms-overflow-style: none;
        }
        .audit-flow::-webkit-scrollbar { display: none; }

        .audit-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            flex: 0 0 auto;
        }

        .audit-sub-pill {
            padding: 0.35rem 0.7rem;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
            background: #111111 !important;
            color: var(--ocp-soft) !important;
            font-size: 0.72rem;
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            position: relative;
            z-index: 2;
        }

        .audit-sub-icon {
            font-family: "Material Symbols Outlined" !important;
            font-size: 18px !important;
            color: var(--ocp-orange);
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }

        .audit-step {
            padding: 0.5rem 0.85rem;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.02);
            color: var(--ocp-white) !important;
            font-size: 0.82rem;
            font-weight: 700;
            white-space: nowrap;
            transition: transform 0.22s ease, border-color 0.22s ease, background 0.22s ease, color 0.22s ease, box-shadow 0.22s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            position: relative;
        }

        .audit-step::after {
            content: "";
            position: absolute;
            bottom: -12px; /* Tamanho exato do gap definido no audit-item */
            left: 50%;
            width: 1px;
            height: 12px;
            background: rgba(255, 107, 0, 0.4); /* Fio laranja sutil */
            z-index: 1;
            pointer-events: none;
            transition: background 0.22s ease;
        }

        .audit-step.is-bronze:hover::after {
            background: rgba(205, 127, 50, 0.7);
        }

        .audit-step.is-silver:hover::after {
            background: rgba(192, 192, 192, 0.7);
        }

        .audit-step.is-gold:hover::after {
            background: rgba(255, 215, 0, 0.7);
        }

        .audit-step.is-model:hover::after {
            background: rgba(52, 199, 89, 0.7);
        }

        .audit-step.is-prediction:hover::after {
            background: rgba(64, 156, 255, 0.7);
        }

        .audit-step.is-accent:hover::after {
            background: rgba(255,107,0,0.7);
        }

        .audit-step.is-accent::after {
            background: rgba(255,107,0,0.4);
        }

        .audit-step-icon {
            font-family: "Material Symbols Outlined" !important;
            font-size: 18px !important;
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            color: inherit;
        }

        .audit-step:hover {
            transform: translateY(-8px);
            z-index: 20;
        }

        .audit-step.is-bronze:hover {
            border-color: rgba(205, 127, 50, 0.58);
            background: rgba(205, 127, 50, 0.16);
            color: #D9A066 !important;
            box-shadow: 0 10px 24px rgba(205, 127, 50, 0.14);
        }

        .audit-step.is-silver:hover {
            border-color: rgba(192, 192, 192, 0.62);
            background: rgba(192, 192, 192, 0.14);
            color: #E3E3E3 !important;
            box-shadow: 0 10px 24px rgba(192, 192, 192, 0.12);
        }

        .audit-step.is-gold:hover {
            border-color: rgba(255, 215, 0, 0.56);
            background: rgba(255, 215, 0, 0.16);
            color: #FFD84D !important;
            box-shadow: 0 10px 24px rgba(255, 215, 0, 0.12);
        }

        .audit-step.is-model:hover {
            border-color: rgba(52, 199, 89, 0.6);
            background: rgba(52, 199, 89, 0.16);
            color: #7EE2A0 !important;
            box-shadow: 0 10px 24px rgba(52, 199, 89, 0.14);
        }

        .audit-step.is-prediction:hover {
            border-color: rgba(64, 156, 255, 0.62);
            background: rgba(64, 156, 255, 0.16);
            color: #7EB7FF !important;
            box-shadow: 0 10px 24px rgba(64, 156, 255, 0.14);
        }

        .audit-step.is-accent {
            border-color: rgba(255,107,0,0.28);
            background: rgba(255,107,0,0.08);
            color: var(--ocp-orange) !important;
        }

        .audit-step.is-accent:hover {
            border-color: rgba(255,107,0,0.52);
            background: rgba(255,107,0,0.14);
            color: var(--ocp-orange-2) !important;
            box-shadow: 0 10px 24px rgba(255,107,0,0.16);
        }

        .audit-arrow {
            color: rgba(255,255,255,0.32) !important;
            margin-top: 12px;
            font-size: 0.9rem;
            font-weight: 900;
            flex-shrink: 0;
        }

        .audit-copy {
            color: var(--ocp-muted) !important;
            font-size: 1rem;
            line-height: 1.7;
            max-width: 100%;
            text-align: justify;
            margin: 0;
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

        .section-title-icon {
            width: 26px;
            height: 26px;
            flex: 0 0 26px;
            margin-right: 0.1rem;
            color: rgba(255, 107, 0, 0.9);
            font-family: "Material Symbols Outlined" !important;
            font-weight: 400;
            font-style: normal;
            font-size: 26px;
            line-height: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            letter-spacing: normal;
            text-transform: none;
            white-space: nowrap;
            direction: ltr;
            font-variation-settings: "FILL" 0, "wght" 400, "GRAD" 0, "opsz" 24;
            -webkit-font-smoothing: antialiased;
            text-rendering: optimizeLegibility;
            -moz-osx-font-smoothing: grayscale;
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
            gap: 26px;
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

        .roadmap-native {
            margin-top: 0.25rem;
        }

        .roadmap-native-header {
            color: var(--ocp-orange) !important;
            font-size: clamp(2rem, 3.4vw, 3.1rem);
            line-height: 1.08;
            letter-spacing: -0.04em;
            font-weight: 800;
            text-align: center;
            margin: 0 0 3.8rem 0;
        }

        .roadmap-native-grid {
            display: grid;
            grid-template-columns: repeat(var(--roadmap-cols, 5), minmax(0, 1fr));
            gap: 20px;
        }

        .roadmap-card {
            position: relative;
            background: #1E1E1E;
            border: 1px solid var(--ocp-border);
            border-radius: 18px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            min-height: 100%;
            box-shadow: 0 0 0 1px rgba(255,255,255,0.02) inset;
            transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
        }

        .roadmap-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255,107,0,0.34);
            box-shadow: 0 18px 34px rgba(255,107,0,0.08), 0 0 0 1px rgba(255,107,0,0.05) inset;
        }

        .roadmap-card.active {
            border: 2px solid var(--ocp-orange);
            background: #252525;
            box-shadow: 0 0 30px rgba(255,107,0,0.12);
        }

        .roadmap-level-tag {
            font-size: 0.75rem;
            font-weight: 900;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .roadmap-card.active .roadmap-level-tag {
            color: var(--ocp-orange) !important;
        }

        .roadmap-card-title {
            font-size: 1.45rem;
            line-height: 1.12;
            font-weight: 800;
            color: #F7F7F7;
            margin-bottom: 12px;
        }

        .roadmap-card-price {
            font-size: 1.9rem;
            line-height: 1;
            font-weight: 900;
            color: var(--ocp-orange);
            margin-bottom: 20px;
        }

        .roadmap-card-desc {
            font-size: 0.95rem;
            color: #AAAAAA;
            line-height: 1.45;
            margin-bottom: 20px;
            min-height: 86px;
        }

        .roadmap-features {
            list-style: none;
            margin: 0;
            padding: 0;
            font-size: 0.88rem;
        }

        .roadmap-features li {
            position: relative;
            margin-bottom: 8px;
            padding-left: 15px;
            color: #D7D7D7;
            line-height: 1.35;
        }

        .roadmap-features li b {
            color: var(--ocp-orange) !important;
            font-weight: 800;
        }

        .roadmap-features li::before {
            content: "•";
            position: absolute;
            left: 0;
            color: var(--ocp-orange);
        }

        .roadmap-card-footer {
            margin-top: auto;
        }

        .roadmap-market-divider {
            margin: 20px 0 15px 0;
            border-top: 1px solid #333;
            padding-top: 15px;
            font-size: 0.75rem;
            color: #888;
            text-transform: uppercase;
            font-weight: 800;
            letter-spacing: 0.02em;
        }

        .roadmap-market-content {
            font-size: 0.8rem;
            color: #777;
            font-style: italic;
            line-height: 1.35;
        }

        .roadmap-status-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: var(--ocp-orange);
            color: #FFFFFF;
            font-size: 0.65rem;
            font-weight: 900;
            padding: 4px 8px;
            border-radius: 4px;
        }

        .roadmap-status-badge.future {
            background: transparent;
            border: 1px solid var(--ocp-orange);
            color: var(--ocp-orange);
        }

        .roadmap-native-footer {
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 1.8rem;
        }

        .roadmap-market-break {
            margin-top: 0.2rem;
            font-size: 0.96rem;
            text-align: center;
            color: var(--ocp-orange);
            font-weight: 800;
        }

        .roadmap-trajectory {
            margin-top: 1rem;
            font-size: 1rem;
            text-align: center;
            line-height: 1.55;
            color: var(--ocp-white) !important;
        }

        .roadmap-pipeline-note {
            margin-top: 1rem;
            font-size: 0.92rem;
            text-align: center;
            color: #8A8A8A;
            line-height: 1.6;
        }

        .roadmap-highlight-quote {
            margin-top: 1.9rem;
            padding: 18px 30px;
            max-width: 790px;
            border-left: 4px solid var(--ocp-orange);
            border-radius: 12px;
            background: linear-gradient(180deg, rgba(255,102,0,0.10) 0%, rgba(255,102,0,0.04) 100%);
            color: #F3F3F3;
            font-size: 1.15rem;
            font-weight: 700;
            font-style: italic;
            letter-spacing: -0.02em;
            text-align: center;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28);
        }

        .roadmap-emilia-row {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 0.15rem;
        }

        .roadmap-emilia-badge {
            opacity: 0.85;
            transition: transform 0.3s ease, opacity 0.3s ease;
        }

        .roadmap-emilia-badge:hover {
            transform: scale(1.05);
            opacity: 1;
        }

        .roadmap-emilia-badge img {
            height: 150px;
            display: block;
            margin: 0 auto;
        }

        .roadmap-footer-note {
            margin-top: 0.35rem;
            text-align: center;
            color: #555;
            line-height: 1.5;
        }

        .map-section {
            margin-top: 0.5rem;
        }

        .map-section .section-subtitle.map-subtitle-wide {
            max-width: none;
            width: 100%;
        }

        .map-wide-shell {
            width: min(calc(100vw - 64px), 1360px);
            margin: 0 auto;
            position: relative;
            left: 50%;
            transform: translateX(-50%);
        }

        .performance-wide-shell {
            width: min(calc(100vw - 64px), 1360px);
            margin: 0 auto;
            position: relative;
            left: 50%;
            transform: translateX(-50%);
        }

        .roadmap-wide-shell {
            width: min(calc(100vw - 64px), 1420px);
            margin: 0 auto;
            position: relative;
            left: 50%;
            transform: translateX(-50%);
        }

        .ocp-roadmap-embed iframe {
            display: block;
            width: 100%;
            min-height: 1180px;
            border: 0;
            background: transparent;
        }

        .roadmap-wide-shell [data-testid="stIFrame"] {
            height: 1180px !important;
        }

        .roadmap-wide-shell [data-testid="stIFrame"] iframe {
            height: 100% !important;
        }

        .map-shell {
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            overflow: hidden;
            background: linear-gradient(180deg, rgba(18,18,18,0.96) 0%, rgba(11,11,11,0.98) 100%);
            box-shadow: 0 18px 42px rgba(0,0,0,0.24);
        }

        .map-open-row {
            display: flex;
            justify-content: flex-end;
            margin: 1rem 0 0 0;
        }

        .map-open-link {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 44px;
            padding: 0 18px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.12);
            background: linear-gradient(90deg, var(--ocp-orange) 0%, var(--ocp-orange-2) 100%);
            color: #FFFFFF !important;
            text-decoration: none !important;
            font-size: 0.92rem;
            font-weight: 800;
            box-shadow: 0 8px 20px rgba(255,107,0,0.18);
            transition: all 0.25s ease;
        }

        .map-open-link:hover {
            background: #0D0D0D !important;
            color: var(--ocp-orange) !important;
            border-color: var(--ocp-orange) !important;
            box-shadow: none !important;
        }

        .map-fallback {
            padding: 1rem 1.1rem;
            color: var(--ocp-soft) !important;
            line-height: 1.7;
        }

        .map-fallback code {
            color: var(--ocp-orange);
            background: rgba(255,107,0,0.08);
            border: 1px solid rgba(255,107,0,0.12);
            padding: 0.12rem 0.35rem;
            border-radius: 8px;
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
            margin-top: 2rem;
        }

        .social-link {
            width: 46px;
            height: 46px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.12);
            background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 45%, rgba(255,255,255,0.015) 100%);
            color: var(--ocp-soft) !important;
            text-decoration: none;
            box-shadow: 0 6px 14px rgba(0,0,0,0.18), 0 0 0 1px rgba(255,255,255,0.015) inset;
            transition: transform 0.24s ease, border-color 0.24s ease, color 0.24s ease, background 0.24s ease, box-shadow 0.24s ease;
        }

        .social-link:hover {
            transform: translateY(-3px) scale(1.03);
            border-color: rgba(255,107,0,0.55);
            background: radial-gradient(circle at 30% 30%, rgba(255,149,64,0.22) 0%, rgba(255,107,0,0.12) 48%, rgba(255,107,0,0.08) 100%);
            color: var(--ocp-orange) !important;
            box-shadow: 0 14px 28px rgba(255,107,0,0.16), 0 0 18px rgba(255,107,0,0.14), 0 0 0 1px rgba(255,107,0,0.08) inset;
        }

        .social-link svg {
            width: 19px;
            height: 19px;
        }

        .partner-spotlight {
            margin-top: 2.25rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1.5rem;
        }

        .partner-spotlight-note {
            max-width: 680px;
            width: 100%;
            text-align: center;
            color: rgba(255,255,255,0.82) !important;
            font-size: 0.95rem;
            line-height: 1.45;
            font-weight: 700;
        }

        .partner-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            border-radius: 16px;
            border: 1px solid rgba(66, 153, 225, 0.28);
            background: linear-gradient(180deg, rgba(11, 28, 45, 0.92) 0%, rgba(7, 17, 29, 0.96) 100%);
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.24), 0 0 0 1px rgba(66, 153, 225, 0.08);
            max-width: 680px;
            transition: transform 0.24s ease, box-shadow 0.24s ease, border-color 0.24s ease, background 0.24s ease;
        }

        .partner-badge:hover {
            transform: translateY(-2px);
            border-color: rgba(66, 153, 225, 0.45);
            box-shadow: 0 14px 32px rgba(0, 0, 0, 0.28), 0 0 0 1px rgba(66, 153, 225, 0.14), 0 0 26px rgba(66, 153, 225, 0.24);
        }

        .partner-badge-logo {
            width: 122px;
            height: 46px;
            flex: 0 0 122px;
            display: grid;
            place-items: center;
            border-radius: 10px;
            background: transparent;
            border: 0;
            overflow: visible;
            filter: none;
            transition: transform 0.24s ease, filter 0.24s ease, border-color 0.24s ease, background 0.24s ease;
        }

        .partner-badge:hover .partner-badge-logo {
            transform: scale(1.03);
        }

        .partner-badge-logo img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            object-position: left center;
            display: block;
            transition: filter 0.24s ease;
        }

        .partner-badge:hover .partner-badge-logo img {
            filter: drop-shadow(0 0 12px rgba(66, 153, 225, 0.24));
        }

        .partner-badge-copy {
            text-align: left;
            min-width: 0;
        }

        .partner-badge-kicker {
            color: #83BFFF !important;
            font-size: 0.7rem;
            letter-spacing: 0.12em;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 0.12rem;
        }

        .partner-badge-title {
            color: #FFFFFF !important;
            font-size: 0.95rem;
            font-weight: 800;
            line-height: 1.2;
        }

        .partner-badge-subtitle {
            color: rgba(255,255,255,0.72) !important;
            font-size: 0.84rem;
            line-height: 1.45;
            margin-top: 0.18rem;
        }

        .partner-badge-disclaimer {
            color: rgba(255,255,255,0.46) !important;
            font-size: 0.72rem;
            line-height: 1.35;
            margin-top: 0.22rem;
        }

        .desafix-banner {
            max-width: 680px;
            width: 100%;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.08);
            background: linear-gradient(180deg, #2A0637 0%, #3B0A4D 100%);
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.24);
            overflow: hidden;
            transition: transform 0.24s ease, box-shadow 0.24s ease;
        }
        .desafix-banner:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 32px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(186, 85, 255, 0.16), 0 0 28px rgba(133, 46, 196, 0.28);
            border-color: rgba(186, 85, 255, 0.34);
        }
        .desafix-banner img {
            width: 100%;
            height: auto;
            display: block;
            transform: scale(1.035);
            transform-origin: center center;
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

        /* FAQ Styles */
        .faq-wrap {
            max-width: 1240px;
            margin: 0 auto;
            background: transparent !important;
        }

        /* Nuke: Remove fundos brancos e bordas fantasmas dos containers do Streamlit */
        .stMarkdown div:has(.faq-item), 
        .element-container:has(.faq-item) {
            background-color: transparent !important;
        }

        .faq-grid {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 1.5rem !important;
            align-items: stretch !important;
            background: transparent !important;
        }

        .faq-item {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            margin-bottom: 0 !important;
            padding: 1.5rem;
            transition: all 0.22s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            height: 100%;
            display: flex;
            flex-direction: column;
        }

        .faq-item:hover {
            border-color: rgba(255,107,0,0.25);
            background: rgba(255,255,255,0.04);
            transform: translateY(-2px);
        }

        .faq-question {
            color: var(--ocp-white) !important;
            font-size: 1.1rem;
            font-weight: 800;
            margin-bottom: 0.6rem;
            display: flex;
            align-items: center;
            gap: 12px;
            line-height: 1.3;
        }

        .faq-answer {
            color: var(--ocp-soft) !important;
            font-size: 0.98rem;
            line-height: 1.6;
            text-align: justify;
        }

        @media (max-width: 900px) {
            .faq-grid {
                grid-template-columns: 1fr !important;
            }
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
            .hero-title-row {
                grid-template-columns: 88px 1fr;
                column-gap: 0.75rem;
            }

            .hero-title-logo,
            .hero-title-spacer {
                width: 80px;
                flex-basis: 80px;
            }

            .hero-logo-wrap {
                min-height: auto;
                padding-top: 0.15rem;
                margin-bottom: 0.5rem;
            }

            .hero-logo-img {
                width: 145px;
            }

            .hero-title {
                font-size: 1.75rem;
            }

            .hero-subcopy {
                font-size: 2.3rem;
            }

            .hero-highlight,
            .hero-pipeline-line {
                font-size: 0.98rem;
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

            .capability-grid {
                grid-template-columns: repeat(2, minmax(220px, 1fr));
            }

            .audit-shell {
                padding: 24px;
            }

            .map-wide-shell {
                width: 100%;
                left: auto;
                transform: none;
            }

            .performance-wide-shell {
                width: 100%;
                left: auto;
                transform: none;
            }

            .roadmap-wide-shell {
                width: 100%;
                left: auto;
                transform: none;
            }

            .roadmap-wide-shell [data-testid="stIFrame"] {
                height: 2850px !important;
            }

            .roadmap-native-grid {
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }

            .faq-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 700px) {
            .block-container {
                padding-left: 1.25rem !important;
                padding-right: 1.25rem !important;
            }

            .capability-grid {
                grid-template-columns: 1fr;
            }

            .roadmap-wide-shell [data-testid="stIFrame"] {
                height: 5600px !important;
            }

            .roadmap-native-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .roadmap-native-header {
                margin-bottom: 1.7rem;
            }

            .map-open-row {
                justify-content: stretch;
            }

            .map-open-link {
                width: 100%;
            }

            .partner-spotlight {
                gap: 1rem;
            }

            .partner-spotlight-note {
                font-size: 0.88rem;
                line-height: 1.4;
            }

            .partner-badge {
                width: 100%;
                padding: 1rem;
                flex-direction: column;
                text-align: center;
            }

            .partner-badge-logo {
                width: 144px;
                height: 54px;
                flex: 0 0 auto;
            }

            .partner-badge-logo img {
                object-position: center center;
            }

            .partner-badge-copy {
                text-align: center;
            }
        }

        @media (max-width: 480px) {
            .roadmap-wide-shell [data-testid="stIFrame"] {
                height: 6400px !important;
            }

            .roadmap-native-grid {
                grid-template-columns: 1fr;
            }

            .roadmap-card-title {
                min-height: auto;
            }

            .roadmap-card-desc {
                min-height: auto;
            }

            .roadmap-highlight-quote {
                padding: 16px 18px;
                font-size: 1.02rem;
            }

            .roadmap-emilia-badge img {
                height: 132px;
            }

            .partner-spotlight-note {
                font-size: 0.82rem;
            }

            .desafix-banner img {
                transform: scale(1.05);
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if map_only_view:
    st.markdown(
        """
        <style>
            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stAppViewContainer"] > .main,
            [data-testid="stAppViewContainer"] > .main .block-container,
            [data-testid="stMainBlockContainer"] {
                background: #0D0D0D !important;
                padding: 0 !important;
                margin: 0 !important;
                max-width: none !important;
            }

            [data-testid="stAppViewContainer"] > .main .block-container,
            [data-testid="stMainBlockContainer"] {
                gap: 0 !important;
            }

            html, body {
                overflow: hidden !important;
            }

        </style>
        """,
        unsafe_allow_html=True,
    )

    if snis_map_html:
        st.iframe(snis_map_html, height=1200)
        st.html(
            """
            <style>
                html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
                    margin: 0 !important;
                    padding: 0 !important;
                    overflow: hidden !important;
                }

                [data-testid="stMainBlockContainer"] {
                    max-width: none !important;
                    padding: 0 !important;
                    margin: 0 !important;
                }

                [data-testid="stIFrame"] {
                    width: calc(100vw + 6px) !important;
                    height: calc(100vh + 6px) !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    transform: translate(-3px, -3px);
                }

                [data-testid="stIFrame"] iframe {
                    height: 100% !important;
                    width: 100% !important;
                    display: block !important;
                    border: 0 !important;
                }
            </style>
            <script>
                (function() {
                    function resizeFullscreenMap() {
                        const wrapper = parent.document.querySelector('[data-testid="stIFrame"]');
                        const frame = wrapper ? wrapper.querySelector('iframe') : null;
                        const viewport = window.innerHeight || parent.innerHeight || 900;
                        const height = Math.max(viewport + 6, 720);

                        if (wrapper) {
                            wrapper.style.width = 'calc(100vw + 6px)';
                            wrapper.style.height = height + 'px';
                            wrapper.style.margin = '0';
                            wrapper.style.padding = '0';
                            wrapper.style.transform = 'translate(-3px, -3px)';
                        }

                        if (frame) {
                            frame.style.width = '100%';
                            frame.style.height = height + 'px';
                            frame.style.border = '0';
                            frame.style.display = 'block';
                        }
                    }

                    resizeFullscreenMap();
                    window.addEventListener('load', resizeFullscreenMap);
                    window.addEventListener('resize', resizeFullscreenMap);
                    setTimeout(resizeFullscreenMap, 150);
                    setTimeout(resizeFullscreenMap, 500);
                })();
            </script>
            """,
            unsafe_allow_javascript=True,
        )
    else:
        st.markdown(
            f'<div class="map-shell"><div class="map-fallback">{tr(lang, "snis_map_missing")}</div></div>',
            unsafe_allow_html=True,
        )

    st.stop()

capabilities_section_html = dedent(
    f"""
    <div class="section-shell-soft">
        <div class="feature-intro">
            <div class="section-title">{tr(lang, "capabilities_title")}</div>
            <div class="section-subtitle">{tr(lang, "capabilities_subtitle")}</div>
        </div>
        <div class="capability-grid">
            <div class="capability-card">
                <div class="capability-topline">
                    <div class="capability-index">01</div>
                    <span class="capability-icon" aria-hidden="true">fact_check</span>
                </div>
                <div class="capability-title">{tr(lang, "capability_1_title")}</div>
                <div class="capability-desc">{tr(lang, "capability_1_desc")}</div>
            </div>
            <div class="capability-card">
                <div class="capability-topline">
                    <div class="capability-index">02</div>
                    <span class="capability-icon" aria-hidden="true">show_chart</span>
                </div>
                <div class="capability-title">{tr(lang, "capability_2_title")}</div>
                <div class="capability-desc">{tr(lang, "capability_2_desc")}</div>
            </div>
            <div class="capability-card">
                <div class="capability-topline">
                    <div class="capability-index">03</div>
                    <span class="capability-icon" aria-hidden="true">hub</span>
                </div>
                <div class="capability-title">{tr(lang, "capability_3_title")}</div>
                <div class="capability-desc">{tr(lang, "capability_3_desc")}</div>
            </div>
            <div class="capability-card">
                <div class="capability-topline">
                    <div class="capability-index">04</div>
                    <span class="capability-icon" aria-hidden="true">warning</span>
                </div>
                <div class="capability-title">{tr(lang, "capability_4_title")}</div>
                <div class="capability-desc">{tr(lang, "capability_4_desc")}</div>
            </div>
            <div class="capability-card">
                <div class="capability-topline">
                    <div class="capability-index">05</div>
                    <span class="capability-icon" aria-hidden="true">timeline</span>
                </div>
                <div class="capability-title">{tr(lang, "capability_5_title")}</div>
                <div class="capability-desc">{tr(lang, "capability_5_desc")}</div>
            </div>
        </div>
    </div>
    """
).strip()

audit_section_html = dedent(
    f"""
    <div class="audit-shell">
        <div class="feature-intro" style="margin-bottom:0;">
            <div class="section-title">{tr(lang, "audit_title")}</div>
        </div>
        <div class="audit-flow">
            <div class="audit-item">
                <div class="audit-step is-bronze">
                    <span class="material-symbols-outlined audit-step-icon">database_upload</span>
                    {tr(lang, "audit_step_bronze")}
                </div>
                <div class="audit-sub-pill">
                    {tr(lang, "audit_sub_bronze")}
                </div>
            </div>
            <div class="audit-arrow">→</div>
            <div class="audit-item">
                <div class="audit-step is-silver">
                    <span class="material-symbols-outlined audit-step-icon">cleaning_services</span>
                    {tr(lang, "audit_step_silver")}
                </div>
                <div class="audit-sub-pill">
                    {tr(lang, "audit_sub_silver")}
                </div>
            </div>
            <div class="audit-arrow">→</div>
            <div class="audit-item">
                <div class="audit-step is-gold">
                    <span class="material-symbols-outlined audit-step-icon">verified</span>
                    {tr(lang, "audit_step_gold")}
                </div>
                <div class="audit-sub-pill">
                    {tr(lang, "audit_sub_gold")}
                </div>
            </div>
            <div class="audit-arrow">→</div>
            <div class="audit-item">
                <div class="audit-step is-model">
                    <span class="material-symbols-outlined audit-step-icon">neurology</span>
                    {tr(lang, "audit_step_model")}
                </div>
                <div class="audit-sub-pill">
                    {tr(lang, "audit_sub_model")}
                </div>
            </div>
            <div class="audit-arrow">→</div>
            <div class="audit-item">
                <div class="audit-step is-prediction">
                    <span class="material-symbols-outlined audit-step-icon">online_prediction</span>
                    {tr(lang, "audit_step_prediction")}
                </div>
                <div class="audit-sub-pill">
                    {tr(lang, "audit_sub_prediction")}
                </div>
            </div>
            <div class="audit-arrow">→</div>
            <div class="audit-item">
                <div class="audit-step is-accent">
                    <span class="material-symbols-outlined audit-step-icon">gavel</span>
                    {tr(lang, "audit_step_contract")}
                </div>
                <div class="audit-sub-pill">
                    {tr(lang, "audit_sub_contract")}
                </div>
            </div>
        </div>
        <div class="audit-copy">{tr(lang, "audit_body")}</div>
    </div>
    """
).strip()

# =========================================================
# HERO
# =========================================================
st.markdown(
    f"""
    <div class="hero-copy-wrap">
        <div class="hero-title-row">
            <img src="{logo_uri}" class="hero-title-logo" alt="OpenCanvas Pro Logo" />
            <div class="hero-title">OpenCanvas <span class="accent">Pro™</span></div>
        </div>
        <div class="hero-subcopy">
            {tr(lang, "hero_title")}
        </div>
        <div class="hero-highlight">
            {tr(lang, "hero_description")}
        </div>
        <div class="hero-pipeline-line">
            {tr(lang, "hero_pipeline")}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

        

st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)

        

# =========================================================
# WHAT THE PLATFORM DOES
# =========================================================
st.markdown(capabilities_section_html, unsafe_allow_html=True)

st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)

# =========================================================
# AUDITABLE PIPELINE
# =========================================================
st.markdown(audit_section_html, unsafe_allow_html=True)

st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)

# =========================================================
# DIFFERENTIALS
# =========================================================
st.markdown(
    '''
    <div class="feature-intro">
        <div class="section-title">''' + tr(lang, "feature_title") + '''</div>
        <div class="section-subtitle feature-subtitle-wide">
            ''' + tr(lang, "feature_subtitle_1") + '''<br><br>
            ''' + tr(lang, "feature_subtitle_2") + '''
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
                        <div class="benefit-label"><span class="benefit-label-icon">{lucide_icon("brain")}</span> {tr(lang, "feature_label_brain")}</div>
                        <div class="benefit-desc">{tr(lang, "benefit_brain_desc")}</div>
                    </div>
                    <div class="benefit-item">
                        <div class="benefit-label"><span class="benefit-label-icon">{lucide_icon("shield")}</span> {tr(lang, "feature_label_shield")}</div>
                        <div class="benefit-desc">{tr(lang, "benefit_shield_desc")}</div>
                    </div>
                    <div class="benefit-item">
                        <div class="benefit-label"><span class="benefit-label-icon">{lucide_icon("file-text")}</span> {tr(lang, "feature_label_file")}</div>
                        <div class="benefit-desc">{tr(lang, "benefit_file_desc")}</div>
                    </div>
                    <div class="benefit-item">
                        <div class="benefit-label"><span class="benefit-label-icon">{lucide_icon("sliders")}</span> {tr(lang, "feature_label_sliders")}</div>
                        <div class="benefit-desc">{tr(lang, "benefit_sliders_desc")}</div>
                    </div>
                    <div class="benefit-item">
                        <div class="benefit-label"><span class="benefit-label-icon">{lucide_icon("building")}</span> {tr(lang, "feature_label_building")}</div>
                        <div class="benefit-desc">{tr(lang, "benefit_building_desc")}</div>
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
    f'<div class="section-title"><span class="section-title-icon" aria-hidden="true">rocket_launch</span> {tr(lang, "pillars_title")}</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="section-subtitle">{tr(lang, "pillars_subtitle")}</div>',
    unsafe_allow_html=True,
)

p1, p2, p3 = st.columns(3, gap="medium")

with p1:
    st.markdown(
        f"""
        <div class="content-box pillar-card">
            <div class="mini-kicker">Trust by Design</div>
            <h4>{tr(lang, "pillar_1_title")}</h4>
            <div class="pillar-body">
                {tr(lang, "pillar_1_desc")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with p2:
    st.markdown(
        f"""
        <div class="content-box pillar-card">
            <div class="mini-kicker">White-Box ML</div>
            <h4>{tr(lang, "pillar_2_title")}</h4>
            <div class="pillar-body">
                {tr(lang, "pillar_2_desc")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with p3:
    st.markdown(
        f"""
        <div class="content-box pillar-card">
            <div class="mini-kicker">Local-First Efficiency</div>
            <h4>{tr(lang, "pillar_3_title")}</h4>
            <div class="pillar-body">
                {tr(lang, "pillar_3_desc")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# MATURITY ROADMAP
# =========================================================
st.markdown(render_native_roadmap(lang), unsafe_allow_html=True)

# =========================================================
# SNIS MAP
# =========================================================
st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="map-section">
        <div class="section-title">{tr(lang, "snis_map_title")}</div>
        <div class="section-subtitle map-subtitle-wide">{tr(lang, "snis_map_subtitle")}</div>
        <div class="section-subtitle map-subtitle-wide" style="margin-top:-0.55rem; margin-bottom:1.35rem;">{tr(lang, "snis_map_subtitle_2")}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if snis_map_html:
    st.iframe(snis_map_html, height=SNIS_MAP_HEIGHT)
    st.markdown(
        f"""
        <div class="map-open-row">
            <a class="map-open-link" href="{map_view_url}" target="_blank" rel="noopener noreferrer">{tr(lang, "snis_map_expand")}</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f'<div class="map-shell"><div class="map-fallback">{tr(lang, "snis_map_missing")}</div></div>',
        unsafe_allow_html=True,
    )

# =========================================================
# VERSÕES E PREÇOS
# =========================================================
pricing_items: list[RoadmapItem] = [
    {
        "level": "Free Starter",
        "title": tr(lang, "pricing_c1_title"),
        "desc": tr(lang, "pricing_c1_desc"),
        "features": [tr(lang, f"pricing_c1_f{i}") for i in range(1, 11)],
        "footer_label": "",
        "footer_items": ["EM BREVE"],
        "status": f"{tr(lang, 'pricing_c1_price')} ({tr(lang, 'pricing_c1_period')})",
        "active": True
    },
    {
        "level": "Pro Workspace",
        "title": tr(lang, "pricing_c2_title"),
        "desc": tr(lang, "pricing_c2_desc"),
        "features": [tr(lang, f"pricing_c2_f{i}") for i in range(1, 10)],
        "footer_label": "Next Step",
        "footer_items": [{"label": tr(lang, "pricing_c2_cta"), "link": get_mailto_link("Journey", lang)}],
        "status": tr(lang, "pricing_c2_price"),
        "future": True
    },
    {
        "level": "Corporate",
        "title": tr(lang, "pricing_c3_title"),
        "desc": tr(lang, "pricing_c3_desc"),
        "features": [tr(lang, f"pricing_c3_f{i}") for i in range(1, 11)],
        "footer_label": "Enterprise",
        "footer_items": [{"label": tr(lang, "pricing_c3_cta"), "link": get_mailto_link("Enterprise", lang)}],
        "status": tr(lang, "pricing_c3_price")
    }
]
st.markdown(render_native_roadmap(lang, title_text=tr(lang, "pricing_title"), subtitle_text=tr(lang, "pricing_subtitle"), items=pricing_items, cols=3, show_footer=False), unsafe_allow_html=True)

# =========================================================
# FAQ SECTION
# =========================================================
st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)

faq_items_html = ""
# Contagem dinâmica para manter o grid de 2 colunas equilibrado independente do número de perguntas
faq_keys = [k for k in I18N["pt"].keys() if k.startswith("faq_q") and k[5:].isdigit()]
num_faq = len(faq_keys)
half = (num_faq + 1) // 2

for i in range(1, half + 1):
    for idx in [i, i + half]:
        if idx <= num_faq:
            q, a = tr(lang, f"faq_q{idx}"), tr(lang, f"faq_a{idx}")
            faq_items_html += f'<div class="faq-item"><div class="faq-question">{idx}. {q}</div><div class="faq-answer">{a}</div></div>'

st.markdown(
    f'<div class="faq-wrap">'
    f'<div class="feature-intro" style="text-align:center;">'
    f'<div class="section-title">{tr(lang, "faq_title")}</div>'
    f'<div class="section-subtitle" style="margin: 0 auto 2.5rem auto;">{tr(lang, "faq_subtitle")}</div>'
    f'</div>'
    f'<div class="faq-grid">{faq_items_html}</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# =========================================================
# WAITLIST
# =========================================================
st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)
st.markdown(f'<div class="waitlist-title">{tr(lang, "waitlist_title")}</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="waitlist-subtitle">
        {tr(lang, "waitlist_subtitle")}
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
            email = st.text_input(tr(lang, "email_label"), placeholder=tr(lang, "waitlist_placeholder"))

        cta_icon_col, cta_button_col = st.columns([0.08, 0.92], gap="small")
        with cta_icon_col:
            st.markdown(
                f'<div class="waitlist-cta-icon">{lucide_icon("bell-ring")}</div>',
                unsafe_allow_html=True,
            )
        with cta_button_col:
            submitted = st.form_submit_button(tr(lang, "waitlist_button"))

        if submitted:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if email and re.match(email_pattern, email):
                ok, msg = send_waitlist_email(email, lang)
                if ok:
                    st.success(f"✔ {tr(lang, 'success_msg')}")
                else:
                    st.error(f"Não foi possível registrar agora: {msg}")
            else:
                st.warning(tr(lang, "warning_msg"))

st.markdown(
    f"""
    <div class="social-row">
        <a class="social-link" href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
            {social_icon("linkedin")}
        </a>
        <a class="social-link" href="{YOUTUBE_URL}" target="_blank" rel="noopener noreferrer" aria-label="YouTube">
            {social_icon("youtube")}
        </a>
        <a class="social-link" href="{X_URL}" target="_blank" rel="noopener noreferrer" aria-label="X">
            {social_icon("x")}
        </a>
        <a class="social-link" href="{GITHUB_URL}" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
            {social_icon("github")}
        </a>
    </div>
    <div class="partner-spotlight">
        <div class="partner-spotlight-note">{tr(lang, "partner_spotlight_note")}</div>
        <div class="partner-badge">
            <div class="partner-badge-logo" aria-hidden="true">
                <img src="{neo4j_uri}" alt="" />
            </div>
            <div class="partner-badge-copy">
                <div class="partner-badge-kicker">{tr(lang, "partner_tag")}</div>
                <div class="partner-badge-title">{tr(lang, "partner_title")}</div>
                <div class="partner-badge-subtitle">{tr(lang, "partner_subtitle")}</div>
                <div class="partner-badge-disclaimer">{tr(lang, "partner_disclaimer")}</div>
            </div>
        </div>
        {f'<div class="desafix-banner"><img src="{desafix_uri}" alt="Desafio 2026" /></div>' if desafix_uri else ""}
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    f'<div class="footer-wrap">'
    f'<div class="footer-main">{tr(lang, "footer_main")}</div>'
    f'<div class="footer-sub">{tr(lang, "footer_sub")}</div>'
    f'</div>',
    unsafe_allow_html=True,
)
