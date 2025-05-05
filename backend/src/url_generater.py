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
def handler(event, context):
    try:
        # Parse the incoming request body
        request_body = json.loads(event.get('body', '{}'))
        original_url = request_body.get('url')
        
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
              
        
        # Check if URL already exists
        response = table.query(
            IndexName='originalUrl-index',
            KeyConditionExpression='originalUrl = :original_url',
            ExpressionAttributeValues={
                ':original_url': original_url
            }
        )
        
        # check if the URL already exists in the database
        # If it exists, return the existing short URL
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
                    'originalUrl': original_url,
                    'shortUrl': item['short_ur'],
                    'urlId': item['urlId'],
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
                    'urlId': urlId,
                    'originalUrl': original_url,
                    'shortUrl': short_ur,                   
                    'createdAt': datetime.now().isoformat(),
                    'description': 'Short URL for the original URL',
                    'clicks': 0
                }
            )
            

            return {
                'statusCode': 201,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'originalUrl': original_url,                    
                    'shortId': urlId,
                    'shortUrl': short_ur,
                    'createdAt': datetime.now().isoformat(),
                    'clicks': 0
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
    



if __name__ == "__main__":
    # Test the function locally

    (val_url,message)=validate_url("https://www.example.com")
    print(val_url)
    print(message)
  