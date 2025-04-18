# create-short-url.py
import json
import boto3
import pyshorteners
import validators

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
    if url is None or url == "":
        return False, "URL cannot be None or empty"
    try:
        # Use validators library to check if the URL is valid
        # This will also check for common URL formats (http, https, etc.)
        if not validators.url(url):
            return False, "Invalid URL format"
    except Exception as e:
        print(f"Error validating URL: {e}")
        return False, "Invalid URL format"

    return validators.url(url), url


    
    
    

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
    valid_url = validate_url("https://www.kaggle.com/code/abdoomoh/10-ways-to-shorten-your-urls-in-python")
    print("Valid URL:", valid_url)
    
