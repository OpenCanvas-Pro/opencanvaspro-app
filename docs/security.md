# 🔐 Segurança — OpenCanvas Pro

![Security](https://img.shields.io/badge/Security-Best%20Effort-blue)
![Open Source](https://img.shields.io/badge/Open%20Source-MIT-lightgrey)
![Hosting](https://img.shields.io/badge/Hosting-Streamlit%20Community%20Cloud-purple)
![Compliance](https://img.shields.io/badge/Compliance-LGPD%20%7C%20GDPR-green)

**Última atualização:** 31 de janeiro de 2026

O **OpenCanvas Pro** adota práticas de segurança compatíveis com seu propósito: uma plataforma gratuita, open-source e educacional de AutoML, priorizando proteção de dados, transparência e responsabilidade.

---

## 1. Princípios de segurança

O OpenCanvas Pro é desenvolvido com base nos seguintes princípios:

- **Minimização de dados**  
  Apenas os dados estritamente necessários são processados.

- **Processamento temporário**  
  Datasets enviados são utilizados apenas durante a sessão ativa.

- **Transparência**  
  O código é open-source e auditável pela comunidade.

- **Sem lock-in**  
  Nenhum dado do usuário é retido para fins comerciais.

---

## 2. Armazenamento e processamento de dados

- Os dados enviados são processados **em memória ou armazenamento temporário**
- Nenhum dataset é armazenado permanentemente por padrão
- Modelos treinados pertencem exclusivamente ao usuário
- Logs técnicos não contêm dados sensíveis ou datasets

---

## 3. Autenticação e contas (quando aplicável)

Quando funcionalidades de login estiverem habilitadas:
- autenticação será realizada via provedores confiáveis (ex.: Google, Microsoft)
- o OpenCanvas Pro não armazena senhas
- tokens e credenciais seguem boas práticas de segurança

---

## 4. Cookies e analytics

- Cookies essenciais são utilizados para funcionamento da aplicação
- Cookies analíticos (Google Analytics 4) **só são ativados com consentimento**
- Nenhuma informação pessoal identificável é coletada

Consulte:
- `docs/PRIVACY.md`
- `docs/COOKIES.md`

---

## 5. Infraestrutura

O OpenCanvas Pro utiliza serviços amplamente adotados e confiáveis:

- **Streamlit Community Cloud** (hospedagem)
- **Cloudflare** (DNS, HTTPS, proteção básica)
- **GitHub** (controle de versão e transparência)

---

## 6. Limitações conhecidas

Por se tratar de um serviço gratuito e open-source:
- não há garantia de disponibilidade contínua
- não há SLA formal
- recursos computacionais podem ser limitados
- datasets muito grandes podem ser bloqueados preventivamente

Essas limitações existem para garantir estabilidade e uso justo.

---

## 7. Responsabilidade do usuário

O usuário é responsável por:
- não enviar dados pessoais sensíveis
- não enviar informações confidenciais ou protegidas
- garantir que possui direito de uso sobre os dados

O OpenCanvas Pro não se responsabiliza por uso indevido.

---

## 8. Reportando vulnerabilidades

Se você identificar uma vulnerabilidade de segurança, pedimos que **não a explore**.

Entre em contato de forma responsável:

📧 **contato@opencanvaspro.com**

Relatos serão analisados com prioridade.

---

## 9. Atualizações deste documento

Esta política pode ser atualizada conforme a evolução do projeto.  
A data de atualização será sempre informada no topo do documento.

---

## 🛡️ Compromisso

> Segurança não é promessa absoluta.  
> É compromisso contínuo com boas práticas, transparência e respeito ao usuário.
