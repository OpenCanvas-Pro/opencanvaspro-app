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
EMILIA_PATH = os.path.join(ASSETS_DIR, "Emilia_hires.png")
MATURITY_HTML_PATH = "maturidade_ia_opencanvas_v4.3.html"
LINKEDIN_URL = "https://www.linkedin.com/company/opencanvaspro"
X_URL = "https://x.com/opencanvaspro"
GITHUB_URL = "https://github.com/OpenCanvas-Pro/opencanvaspro-app"

LANG_LABELS = {
    "pt": "Português",
    "en": "English",
    "es": "Español",
    "hi": "Hindi",
    "fr": "Français",
    "de": "Deutsch",
}

I18N = {
    "pt": {
        "hero_subcopy": "Projetado para times que não podem errar decisões baseadas em dados",
        "page_description": "A plataforma de AutoML que une Integridade Científica e Navegação Cognitiva. Desenvolvida para modelos de alta confiança.",
        "feature_title": "Trusted Platform & <span class=\"accent\">Diferenciais</span>",
        "feature_subtitle_1": "A OpenCanvas Pro é uma startup brasileira em nascimento, construída para transformar automação em confiança: unindo AutoML, governança, integridade científica e auditoria técnica para equipes que precisam de clareza - não apenas métricas bonitas.",
        "feature_subtitle_2": "Não somos apenas mais uma interface para treinar modelos. Estamos desenhando uma nova categoria de software: uma plataforma de AutoML cognitiva, auditável e orientada à confiança.",
        "benefit_brain_desc": "Assistente contextual com grafo de conhecimento para orientar estratégias de treino, identificar riscos e evitar “pântanos estatísticos”.",
        "benefit_shield_desc": "19+ validações avançadas para leakage, overfitting, inconsistências, desequilíbrio, colunas problemáticas e falhas silenciosas de modelagem.",
        "benefit_file_desc": "Relatórios executivos, contratos de auditoria, documentação técnica e rastreabilidade para ambientes que exigem governança real.",
        "benefit_sliders_desc": "Pipeline pronto para inferência em lote, exportação de modelos e operacionalização local-first com menor fricção.",
        "benefit_building_desc": "Processamento na infraestrutura do cliente, com foco em LGPD/GDPR, compliance, transparência e soberania sobre dados e artefatos.",
        "pillars_title": "Pilares de <span class=\"accent\">Performance</span>",
        "pillars_subtitle": "Cada pilar foi desenhado para reduzir fricção, aumentar confiança e tornar o uso de Machine Learning mais seguro para times técnicos e executivos.",
        "pillar_1_desc": "Cada execução pode gerar trilha de auditoria, histórico de transformação, contratos técnicos e certificado de integridade científica para decisões com respaldo.",
        "pillar_2_desc": "Controle explícito sobre dados, etapas de preparação, checks, métricas e artefatos. Nada de caixa-preta disfarçada de conveniência.",
        "pillar_3_desc": "Arquitetura orientada a performance local, redução de fricção operacional e menor dependência de nuvem para workloads sensíveis.",
        "pillar_1_title": "Auditoria Gold Standard",
        "pillar_2_title": "Transparência Operacional",
        "pillar_3_title": "Eficiência de Recurso",
        "feature_label_brain": "Navegação Cognitiva (E.M.I.L.I.A.)",
        "feature_label_shield": "Escudo de Integridade Científica™",
        "feature_label_file": "Artefatos de Nível Executivo",
        "feature_label_sliders": "Previsão em Lote e Exportação de Modelo",
        "feature_label_building": "Soberania de IA Local-First",
        "waitlist_title": "Entre cedo no radar da OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro</span>",
        "waitlist_subtitle": "Estamos abrindo terreno para o lançamento oficial. Cadastre seu e-mail para acompanhar a evolução da plataforma, os previews técnicos e novidades.",
        "waitlist_button": "QUERO SER AVISADO NO LANÇAMENTO",
        "waitlist_input": "Seu e-mail:",
        "waitlist_placeholder": "exemplo@empresa.com",
        "footer_main": "© OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro™</span> 2026 | <span class=\"footer-highlight\">Cognitive AutoMLOps Trust Platform</span>",
        "footer_sub": "Plataforma em early-stage | CNPJ 64.918.004/0001-36 | opencanvaspro.com<br>Built for Science. Built for Trust. Powered by E.M.I.L.I.A.™ | <a href=\"mailto:contato@opencanvaspro.com\">contato@opencanvaspro.com</a>",
        "page_title": "OpenCanvas Pro | Cognitive AutoMLOps",
        "email_subject": "Novo cadastro na waitlist — OpenCanvas Pro",
        "email_body": "Novo interesse registrado na waitlist da OpenCanvas Pro.",
        "email_label": "Seu e-mail:",
        "success_msg": "Você entrou na lista. Em breve novidades.",
        "warning_msg": "Por favor, informe um e-mail válido.",
    },
    "en": {
        "hero_subcopy": "Built for teams that cannot afford to get data-driven decisions wrong",
        "page_description": "The AutoML platform that unites Scientific Integrity and Cognitive Navigation. Built for high-trust models.",
        "feature_title": "Trusted Platform & <span class=\"accent\">Differentiators</span>",
        "feature_subtitle_1": "OpenCanvas Pro is a Brazilian startup in the making, designed to turn automation into trust by combining AutoML, governance, scientific integrity and technical auditing for teams that need clarity, not vanity metrics.",
        "feature_subtitle_2": "We are not just another model-building interface. We are creating a new software category: a cognitive, auditable AutoML platform designed around trust.",
        "benefit_brain_desc": "A contextual assistant with a knowledge graph that helps shape training strategy, surface risks and keep teams out of statistical dead ends.",
        "benefit_shield_desc": "19+ advanced checks for leakage, overfitting, inconsistencies, class imbalance, problematic columns and silent modeling failures.",
        "benefit_file_desc": "Executive-ready reports, audit contracts, technical documentation and traceability for environments that need real governance.",
        "benefit_sliders_desc": "A production-ready pipeline for batch inference, model export and local-first deployment with less friction.",
        "benefit_building_desc": "Runs inside the client's infrastructure, with a focus on LGPD/GDPR, compliance, transparency and control over data and artifacts.",
        "pillars_title": "Pillars of <span class=\"accent\">Performance</span>",
        "pillars_subtitle": "Each pillar is shaped to reduce friction, build confidence and make machine learning safer for both technical and executive teams.",
        "pillar_1_desc": "Every run can produce an audit trail, transformation history, technical contracts and a scientific integrity certificate to support decisions.",
        "pillar_2_desc": "Explicit control over data, preparation steps, checks, metrics and artifacts. No black box disguised as convenience.",
        "pillar_3_desc": "Architecture focused on local performance, lower operational friction and less dependence on cloud for sensitive workloads.",
        "pillar_1_title": "Gold Standard Auditing",
        "pillar_2_title": "Operational Transparency",
        "pillar_3_title": "Resource Efficiency",
        "feature_label_brain": "Cognitive Navigation (E.M.I.L.I.A.)",
        "feature_label_shield": "Scientific Integrity Shield™",
        "feature_label_file": "Executive-Grade Artifacts",
        "feature_label_sliders": "Batch Prediction & Model Export",
        "feature_label_building": "Local-First AI Sovereignty",
        "waitlist_title": "Get early access to the OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro</span> radar",
        "waitlist_subtitle": "We are preparing for the official launch. Drop your email to follow the platform's evolution, technical previews and updates.",
        "waitlist_button": "NOTIFY ME WHEN WE LAUNCH",
        "waitlist_input": "Your email:",
        "waitlist_placeholder": "example@company.com",
        "footer_main": "© OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro™</span> 2026 | <span class=\"footer-highlight\">Cognitive AutoMLOps Trust Platform</span>",
        "footer_sub": "Early-stage platform | CNPJ 64.918.004/0001-36 | opencanvaspro.com<br>Built for Science. Built for Trust. Powered by E.M.I.L.I.A.™ | <a href=\"mailto:contato@opencanvaspro.com\">contato@opencanvaspro.com</a>",
        "page_title": "OpenCanvas Pro | Cognitive AutoMLOps",
        "email_subject": "New waitlist signup — OpenCanvas Pro",
        "email_body": "New interest registered in the OpenCanvas Pro waitlist.",
        "email_label": "Email:",
        "success_msg": "You are on the list. More updates soon.",
        "warning_msg": "Please enter a valid email.",
    },
    "es": {
        "hero_subcopy": "Hecho para equipos que no pueden permitirse equivocarse con decisiones basadas en datos",
        "page_description": "La plataforma de AutoML que une Integridad Científica y Navegación Cognitiva. Diseñada para modelos de alta confianza.",
        "feature_title": "Plataforma de confianza & <span class=\"accent\">Diferenciales</span>",
        "feature_subtitle_1": "OpenCanvas Pro es una startup brasileña en desarrollo, creada para convertir automatización en confianza combinando AutoML, gobernanza, integridad científica y auditoría técnica para equipos que necesitan claridad, no métricas vacías.",
        "feature_subtitle_2": "No somos solo otra interfaz para entrenar modelos. Estamos creando una nueva categoría de software: una plataforma de AutoML cognitiva, auditable y diseñada alrededor de la confianza.",
        "benefit_brain_desc": "Un asistente contextual con un grafo de conocimiento que ayuda a orientar la estrategia de entrenamiento, detectar riesgos y evitar callejones estadísticos.",
        "benefit_shield_desc": "Más de 19 controles avanzados para leakage, overfitting, inconsistencias, desbalance, columnas problemáticas y fallas silenciosas de modelado.",
        "benefit_file_desc": "Informes ejecutivos, contratos de auditoría, documentación técnica y trazabilidad para entornos que necesitan gobernanza real.",
        "benefit_sliders_desc": "Un pipeline listo para inferencia por lotes, exportación de modelos y despliegue local-first con menos fricción.",
        "benefit_building_desc": "Corre dentro de la infraestructura del cliente, con foco en LGPD/GDPR, cumplimiento, transparencia y control sobre datos y artefactos.",
        "pillars_title": "Pilares de <span class=\"accent\">Rendimiento</span>",
        "pillars_subtitle": "Cada pilar está pensado para reducir fricción, aumentar confianza y hacer que el machine learning sea más seguro para equipos técnicos y ejecutivos.",
        "pillar_1_desc": "Cada ejecución puede generar una trazabilidad de auditoría, historial de transformación, contratos técnicos y un certificado de integridad científica para respaldar decisiones.",
        "pillar_2_desc": "Control explícito sobre datos, pasos de preparación, verificaciones, métricas y artefactos. Nada de caja negra disfrazada de conveniencia.",
        "pillar_3_desc": "Arquitectura centrada en rendimiento local, menor fricción operativa y menos dependencia de la nube para cargas sensibles.",
        "pillar_1_title": "Auditoría Gold Standard",
        "pillar_2_title": "Transparencia Operativa",
        "pillar_3_title": "Eficiencia de Recursos",
        "feature_label_brain": "Navegación Cognitiva (E.M.I.L.I.A.)",
        "feature_label_shield": "Escudo de Integridad Científica™",
        "feature_label_file": "Artefactos de Nivel Ejecutivo",
        "feature_label_sliders": "Predicción por Lotes y Exportación de Modelos",
        "feature_label_building": "Soberanía de IA Local-First",
        "waitlist_title": "Accede antes al radar de OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro</span>",
        "waitlist_subtitle": "Estamos preparando el lanzamiento oficial. Deja tu correo para seguir la evolución de la plataforma, los avances técnicos y las novedades.",
        "waitlist_button": "QUIERO RECIBIR AVISO DEL LANZAMIENTO",
        "waitlist_input": "Tu correo:",
        "waitlist_placeholder": "ejemplo@empresa.com",
        "footer_main": "© OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro™</span> 2026 | <span class=\"footer-highlight\">Plataforma de Confianza de AutoMLOps</span>",
        "footer_sub": "Plataforma en fase temprana | CNPJ 64.918.004/0001-36 | opencanvaspro.com<br>Construida para la ciencia. Construida para la confianza. Impulsada por E.M.I.L.I.A.™ | <a href=\"mailto:contato@opencanvaspro.com\">contato@opencanvaspro.com</a>",
        "page_title": "OpenCanvas Pro | Cognitive AutoMLOps",
        "email_subject": "Nuevo registro en la waitlist — OpenCanvas Pro",
        "email_body": "Nuevo interés registrado en la waitlist de OpenCanvas Pro.",
        "email_label": "Correo:",
        "success_msg": "Ya estás en la lista. Pronto habrá más novedades.",
        "warning_msg": "Por favor, ingresa un correo válido.",
    },
    "fr": {
        "hero_subcopy": "Conçu pour les équipes qui ne peuvent pas se permettre de se tromper dans leurs décisions fondées sur les données",
        "page_description": "La plateforme AutoML qui unit intégrité scientifique et navigation cognitive. Conçue pour des modèles à forte confiance.",
        "feature_title": "Plateforme de confiance & <span class=\"accent\">Différenciateurs clés</span>",
        "feature_subtitle_1": "OpenCanvas Pro est une startup brésilienne en construction, pensée pour transformer l'automatisation en confiance en réunissant AutoML, gouvernance, intégrité scientifique et audit technique pour les équipes qui ont besoin de clarté, pas de métriques flatteuses.",
        "feature_subtitle_2": "Nous ne sommes pas simplement une autre interface pour entraîner des modèles. Nous construisons une nouvelle catégorie de logiciel : une plateforme AutoML cognitive, auditable et centrée sur la confiance.",
        "benefit_brain_desc": "Un assistant contextuel doté d'un graphe de connaissances pour orienter la stratégie d'entraînement, faire remonter les risques et éviter les impasses statistiques.",
        "benefit_shield_desc": "Plus de 19 contrôles avancés pour les fuites de données, l'overfitting, les incohérences, le déséquilibre, les colonnes problématiques et les échecs de modélisation silencieux.",
        "benefit_file_desc": "Rapports exécutifs, contrats d'audit, documentation technique et traçabilité pour les environnements qui exigent une gouvernance réelle.",
        "benefit_sliders_desc": "Un pipeline prêt pour l'inférence par lots, l'export de modèles et un déploiement local-first, avec moins de friction.",
        "benefit_building_desc": "S'exécute dans l'infrastructure du client, avec un focus sur LGPD/GDPR, conformité, transparence et contrôle des données et des artefacts.",
        "pillars_title": "Piliers de <span class=\"accent\">Performance</span>",
        "pillars_subtitle": "Chaque pilier est conçu pour réduire la friction, renforcer la confiance et rendre le machine learning plus sûr pour les équipes techniques et exécutives.",
        "pillar_1_desc": "Chaque exécution peut produire une piste d'audit, un historique de transformation, des contrats techniques et un certificat d'intégrité scientifique pour étayer les décisions.",
        "pillar_2_desc": "Contrôle explicite des données, des étapes de préparation, des vérifications, des métriques et des artefacts. Pas de boîte noire déguisée en commodité.",
        "pillar_3_desc": "Architecture orientée performance locale, moins de friction opérationnelle et moindre dépendance au cloud pour les charges sensibles.",
        "pillar_1_title": "Audit Gold Standard",
        "pillar_2_title": "Transparence Opérationnelle",
        "pillar_3_title": "Efficacité des Ressources",
        "feature_label_brain": "Navigation cognitive (E.M.I.L.I.A.)",
        "feature_label_shield": "Bouclier d'intégrité scientifique™",
        "feature_label_file": "Artefacts de niveau direction",
        "feature_label_sliders": "Prédiction par lots et export de modèles",
        "feature_label_building": "Souveraineté IA locale d'abord",
        "waitlist_title": "Soyez parmi les premiers à découvrir OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro</span>",
        "waitlist_subtitle": "Nous préparons le lancement officiel. Laissez votre e-mail pour suivre l'évolution de la plateforme, les aperçus techniques et les nouveautés.",
        "waitlist_button": "PRÉVENEZ-MOI AU LANCEMENT",
        "waitlist_input": "Votre e-mail :",
        "waitlist_placeholder": "exemple@entreprise.com",
        "footer_main": "© OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro™</span> 2026 | <span class=\"footer-highlight\">Plateforme de Confiance AutoMLOps</span>",
        "footer_sub": "Plateforme en phase initiale | CNPJ 64.918.004/0001-36 | opencanvaspro.com<br>Conçue pour la science. Conçue pour la confiance. Propulsée par E.M.I.L.I.A.™ | <a href=\"mailto:contato@opencanvaspro.com\">contato@opencanvaspro.com</a>",
        "page_title": "OpenCanvas Pro | Cognitive AutoMLOps",
        "email_subject": "Nouvelle inscription sur la waitlist — OpenCanvas Pro",
        "email_body": "Un nouvel intérêt a été enregistré sur la waitlist d'OpenCanvas Pro.",
        "email_label": "E-mail :",
        "success_msg": "Vous êtes sur la liste. Plus de nouveautés bientôt.",
        "warning_msg": "Veuillez saisir un e-mail valide.",
    },
    "de": {
        "hero_subcopy": "Für Teams entwickelt, die sich bei datenbasierten Entscheidungen keinen Fehler leisten können",
        "page_description": "Die AutoML-Plattform, die wissenschaftliche Integrität und kognitive Navigation vereint. Für Modelle mit hohem Vertrauen entwickelt.",
        "feature_title": "Vertrauensplattform & <span class=\"accent\">Kernvorteile</span>",
        "feature_subtitle_1": "OpenCanvas Pro ist ein brasilianisches Startup im Aufbau, das Automatisierung in Vertrauen verwandeln soll: mit AutoML, Governance, wissenschaftlicher Integrität und technischer Auditierung für Teams, die Klarheit brauchen, nicht nur schöne Kennzahlen.",
        "feature_subtitle_2": "Wir sind nicht einfach nur eine weitere Oberfläche zum Trainieren von Modellen. Wir bauen eine neue Softwarekategorie: eine kognitive, prüfbare und vertrauenszentrierte AutoML-Plattform.",
        "benefit_brain_desc": "Ein kontextsensitiver Assistent mit Wissensgraph, der die Trainingsstrategie lenkt, Risiken sichtbar macht und Teams aus statistischen Sackgassen heraushält.",
        "benefit_shield_desc": "19+ erweiterte Prüfungen für Leckagen, Overfitting, Inkonsistenzen, Klassenungleichgewicht, problematische Spalten und stille Modellfehler.",
        "benefit_file_desc": "Führungsreife Berichte, Audit-Verträge, technische Dokumentation und Nachvollziehbarkeit für Umgebungen, die echte Governance verlangen.",
        "benefit_sliders_desc": "Eine produktionsreife Pipeline für Batch-Inferenz, Modellexport und Local-First-Deployment mit weniger Reibung.",
        "benefit_building_desc": "Läuft in der Infrastruktur des Kunden mit Fokus auf LGPD/GDPR, Compliance, Transparenz und Kontrolle über Daten und Artefakte.",
        "pillars_title": "Säulen der <span class=\"accent\">Leistung</span>",
        "pillars_subtitle": "Jede Säule ist darauf ausgelegt, Reibung zu reduzieren, Vertrauen aufzubauen und Machine Learning für technische und operative Teams sicherer zu machen.",
        "pillar_1_desc": "Jeder Lauf kann einen Audit-Trace, Transformationsverlauf, technische Verträge und ein wissenschaftliches Integritätszertifikat erzeugen, um Entscheidungen zu stützen.",
        "pillar_2_desc": "Explizite Kontrolle über Daten, Vorbereitungsschritte, Prüfungen, Metriken und Artefakte. Keine getarnte Blackbox.",
        "pillar_3_desc": "Architektur mit Fokus auf lokale Performance, weniger operative Reibung und geringere Cloud-Abhängigkeit für sensible Workloads.",
        "pillar_1_title": "Gold Standard Auditing",
        "pillar_2_title": "Operative Transparenz",
        "pillar_3_title": "Ressourceneffizienz",
        "feature_label_brain": "Kognitive Navigation (E.M.I.L.I.A.)",
        "feature_label_shield": "Schild für wissenschaftliche Integrität™",
        "feature_label_file": "Artefakte auf Leitungsebene",
        "feature_label_sliders": "Batch-Vorhersage und Modellexport",
        "feature_label_building": "Lokale KI-Souveränität",
        "waitlist_title": "Seien Sie früh mit dabei bei OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro</span>",
        "waitlist_subtitle": "Wir bereiten den offiziellen Launch vor. Hinterlassen Sie Ihre E-Mail, um die Entwicklung der Plattform, technische Einblicke und Neuigkeiten zu verfolgen.",
        "waitlist_button": "BEIM LAUNCH BENACHRICHTIGEN",
        "waitlist_input": "Ihre E-Mail:",
        "waitlist_placeholder": "beispiel@firma.de",
        "footer_main": "© OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro™</span> 2026 | <span class=\"footer-highlight\">Cognitive AutoMLOps Trust Platform</span>",
        "footer_sub": "Plattform in der Frühphase | CNPJ 64.918.004/0001-36 | opencanvaspro.com<br>Für Wissenschaft gebaut. Für Vertrauen gebaut. Angetrieben von E.M.I.L.I.A.™ | <a href=\"mailto:contato@opencanvaspro.com\">contato@opencanvaspro.com</a>",
        "page_title": "OpenCanvas Pro | Cognitive AutoMLOps",
        "email_subject": "Neue Anmeldung für die Warteliste — OpenCanvas Pro",
        "email_body": "Neues Interesse wurde für die OpenCanvas Pro-Warteliste registriert.",
        "email_label": "E-Mail:",
        "success_msg": "Sie stehen auf der Liste. Weitere Updates folgen bald.",
        "warning_msg": "Bitte geben Sie eine gültige E-Mail-Adresse ein.",
    },
    "hi": {
        "hero_subcopy": "उन टीमों के लिए बनाया गया है जिन्हें डेटा-आधारित फैसलों में बिल्कुल गलती की गुंजाइश नहीं है",
        "page_description": "वैज्ञानिक अखंडता और संज्ञानात्मक मार्गदर्शन को जोड़ने वाला AutoML प्लेटफ़ॉर्म। उच्च-विश्वास मॉडल के लिए तैयार।",
        "feature_title": "विश्वसनीय प्लेटफ़ॉर्म & <span class=\"accent\">मुख्य अंतर</span>",
        "feature_subtitle_1": "OpenCanvas Pro एक उभरती हुई ब्राज़ीलियाई कंपनी है, जो ऑटोमेशन को भरोसे में बदलने के लिए बनाई जा रही है: AutoML, शासन, वैज्ञानिक अखंडता और तकनीकी ऑडिटिंग को एक ही अनुभव में जोड़कर, उन टीमों के लिए जो केवल साफ़ मीट्रिक्स नहीं, असली स्पष्टता चाहती हैं।",
        "feature_subtitle_2": "हम सिर्फ मॉडल ट्रेन करने का एक और इंटरफ़ेस नहीं हैं। हम एक नई सॉफ़्टवेयर श्रेणी बना रहे हैं: एक संज्ञानात्मक, ऑडिटेबल और भरोसा-केंद्रित AutoML प्लेटफ़ॉर्म।",
        "benefit_brain_desc": "एक संदर्भ-सजग सहायक, जो नॉलेज ग्राफ़ के साथ प्रशिक्षण दिशा तय करने, जोखिम सामने लाने और टीम को सांख्यिकीय भटकावों से बचाने में मदद करता है।",
        "benefit_shield_desc": "लीकेज, ओवरफ़िटिंग, असंगतियों, असंतुलन, समस्याग्रस्त कॉलम और मूक मॉडलिंग विफलताओं के लिए 19+ उन्नत जाँचें।",
        "benefit_file_desc": "कार्यकारी-स्तर की रिपोर्टें, ऑडिट अनुबंध, तकनीकी दस्तावेज़ और ट्रेसबिलिटी - उन वातावरणों के लिए जहाँ असली governance चाहिए।",
        "benefit_sliders_desc": "बैच निष्पादन, मॉडल निर्यात और स्थानीय-प्रथम परिनियोजन के लिए तैयार उत्पादन-स्तरीय पाइपलाइन, कम रुकावट के साथ।",
        "benefit_building_desc": "क्लाइंट के अपने बुनियादी ढांचे में चलता है, LGPD/GDPR, अनुपालन, पारदर्शिता और डेटा/आर्टिफ़ैक्ट नियंत्रण पर पूरा ध्यान देता है।",
        "pillars_title": "प्रदर्शन के <span class=\"accent\">स्तंभ</span>",
        "pillars_subtitle": "हर स्तंभ घर्षण घटाने, भरोसा बढ़ाने और तकनीकी व कार्यकारी टीमों के लिए मशीन लर्निंग को अधिक सुरक्षित बनाने के लिए डिज़ाइन किया गया है।",
        "pillar_1_title": "गोल्ड-स्टैंडर्ड ऑडिटिंग",
        "pillar_2_title": "संचालन पारदर्शिता",
        "pillar_3_title": "संसाधन दक्षता",
        "pillar_1_desc": "हर रन ऑडिट ट्रेल, ट्रांसफ़ॉर्मेशन इतिहास, तकनीकी अनुबंध और वैज्ञानिक अखंडता प्रमाणपत्र तैयार कर सकता है, ताकि निर्णयों को मज़बूत आधार मिल सके।",
        "pillar_2_desc": "डेटा, तैयारी-चरणों, जाँचों, मेट्रिक्स और आर्टिफ़ैक्ट्स पर स्पष्ट नियंत्रण। सुविधा के नाम पर कोई ब्लैक बॉक्स नहीं।",
        "pillar_3_desc": "स्थानीय प्रदर्शन-केंद्रित आर्किटेक्चर, कम संचालनात्मक घर्षण और संवेदनशील कार्यभार के लिए क्लाउड पर कम निर्भरता।",
        "waitlist_title": "OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro</span> की झलक सबसे पहले पाएँ",
        "waitlist_subtitle": "हम आधिकारिक लॉन्च की तैयारी कर रहे हैं। प्लेटफ़ॉर्म की प्रगति, तकनीकी झलकियों और नए अपडेट्स के लिए अपना ईमेल जोड़ें।",
        "waitlist_button": "लॉन्च पर मुझे बताइए",
        "waitlist_input": "आपका ईमेल:",
        "waitlist_placeholder": "example@company.com",
        "footer_main": "© OpenCanvas <span class=\"accent\" style=\"color:#FF6B00;\">Pro™</span> 2026 | <span class=\"footer-highlight\">Cognitive AutoMLOps Trust Platform</span>",
        "footer_sub": "शुरुआती चरण का प्लेटफ़ॉर्म | CNPJ 64.918.004/0001-36 | opencanvaspro.com<br>विज्ञान के लिए बनाया गया। भरोसे के लिए बनाया गया। E.M.I.L.I.A.™ द्वारा संचालित | <a href=\"mailto:contato@opencanvaspro.com\">contato@opencanvaspro.com</a>",
        "page_title": "OpenCanvas Pro | Cognitive AutoMLOps",
        "email_subject": "नई waitlist साइनअप — OpenCanvas Pro",
        "email_body": "OpenCanvas Pro waitlist में नई रुचि दर्ज हुई है।",
        "email_label": "ईमेल:",
        "success_msg": "आप सूची में शामिल हो गए हैं। जल्द ही और अपडेट मिलेंगे।",
        "warning_msg": "कृपया वैध ईमेल दर्ज करें।",
        "feature_label_brain": "संज्ञानात्मक मार्गदर्शन (E.M.I.L.I.A.)",
        "feature_label_shield": "वैज्ञानिक अखंडता शील्ड™",
        "feature_label_file": "कार्यकारी-स्तर के आर्टिफ़ैक्ट्स",
        "feature_label_sliders": "बैच पूर्वानुमान और मॉडल निर्यात",
        "feature_label_building": "स्थानीय-प्रथम एआई संप्रभुता",
    },
}


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


