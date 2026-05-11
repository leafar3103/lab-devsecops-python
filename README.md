# 🛡️ Lab DevSecOps: Python Flask Security Pipeline

Este repositório é um laboratório prático de **DevSecOps**, focado na implementação de uma esteira de CI/CD blindada (Shift Left) para uma aplicação Python/Flask propositalmente vulnerável (OWASP Top 10).

## 🚀 Tecnologias e Ferramentas
- **Linguagem:** Python 3.12+ (Gerenciado via [uv](https://astral.sh))
- **Framework:** Flask
- **Orquestração CI/CD:** GitHub Actions
- **Infraestrutura Local:** WSL2 (Kali Linux) / Proxmox
- **Análise de Dados:** Pandas & Streamlit

## 🏗️ Estrutura do Projeto
```text
├── .github/workflows/    # Esteira de segurança (YAML)
├── src/                  # Código-fonte e Dashboard Analytics
├── public/               # Artefatos e Reports de segurança (Ignorado pelo Git)
├── pyproject.toml        # Gestão moderna de dependências com UV
└── uv.lock               # Snapshot determinístico do ambiente
```

## 🔒 Controles de Segurança Implementados

### 1. Shift Left (Análise Local)
- **SonarLint:** Feedback em tempo real na IDE para detecção de falhas de código.
- **UV Sync:** Isolamento de ambiente e garantia de integridade das bibliotecas via Checksums.

### 2. Pipeline de Segurança (GitHub Actions)
A cada `push` ou `PR`, a esteira executa automaticamente:
- **SAST (Static Application Security Testing):** O **Bandit** varre o código em busca de falhas como SQL Injection e XSS.
- **SCA (Software Composition Analysis):** O **Trivy** analisa o `uv.lock` em busca de dependências com CVEs conhecidas.
- **SBOM (Software Bill of Materials):** Geração automática de inventário no padrão **CycloneDX (JSON)**.
- **Security Gate:** O pipeline é bloqueado (Exit Code 1) se falhas de severidade **CRITICAL** ou **HIGH** forem detectadas.

### 3. Visibilidade e Gestão
- **GitHub Pages:** Publicação automática do relatório HTML do Bandit.
- **Issue Automation:** Abertura automática de Issues no GitHub caso o scan de dependências encontre vulnerabilidades críticas.
- **GitHub Artifacts:** Armazenamento dos arquivos JSON para auditoria e análise de dados posterior.

## 📊 Dashboard Analytics (Streamlit + Pandas)
Desenvolvemos uma ferramenta de análise local para consumir os dados do pipeline:
- **Input:** Arquivo `sbom.json` gerado pelo Trivy.
- **Processamento:** Normalização de dados aninhados via **Pandas**.
- **Visualização:** Gráficos interativos em **Streamlit/Plotly** mostrando a distribuição de severidade das falhas detectadas.

---

## 🛠️ Como rodar o Dashboard Localmente

1. **Baixe o Artefato:** Vá na aba *Actions* do GitHub e baixe o `security-reports`.
2. **Extraia os Dados:** Coloque o arquivo `sbom.json` na pasta `public/`.
3. **Instale as dependências:**
   ```bash
   uv sync
   ```
4. **Execute:**
   ```bash
   uv run streamlit run src/dashboard.py
   ```
