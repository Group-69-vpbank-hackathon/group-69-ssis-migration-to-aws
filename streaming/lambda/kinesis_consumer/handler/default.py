import json

def handle(data, metadata, cur, conn):
    table = metadata.get("table-name", "unknown")

    cols = list(data.keys())
    vals = [
        json.dumps(data[col], ensure_ascii=False) if isinstance(data[col], dict) else data[col]
        for col in cols
    ]

    insert_cols = ', '.join([f'"{col}"' for col in cols])
    insert_vals = ', '.join(['%s'] * len(cols))
    set_cols = ', '.join([f"{col}=EXCLUDED.{col}" for col in cols if col != 'ID'])
    
    sql = f"""
        INSERT INTO "{table}" ({insert_cols})
        VALUES ({insert_vals})
        ON CONFLICT ("ID") 
        DO UPDATE SET {set_cols};
    """
    cur.execute(sql, vals)
    conn.commit()
    print(f"✅ Default insert for table '{table}'")
