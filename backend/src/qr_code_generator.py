import json
import boto3

from utils.generate_qrcode import generate_qr_code

s3 = boto3.client('s3')
s3_bucket = 'short_url_qr_code_bucket'

def lambda_handler(event, context):
    print("TEsting QR code generator")
    # try:
        # Parse the incoming request body

    #     for record in event['Records']:
    #         if record['eventName'] == 'INSERT':
    #             # Extract the short URL from the DynamoDB stream record and generate QR code for the short URL
    #             short_url = record['dynamodb']['NewImage']['shortUrl']['S']               
    #             (qr_code_image,image_path) = generate_qr_code(short_url)
    #             print(f"QR code for {short_url} generated successfully.")
    #         elsif record['eventName'] == 'MODIFY':
    #             # Extract the short URL from the DynamoDB stream record
    #             short_url = record['dynamodb']['NewImage']['shortUrl']['S']
    #             # Generate QR code for the short URL
    #             (qr_code_image,image_path) = generate_qr_code(short_url)
    #         elif record['eventName'] == 'REMOVE':
    #             # Extract the short URL from the DynamoDB stream record
    #             short_url = record['dynamodb']['OldImage']['shortUrl']['S']
    #             # Generate QR code for the short URL
    #             (qr_code_image,image_path) = generate_qr_code(short_url)
    #         else:
    #             continue  # Skip other event types

    #             # save the QR code image to S3 bucket
                
    #         qr_code_key = f'qr_code/{short_url}.png'
    #         s3.put_object(
    #                 Bucket=s3_bucket,
    #                 Key=qr_code_key,
    #                 Body=qr_code_image,
    #                 ContentType='image/png'
    #             )
                
    #     request_body = json.loads(event.get('body', '{}'))
    #     short_url = request_body.get('short_url')

    #     if not short_url:
    #         return {
    #             'statusCode': 400,
    #             'headers': {
    #                 'Content-Type': 'application/json',
    #                 'Access-Control-Allow-Origin': '*'
    #             },
    #             'body': json.dumps({'error': 'short_url is required'})
    #         }
    #     else:
    #         # Generate QR code for the short URL
    #         (qr_code_image,image_path) = generate_qr_code(short_url)

    #         # save the QR code image to S3 bucket
            
    #         qr_code_key = f'qr_code/{short_url}.png'
    #         s3.put_object(
    #             Bucket=s3_bucket,
    #             Key=qr_code_key,
    #             Body=qr_code_image,
    #             ContentType='image/png'
    #         )


    #         # Return the QR code image as a base64 string
    #         return {
    #             'statusCode': 200,
    #             'headers': {
    #                 'Content-Type': 'application/json',
    #                 'Access-Control-Allow-Origin': '*'
    #             },
    #             'body': json.dumps({'qr_code_image': qr_code_image})
    #         }





    # except json.JSONDecodeError:
    #     return {
    #         'statusCode': 400,
    #         'headers': {
    #             'Content-Type': 'application/json',
    #             'Access-Control-Allow-Origin': '*'
    #         },
    #         'body': json.dumps({'error': 'Invalid JSON format'})
    #     }

if __name__ == "__main__":
    short_url = "https://short.url/example"
    (qr_code_image, message) = generate_qr_code(short_url)

    print("QR code generated successfully.")
    print(message)
    print("QR code image:", qr_code_image)