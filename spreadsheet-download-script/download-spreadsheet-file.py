import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def run():
    # Obtains the repository name from GitHub Actions
    # repository_name = os.environ.get("REPOSITORY_NAME")

    # Route of service account credentials JSON file
    # credentials_path = '/home/runner/work/' + repository_name + '/' + repository_name + '/service_account_credentials.json'
    credentials_path = './service_account_credentials.json'

    # Google Drive file ID
    file_id = '13cCcKM6U_nXlFFxLmF0CUQkSSDOSZQFdJJLllK20Npw'

    # Destination file name for saving the spreadsheet
    output_file = 'employees-raw-data.xlsx'

    # Authentication using the service account credentials file
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=['https://www.googleapis.com/auth/drive.readonly']
    )

    # Create a Google Drive service instance
    drive_service = build('drive', 'v3', credentials=credentials)

    # Downloads the file
    request = drive_service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Saves the file in disk
    with open(output_file, 'wb') as file:
        file.write(request.execute())

    print(f"The file '{output_file}' has been downloaded succesfully.")

#Prueba
run()