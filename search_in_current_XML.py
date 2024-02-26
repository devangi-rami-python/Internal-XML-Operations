import click
from datetime import datetime
import duckdb
import pandas as pd
import os
import csv
import xml.etree.ElementTree as ET
from scripts.download_xml import download_current_date_xml
import subprocess

def xml_to_csv(xml_file_path=None, csv_name=None):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        csv_file = "./input_files/" + csv_name + '.csv'

        with open(csv_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write header row
            header = []
            for child in root[0]:
                # Extracting local name of the XML tag
                column_name = child.tag.split('}')[1] if '}' in child.tag else child.tag
                header.append(column_name)
            csv_writer.writerow(header)

            # Write data rows
            for element in root:
                row = []
                for child in element:
                    row.append(child.text)
                csv_writer.writerow(row)
    
        return csv_file
    except Exception as e:
        click.echo("Error: step xml_to_csv - ",e)
        return


def duckdb_query(current_date_file_path,find_date):
        try:
            ## Read CSV file into a Pandas DataFrame
            df = pd.read_csv(current_date_file_path)

            ## DuckDB Oprations
            conn = duckdb.connect(database=':memory:', read_only=False) # Connect to DuckDB

            # Create a DuckDB table from the DataFrame
            conn.register('data_table', df)

            # Step 4: Run Select Queries
            # Step 4: Run Select Queries with a parameter
            join_query = """
            SELECT *
            FROM data_table 
            WHERE lastmod = ?
            """

            # Define the parameter
            parameter = (find_date,)

            # Execute the query with the parameter
            join_result = conn.execute(join_query, parameter).fetchdf()

            # Write the result to a file
            with open('output/current_date_output.txt', 'w') as f:
                f.write(f"find_date: {find_date}\n")  # Write the find_date
                f.write(f"-----------------------\n")  # Write the find_date
                f.write(join_result.to_string(index=False))

            # Step 6: Close the connection
            conn.close()
        except Exception as e:
            click.echo("Error: step duckdb_query - ",e)
            return

def check_if_xml_exist(input_date):
    # Check XML file exists in our system or not matched with input requsted
    folder_path = 'input_files'

    # process file 1
    input_date_file_name = input_date + '.xml'
    input_date_file_path = os.path.join(folder_path, input_date_file_name)
    if not os.path.exists(input_date_file_path):
        return False, ''
    
    return True,input_date_file_path


@click.command()
@click.option('--find_date', help='Find date in YYYY-MM-DD format')
def main(find_date):
    if find_date:
        ## Step 1: Validate Inputs
        try:
            # Parse the date strings
            find_date_parsed = datetime.strptime(find_date, "%Y-%m-%d")
            current_date = datetime.now().date()

        except ValueError as e:
            click.echo("Error: Invalid date format in input command. Please provide dates in YYYY-MM-DD format.")
            return
        
        download_current_date_xml()

        ## Step 3: check_if_xml_exist
        if_xml_exist, current_date_file_path = check_if_xml_exist(str(current_date))
        if not if_xml_exist:
            print(f"Error: The file {current_date}.xml does not exist in the folder - '/input_files'.")
            return


        ## Step 4: Convert XML to CSV 
        csv_file_old_date_path = xml_to_csv(current_date_file_path,str(current_date))

        ## Step 5: perform query on CSV files with duckDB 
        duckdb_query(csv_file_old_date_path,find_date)
        print("Done: Successfully generated output.txt")

        print("Git Push --")
        
        subprocess.run(["git", "config", "user.email", "devangi.rami@bacancy.com"])
        subprocess.run(["git", "config", "user.name", "Devangi Rami"])
        subprocess.run(["git", "status"])


        # Change directory to the root of the Git repository
        os.chdir("/home/runner/work/Internal-XML-Operations/Internal-XML-Operations/")
        
        # Stage the new XML file
        subprocess.run(["git", "add", "."])
        
        # Commit the changes
        subprocess.run(["git", "commit", "-m", f"Saved current_date_output.txt"])
        
        # Push the changes back to the repository
        subprocess.run(["git", "push"])
        print("Done: Successfully Saved output.txt")

    else:
        click.echo("Error: Please provide parameter : --find_date")
        return

if __name__ == "__main__":
    main()
