import boto3
from botocore.exceptions import ClientError

# Create an EC2 client
ec2 = boto3.client('ec2')

def create_key_pair(key_name):
    """
    Create a new key pair.

    :param key_name: The name of the key pair
    :return: The key pair details
    """
    try:
        key_pair = ec2.create_key_pair(KeyName=key_name)
        print(f"Created key pair: {key_pair['KeyName']}")
        return key_pair
    except ClientError as e:
        print(f"Error creating key pair: {e}")
        raise

# Example usage
if __name__ == "__main__":
    key_name = 'autosslkey'
    key_pair = create_key_pair(key_name)
    # Save the private key to a file
    with open(f"{key_name}.pem", "w") as file:
        file.write(key_pair['KeyMaterial'])
    print(f"Key pair saved to {key_name}.pem")