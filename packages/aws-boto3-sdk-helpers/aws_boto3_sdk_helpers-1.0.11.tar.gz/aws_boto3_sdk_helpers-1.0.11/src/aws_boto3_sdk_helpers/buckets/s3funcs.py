"""
somethin gin here
"""
import sys
import boto3

def s3_ls(**kwargs):
    """List the contents from a given S3 Bucket + Key combination and return a list of contents.
    
    Parameters
    -----------
    kwargs: Set of key value parameters required for boto3 list object operation
    
    Required Arguments
    -----------------
    
    - Bucket: Name of the S3 Bucket (Key name is case-sensitive)
    - Prefix: S3 Prefix (Key name is case-sensitive)
    """
    
    required_args = ['Bucket', 'Prefix']
    
    if not all(arg in kwargs for arg in required_args):
        print("All required args are not supplied.")
        print(f"Required Args : {required_args}")
        print(f"Supplied Args : {list(kwargs.keys())}")
        sys.exit(1)
    else:
        keys = []
        fs = boto3.client('s3')
        while True:
            ls_content = fs.list_objects_v2(**kwargs)
            keys.extend([item['Key'] for item in ls_content['Contents']])
            if not ls_content['IsTruncated']:
                break
            else:
                kwargs['ContinuationToken'] = ls_content['NextContinuationToken']
        return keys
