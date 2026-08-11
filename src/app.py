import streamlit as st
import duckdb
import pandas as pd
from ai_agent import InventoryAIAgent

st.set_page_config(page_title="Retail Supply Chain AI Agent", layout="wide")

st.title("Retail Supply Chain AI Agent & Medallion Pipeline")

st.sidebar.header("Navigation")
option = st.sidebar.radio("View Section", ["Gold Anomalies", "AI Purchase Order Generator"])

DB_PATH = "data/inventory.duckdb"

@st.cache_data
def load_gold_data():
    # If DB doesn't exist on Cloud container, run your pipeline build script first
    if not os.path.exists(DB_PATH):
        # Import and run your pipeline setup function here if available
        # e.g., from src.pipeline import run_pipeline; run_pipeline()
        st.error(f"Database file not found at {DB_PATH}. Ensure data pipeline generates the file.")
        st.stop()
        
    conn = duckdb.connect(DB_PATH)
    df = conn.execute("SELECT * FROM gold_inventory_anomalies").df()
    conn.close()
    return df

if option == "Gold Anomalies":
    st.subheader("Gold Layer: Low-Stock Inventory Anomalies")
    df = load_gold_data()

    # Key Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Flagged Items", len(df))
    col2.metric("Critical Items (<5 units)", len(df[df['anomaly_status'] == 'CRITICAL']))
    col3.metric("Warning Items (<15 units)", len(df[df['anomaly_status'] == 'WARNING']))

    st.dataframe(df, use_container_width=True)

elif option == "AI Purchase Order Generator":
    st.subheader("Groq AI Supply Chain Assistant")
    if st.button("Generate Executive Report & Purchase Orders"):
        with st.spinner("Analyzing Gold layer anomalies via Groq Llama 3.3..."):
            agent = InventoryAIAgent()
            report = agent.get_gold_anomalies_summary()
            st.markdown(report)