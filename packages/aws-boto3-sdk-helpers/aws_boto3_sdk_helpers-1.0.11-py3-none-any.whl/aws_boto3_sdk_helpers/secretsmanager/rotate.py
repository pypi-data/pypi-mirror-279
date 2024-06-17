import boto3, os

client = boto3.client('secretsmanager', region_name=os.environ.get('AWS_REGION'))

response = client.rotate_secret(
    SecretId='some-secret-id',
    RotationLambdaARN='<arn>',
    RotateImmediately=True
)

# print(response)
print(response['Payload'].read().decode("utf-8"))
