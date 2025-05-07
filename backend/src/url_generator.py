import json
import boto3

from validate_url import validate_url
from generate_short_url import generate_short_url

import secrets
from datetime import datetime


# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('url-shortener')


# Main Lambda function handler
def lambda_handler(event, context):
    try:
        # Parse the incoming request body
        # request_body = event
        original_url = event['originalUrl']
        
        # Validate the URL format
        # Check if the URL is valid using the validate_url function
        
        (val_url,message) = validate_url(original_url)
        if not val_url:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': message})
                }
        else:
                original_url = message
              
        
        
        # check if the URL already exists in the database
        # If it exists, return the existing short URL
        response = table.get_item(
            Key={
                'urlId': original_url,
                'createdAt': '2025-05-07T13:01:53.077591'
            }
        )      
        
        
        
        if response.get('Items') and len(response['Items']) > 0:
            # Return existing short URL
            item = response['Items'][0]
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'urlId':item['urlId'],
                    'originalUrl': item['originalUrl'],
                    'shortUrl': item['shortUrl'],                   
                    'createdAt': item['createdAt'],
                    'description': item['description'],
                    'clicks': item['clicks']
                })
            }
        else:
    
        # Generate a random short ID (6 characters)
            urlId = secrets.token_hex(3)  # 3 bytes = 6 hex chara cters
            short_ur= generate_short_url(original_url)
             # Store the mapping in DynamoDB
                      
            table.put_item(
                Item={
                    'urlId':urlId,
                    'originalUrl': event['originalUrl'],
                    'shortUrl': short_ur,                   
                    'createdAt': datetime.now().isoformat(),
                    'description': event['description'],
                    'clicks': event['clicks']
                }
            )

            return {
                'statusCode': 201,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                   'urlId':event['urlid'],
                    'originalUrl': event['originalUrl'],
                    'shortUrl': event['shortUrl'],                   
                    'createdAt': datetime.now().isoformat(),
                    'description': event['description'],
                    'clicks': event['clicks']
                })
            }
        

    except Exception as e:
            print(f"Error creating short URL: {str(e)}")
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Failed to create short URL'})
            }
    



