import boto3

def s3_client(args):
    """
    Description
    -----------
    Initialize the S3 bucket client for the Python AWS SDK.
    """
    s3 = boto3.client('s3', region_name=args.aws_region)
    return s3

def cloudwatch_logs_client(args):
    """
    Description
    -----------
    Initialize the cloudwatch logs client for the Python AWS SDK.

    Parameters
    ------------
        args: parser.parse_args()
            The args object needed to initialize the client object.

    Return
    -----------
        age : boto3.client()
            Configured boto3 client.
    """
    logs = boto3.client('logs', region_name=args.aws_region)
    return logs

