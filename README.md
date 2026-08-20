# Retail Supply Chain AI Agent & Medallion Data Pipeline

An end-to-end data engineering and AI agent application that ingests retail inventory data into a DuckDB Medallion Architecture (Bronze -> Silver -> Gold), detects low-stock anomalies, and generates automated Purchase Orders using Groq and Streamlit.

Live Application: [Launch Streamlit Web App](https://retail-supply-chain-agent-8z2pvjcmwdgzshy4hgnupc.streamlit.app/)

Architecture

    Bronze Layer: Raw inventory ingestion into DuckDB.

    Silver Layer: Cleaned, structured, and normalized data tables.

    Gold Layer: Low-stock anomaly detection (CRITICAL <5 units, WARNING <15 units).

    AI Agent: Groq API (llama-3.3-70b-versatile) for executive purchase order reports.

    UI & API: Streamlit dashboard and API integration points.

Setup & Local Execution
1. Clone the Repository:
```Bash

git clone https://github.com/np258/retail-supply-chain-agent.git
cd retail-supply-chain-agent
```
2. Install Dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure Secrets:
Add your API key to .streamlit/secrets.toml:
```
Ini, TOML

GROQ_API_KEY = "your_groq_api_key_here"
```
4. Run App:
```
streamlit run src/app.py
```
