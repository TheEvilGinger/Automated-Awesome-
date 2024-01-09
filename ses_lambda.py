import json
import boto3

def send_email_notification(customer_id, time_left):
    ses = boto3.client('ses', region_name='us-east-1')  # SES region defined
    sender_email = 'your@example.com'  #verified sender email

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CustomerInformationTable')
    response = table.get_item(
        Key={
            'customer_id': customer_id
        }
    )
    customer_email = response.get('Item', {}).get('email', '')

    if not customer_email:
        raise ValueError(f"Customer with ID {customer_id} does not have a valid email address.")

    subject = f"Your vehicle repair/service is ready in {time_left} minutes"
    body = f"Dear customer,\n\nYour vehicle repair/service will be ready in {time_left} minutes.\n\nThank you for choosing our service."

    ses.send_email(
        Source=sender_email,
        Destination={
            'ToAddresses': [customer_email]
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': body
                }
            }
        }
    )

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    sqs = boto3.resource('sqs')

    customer_id = event['customer_id']
    status_queue_url = event['status_queue_url']

    messages = sqs.Queue(status_queue_url).receive_messages(MaxNumberOfMessages=10)
    remaining_time = sum([int(message.body) for message in messages])

    if remaining_time == 15:
        send_email_notification(customer_id, 15)
    elif remaining_time == 0:
        send_email_notification(customer_id, 0)

    for message in messages:
        message.delete()

    return {
        'statusCode': 200,
        'body': json.dumps('Email notifications processed successfully!')
    }
