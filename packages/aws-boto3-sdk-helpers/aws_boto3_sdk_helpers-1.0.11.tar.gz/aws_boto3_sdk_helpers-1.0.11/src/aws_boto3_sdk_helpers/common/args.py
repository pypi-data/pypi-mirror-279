import argparse

AWS_REGION_CONST = "Target AWS region where to perform the action"

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

## Bucket
###############################################################################
def bucket_args():
    """
    Description
    -----------
    Initializes the arguments needed to excecute operations on a given S3 bucket.

    Example
    -------
    a_bucket_function(bucket_args())
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True, help="Name of the bucket")
    parser.add_argument("--aws-region", required=True, help=AWS_REGION_CONST)
    parser.add_argument("--prefix", required=True, help="Buckets Prefix")
    args = parser.parse_args()
    return args

###############################################################################

## CloudWatch Logs
###############################################################################
def cloudwatch_logs_args():
    """
    Description
    -----------
    Initializes the arguments needed to excecute operations on a given cloudwatch log group.

    Example
    -------
    a_cloudwatch_log_group_function(cloudwatch_logs_args())
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--group-name", required=True, help="CloudWatch log group name")
    parser.add_argument("--dry-run", type=str2bool, required=True, help="Whether or not to to perfom a dry run, if set to True the log group will not be removed.")
    parser.add_argument("--aws-region", required=True, help=AWS_REGION_CONST)
    args = parser.parse_args()
    return args
#################################################################################

if __name__ == "__main__":
    print("Test")
