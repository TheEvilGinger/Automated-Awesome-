import json
import boto3

def check_customer_info(customer_id, table):
    response = table.get_item(
        Key={
            'customer_id': customer_id
        }
    )
    return 'Item' in response

def save_customer_info(customer_id, first_name, last_name, email, year, make, table):
    table.put_item(
        Item={
            'customer_id': customer_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'year': year,
            'make': make
        }
    )

def lambda_handler(event, context):
    customer_id = event['customer_id']
    first_name = event['first_name']
    last_name = event['last_name']
    email = event['email']
    year = event['year']
    make = event['make']

    dynamodb_table = boto3.resource('dynamodb').Table('CustomerInformationTable')

    if not check_customer_info(customer_id, dynamodb_table):
        save_customer_info(customer_id, first_name, last_name, email, year, make, dynamodb_table)

    return {
        'statusCode': 200,
        'body': json.dumps('Customer information processed successfully!')
    }