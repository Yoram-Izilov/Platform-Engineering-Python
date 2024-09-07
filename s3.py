import json
import boto3
from botocore.exceptions import ClientError
from consts import Tag

# Initialize S3 client
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

def s3_handler(action: str, bucket_name, file_path, access: str):
    """Handles S3 actions based on the action value.
    
    :param str action: The action to perform ('create', 'upload', 'list')
    :param bucket_name: str or None - Name of the S3 bucket (required for 'create' and 'upload')
    :param file: str or None - File path to upload (required for 'upload')
    :param str access: Access level for the bucket ('public' or 'private', default: 'private')
    """
    match action:
        case "create":
            create_bucket(bucket_name, access)
        case "upload":
            upload_file_to_bucket(bucket_name, file_path)
        case "list":
            list_buckets()

def create_bucket(bucket_name: str, access: str):
    """Creates a new S3 bucket (private) with the specified name and access type.
    
    :param str bucket_name: Name of the S3 bucket to create
    :param str access: Access level for the bucket ('public' or 'private')
    """
    try:
        # Create the bucket
        s3_client.create_bucket(Bucket=bucket_name)
        
        # Add tags to identify the bucket as created by the CLI
        s3_client.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [
                    {
                        'Key': 'tag:{}'.format(Tag.TAG_KEY.value),
                        'Value': Tag.TAG_VALUE.value
                    }
                ]
            }
        )

        print(f"Bucket '{bucket_name}' created successfully with {'public' if access=='public' else 'private'} access.")

    except Exception as e:
        print(f"Error creating bucket: {str(e)}")

def upload_file_to_bucket(bucket_name: str, file_path: str):
    """Uploads a file to the specified S3 bucket.
    
    :param str file_path: Path to the file to upload
    :param str bucket_name: Name of the S3 bucket to upload the file to
    """
    try:
        # Verify that the bucket was created by the user
        bucket_tagging = s3_client.get_bucket_tagging(Bucket=bucket_name)
        tags = {tag['Key']: tag['Value'] for tag in bucket_tagging['TagSet']}
        
        if tags.get('tag:{}'.format(Tag.TAG_KEY.value)) == Tag.TAG_VALUE.value:
            # Upload the file
            file_name = file_path.split('/')[-1] # if uploading from windows change to '\\'
            s3_client.upload_file(file_path, bucket_name, file_name)
            print(f"File '{file_name}' uploaded to bucket '{bucket_name}'.")
        else:
            print(f"Cannot upload file: Bucket '{bucket_name}' was not created through the CLI.")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")

def list_buckets():
    """Prints all S3 buckets of the user"""
    try:
        buckets = s3_client.list_buckets()['Buckets']
        my_buckets = []
        for bucket in buckets:
            try:
                bucket_tagging = s3_client.get_bucket_tagging(Bucket=bucket['Name'])
                tags = {tag['Key']: tag['Value'] for tag in bucket_tagging['TagSet']}
     
                if tags.get('tag:{}'.format(Tag.TAG_KEY.value)) == Tag.TAG_VALUE.value:
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
            print(f"S3 Buckets created by '{Tag.TAG_VALUE.value}':")
            for bucket_name in my_buckets:
                print(f" - {bucket_name}")
        else:
            print(f"No buckets created by '{Tag.TAG_VALUE.value}'.")
    except Exception as e:
        print(f"Error listing buckets: {str(e)}")