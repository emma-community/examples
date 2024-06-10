import requests
import json
import os

CLIENT_ID=os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')

# Get a list of VMs with IPs and provider 
def get_VMs():
    # Issue token request
    token_url = 'https://api.emma.ms/external/v1/issue-token'
    token_payload = {
        'clientId': CLIENT_ID,
        'clientSecret': CLIENT_SECRET
    }
    token_headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(token_url, headers=token_headers, data=json.dumps(token_payload))
    response_data = response.json()
    ACCESS_TOKEN = response_data.get('accessToken')

    # Fetch VMS information
    vms_url = 'https://api.emma.ms/external/v1/vms'
    vms_headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    vms_response = requests.get(vms_url, headers=vms_headers)
    vms_data = vms_response.json()

    # Extract and print VM names and IDs
    vm_info = {}
    for vm in vms_data:
        name = vm['name']
        provider = vm['dataCenter']['providerName']
        networks = vm['networks']
        public_ip = None
        
        for network in networks:
            if network['networkType'] == 'PUBLIC':
                public_ip = network['ip']
                break
                
        if public_ip:  # Ensure there is a public IP before adding to the dictionary
            vm_info[public_ip] = {'name': name, 'provider': provider}

    return vm_info
    
