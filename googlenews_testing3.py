import boto3
import json
 
def lambda_handler(event, context):
    prefix = "news_links_"
    bucket_name = 'ottoofellow'
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
 
    if 'Contents' in response:
        last_modified_file = max(response['Contents'], key=lambda obj: obj['LastModified'])['Key']
        obj = s3.get_object(Bucket=bucket_name, Key=last_modified_file)
        try:
            json_data = json.loads(obj['Body'].read().decode('utf-8'))
            if json_data:
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        "message": "File content is full",
                        "file_name": last_modified_file,
                    })
                }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        "message": "JSON file is empty",
                        "file_name": last_modified_file
                    })
                }
        except json.JSONDecodeError as e:
            return {
                'statusCode': 500,
                'body': json.dumps("JSON file is invalid: {}. File Name: {}".format(str(e), last_modified_file))
            }