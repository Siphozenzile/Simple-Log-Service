import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])

        # Sort logs by DateTime descending and get the latest 100
        sorted_items = sorted(items, key=lambda x: x['DateTime'], reverse=True)[:100]

        return {
            'statusCode': 200,
            'body': json.dumps(sorted_items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
