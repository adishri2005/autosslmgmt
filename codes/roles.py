import boto3
import json
from botocore.exceptions import ClientError

# Create an IAM client
iam = boto3.client('iam')

def create_iam_role(iam_client, role_name, trust_policy, description):
    """
    Create an IAM role with the specified trust policy.
    If the role already exists, it will not be created again.

    :param iam_client: The IAM client
    :param role_name: The name of the role to create
    :param trust_policy: The trust policy for the role
    :param description: The description of the role
    :return: The ARN of the created or existing role
    """
    try:
        # Check if the role already exists
        role = iam_client.get_role(RoleName=role_name)
        print(f"Role {role_name} already exists.")
        return role['Role']['Arn']
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            try:
                # Create the IAM role
                role_response = iam_client.create_role(
                    RoleName=role_name,
                    AssumeRolePolicyDocument=json.dumps(trust_policy),
                    Description=description
                )
                print(f"Created role: {role_response['Role']['Arn']}")
                return role_response['Role']['Arn']
            except ClientError as create_error:
                print(f"Error creating role: {create_error}")
                raise
        else:
            print(f"Error checking role existence: {e}")
            raise

def attach_policies_to_role(iam_client, role_name, policies):
    """
    Attach the specified policies to the IAM role.

    :param iam_client: The IAM client
    :param role_name: The name of the role to attach policies to
    :param policies: A list of policy ARNs to attach
    """
    for policy_arn in policies:
        try:
            iam_client.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
            print(f"Attached policy {policy_arn} to role {role_name}.")
        except ClientError as e:
            print(f"Error attaching policy {policy_arn} to role {role_name}: {e}")
            raise

# Define the trust policies
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "ec2.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
}

# Define the roles and their policies
roles = {
    "SSLManagerRole": {
        "description": "Role for EC2 to manage SSL certs and access S3 and Lambda",
        "policies": [
            "arn:aws:iam::aws:policy/AmazonEC2FullAccess",
            "arn:aws:iam::aws:policy/AmazonS3FullAccess",
            "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
        ]
    },
    "ACMManagerRole": {
        "description": "Role for managing SSL certificates using ACM",
        "policies": [
            "arn:aws:iam::aws:policy/AWSCertificateManagerFullAccess"
        ]
    },
    "CloudWatchLogsRole": {
        "description": "Role for logging events to CloudWatch",
        "policies": [
            "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
        ]
    },
    "Route53ManagerRole": {
        "description": "Role for managing DNS records in Route 53",
        "policies": [
            "arn:aws:iam::aws:policy/AmazonRoute53FullAccess"
        ]
    }
}

# Main execution
if __name__ == "__main__":
    for role_name, role_info in roles.items():
        # Create the IAM role
        role_arn = create_iam_role(iam, role_name, trust_policy, role_info["description"])

        # Attach the policies to the role
        attach_policies_to_role(iam, role_name, role_info["policies"])

    print("All roles and policies have been set up.")