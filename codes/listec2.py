import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')

def list_ec2_instances():
    """
    List all EC2 instances.
    """
    try:
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")
    except Exception as e:
        print(f"Error listing EC2 instances: {e}")

# Example usage
if __name__ == "__main__":
    list_ec2_instances()