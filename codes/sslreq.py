import boto3
from botocore.exceptions import ClientError

# Create an ACM client
acm = boto3.client('acm')

def request_ssl_certificate(domain_name, validation_method='DNS'):
    """
    Request an SSL certificate for the specified domain name.

    :param domain_name: The domain name for the SSL certificate
    :param validation_method: The validation method ('DNS' or 'EMAIL')
    :return: The ARN of the requested certificate
    """
    try:
        response = acm.request_certificate(
            DomainName=domain_name,
            ValidationMethod=validation_method
        )
        certificate_arn = response['CertificateArn']
        print(f"Requested SSL certificate: {certificate_arn}")
        return certificate_arn
    except ClientError as e:
        print(f"Error requesting SSL certificate: {e}")
        raise

# Example usage
if __name__ == "__main__":
    domain_name = 'upes.ac.in'
    certificate_arn = request_ssl_certificate(domain_name)