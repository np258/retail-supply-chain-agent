import os
import duckdb
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "data/inventory.duckdb"

class InventoryAIAgent:
    def __init__(self):
        api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def get_gold_anomalies_summary(self):
        conn = duckdb.connect(DB_PATH)
        anomalies = conn.execute("SELECT * FROM gold_inventory_anomalies").df().to_dict(orient="records")
        conn.close()

        prompt = f"""
        You are an Enterprise ERP Supply Chain Assistant. 
        Below is a JSON list of inventory items flagged with low stock anomalies:

        {anomalies}

        Task:
        1. Provide an executive summary of critical stock shortages.
        2. Draft a Purchase Order Reorder Request table with Product ID, Description, Suggested Reorder Qty, and Estimated Cost.
        3. Keep the tone concise, clear, and professional.
        """

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful supply chain and data engineering assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    agent = InventoryAIAgent()
    print(agent.get_gold_anomalies_summary())