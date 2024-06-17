import boto3
import botocore
import argparse

def check_backup_jobs():
    """
    Check backup jobs
    """
    args = flag_init()
    client = boto3.client('backup',region_name=args.aws_region)
    # First stop any backup jobs that are currently running or created or pending
    try:
        if client.can_paginate('list_backup_jobs'):
            # Get paginator for the list_backup_jobs method
            paginator = client.get_paginator('list_backup_jobs')
            # Iterate through pages of backup jobs for the specified backup vault
            for page in paginator.paginate(ByBackupVaultName=args.backup):
                print(page['BackupJobs'])

        else:
            print("\n\n\n\nlist_backup_jobs canot be pagginated, continuing...\n\n\n\n")

    except botocore.exceptions.ClientError as err:
        if err.response['Error']['Code'] == 'AccessDeniedException':
            print('Request ID: {}'.format(err.response['ResponseMetadata']['RequestId']))
            print('Http code: {}'.format(err.response['ResponseMetadata']['HTTPStatusCode']))
            print("\n\nBackup vault not found....\n\n")
        else:
            print("Error occured : ", err)
            raise err

def flag_init():
    """
    Init flags required by the module
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--backup", required=True, help="Name of the backup")
    parser.add_argument("--aws_region", required=True, help="aws region where to look for the bucket")
    args = parser.parse_args()

    return args


check_backup_jobs()
