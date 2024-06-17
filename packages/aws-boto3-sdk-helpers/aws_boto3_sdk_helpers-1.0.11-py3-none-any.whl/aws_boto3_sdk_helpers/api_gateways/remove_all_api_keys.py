import boto3, botocore
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--aws_region", help="aws region where to look for the bucket")
args = parser.parse_args()

my_config = botocore.config.Config(
    region_name = args.aws_region,
    retries = {
        'max_attempts': 3,
        'mode': 'standard'
    }
)
exceptions = ["BadRequestException","NotFoundException","UnauthorizedException","TooManyRequestsException"]
sleep_time = 15

try:
    client = boto3.client('apigateway', config=my_config)
    response = client.get_api_keys(limit=123)
    for item in response['items']:
        print(f"\nAttempting to delete API Key ID: {item['id']}")
        client.delete_api_key(apiKey=item['id'])
        print(f"{item['id']} API Key deleted. Sleeping now for {sleep_time}")
        time.sleep(sleep_time)

except botocore.exceptions.ClientError as err:
    if err.response['Error']['Code'] in exceptions:
        print(f"Error Code: {format(err.response['Error']['Code'])}")
        print(f"Message: {format(err.response['Error']['Message'])}")
        print(f"Request ID: {format(err.response['ResponseMetadata']['RequestId'])}")
        print(f"Http code: {format(err.response['ResponseMetadata']['HTTPStatusCode'])}")   
    else:
        print("Error occured : ", err)
