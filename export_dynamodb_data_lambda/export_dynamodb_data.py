import boto3
import pandas as pd

# Configura la región y el nombre de la tabla
region = 'us-east-1'
table_name = 'Employee'

# Inicializa el cliente de DynamoDB
dynamodb = boto3.client('dynamodb', region_name=region)

# Escanea la tabla DynamoDB
response = dynamodb.scan(TableName=table_name)

# Obtiene los elementos escaneados
items = response.get('Items', [])

# Convierte los datos en un DataFrame de pandas
df = pd.DataFrame(items)

# Nombre del archivo CSV de salida
csv_file = 'employees-dynamodb-data.csv'

# Exporta el DataFrame a un archivo CSV
df.to_csv(csv_file, index=False)

print(f'Datos exportados a {csv_file}')
