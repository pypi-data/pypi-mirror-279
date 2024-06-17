
import pytest
import boto3
from moto import mock_s3
from verification_modules.s3funcs import s3_ls

@pytest.fixture
def s3_boto():
    """Create an S3 boto3 client and return the client object"""
    
    s3 = boto3.client('s3', region_name='us-east-1')
    return s3

@mock_s3
def test_ls(s3_boto):
    """Test the custom s3 ls function mocking S3 with moto"""
    
    bucket = "testbucket"
    key = "testkey"
    body = "testing"
    s3_boto.create_bucket(Bucket=bucket)
    s3_boto.put_object(Bucket=bucket, Key=key, Body=body)
    ls_output = s3_ls(Bucket=bucket, Prefix=key)
    assert len(ls_output) == 1
    assert ls_output[0] == 'testkey'
