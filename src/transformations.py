import json
import duckdb

DB_PATH = "data/inventory.duckdb"

def process_medallion_layers():
    conn = duckdb.connect(DB_PATH)

    # 1. Silver Layer: Cleaned, structured products
    conn.execute("""
        CREATE TABLE IF NOT EXISTS silver_inventory (
            product_id VARCHAR PRIMARY KEY,
            brand VARCHAR,
            description VARCHAR,
            category VARCHAR,
            price DOUBLE,
            stock_level INT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Parse raw JSON from Bronze
    raw_rows = conn.execute("SELECT raw_json FROM bronze_inventory").fetchall()
    for row in raw_rows:
        data = json.loads(row[0])
        prod_id = data.get("productId", "UNKNOWN")
        brand = data.get("brand", "Generic")
        description = data.get("description", "No description")

        # Extract category if present
        categories = data.get("categories", [])
        category = categories[0] if categories else "General"

        # Extract pricing (mock fallback if unlisted)
        items = data.get("items", [])
        price = 3.99
        if items and "price" in items[0]:
            price = items[0]["price"].get("regular", 3.99)

        # Generate synthetic stock level (simulating ERP inventory)
        stock_level = (hash(prod_id) % 40) + 2  # Range 2 to 41

        conn.execute("""
            INSERT OR REPLACE INTO silver_inventory 
            (product_id, brand, description, category, price, stock_level)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [prod_id, brand, description, category, price, stock_level])

    # 2. Gold Layer: Low-stock anomalies (< 15 units)
    conn.execute("DROP TABLE IF EXISTS gold_inventory_anomalies")
    conn.execute("""
        CREATE TABLE gold_inventory_anomalies AS
        SELECT 
            product_id,
            brand,
            description,
            category,
            price,
            stock_level,
            CASE 
                WHEN stock_level < 5 THEN 'CRITICAL'
                WHEN stock_level < 15 THEN 'WARNING'
                ELSE 'OK'
            END AS anomaly_status,
            (25 - stock_level) AS suggested_reorder_qty
        FROM silver_inventory
        WHERE stock_level < 15
    """)

    silver_cnt = conn.execute("SELECT count(*) FROM silver_inventory").fetchone()[0]
    gold_cnt = conn.execute("SELECT count(*) FROM gold_inventory_anomalies").fetchone()[0]
    conn.close()

    print(f"Medallion Transformation Complete!")
    print(f"Silver Table: {silver_cnt} products | Gold Anomalies: {gold_cnt} items requiring reorder")

if __name__ == "__main__":
    process_medallion_layers()