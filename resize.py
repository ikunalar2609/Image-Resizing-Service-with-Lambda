import json
import boto3
from PIL import Image
from io import BytesIO

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = 'your-s3-bucket-name'
    target_bucket_name = 'your-target-s3-bucket-name'

    # Iterate through the S3 event records
    for record in event['Records']:
        # Get the S3 bucket and object key
        source_bucket = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        
        # Download the image from S3
        response = s3_client.get_object(Bucket=source_bucket, Key=object_key)
        image_content = response['Body'].read()
        
        # Open the image with Pillow
        image = Image.open(BytesIO(image_content))
        
        # Resize the image
        resized_image = image.resize((100, 100))
        
        # Save the resized image to a BytesIO object
        buffer = BytesIO()
        resized_image.save(buffer, 'JPEG')
        buffer.seek(0)
        
        # Upload the resized image to the target S3 bucket
        s3_client.put_object(Bucket=target_bucket_name, Key=f'resized-{object_key}', Body=buffer, ContentType='image/jpeg')

    return {
        'statusCode': 200,
        'body': json.dumps('Image resized and uploaded successfully')
    }
