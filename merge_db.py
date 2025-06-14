import sqlite3

conn = sqlite3.connect("db.sqlite3")
conn.execute("ATTACH DATABASE 'old_db.sqlite3' AS old")

# Table and columns (excluding 'id')
table = "proplistpage_propertyimage"
columns = ["property_id", "image", "caption"]  # <- Update based on actual output

col_str = ", ".join(columns)

try:
    conn.execute(f"""
    INSERT INTO {table} ({col_str})
    SELECT {col_str} FROM old.{table}
    """)
    print(f"✅ Merged table: {table}")
except Exception as e:
    print(f"❌ Failed to merge table {table}: {e}")

conn.commit()
conn.close()

print("✅ Merge complete.")
