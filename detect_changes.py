# to install: pip install duckdb
import pandas as pd
import duckdb



# con = duckdb.connect(database=':memory:')
# con.execute("COPY INTO your_table
# FROM 'your_file.csv'
# WITH (FORMAT csv, HEADER = TRUE);
# ")


# duckdb.query()

import duckdb
import pandas as pd

# Function to create a DuckDB table from a CSV file
def create_table_from_csv(connection, csv_file_path, table_name):
    # Read CSV into a Pandas DataFrame
    df = pd.read_csv(csv_file_path)
    print('df: ', df.head(1))

    # Extract column names from the first row
    # column_names = df.columns.tolist()
    # print('column_names: ', column_names)

    # Create DuckDB table from the DataFrame
    # df.to_sql(table_name, connection, index=False, if_exists='replace',columns=columns)


    #  Create DuckDB table with specified column names
    if columns is not None:
        column_definitions = ', '.join(f'{col} VARCHAR' for col in columns)
        create_table_query = f'CREATE TABLE {table_name} ({column_definitions})'
        connection.execute(create_table_query)

    # Insert data into the DuckDB table
    df.to_sql(table_name, connection, index=False, if_exists='replace')


# Function to perform a search operation on the DuckDB table
def search_table(connection, table_name, column_name, search_value):
    # query = f'SELECT * FROM {table_name} where "{column_name}"="{search_value}"'
    # print('query: ', query)

    query = f"PRAGMA table_info({table_name})"  #getting column name

    # query = f"SELECT * FROM {table_name}"
    # print('query: ', query)

    result = connection.execute(query).fetchall()
    # print('result: ', result)
    return result

# Connect to DuckDB (this will create an in-memory database)
con = duckdb.connect(database=':memory:')

# Define CSV file path, table name, and search criteria
csv_file_path = 'your_output_neww.csv'  # Replace with your CSV file path
table_name = 'temp_table'         # Replace with your desired table name
search_column = 'lastmod'     # Replace with the column to search
search_value = '2023-10-18'    # Replace with the value to search for
columns = ["loc","lastmod","changefreq","priority"]

# Step 1: Create DuckDB table from CSV
create_table_from_csv(con, csv_file_path, table_name)

# Step 2: Search operation on the table
result = search_table(con, table_name, search_column, search_value)

# Display the result
print(result)

# Close the connection
con.close()
