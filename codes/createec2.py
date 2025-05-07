import boto3
from botocore.exceptions import ClientError

# Create an EC2 client
ec2 = boto3.client('ec2')

def create_ec2_instance_without_key(image_id, instance_type, security_group_id, subnet_id):
    """
    Create and launch an EC2 instance without a key pair.

    :param image_id: The ID of the AMI
    :param instance_type: The instance type (e.g., 't2.micro')
    :param security_group_id: The ID of the security group
    :param subnet_id: The ID of the subnet
    :return: The ID of the created instance
    """
    try:
        response = ec2.run_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            SecurityGroupIds=[security_group_id],
            SubnetId=subnet_id,
            MinCount=1,
            MaxCount=1
        )
        instance_id = response['Instances'][0]['InstanceId']
        print(f"Created EC2 instance: {instance_id}")
        return instance_id
    except ClientError as e:
        print(f"Error creating EC2 instance: {e}")
        raise

# Example usage
if __name__ == "__main__":
    image_id = 'ami-00a929b66ed6e0de6'  # Replace with your AMI ID
    instance_type = 't2.micro'
    security_group_id = 'sg-0e046b6a95b43a069'  # Replace with your security group ID
    subnet_id = 'subnet-036a3d8013eef2a1e'  # Replace with your subnet ID
    instance_id = create_ec2_instance_without_key(image_id, instance_type, security_group_id, subnet_id)