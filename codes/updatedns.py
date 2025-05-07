import boto3
from botocore.exceptions import ClientError

# Create a Route 53 client
route53 = boto3.client('route53')

def update_dns_record(zone_id, record_name, record_type, record_value):
    """
    Update the DNS record to point to the new certificate.

    :param zone_id: The ID of the hosted zone
    :param record_name: The name of the DNS record
    :param record_type: The type of the DNS record (e.g., 'A', 'CNAME')
    :param record_value: The value of the DNS record
    """
    try:
        response = route53.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [{
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': record_type,
                        'TTL': 300,
                        'ResourceRecords': [{'Value': record_value}]
                    }
                }]
            }
        )
        print(f"Updated DNS record: {response}")
    except ClientError as e:
        print(f"Error updating DNS record: {e}")
        raise

# Example usage
if __name__ == "__main__":
    zone_id = 'Z3M3LMPEXAMPLE'
    record_name = 'example.com'
    record_type = 'A'
    record_value = '192.0.2.1'
    update_dns_record(zone_id, record_name, record_type, record_value)