# create-short-url.py
import json
import boto3
import pyshorteners


import re
from urllib.parse import urlparse
import os
import secrets
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'url-shortener'))



def validate_url(url):
    """
    Validates if the given string is a properly formatted URL.
    
    Args:
        url (str): The URL string to validate
        
    Returns:
        bool: True if the URL is valid, False otherwise
    """
    # Check if URL is None or empty
    if not url or not isinstance(url, str):
        return False, "URL cannot be None or empty"
    
    # Basic pattern matching for URL format
    pattern = re.compile(
        r'^(?:http|https)://'             # http:// or https:// (required)
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'                      # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # or IP
        r'(?::\d+)?'                       # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)  # path and query string
    
    if not pattern.match(url):
        print(f"Invalid URL format: {url}")
        return False, "Invalid URL format"
    
    # Use urlparse for additional validation
    try:
        result = urlparse(url)
        print(f"Parsed URL: {result}")
        # Check if scheme and netloc are present
        return True, url if result.scheme and result.netloc else (False, "Invalid URL format")
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return False, "Invalid URL format"
    # except:
    #     return False
    

def generate_short_url(original_url):
    """
    Generates a short URL for the given original URL.
    
    Args:
        original_url (str): The original URL to shorten
        
    Returns:
        str: The generated short URL
    """
    try:
        # Create an instance of the Bitly API client
        shortner = pyshorteners.Shortener()      
        # Shorten the URL using Bitly
        short_url = shortner.tinyurl.short(original_url)
        return short_url
    except Exception as e:
        print(f"Error generating short URL: {e}")
        return json.dumps({'error': str(e)})
    

    




def handler(event, context):
    try:
        # Parse the incoming request body
        request_body = json.loads(event.get('body', '{}'))
        original_url = request_body.get('url')
        
       
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
                    'shortId': item['shortId'],
                    'clicks': item['clicks']
                })
            }
        else:
    
        # Generate a random short ID (6 characters)
            short_id = secrets.token_hex(3)  # 3 bytes = 6 hex chara cters
            short_ur= generate_short_url(original_url)
             # Store the mapping in DynamoDB
            table.put_item(
                Item={
                    'shortId': short_id,
                    'originalUrl': original_url,
                    'shortUrl': short_ur,                   
                    'createdAt': datetime.now().isoformat(),
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
                    'shortId': short_id,
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
    # Test the unction locally
    test_event = {
        'body': json.dumps({
            'url': 'https://www.example.com'
        })
    }
    test_context = {}

    
   
