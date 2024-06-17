from datetime import datetime

def operation_start_msg(action, resource_name, resource_type):
    """
    Operation message for cloud resources.
    """
    msg = f"""
##################################################################################################
#
#    {action} operation started for:
#    - {resource_name} ({resource_type})
#
##################################################################################################
    """

    return print(msg)


def outcome_banner(action, resource_name, resource_type, rc, total_time):
    """
    Clean-up success banner
    """
    msg = f"""
##################################################################################################
#
#     {action} action executed on:
#     - {resource_name} ({resource_type})
#
#     Return code: { rc }
#     Time taken to complete (hours minutes and seconds): { total_time }
#     Current date and time: {datetime.now()}
#
##################################################################################################
    """
    return print(msg)
