"""
check_alarm_status.py determines whether the passed alarm status if found in the provided alarm name.
All options can be found at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/describe_alarms.html
Be aware that not all options can be use at the same time
"""

import sys
import argparse
import boto3
import botocore

exceptions = ["InvalidNextToken"]

def flag_init():
    """
    Init flags required by the module
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--alarm_name", required=True, help="Name of the alarm")
    parser.add_argument("--alarm_status", required=True, choices= ['OK','ALARM','INSUFFICIENT_DATA'], help="Alarm status")
    parser.add_argument("--aws_region", required=True, help="AWS region where to run the script")
    args = parser.parse_args()
    return args

def cw_describe_alarms():
    """
    cw_describe_alarms describes the passed alarm.

    It returns a message and a bool, the message is to report what has happened and the bool is to let the function caller decide what to do next depending on the bool value.

    usage example:
    python check_alarm_status.py --aws_region <region> --alarm_name <alarm> --alarm-status OK|ALARM|INSUFFICIENT_DATA 
    """
    args = flag_init()
    client = boto3.client('cloudwatch',region_name=args.aws_region)
    try:
        response = client.describe_alarms(
            AlarmNames=[f"{args.alarm_name}"],
            AlarmTypes=['MetricAlarm'],
            MaxRecords=50,
        )
        # print(response['MetricAlarms']) // MetricAlarms is the key containing multiple records but it ussualy returns only one with multuple data points

        for alarm in response['MetricAlarms']:
            if len(response['MetricAlarms']) < 1:
                print(f'ERROR: The {args.alarm_name} alarm does not have a record with status {args.alarm_status}')
                return sys.exit(1)
            elif alarm['StateValue'] != args.alarm_status:
                print(f"ERROR: The {alarm['AlarmName']} alarm does not have any recent records in {args.alarm_status} state")
                return sys.exit(1)
            print(f'SUCCESS: The current state of the {alarm["AlarmName"]} alarm is: {args.alarm_status}\nState Reason: {alarm["StateReason"]}')
            return sys.exit(0)
                
    except botocore.exceptions.ClientError as error_found:
        if error_found.response['Error']['Code'] in exceptions:
            print(f'''
            Error Code: {error_found.response['Error']['Code']}
            Message: {error_found.response['Error']['Message']}
            Request ID: {error_found.response['ResponseMetadata']['RequestId']}
            Http code: {error_found.response['ResponseMetadata']['HTTPStatusCode']}
            ''')
        return f"Error occured : {error_found}"

