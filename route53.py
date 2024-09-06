import boto3
from consts import Route

route53_client = boto3.client('route53')

def create_private_hosted_zone(zone_name):
    try:
        response = route53_client.create_hosted_zone(
            Name = zone_name,
            CallerReference=str(hash(zone_name)),  # Unique string to ensure idempotency
            HostedZoneConfig = {
                'Comment': 'Private hosted zone created by ' + Route['Hostname'].value,
                'PrivateZone': True
            },
            VPC = {
                'VPCRegion': 'us-east-1',  # Replace with your region
                'VPCId': Route['VPC_ID'].value  # For a single VPC; adjust for multiple VPCs if needed
            }
        )
        hosted_zone_id = response['HostedZone']['Id']
        print(f"Private hosted zone '{zone_name}' created successfully with ID '{hosted_zone_id}'.")
        return hosted_zone_id
    except Exception as e:
        print(f"Error creating private hosted zone: {str(e)}")
        return None

def manage_dns_records(zone_id, action, record_name, record_type, record_value):
    try:
        # Get all hosted zones
        response = route53_client.list_hosted_zones()
        hosted_zones = response['HostedZones']

        # Filter hosted zones by comment and PrivateZone attribute
        comment = 'Private hosted zone created by ' + Route['Hostname'].value
        matching_zones = []
        for zone in hosted_zones:
            if zone['Config']['PrivateZone']:
                zone_details = route53_client.get_hosted_zone(Id=zone['Id'])
                if 'Comment' in zone_details['HostedZone']['Config']:
                    zone_comment = zone_details['HostedZone']['Config']['Comment']
                    if comment in zone_comment:
                        matching_zones.append({
                            'Id': zone['Id'],
                            'Name': zone['Name'],
                            'Comment': zone_comment
                        })
        # If no such hosted zone / made by a different user
        if not matching_zones: 
            return

        change_batch = {
            'Changes': [
                {
                    'Action': action.upper(),  # Capitalize to match API requirements
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': record_type,
                        'TTL': 60,
                        'ResourceRecords': [{'Value': record_value}]
                    }
                }
            ]
        }
        
        # Creating / Updating / Deleting record 
        response = route53_client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch=change_batch
        )

        if action == 'upsert': # to match the output syntax
            action == 'update'
        print(f"DNS record {action}d successfully.")

    except Exception as e:
        print(f"Error managing DNS records: {str(e)}")