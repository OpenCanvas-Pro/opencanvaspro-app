# 🏗️ OpenCanvas Pro — Arquitetura do Sistema

![Architecture](https://img.shields.io/badge/Architecture-System%20Design-blue)
![AutoML](https://img.shields.io/badge/AutoML-PyCaret-orange)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)
![Cloud](https://img.shields.io/badge/Cloud-Agnostic-lightgrey)
![Open Source](https://img.shields.io/badge/Open%20Source-MIT-green)

**Última atualização:** 31 de janeiro de 2026

Este documento descreve a arquitetura do **OpenCanvas Pro**, uma plataforma de AutoML open-source projetada para ser **simples para o usuário**, **modular internamente** e **segura para execução pública**.

O foco do design é:

- facilidade de uso
- transparência técnica
- extensibilidade futura
- estabilidade em ambiente multiusuário

---

## 🎯 Visão Geral

O OpenCanvas Pro segue uma arquitetura **UI-first**, onde toda a experiência acontece no navegador, sem necessidade de configuração de infraestrutura pelo usuário.

**Fluxo principal de execução:**

Usuário (Browser)
↓
Interface Web (Streamlit)
↓
Preparação de Dados
↓
AutoML Engine (PyCaret)
↓
Predições • Visualizações • Exportações

---

## 🧩 Componentes Principais

### 1. Interface do Usuário (UI)

**Tecnologia:** Streamlit

Responsável por:

- Upload de datasets (CSV / Parquet)
- Navegação por abas (Dados, Modelo, Predições, Guia)
- Configuração visual do AutoML
- Exibição de métricas, gráficos e resultados
- Consentimento de cookies (LGPD)

Arquivos principais:

- `app.py`
- `opencanvaspro/ui/layout.py`
- `opencanvaspro/ui/styles.css`
- `opencanvaspro/pages/*.py`

---

### 2. Camada de Preparação de Dados

Responsável por transformar dados brutos em datasets prontos para AutoML.

Funcionalidades:

- Conversão automática CSV → Parquet
- Otimização de tipos (`optimize_dtypes`)
- Exclusão de colunas (IDs / leakage)
- Tratamento guiado de datas
- Imputação manual e automática
- Relatório de saúde do dataset

Arquivos principais:

- `opencanvaspro/core/preprocess.py`
- `opencanvaspro/core/io.py`

---

### 3. AutoML Engine

**Tecnologia:** PyCaret 3.x

Responsável por:

- Auto-detecção do tipo de problema
- Setup do experimento
- Comparação automática de modelos
- Treinamento otimizado (modo rápido vs completo)
- Geração de métricas e artefatos

Arquivos principais:

- `opencanvaspro/core/automl.py`

---

### 4. Visualizações & Interpretabilidade

Os gráficos são gerados pelo PyCaret e integrados de forma segura ao Streamlit.

Tipos de visualizações:

- Classificação: Matriz de Confusão, ROC, PR Curve
- Regressão: Resíduos, Predito vs Real, SHAP
- Clustering: Elbow, Silhouette, PCA
- Anomalia: PCA, t-SNE, UMAP
- Séries Temporais: Forecast, ACF, PACF, Decomposição

A renderização é protegida por *fallbacks*, evitando que erros de gráfico quebrem a interface.

---

### 5. Predição & Exportação

Responsável por transformar modelos treinados em resultados utilizáveis.

Funcionalidades:

- Batch prediction
- Exportação CSV e Parquet
- Exportação de modelo `.pkl`
- Geração automática de arquivos **Kaggle-ready**

Arquivos principais:

- `opencanvaspro/pages/predict_tab.py`
- `opencanvaspro/core/automl.py`
- `opencanvaspro/core/kaggle_exporter.py`

---

### 6. Telemetria & Compliance

O OpenCanvas Pro utiliza **Google Analytics 4** de forma opcional e transparente.

Características:

- Consentimento explícito (opt-in)
- Cookies persistentes
- Eventos deduplicados
- Sem coleta de dados sensíveis

Arquivos principais:

- `opencanvaspro/core/analytics.py`
- `opencanvaspro/core/consent.py`

---

## 🔐 Segurança & Estabilidade

- Hard block por tamanho de dataset
- Prevenção de uso excessivo de memória
- Nenhuma execução arbitrária de código do usuário
- Ambiente isolado por sessão do Streamlit

---

## 🔮 Evolução Planejada

- Login OAuth (Google / Microsoft)
- Persistência de usuários (Firebase)
- Execução assíncrona de treinos
- Fila de jobs e workers
- Deploy de modelos como API

---

## 📌 Considerações Finais

O OpenCanvas Pro foi projetado para **escala educacional e experimental**, sem sacrificar boas práticas de engenharia.

> *Simplicidade na interface. Clareza na arquitetura. Liberdade no uso.*
