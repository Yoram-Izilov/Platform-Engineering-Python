import boto3
from consts import Route

route53_client = boto3.client('route53')

def create_private_hosted_zone(zone_name):
    try:
        # Creating the zone
        response = route53_client.create_hosted_zone(
            Name = zone_name,
            CallerReference=str(hash(zone_name)),  # Unique string to ensure it runs only one time
            HostedZoneConfig = {
                'Comment': 'Private hosted zone created by ' + Route['Hostname'].value,
                'PrivateZone': True
            },
            VPC = {
                'VPCRegion': 'us-east-1',
                'VPCId': Route['VPC_ID'].value
            }
        )

        # Get the hosted zone ID from the response
        hosted_zone_id = response['HostedZone']['Id']

        # Add tags to the hosted zone after creation
        route53_client.change_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=hosted_zone_id.split('/')[-1],  # Extract the actual ID
            AddTags=[
                {'Key': Route['Hostname'].name, 'Value': Route['Hostname'].value}
            ]
        )
        print(f"Private hosted zone '{zone_name}' created successfully with ID '{hosted_zone_id}'.")

    except Exception as e:
        print(f"Error creating private hosted zone: {str(e)}")
        return None

def manage_dns_records(zone_id, action, record_name, record_type, record_value):
    try:
        # Get all hosted zones
        response = route53_client.list_hosted_zones()
        hosted_zones = response['HostedZones']
        # Get only the maching zones with the host tag
        matching_zones = get_host_zones(hosted_zones)

        # If no such hosted zone / made by a different user
        if not matching_zones:
            print("No hosted zone or the zone was not created by the host")
            return

        # Wrap record_value in quotes for TXT records
        if record_type == 'TXT':
            record_value = f'"{record_value}"'
    
        # Managing DNS records for the filtered zone
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

        # Adjusting the output for upsert (update)
        if action == 'upsert':
            action == 'update'
        print(f"DNS record {action}d successfully.")

    except Exception as e:
        print(f"Error managing DNS records: {str(e)}")

def get_host_zones(all_hosted_zones):
    # Filter hosted zones by tag
    matching_zones = []
    for zone in all_hosted_zones:
        # Retrieve tags for each hosted zone
        tags_response = route53_client.list_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=zone['Id'].split('/')[-1]  # Extract actual hosted zone ID
        )
        tags = tags_response['ResourceTagSet']['Tags']

        # Check if the host made this zone by checking tags
        for tag in tags:
            if tag['Key'] == Route['Hostname'].name and tag['Value'] == Route['Hostname'].value:
                if zone['Config']['PrivateZone']:  # Ensure it's a private hosted zone
                    matching_zones.append({
                        'Id': zone['Id'],
                        'Name': zone['Name'],
                        'Tags': tags
                    })
                break
    return matching_zones