"""
describe_alarms.py returns an alarm with the values specified on the paramater of the describe_alarms function.

All options can be found at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/describe_alarms.html
Be aware that not all options can be use at the same time
"""

import boto3, botocore
import argparse


exceptions = ["InvalidNextToken"]

def flag_init():
    """
    Init flags required by the module
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--alarm_name", required=True, help="Name of the alarm")
    parser.add_argument("--aws_region", required=True, help="AWS region where to run the script")
    args = parser.parse_args()
    return args

def cw_describe_alarms():
    """
    cw_describe_alarms describes the passed alarm
    """
    args = flag_init()
    client = boto3.client('cloudwatch',region_name=args.aws_region)
    try:
        response = client.describe_alarms(
            AlarmNames=[f"{args.alarm_name}"],
            AlarmTypes=['MetricAlarm'],
            StateValue='OK',
            MaxRecords=5,
        )
        print(response) ## A quick way to see the whole return object

    except botocore.exceptions.ClientError as error_found:
        if error_found.response['Error']['Code'] in exceptions:
            print(f"Error Code: {format(error_found.response['Error']['Code'])}")
            print(f"Message: {format(error_found.response['Error']['Message'])}")
            print(f"Request ID: {format(error_found.response['ResponseMetadata']['RequestId'])}")
            print(f"Http code: {format(error_found.response['ResponseMetadata']['HTTPStatusCode'])}")   
        else:
            print(f"Error occured : {error_found}")

cw_describe_alarms()