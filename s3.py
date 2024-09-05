import json
import boto3
from botocore.exceptions import ClientError
from consts import Tag

# Initialize S3 client
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

def s3_handler(action, bucket_name, file_path, access):
    match action:
        case "create":
            create_bucket(bucket_name, access)
        case "upload":
            upload_file_to_bucket(bucket_name, file_path)
        case "list":
            list_buckets()

def create_bucket(bucket_name, access):
    try:
        # Create the bucket
        s3_client.create_bucket(Bucket=bucket_name)
        
        # Add tags to identify the bucket as created by the CLI
        s3_client.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [
                    {
                        'Key': 'tag:{}'.format(Tag['Key'].value),
                        'Value': Tag['Value'].value
                    }
                ]
            }
        )

        print(f"Bucket '{bucket_name}' created successfully with {'public' if access=='public' else 'private'} access.")

    except Exception as e:
        print(f"Error creating bucket: {str(e)}")

def upload_file_to_bucket(bucket_name, file_path):
    try:
        # Verify that the bucket was created by the user
        bucket_tagging = s3_client.get_bucket_tagging(Bucket=bucket_name)
        tags = {tag['Key']: tag['Value'] for tag in bucket_tagging['TagSet']}
        
        if tags.get('tag:{}'.format(Tag['Key'].value)) == Tag['Value'].value:
            # Upload the file
            file_name = file_path.split('/')[-1] # if uploading from windows change to '\\'
            s3_client.upload_file(file_path, bucket_name, file_name)
            print(f"File '{file_name}' uploaded to bucket '{bucket_name}'.")
        else:
            print(f"Cannot upload file: Bucket '{bucket_name}' was not created through the CLI.")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")

def list_buckets():
    try:
        buckets = s3_client.list_buckets()['Buckets']
        my_buckets = []
        for bucket in buckets:
            try:
                bucket_tagging = s3_client.get_bucket_tagging(Bucket=bucket['Name'])
                tags = {tag['Key']: tag['Value'] for tag in bucket_tagging['TagSet']}
     
                if tags.get('tag:{}'.format(Tag['Key'].value)) == Tag['Value'].value:
                    my_buckets.append(bucket['Name'])
            except ClientError as e:
                # Handle the case when the bucket has no tags
                if e.response['Error']['Code'] == 'NoSuchTagSet':
                    continue
                # Handle access denied errors
                elif e.response['Error']['Code'] == 'AccessDenied':
                    continue
                else:
                    print(f"Error getting tags for bucket '{bucket['Name']}': {e}")

        if my_buckets:
            print(f"S3 Buckets created by '{Tag['Value'].value}':")
            for bucket_name in my_buckets:
                print(f" - {bucket_name}")
        else:
            print(f"No buckets created by '{Tag['Value'].value}'.")
    except Exception as e:
        print(f"Error listing buckets: {str(e)}")