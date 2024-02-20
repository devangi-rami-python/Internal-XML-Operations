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


def duckdb_query(csv_file_old_date_path, csv_file_new_date_path,find_date):
        try:
            ## Read CSV file into a Pandas DataFrame
            df1 = pd.read_csv(csv_file_old_date_path)
            df2 = pd.read_csv(csv_file_new_date_path)

            ## DuckDB Oprations
            conn = duckdb.connect(database=':memory:', read_only=False) # Connect to DuckDB

            # Create a DuckDB table from the DataFrame
            conn.register('old_data_table', df1)
            conn.register('new_data_table', df2)


            # Step 4: Run Select Queries
            # Step 4: Run Select Queries with a parameter
            join_query = """
            SELECT *
            FROM new_data_table t2
            LEFT JOIN old_data_table t1 ON t1.loc = t2.loc AND t1.lastmod = t2.lastmod
            WHERE t2.lastmod = ?
            AND t1.loc IS NULL
            """

            # Define the parameter
            parameter = (find_date,)

            # Execute the query with the parameter
            join_result = conn.execute(join_query, parameter).fetchdf()

            # Write the result to a file
            with open('output.txt', 'w') as f:
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
@click.option('--old_date', help='old_date in YYYY-MM-DD format')
@click.option('--new_date', help='End date in YYYY-MM-DD format')
@click.option('--find_date', help='Find date in YYYY-MM-DD format')
def main(old_date, new_date, find_date):
    if old_date and new_date and find_date:
        
        ## Step 1: Validate Inputs
        try:
            # Parse the date strings
            old_date_parsed = datetime.strptime(old_date, "%Y-%m-%d")
            new_date_parsed = datetime.strptime(new_date, "%Y-%m-%d")
            find_date_parsed = datetime.strptime(find_date, "%Y-%m-%d")
            current_date = datetime.now().date()


        except ValueError as e:
            click.echo("Error: Invalid date format in input command. Please provide dates in YYYY-MM-DD format.")
            return
        
        ## Step 2: Get latest file for Current date  
        if old_date_parsed.date() == current_date:
            download_current_date_xml()
        if new_date_parsed.date() == current_date:
            download_current_date_xml()

        ## Step 3: check_if_xml_exist
        if_xml_exist, get_old_date_file_path = check_if_xml_exist(old_date)
        if not if_xml_exist:
            print(f"Error: The file {old_date}.xml does not exist in the folder - '/input_files'.")
            return

        if_xml_exist, get_new_date_file_path = check_if_xml_exist(new_date)
        if not if_xml_exist:
            print(f"Error: The file {new_date}.xml does not exist in the folder - '/input_files'.")
            return

        ## Step 4: Convert XML to CSV 
        csv_file_old_date_path = xml_to_csv(get_old_date_file_path,old_date)
        csv_file_new_date_path = xml_to_csv(get_new_date_file_path,new_date)

        ## Step 5: perform query on CSV files with duckDB 
        duckdb_query(csv_file_old_date_path, csv_file_new_date_path,find_date)
        print("Done: Successfully generated output.txt")

        print("Git Push --")
        subprocess.run(["git", "config", "user.email", "devangi.rami@bacancy.com"])
        subprocess.run(["git", "config", "user.name", "Devangi Rami"])

        # Change directory to the root of the Git repository
        os.chdir("/home/runner/work/Internal-XML-Operations/Internal-XML-Operations/")
        
        # Stage the new XML file
        subprocess.run(["git", "add", "output.txt"])
        
        # Commit the changes
        subprocess.run(["git", "commit", "-m", f"Saved output.txt"])
        
        # Push the changes back to the repository
        subprocess.run(["git", "push"])
        print("Done: Successfully Saved output.txt")

    else:
        click.echo("Error: Please provide all 3 parameters : --old_date, --new_date and --find_date")
        return

if __name__ == "__main__":
    main()
