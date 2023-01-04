import requests

def getOrganization(token: str):
    headers = {"x-integration-token": token}
    payload = {}
    url = "https://integrations-api.ftservices.cloud/integrators/kds-information"
    response = requests.request("GET", url=url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()

    else:
        return response.status_code


def getStores(token: str):
    headers = {"x-integration-token": token}
    payload = {}
    url = "https://integrations-api.ftservices.cloud/integrators/kds-information/locations"
    response = requests.request("GET", url=url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()

    else:
        return response.status_code

def getDevices(token: str, store: str):
    headers = {"x-integration-token": token}
    
    payload = {}
    
    url = f"https://integrations-api.ftservices.cloud/integrators/kds-information/locations/{store}/devices"
    
    response = requests.request("GET", url=url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()

    else:
        return response.status_code



def getOrders(token: str, store: str, device: str):
    headers = {
        "x-integration-token": token,
        "x-location-id": store,
        "x-device-ids": device
        }
    payload = {}
    url = "https://integrations-api.ftservices.cloud/integrators/kds-orders/active"
    
    response = requests.request("GET", url=url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()

    else:
        return response.status_code







        