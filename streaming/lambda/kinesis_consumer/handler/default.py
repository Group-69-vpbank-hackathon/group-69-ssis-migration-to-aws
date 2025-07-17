import json
from psycopg2.extras import execute_values

def handle(records, cur, conn):
    if not records:
        return

    # Lấy table name từ record đầu tiên (vì cùng bảng)
    table = records[0][1].get("table-name", "unknown")

    # Chuẩn hóa dữ liệu
    data_list = [r[0] for r in records]
    columns = list(data_list[0].keys())

    # Chuyển dict thành list các tuple giá trị
    values = []
    for data in data_list:
        row = [
            json.dumps(data[col], ensure_ascii=False) if isinstance(data[col], dict) else data[col]
            for col in columns
        ]
        values.append(tuple(row))

    # SQL insert
    insert_cols = ', '.join([f'"{col}"' for col in columns])
    set_cols = ', '.join([f'"{col}"=EXCLUDED."{col}"' for col in columns if col != "ID"])
    sql = f"""
        INSERT INTO "{table}" ({insert_cols})
        VALUES %s
        ON CONFLICT ("ID")
        DO UPDATE SET {set_cols};
    """

    # Ghi batch vào DB
    execute_values(cur, sql, values)
    conn.commit()
    print(f"✅ Batch insert {len(values)} rows into '{table}'")
