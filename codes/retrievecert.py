import boto3
from botocore.exceptions import ClientError

# Create an ACM client
acm = boto3.client('acm')

def get_certificate(certificate_arn):
    """
    Retrieve the details of the specified SSL certificate.

    :param certificate_arn: The ARN of the certificate
    :return: The certificate details
    """
    try:
        response = acm.describe_certificate(CertificateArn=certificate_arn)
        return response['Certificate']
    except ClientError as e:
        print(f"Error retrieving certificate: {e}")
        raise

# Example usage
if __name__ == "__main__":
    certificate_arn = 'arn:aws:acm:region:account-id:certificate/certificate-id'
    certificate_details = get_certificate(certificate_arn)
    print(certificate_details)