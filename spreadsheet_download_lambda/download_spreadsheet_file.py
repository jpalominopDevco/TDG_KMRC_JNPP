import os
import boto3
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def run(event, context):
    # Obtener el valor del identificador del archivo de Google Drive desde Secrets Manager
    secret_file = get_secret("StaffAssessmentSMDrive")
    file_id = extract_json_value(secret_file, "file_id")

    # Obtener las credenciales de la cuenta de servicio desde Secrets Manager
    secret_credentials = json.loads(get_secret("StaffAssessmentSMAccountCredentials"))

    # Autenticación utilizando las credenciales de la cuenta de servicio
    credentials = service_account.Credentials.from_service_account_info(
        secret_credentials, scopes=['https://www.googleapis.com/auth/drive.readonly']
    )

    # Crea una instancia del servicio de Google Drive
    drive_service = build('drive', 'v3', credentials=credentials)

    # Descarga el archivo de Google Drive
    request = drive_service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    # Nombre del archivo de destino para guardar la hoja de cálculo
    output_file = '/tmp/employees-raw-data.xlsx'

    # Ruta completa para guardar el archivo en el sistema de archivos local
    # script_directory = os.path.dirname(os.path.abspath(__file__))
    # output_file_path = os.path.join(script_directory, output_file)

    # Guarda el archivo en el sistema de archivos local
    # with open(output_file_path, 'wb') as file:
    #     file.write(request.execute())
    with open(output_file, 'wb') as file:
        file.write(request.execute())

    # Rutas a los archivos locales
    # local_file_path = "employees-raw-data.xlsx"

    # Clave S3 para el archivo
    s3_key = "employees-raw-data.xlsx"

    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(output_file, 'staff-assessment-bucket', s3_key)
        # os.remove(local_file_path)
        return(print("El archivo se ha subido exitosamente a S3"))
    except Exception as e:
        # os.remove(local_file_path)
        return(print(f"Error al subir el archivo a S3: {str(e)}"))

def get_secret(secret_name):
    # Crea un cliente de Secrets Manager
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-1"
    )

    # Obtiene el valor del secreto desde Secrets Manager
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    secret = get_secret_value_response['SecretString']

    return secret

def extract_json_value(var_json, dato):
    data = json.loads(var_json)
    return data[dato]

