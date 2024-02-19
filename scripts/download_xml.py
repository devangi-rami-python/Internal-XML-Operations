import requests
from datetime import datetime

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

        print("XML file saved successfully.")
    else:
        print(f"Failed to fetch XML file. Status code: {response.status_code}")


if __name__ == "__main__":
    download_current_date_xml()
