import boto3
from botocore.exceptions import ClientError

# Create an EC2 client
ec2 = boto3.client('ec2')

def terminate_ec2_instance(instance_id):
    """
    Terminate an EC2 instance.

    :param instance_id: The ID of the instance to terminate
    """
    try:
        response = ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"Terminating EC2 instance: {instance_id}")
        print("EC2 instance terminated successfully.")
        return response
    except ClientError as e:
        print(f"Error terminating EC2 instance: {e}")
        raise

# Example usage
if __name__ == "__main__":
    instance_id = 'i-0c3e4dea8edede943'  # Replace with your instance ID
    terminate_ec2_instance(instance_id)