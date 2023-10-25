import os
import boto3
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Constantes
SECRET_DRIVE_NAME = "StaffAssessmentSMDrive"
SECRET_CREDENTIALS_NAME = "StaffAssessmentSMAccountCredentials"
S3_BUCKET_NAME = "staff-assessment-bucket"
OUTPUT_FILE_NAME = "employees-raw-data.xlsx"
MIME_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

def run(event, context):
    try:
        # Obtiene el valor del identificador del archivo de Google Drive desde Secrets Manager
        file_id = extract_secret_value(SECRET_DRIVE_NAME, "file_id")

        # Obtiene las credenciales de la cuenta de servicio desde Secrets Manager
        secret_credentials = json.loads(get_secret(SECRET_CREDENTIALS_NAME))

        # Autenticación utilizando las credenciales de la cuenta de servicio
        credentials = service_account.Credentials.from_service_account_info(
            secret_credentials, scopes=['https://www.googleapis.com/auth/drive.readonly']
        )

        # Crea una instancia del servicio de Google Drive
        drive_service = build('drive', 'v3', credentials=credentials)

        # Descarga el archivo de Google Drive
        request = drive_service.files().export_media(fileId=file_id, mimeType=MIME_TYPE)
        output_file = '/tmp/' + OUTPUT_FILE_NAME

        # Guarda el archivo en el sistema de archivos local
        with open(output_file, 'wb') as file:
            file.write(request.execute())

        # Sube el archivo a S3
        upload_to_s3(output_file, S3_BUCKET_NAME, OUTPUT_FILE_NAME)

        # Elimina el archivo local
        os.remove(output_file)

        return logger.info("El archivo se ha subido exitosamente a S3")
    except Exception as e:
        return logger.info(f"Error al subir el archivo a S3: {str(e)}")

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

def extract_secret_value(secret_name, key):
    secret_value = get_secret(secret_name)
    data = json.loads(secret_value)
    return data.get(key, None)

def upload_to_s3(local_path, bucket_name, s3_key):
    s3_client = boto3.client('s3')
    s3_client.upload_file(local_path, bucket_name, 'raw_data/' + s3_key)