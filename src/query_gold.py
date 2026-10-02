import duckdb

con = duckdb.connect("data/gold/analytics.duckdb")

print("\nTABLES:")
print(con.execute("SHOW TABLES").fetchdf())

print("\nMONTHLY SALES:")
print(con.execute("""
    SELECT *
    FROM monthly_sales
    ORDER BY order_month
""").fetchdf())

print("\nTOP CATEGORIES:")
print(con.execute("""
    SELECT *
    FROM category_sales
    ORDER BY revenue DESC
""").fetchdf())

print("\nREGION SALES:")
print(con.execute("""
    SELECT *
    FROM region_sales
    ORDER BY revenue DESC
""").fetchdf())

con.close()