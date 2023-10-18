import os
import boto3
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def run(event, context):
    # Identificador del archivo en Google Drive
    # Obtener el valor secreto a partir del ID del archivo
    secret_file = get_secret("StaffAssessmentSMDrive")
    file_id = extract_json_value(secret_file, "file_id")

    print(secret_file)
    print(file_id)

    # Obtiene el nombre del repositorio de GitHub Actions
    # repository_name = os.environ.get("REPOSITORY_NAME")

    secret_credentials = json.loads(get_secret("StaffAssessmentSMAccountCredentials"))
    print(secret_credentials)

    with open("./spreadsheet_download_lambda/service_account_credentials.json", "w") as archivo:
        # Escribe los datos JSON en el archivo
        json.dump(secret_credentials, archivo, indent=2)

    # Ruta del archivo JSON de credenciales de la cuenta de servicio
    credentials_path = './spreadsheet_download_lambda/service_account_credentials.json'
    # credentials_path = './service_account_credentials.json'

    # Nombre del archivo de destino para guardar la hoja de cálculo
    output_file = 'employees-raw-data.xlsx'

    # Autenticación utilizando el archivo de credenciales de la cuenta de servicio
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=['https://www.googleapis.com/auth/drive.readonly']
    )

    # Crea una instancia del servicio de Google Drive
    drive_service = build('drive', 'v3', credentials=credentials)

    # Descarga el archivo
    request = drive_service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Guarda el archivo en el mismo directorio que el script de Python
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(script_directory, output_file)

    # Guarda el archivo en el disco
    with open(output_file_path, 'wb') as file:
        file.write(request.execute())

    print(f"El archivo '{output_file}' se ha descargado con éxito.")

    print(f"La función lambda funciona")

    # Rutas a los archivos locales
    # local_file_path = "./spreadsheet_download_lambda/employees-raw-data.xlsx"
    # local_file_path = "./spreadsheet_download_lambda/hola.txt"
    # local_file_path = "./employees-raw-data.xlsx"

    # Clave S3 para el archivo
    # s3_key = "employees-raw-data.xlsx"
    # s3_key = "hola.txt"

    # s3_client = boto3.client('s3')

    # try:
    #     s3_client.upload_file(local_file_path, 'staff-assessment-bucket', s3_key)
    #     return(print("El archivo se ha subido exitosamente a S3"))
    # except Exception as e:
    #     return(print(f"Error al subir el archivo a S3: {str(e)}"))

def get_secret(secret_name):
    # Crea un cliente de Secrets Manager
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-1"
    )

    # Obtiene el valor del secreto
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    secret = get_secret_value_response['SecretString']

    return secret

def extract_json_value(var_json, dato):
    data = json.loads(var_json)
    return data[dato]
