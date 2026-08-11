import duckdb
from fastapi import FastAPI
from src.ai_agent import InventoryAIAgent

app = FastAPI(title="Retail Supply Chain AI API")
DB_PATH = "data/inventory.duckdb"
agent = InventoryAIAgent()

@app.get("/api/gold/anomalies")
def get_anomalies():
    conn = duckdb.connect(DB_PATH)
    df = conn.execute("SELECT * FROM gold_inventory_anomalies").df()
    conn.close()
    return df.to_dict(orient="records")

@app.get("/api/ai/executive-summary")
def get_ai_summary():
    report = agent.get_gold_anomalies_summary()
    return {"summary": report}