def material_icon(name: str) -> str:
    icons = {
        "rocket-launch": "rocket_launch",
    }
    return icons[name]


def tr(lang: str, key: str) -> str:
    return I18N.get(lang, I18N["pt"]).get(key, I18N["pt"].get(key, ""))


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


def load_maturity_section(lang: str) -> str:
    if not os.path.exists(MATURITY_HTML_PATH):
        return ""

    with open(MATURITY_HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

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


def social_icon(name: str) -> str:
    icons = {
        "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.94 8.5H3.56V19h3.38zM5.25 3A1.97 1.97 0 1 0 5.3 6.94 1.97 1.97 0 0 0 5.25 3M20.44 11.12c0-2.93-1.56-4.3-3.65-4.3a3.16 3.16 0 0 0-2.87 1.58h-.05V8.5H10.5c.04.62 0 10.5 0 10.5h3.38v-5.86c0-.31.02-.62.12-.84.25-.62.82-1.27 1.77-1.27 1.25 0 1.75.96 1.75 2.37V19H21z"/></svg>',
        "x": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.9 2H22l-6.77 7.74L23.2 22h-6.26l-4.9-7.39L5.58 22H2.47l7.24-8.27L1.8 2h6.42l4.43 6.75zm-1.1 18h1.73L7.3 3.9H5.45z"/></svg>',
        "github": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5a12 12 0 0 0-3.79 23.39c.6.11.82-.26.82-.58v-2.03c-3.34.73-4.04-1.42-4.04-1.42-.55-1.38-1.33-1.75-1.33-1.75-1.09-.74.08-.72.08-.72 1.2.08 1.84 1.24 1.84 1.24 1.08 1.83 2.82 1.3 3.5.99.11-.78.42-1.3.76-1.6-2.67-.31-5.47-1.33-5.47-5.92 0-1.31.47-2.38 1.24-3.22-.12-.31-.54-1.56.12-3.26 0 0 1.01-.32 3.3 1.23A11.5 11.5 0 0 1 12 6.32c1.02 0 2.05.14 3.01.41 2.29-1.55 3.29-1.23 3.29-1.23.67 1.7.25 2.95.13 3.26.77.84 1.24 1.91 1.24 3.22 0 4.6-2.8 5.6-5.48 5.91.43.37.82 1.1.82 2.22v3.2c0 .32.22.7.83.58A12 12 0 0 0 12 .5"/></svg>',
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
          { property: "og:type", content: "website" },
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
    components.html(seo_script, height=0)

# =========================================================

logo_uri = file_to_data_uri(LOGO_PATH) if os.path.exists(LOGO_PATH) else ""
shield_uri = file_to_data_uri(SHIELD_PATH) if os.path.exists(SHIELD_PATH) else ""

if "ui_lang" not in st.session_state:
    st.session_state.ui_lang = "pt"

lang_bar_left, lang_bar_right = st.columns([9, 1], vertical_alignment="center")
with lang_bar_right:
    st.selectbox(
        "Language",
        options=list(LANG_LABELS.keys()),
        format_func=lambda code: LANG_LABELS[code],
        key="ui_lang",
        label_visibility="collapsed",
    )

lang = st.session_state.ui_lang
inject_seo_tags(lang)
maturity_section_html = load_maturity_section(lang)

st.markdown(
    """
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0,0");
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
            padding-top: 0.30rem !important;
            padding-bottom: 2rem !important;
            max-width: 1500px !important;
        }

        h1, h2, h3, h4, h5, h6, p, li, span, label, div {
            font-family: "Inter", "Noto Sans Devanagari", sans-serif !important;
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

        .hero-title-row {
            display: grid;
            grid-template-columns: 132px 1fr 132px;
            align-items: center;
            width: 100%;
            column-gap: 0.65rem;
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

        .hero-title .white {
            color: var(--ocp-white) !important;
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
            color: var(--ocp-orange) !important;
            font-size: 0.98rem;
            max-width: 900px;
            margin: 0.25rem auto 0 auto;
            line-height: 1.68;
            font-weight: 700;
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
            .hero-title-row {
                grid-template-columns: 88px 1fr 88px;
                column-gap: 0.35rem;
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
st.markdown(
    f"""
    <div class="hero-copy-wrap">
        <div class="hero-title-row">
            <img src="{logo_uri}" class="hero-title-logo" alt="OpenCanvas Pro Logo" />
            <div class="hero-title">OpenCanvas <span class="white"> </span><span class="accent">Pro - Cognitive AutoMLOps</span></div>
            <div class="hero-title-spacer" aria-hidden="true"></div>
        </div>
        <div class="hero-kicker">TRUST PLATFORM FOR SCIENTIFIC INTEGRITY</div>
        <div class="hero-subcopy">
            {tr(lang, "hero_subcopy")}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

        

st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)

        

# =========================================================
# MAIN VALUE SECTION
# =========================================================
st.markdown(
    '''
    <div class="feature-intro">
        <div class="section-title">''' + tr(lang, "feature_title") + '''</div>
        <div class="section-subtitle">
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
if maturity_section_html:
    st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)
    components.html(maturity_section_html, height=1120, scrolling=False)

# =========================================================
# WAITLIST
# =========================================================
st.markdown('<div class="ocp-section-rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="waitlist-wrap">', unsafe_allow_html=True)
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
            if email and "@" in email:
                ok, msg = send_waitlist_email(email, lang)
                if ok:
                    st.success(f"✔ {tr(lang, 'success_msg')}")
                else:
                    st.error(f"Não foi possível registrar agora: {msg}")
            else:
                st.warning(tr(lang, "warning_msg"))

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
        <div class="footer-main">""" + tr(lang, "footer_main") + """</div>
        <div class="footer-sub">
            """ + tr(lang, "footer_sub") + """
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
