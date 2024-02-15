import os
from datetime import datetime, timedelta

def remove_old_files():
    # Step 1: Specify the directory containing the files
    directory = './input_files'

    # Step 2: Get the list of files in the directory
    files = os.listdir(directory)

    # Step 3-7: Iterate over the files and perform the filtering and deletion
    for file in files:
        # Filter files with date format yyyy-mm-dd
        try:
            file_date = datetime.strptime(file[:10], '%Y-%m-%d')
            
            # Calculate the date one week ago
            one_week_ago = datetime.now() - timedelta(days=7)
            
            # Check if the file's date is older than one week
            if file_date < one_week_ago:
                # Delete the file
                os.remove(os.path.join(directory, file))
                print(f"Deleted file: {file}")
        except ValueError:
            # If the filename doesn't match the date format, continue to the next file
            continue

if __name__ == "__main__":
    remove_old_files()