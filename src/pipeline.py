import json
import duckdb
from kroger_client import KrogerAPIClient

DB_PATH = "data/inventory.duckdb"

def run_bronze_ingestion(terms=None):
    if terms is None:
        terms = ["milk", "bread", "eggs", "apple", "chicken"]

    client = KrogerAPIClient()
    raw_records = []

    print("Fetching live data from Kroger API...")
    for term in terms:
        try:
            products = client.search_products(term=term, limit=10)
            for item in products:
                raw_records.append({
                    "search_term": term,
                    "raw_json": json.dumps(item)
                })
        except Exception as e:
            print(f"Error fetching '{term}': {e}")

    conn = duckdb.connect(DB_PATH)

    # Bronze Layer: Raw JSON storage
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bronze_inventory (
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            search_term VARCHAR,
            raw_json VARCHAR
        )
    """)

    # Append new records
    for record in raw_records:
        conn.execute(
            "INSERT INTO bronze_inventory (search_term, raw_json) VALUES (?, ?)",
            [record["search_term"], record["raw_json"]]
        )

    count = conn.execute("SELECT count(*) FROM bronze_inventory").fetchone()[0]
    conn.close()
    print(f"Bronze Ingestion Complete! Total raw records in database: {count}")

if __name__ == "__main__":
    run_bronze_ingestion()