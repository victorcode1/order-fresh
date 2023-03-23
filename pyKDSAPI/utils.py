import requests
from typing import TypedDict

def getOrganization(token: str, headers: dict={}, payload: dict={}):
    headers["x-integration-token"] = token
    url = "https://integrations-api.ftservices.cloud/integrators/kds-information"
    response = requests.request("GET", url=url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()

    else:
        return response.status_code


def getStores(token: str, headers: dict={}, payload: dict={}):
    headers["x-integration-token"] = token
    url = "https://integrations-api.ftservices.cloud/integrators/kds-information/locations"
    response = requests.request("GET", url=url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()

    else:
        return response.status_code

def getDevices(token: str, store: str, headers: dict={}, payload: dict={}):
    headers["x-integration-token"] = token
    
    url = f"https://integrations-api.ftservices.cloud/integrators/kds-information/locations/{store}/devices"
    
    response = requests.request("GET", url=url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()

    else:
        return response.status_code



def getOrders(token: str, store: str, device: str, headers: dict={}, payload: dict={}):
    headers["x-integration-token"] = token
    headers["x-location-id"] = store
    headers["x-device-ids"] = device

    url = "https://integrations-api.ftservices.cloud/integrators/kds-orders/active"
    
    response = requests.request("GET", url=url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()

    else:
        return response.status_code

class Retry(TypedDict):
    notificationUrl: str
    expiration: str

class Item(TypedDict):
    
    #required to create an item
    id: str
    name: str
    qty: int
    mods: list[str]

    #optional fields for an item
    lineId: str
    price: str
    components: list[str]
    specialInstructions: str


def sendOrder(

#used as headers to authorize and send your order
token: str, 
store: str, 
device: str, 

#minimum required arguments to create an order in FreshKDS
id: str, 
name: str, 
time: str,
mode: str,
items: list[Item],
terminal: str,

#optional arguments for an order
phoneNumber: str = None,
optInForSms: bool = None,
deliveryAddress: str = None,
server: str = None,
source: str = None,
pickupTime: str = None,
specialInstructions: str = None,
customerArrivedUrl: str = None,
vehicleModel: str = None,
vehicleColor: str = None,
retry: str = None,
costs: dict = None,

#for requests
headers: dict={}, 


):

    if id == None or name == None or time == None or mode == None or items == None or terminal == None:
        print("Could Not send order")
        return "Could not send order"
    
    headers["x-integration-token"] = token
    headers["x-location-id"] = store
    headers["x-device-ids"] = device
    
    url = "https://integrations-api.ftservices.cloud/integrators/kds-orders"

    payload = {
        "id": id,
        "name": name,
        "time": time,
        "mode": mode,
        "items": items,
        "terminal": terminal,

        "phoneNumber": phoneNumber,
        "optInForSms": optInForSms,
        "deliveryAddress": deliveryAddress,
        "server": server,
        "source": source,
        "pickupTime": pickupTime,
        "specialInstructions": specialInstructions,
        "customerArrivedUrl": customerArrivedUrl,
        "vehicleModel": vehicleModel,
        "vehicleColor": vehicleColor,
        "retry": retry,
        "costs": costs
    }

    response = requests.request("POST", url=url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()

    else:
        return response.status_code



