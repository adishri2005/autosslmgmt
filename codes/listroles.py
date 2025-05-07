import boto3
from botocore.exceptions import ClientError

# Create an IAM client
iam = boto3.client('iam')

def list_iam_roles():
    """
    List all IAM roles.
    """
    try:
        response = iam.list_roles()
        roles = response['Roles']
        for role in roles:
            print(f"Role Name: {role['RoleName']}, ARN: {role['Arn']}")
        return roles
    except ClientError as e:
        print(f"Error listing IAM roles: {e}")
        raise

"""def delete_iam_role(role_name):
    
    Delete an IAM role.

    :param role_name: The name of the role to delete
    
    try:
        # Detach all policies from the role
        attached_policies = iam.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
        for policy in attached_policies:
            iam.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])
            print(f"Detached policy {policy['PolicyArn']} from role {role_name}.")

        # Delete the role
        iam.delete_role(RoleName=role_name)
        print(f"Deleted role: {role_name}")
    except ClientError as e:
        print(f"Error deleting IAM role: {e}")
        raise
"""
# Example usage
if __name__ == "__main__":
    # List all IAM roles
    list_iam_roles()

    # Delete a specific IAM role
    #role_name_to_delete = 'example-role'  # Replace with the role name you want to delete
    #delete_iam_role(role_name_to_delete)