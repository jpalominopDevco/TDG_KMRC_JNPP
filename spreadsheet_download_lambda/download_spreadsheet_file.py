#import os
import boto3
import json
#from google.oauth2 import service_account
#from googleapiclient.discovery import build

def run(event, context):

    #Google Drive file ID
    #Get secret value from file id
    secret = get_secret("StaffAssessmentSMDrive")
    file_id = extract_json_value(secret, "file_id")

    print(secret)
    print(file_id)


    # Obtains the repository name from GitHub Actions
    # repository_name = os.environ.get("REPOSITORY_NAME")

    # Route of service account credentials JSON file
    # credentials_path = '/home/runner/work/' + repository_name + '/' + repository_name + '/service_account_credentials.json'
    #credentials_path = './spreadsheet_download_lambda/service_account_credentials.json'

    # Google Drive file ID
    #file_id = '13cCcKM6U_nXlFFxLmF0CUQkSSDOSZQFdJJLllK20Npw'

    # Destination file name for saving the spreadsheet
    #output_file = 'employees-raw-data.xlsx'

    # Authentication using the service account credentials file
    #credentials = service_account.Credentials.from_service_account_file(
    #    credentials_path, scopes=['https://www.googleapis.com/auth/drive.readonly']
    #)

    # Create a Google Drive service instance
    #drive_service = build('drive', 'v3', credentials=credentials)

    # Downloads the file
    #request = drive_service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Guardar el archivo en el mismo directorio que el script de Python
    #script_directory = os.path.dirname(os.path.abspath(__file__))
    #output_file_path = os.path.join(script_directory, output_file)

    # Saves the file in disk
    #with open(output_file_path, 'wb') as file:
    #    file.write(request.execute())

    #print(f"The file '{output_file}' has been downloaded successfully.")

    print(f"Funciona la lambda")

    #local_file_path = "./spreadsheet_download_lambda/employees-raw-data.xlsx"
    local_file_path = "./spreadsheet_download_lambda/hola.txt"

    #s3_key = "employees-raw-data.xlsx"
    s3_key = "hola.txt"

    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(local_file_path, 'staff-assessment-bucket', s3_key)
        return(print("Archivo subido con éxito a S3"))
    except Exception as e:
        return(print(f"Error al subir el archivo a S3: {str(e)}"))
    
def get_secret(secret_name):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-1"
    )

    #Get the value of the secret
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    secret = get_secret_value_response['SecretString']

    return secret

def extract_json_value(json,dato):

    data = json.loads(json)

    return data[dato]
