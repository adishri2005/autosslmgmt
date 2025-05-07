import boto3
from botocore.exceptions import ClientError

# Create an ELB client
elb = boto3.client('elbv2')

def attach_certificate_to_elb(load_balancer_arn, listener_arn, certificate_arn):
    """
    Attach the SSL certificate to the specified load balancer.

    :param load_balancer_arn: The ARN of the load balancer
    :param listener_arn: The ARN of the listener
    :param certificate_arn: The ARN of the certificate
    """
    try:
        elb.modify_listener(
            ListenerArn=listener_arn,
            Certificates=[{'CertificateArn': certificate_arn}]
        )
        print(f"Attached certificate {certificate_arn} to load balancer {load_balancer_arn}.")
    except ClientError as e:
        print(f"Error attaching certificate to load balancer: {e}")
        raise

# Example usage
if __name__ == "__main__":
    load_balancer_arn = 'arn:aws:elasticloadbalancing:region:account-id:loadbalancer/app/load-balancer-name/id'
    listener_arn = 'arn:aws:elasticloadbalancing:region:account-id:listener/app/load-balancer-name/id'
    certificate_arn = 'arn:aws:acm:region:account-id:certificate/certificate-id'
    attach_certificate_to_elb(load_balancer_arn, listener_arn, certificate_arn)