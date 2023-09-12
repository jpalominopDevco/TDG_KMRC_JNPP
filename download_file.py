import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Ruta al archivo JSON de las credenciales de cuenta de servicio
credentials_path = '/home/runner/work/TDG_KMRC_JNPP/TDG_KMRC_JNPP/service_account_credentials.json'

# ID del archivo de Google Drive
file_id = '13cCcKM6U_nXlFFxLmF0CUQkSSDOSZQFdJJLllK20Npw'

# Nombre de archivo de destino para guardar el spreadsheet
output_file = 'employees-data-raw.xlsx'

# Autenticación con las credenciales de cuenta de servicio
credentials = service_account.Credentials.from_service_account_file(
    credentials_path, scopes=['https://www.googleapis.com/auth/drive.readonly']
)

# Crea una instancia del servicio de Google Drive
drive_service = build('drive', 'v3', credentials=credentials)

# Descarga el archivo
request = drive_service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Guarda el archivo en disco
with open(output_file, 'wb') as file:
    file.write(request.execute())

print(f"El archivo '{output_file}' se ha descargado correctamente.")
