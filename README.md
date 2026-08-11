# Retail Supply Chain AI Agent & Medallion Data Pipeline

An end-to-end data engineering and AI agent application that ingests retail inventory data into a DuckDB Medallion Architecture (Bronze -> Silver -> Gold), detects low-stock anomalies, and generates automated Purchase Orders using **Groq (Llama 3.3 70B)** and **Streamlit**.

## Architecture
- **Bronze Layer:** Ingests raw API inventory responses into DuckDB.
- **Silver Layer:** Cleaned, structured, and normalized data tables.
- **Gold Layer:** Business modeling & low-stock anomaly identification.
- **AI Agent:** Groq API (`llama-3.3-70b-versatile`) generates executive reorder reports.
- **UI & API:** Streamlit dashboard and FastAPI REST backend.

## Setup & Local Execution
1. Clone the repository:
   ```bash
   git clone [https://github.com/np258/retail-supply-chain-agent.git](https://github.com/np258/retail-supply-chain-agent.git)
   cd retail-supply-chain-agent
