import boto3, botocore
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--aws_region", help="aws region where to look for the bucket")
args = parser.parse_args()

try:
    client = boto3.client('apigateway', region_name=args.aws_region)
    response = client.get_rest_apis(limit=123)
    for item in response['items']:
        print(item['id'])

except botocore.exceptions.ClientError as err:
    if err.response['Error']['Code'] == 'NotFoundException':
        print(f"Message: {format(err.response['Error']['Message'])}")
        print(f"Request ID: {format(err.response['ResponseMetadata']['RequestId'])}")
        print(f"Http code: {format(err.response['ResponseMetadata']['HTTPStatusCode'])}")
        
    else:
        print("Error occured : ", err)
