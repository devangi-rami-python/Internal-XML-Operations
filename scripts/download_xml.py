import requests
from datetime import datetime
import os
import subprocess


def download_current_date_xml():
    current_date = datetime.now().strftime("%Y-%m-%d")

    print("Downloading latest XML file of date:", current_date)
    # URL of the XML file
    url = "https://www.scnsoft.com/main.xml"  # Replace with the actual URL of the XML file

    # Send HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the content of the response
        xml_content = response.content
        # Specify the local file path where you want to save the XML file
        local_file_path = f"input_files/{current_date}.xml"
        
        # Write the XML content to a local file
        with open(local_file_path, "wb") as f:
            f.write(xml_content)
        print("XML file saved successfully at -->:", os.path.abspath(local_file_path))  # Print absolute path

        subprocess.run(["git", "config", "user.email", "devangi.rami@bacancy.com"])
        subprocess.run(["git", "config", "user.name", "Devangi Rami"])

        # Change directory to the root of the Git repository
        os.chdir("/home/runner/work/Internal-XML-Operations/Internal-XML-Operations/")
        
        # Stage the new XML file
        subprocess.run(["git", "add", local_file_path])
        
        # Commit the changes
        subprocess.run(["git", "commit", "-m", f"Cron - Add XML file for {current_date}"])
        
        # Push the changes back to the repository
        subprocess.run(["git", "push"])
        print("XML file saved successfully.")

    else:
        print("response",response)
        print(f"Failed to fetch XML file. Status code: {response.status_code}")


if __name__ == "__main__":
    download_current_date_xml()
