import boto3
import paramiko

# Create an EC2 client
ec2 = boto3.client('ec2')

def deploy_certificate_to_ec2(instance_id, certificate_details, private_key, user, key_file):
    """
    Deploy the SSL certificate to the specified EC2 instance.

    :param instance_id: The ID of the EC2 instance
    :param certificate_details: The details of the SSL certificate
    :param private_key: The private key for the certificate
    :param user: The SSH user for the EC2 instance
    :param key_file: The path to the SSH key file
    """
    # Retrieve the public DNS of the instance
    instance = ec2.describe_instances(InstanceIds=[instance_id])
    public_dns = instance['Reservations'][0]['Instances'][0]['PublicDnsName']

    # Connect to the instance via SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(public_dns, username=user, key_filename=key_file)

    # Deploy the certificate and private key
    cert_file = '/etc/ssl/certs/your_certificate.crt'
    key_file = '/etc/ssl/private/your_private_key.key'
    ssh.exec_command(f'echo "{certificate_details}" > {cert_file}')
    ssh.exec_command(f'echo "{private_key}" > {key_file}')

    # Restart the web server to apply the changes
    ssh.exec_command('sudo systemctl restart apache2')  # Adjust for your web server

    ssh.close()

# Example usage
if __name__ == "__main__":
    instance_id = 'i-0abcd1234efgh5678'
    private_key = 'your_private_key'
    user = 'ec2-user'
    key_file = '/path/to/your/key.pem'
    deploy_certificate_to_ec2(instance_id, certificate_details, private_key, user, key_file)