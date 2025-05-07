import boto3
from botocore.exceptions import ClientError

# Create an EC2 client
ec2 = boto3.client('ec2')

def stop_ec2_instance(instance_id):
    """
    Stop an EC2 instance.

    :param instance_id: The ID of the instance to stop
    """
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Stopping EC2 instance: {instance_id}")
        return response
    except ClientError as e:
        print(f"Error stopping EC2 instance: {e}")
        raise

# Example usage
if __name__ == "__main__":
    instance_id = 'i-0c3e4dea8edede943'  # Replace with your instance ID
    stop_ec2_instance(instance_id)