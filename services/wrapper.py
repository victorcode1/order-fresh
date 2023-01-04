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




deviceId = "de787945-d1dd-4af5-b33c-5d98b6f6bb76"
storeId = "86353278-e302-47a6-823d-99c89d6d0b78"
tok = "IuOjJi6uAMkEzybWjogaKYvh2J0KwVxyN7h3M3rgwAY0vlyztgB1kWo6V51V01rFh0nuirqHjutO6STCalnwzc"

mydev = getOrders(tok, storeId, deviceId)
print(mydev)




        