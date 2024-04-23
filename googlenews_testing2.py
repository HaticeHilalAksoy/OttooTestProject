import boto3
import json
def lambda_handler(event, context):
    prefix = "news_links_"
    bucket_name = 'ottoofellow'
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        last_modified_file = max(response['Contents'], key=lambda obj: obj['LastModified'])['Key']
        file_extension = last_modified_file.split('.')[-1].lower()
        if file_extension == 'json':
            return {
                'statusCode': 200,
                'body': json.dumps({
                    "message": "JSON file is detected",
                    "file_name": last_modified_file,
                })
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    "message": "Unsupported file type",
                    "file_name": last_modified_file,
                })
            }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps("No files found")
        }