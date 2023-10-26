import boto3
import pandas as pd
import json
import csv

def get_dynamodb_data(region, table_name):
    dynamodb = boto3.client('dynamodb', region_name=region)
    response = dynamodb.scan(TableName=table_name)
    items = response.get('Items', [])
    return items

def transform_data(items):
    for item in items:
        for key, value in item.items():
            if 'S' in value:
                item[key] = value['S']
    print(items)
    return items

def format_empty(value):
    return '" "' if value.strip() == '' else value

def process_data(data):
    df = pd.DataFrame(data)
    df = df.map(format_empty)
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
    df = df[column_order]
    return df

def export_to_csv(df, csv_file):
    df.to_csv(csv_file, index=False, quoting=csv.QUOTE_ALL)
    print(f'Datos exportados a {csv_file}')

if __name__ == "__main__":
    region = 'us-east-1'
    table_name = 'Employee'
    csv_file = 'employees-dynamodb-data.csv'

    items = get_dynamodb_data(region, table_name)
    data = transform_data(items)
    df = process_data(data)
    export_to_csv(df, csv_file)
