import duckdb
import pandas as pd

# Step 1: Connect to DuckDB
conn = duckdb.connect(database=':memory:', read_only=False)

# Step 2: Read CSV file into a Pandas DataFrame
csv_file_path1 = 'file_current_date.csv' 
csv_file_path2 = 'file_previous_date.csv' 

df1 = pd.read_csv(csv_file_path1)
df2 = pd.read_csv(csv_file_path2)

# Step 3: Create a DuckDB table from the DataFrame
conn.register('table1', df1)
conn.register('table2', df2)

join_query = """
SELECT t2.loc
FROM table2 t2
LEFT JOIN table1 t1 ON t1.loc = t2.loc AND t1.lastmod = t2.lastmod
WHERE t2.lastmod = '2022-08-08' AND t1.loc IS NULL
"""
join_result = conn.execute(join_query).fetchdf()
print("----------------------")
print('join_result: ', join_result)

# Step 6: Close the connection
conn.close()
