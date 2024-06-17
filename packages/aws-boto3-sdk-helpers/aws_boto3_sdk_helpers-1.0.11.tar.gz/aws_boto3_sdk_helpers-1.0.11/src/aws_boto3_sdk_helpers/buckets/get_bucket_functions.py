import sys
import botocore
sys.path.append( '../')
from common.boto_client_declaration import s3_client
from common.args import bucket_args_call

args, s3 = bucket_args_call, s3_client(bucket_args_call)

def get_bucket_region(args):
    """
    Returns the provided bucket's aws region, which comes from the LocationConstraint response field.
    """
    try:
        response = s3.get_bucket_location(Bucket = args.bucket)
        # print(response) # get the full response
        print(f"LocationConstraint: {response['LocationConstraint']}, see more about this operation at: https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketLocation.html")

    except botocore.exceptions.ClientError as err:
        if err.response['Error']['Code'] == 'NoSuchBucket':
            print(f"\nThe bucket named {args.bucket} does not exist on the {args.aws_region} region\n")
            print('Request ID: {}'.format(err.response['ResponseMetadata']['RequestId']))
            print('Http code: {}'.format(err.response['ResponseMetadata']['HTTPStatusCode']))
        else:
            print("Error occured : ", err)

if __name__ == "__main__":
    get_bucket_region(args)
