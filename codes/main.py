import boto3
from createec2 import create_ec2_instance
from keypair import create_key_pair
from roles import create_iam_role, attach_policies_to_role
from sslreq import request_ssl_certificate
from retrievecert import get_certificate
from deploysslec2 import deploy_certificate_to_ec2
from deployssllb import attach_certificate_to_elb
from updatedns import update_dns_record

def main():
    # Create a key pair
    key_name = 'autosslkey'
    try:
        key_pair = create_key_pair(key_name)
    except Exception as e:
        print(f"Key pair creation failed: {e}")
        return

    # Create an EC2 instance
    image_id = 'ami-00a929b66ed6e0de6'
    instance_type = 't2.micro'
    security_group_id = 'sg-0e046b6a95b43a069'
    subnet_id = 'subnet-036a3d8013eef2a1e'
    try:
        instance_id = create_ec2_instance(image_id, instance_type, key_name, security_group_id, subnet_id)
    except Exception as e:
        print(f"EC2 instance creation failed: {e}")
        return

    # Create IAM roles and attach policies
    iam_client = boto3.client('iam')
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
    for role_name, role_info in roles.items():
        try:
            role_arn = create_iam_role(iam_client, role_name, trust_policy, role_info["description"])
            attach_policies_to_role(iam_client, role_name, role_info["policies"])
        except Exception as e:
            print(f"IAM role creation or policy attachment failed: {e}")
            return

    # Request an SSL certificate
    domain_name = 'example.com'
    try:
        certificate_arn = request_ssl_certificate(domain_name)
    except Exception as e:
        print(f"SSL certificate request failed: {e}")
        return

    # Retrieve the SSL certificate details
    try:
        certificate_details = get_certificate(certificate_arn)
    except Exception as e:
        print(f"Retrieving SSL certificate details failed: {e}")
        return

    # Deploy the SSL certificate to the EC2 instance
    private_key = key_pair['KeyMaterial']
    user = 'ec2-user'
    key_file = f"{key_name}.pem"
    try:
        deploy_certificate_to_ec2(instance_id, certificate_details, private_key, user, key_file)
    except Exception as e:
        print(f"Deploying SSL certificate to EC2 instance failed: {e}")
        return

    # Attach the SSL certificate to the load balancer
    load_balancer_arn = 'arn:aws:elasticloadbalancing:region:account-id:loadbalancer/app/load-balancer-name/id'
    listener_arn = 'arn:aws:elasticloadbalancing:region:account-id:listener/app/load-balancer-name/id'
    try:
        attach_certificate_to_elb(load_balancer_arn, listener_arn, certificate_arn)
    except Exception as e:
        print(f"Attaching SSL certificate to load balancer failed: {e}")
        return

    # Update the DNS record
    zone_id = 'Z3M3LMPEXAMPLE'
    record_name = 'example.com'
    record_type = 'A'
    record_value = '192.0.2.1'
    try:
        update_dns_record(zone_id, record_name, record_type, record_value)
    except Exception as e:
        print(f"Updating DNS record failed: {e}")
        return

    print("All operations completed successfully.")

if __name__ == "__main__":
    main()