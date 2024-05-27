import requests
import json

API_URL = "https://search.censys.io/api/v2/hosts/search"
UID = "your-uid"
SECRET = "your-secret"

def search_devices(router_list):
    results = []

    with open(router_list, 'r') as file:
        routers = file.readlines()

    for router in routers:
        query = f"services.software.product:\"{router.strip()}\""
        params = {
            "q": query,
            "per_page": 10
        }

        response = requests.get(API_URL, auth=(UID, SECRET), params=params)

        if response.status_code == 200:
            data = response.json()
            for result in data['results']:
                ip = result['ip']
                ports = [service['port'] for service in result['services']]
                results.append({'ip': ip, 'ports': ports})
        else:
            print(f"Error: {response.status_code}, {response.text}")

    return results

router_list = 'router_list.txt'
found_devices = search_devices(router_list)
print(json.dumps(found_devices, indent=2))
