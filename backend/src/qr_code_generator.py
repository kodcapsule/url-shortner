import json
import boto3

from utils.generate_qrcode import generate_qr_code

s3 = boto3.client('s3')
bucket_name = 'your-s3-bucket-name'

def handler(event, context):
    try:
        # Parse the incoming request body
        request_body = json.loads(event.get('body', '{}'))
        short_url = request_body.get('short_url')

        if not short_url:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'short_url is required'})
            }
        else:
            # Generate QR code for the short URL
            qr_code_image = generate_qr_code(short_url)

            # save the QR code image to S3 bucket
            
            qr_code_key = f'qr_codes/{short_url}.png'
            s3.put_object(
                Bucket=bucket_name,
                Key=qr_code_key,
                Body=qr_code_image,
                ContentType='image/png'
            )


            # Return the QR code image as a base64 string
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'qr_code_image': qr_code_image})
            }





    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Invalid JSON format'})
        }

if __name__ == "__main__":
    short_url = "https://short.url/example"
    qr_code_image = generate_qr_code(short_url)

    print("QR code generated successfully.")
    print("QR code image:", qr_code_image)