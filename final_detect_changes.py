import duckdb
import pandas as pd

# Step 1: Connect to DuckDB
conn = duckdb.connect(database=':memory:', read_only=False)

# Step 2: Read CSV file into a Pandas DataFrame
csv_file_path1 = 'file_previous_date.csv' 
csv_file_path2 = 'file_current_date.csv' 

df1 = pd.read_csv(csv_file_path1)
df2 = pd.read_csv(csv_file_path2)

# Step 3: Create a DuckDB table from the DataFrame
conn.register('old_data_table', df1)
conn.register('new_data_table', df2)

# Step 4: Run Select Queries
# query1 = 'SELECT * FROM example'
query1 = "SELECT * FROM old_data_table WHERE lastmod = '2022-08-08'"
query2 = "SELECT * FROM new_data_table WHERE lastmod = '2022-08-08'"

result1 = conn.execute(query1).fetchdf()
print('Old table data: ', result1)
result2 = conn.execute(query2).fetchdf()
print('New table data: ', result2)

join_query = """
SELECT t2.loc
FROM new_data_table t2
LEFT JOIN old_data_table t1 ON t1.loc = t2.loc AND t1.lastmod = t2.lastmod
WHERE t2.lastmod = '2022-08-08' AND t1.loc IS NULL
"""
join_result = conn.execute(join_query).fetchdf()
print("----------------------")
print('join_result: ', join_result)

# Step 6: Close the connection
conn.close()
