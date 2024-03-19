from ftplib import FTP
import re
from datetime import datetime, timedelta

def get_most_recent_file_ftp(host, username, password, directory):
    try:
        # Connect to FTP server
        ftp = FTP(host)
        ftp.login(username, password)

        # Try to change directory
        try:
            ftp.cwd(directory)
        except Exception as e:
            # Modify directory name using regex
            new_directory = re.sub(r'\d{4}-\d{2}-\d{2}', 'backup', directory)
            ftp.cwd(new_directory)

        # List directory contents using MLSD
        files = ftp.mlsd()

        # Get the most recent file
        most_recent_file = None
        most_recent_time = datetime.min

        for file, metadata in files:
            file_time = datetime.strptime(metadata['modify'], '%Y%m%d%H%M%S')
            if file_time > most_recent_time:
                most_recent_time = file_time
                most_recent_file = file

        # Check if the most recent file was created within the last 1 day
        current_time = datetime.now()
        time_difference = current_time - most_recent_time

        if time_difference <= timedelta(days=1):
            return f"Success: Most recent file '{most_recent_file}' created within the last 1 day."
        else:
            return f"Failure: No recent file found within the last 1 day."

    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
host = "ftp.example.com"
username = "your_username"
password = "your_password"
directory = "/path/to/ftp/directory"

result = get_most_recent_file_ftp(host, username, password, directory)
print(result)
