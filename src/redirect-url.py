# redirect-url.py
import json
import boto3
import os
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'url-shortener'))

def handler(event, context):
    try:
        # Get the short ID from the path parameter
        short_id = event.get('pathParameters', {}).get('shortId')
        
        if not short_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Short ID is required'})
            }
        
        # Look up the original URL in DynamoDB
        response = table.get_item(
            Key={
                'shortId': short_id
            }
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Short URL not found'})
            }
        
        original_url = response['Item']['originalUrl']
        
        # Increment the click count (without waiting for the update to complete)
        table.update_item(
            Key={
                'shortId': short_id
            },
            UpdateExpression='SET clicks = if_not_exists(clicks, :zero) + :inc',
            ExpressionAttributeValues={
                ':inc': 1,
                ':zero': 0
            }
        )
        
        # Return a redirect response
        return {
            'statusCode': 302,
            'headers': {
                'Location': original_url
            }
        }
    except Exception as e:
        print(f"Error processing redirect: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Failed to process redirect'})
        }