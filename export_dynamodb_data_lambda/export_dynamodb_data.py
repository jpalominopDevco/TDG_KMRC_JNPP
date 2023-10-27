# Importa las bibliotecas necesarias
import boto3
import pandas as pd
import csv
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define la región y el nombre de la tabla DynamoDB
REGION = 'us-east-1'
TABLE_NAME = 'Employee'
# Define el nombre del archivo CSV de salida
OUTPUT_FILE_NAME = 'employees-dynamodb-data.csv'
S3_BUCKET_NAME = "staff-assessment-bucket"

def run(event, context):
    
    # Obtiene los datos de DynamoDB
    items = get_dynamodb_data(REGION, TABLE_NAME)
    # Transforma los datos
    data = transform_data(items)
    # Procesa los datos y crea un DataFrame
    df = process_data(data)
    # Ruta del archivo en la lambda
    output_file = '/tmp/' + OUTPUT_FILE_NAME
    # Exporta el DataFrame a un archivo CSV
    export_to_csv(df,output_file)
    # Sube el archivo a S3
    upload_to_s3(output_file, S3_BUCKET_NAME, OUTPUT_FILE_NAME)
    logger.info("El archivo se ha subido exitosamente a S3")

# Función para obtener datos de DynamoDB
def get_dynamodb_data(region, table_name):
    # Inicializa el cliente de DynamoDB en la región especificada
    dynamodb = boto3.client('dynamodb', region_name=region)
    # Escanea la tabla DynamoDB y obtiene la respuesta
    response = dynamodb.scan(TableName=table_name)
    # Extrae los elementos escaneados de la respuesta
    items = response.get('Items', [])
    return items

# Función para transformar los datos
def transform_data(items):
    # Itera a través de los elementos
    for item in items:
        for key, value in item.items():
            # Verifica si el valor tiene una clave 'S' y lo extrae
            if 'S' in value:
                item[key] = value['S']
    return items

# Función para dar formato a los campos vacíos
def format_empty(value):
    return '" "' if value.strip() == '' else value

# Función para procesar los datos y crear un DataFrame de Pandas
def process_data(data):
    # Convierte los datos en un DataFrame de Pandas
    df = pd.DataFrame(data)
    # Aplica la función format_empty a todas las celdas del DataFrame
    df = df.map(format_empty)
    # Define el orden de las columnas
    column_order = [
        "ssn",
        "dateOfHire",
        "disengagementDate",
        "disengagementReason",
        "documentType",
        "email",
        "name",
        "occupation",
        "salary"
    ]
    # Reordena las columnas en el orden deseado
    df = df[column_order]
    return df

# Función para exportar el DataFrame a un archivo CSV
def export_to_csv(df,output_file):
    # Exporta el DataFrame a un archivo CSV sin índice y con todas las celdas rodeadas de comillas
    df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)
    # Imprime un mensaje de confirmación

def upload_to_s3(local_path, bucket_name, s3_key):
    s3_client = boto3.client('s3')
    s3_client.upload_file(local_path, bucket_name, 'dynamodb_data/' + s3_key)