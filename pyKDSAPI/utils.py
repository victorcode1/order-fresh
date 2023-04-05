import requests
from structs import Retry, Components, Mods, Item
from datetime import datetime
import json
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




def sendOrder(

# Used as headers to authorize and send your order
token: str, # Your 'Integration Token' 

store: str, # Name of the location (must be active) 

device: str, # Name of the device to send to (originating device only)

# Minimum required arguments to create an order in FreshKDS
id: str, # ID of the order (must be unique) 

name: str, # Name of customer or order

mode: str, # Order type must be (For Here, ToGo, Pickup, DriveThru, Delivery, CurbSide)

items: list[Item], # Items on the order must be of type 'Item' (see structs Item)

terminal: str, # Name of the terminal that will accept the order

time: str = str(datetime.now().isoformat()), # Time the order is place (must be in ISO 8601 format)

# Optional arguments for an order
phoneNumber: str = None, # Customers phone number

optInForSms: bool = None, # Whether the customer opted into SMS messaging (default true)

deliveryAddress: str = None, # Customers delivery address

server: str = None, # Server Name

source: str = None, # Integration source (for partners only)

pickupTime: str = None, # Pickup time (must be in ISO 8601 format)

specialInstructions: str = None, # Special instructions on the order

customerArrivedUrl: str = None, # URL to integrators system to send a notification that the customer has arrived

vehicleModel: str = None, # Customers vehichle model

vehicleColor: str = None, # Customers vehichle color

retry: Retry = None, # URL to send a success or failure when expiration is reached (see structs Retry)

costs: dict = None, # Costs associated with the order (see structs Costs)

deliveryservice: dict = None, # Object that contains information about the delivery service (see structs DeliveryService)

accessibility: dict = None, # Information regarding ADA needs (see structs Accessibility)

originSource: str = None, # Only used when order is coming from a third party source

# For requests
headers: dict={}, 
):
    # Testing if all required items are filled in
    if id == None or name == None or time == None or mode == None or items == None or terminal == None:
        print("Could Not send order")
        return "Could not send order"
    # Adds your tokens into the headers and sets content type to application/json
    headers["x-integration-token"] = token
    headers["x-location-id"] = store
    headers["x-device-ids"] = device
    headers["Content-Type"] = "application/json"
    
    # Production URL for Fresh KDS
    url = "https://integrations-api.ftservices.cloud/integrators/kds-orders"

    # Data payload for requests
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
        "costs": costs,
        "deliveryservice": deliveryservice,
        "accessibility": accessibility,
        "originSource": originSource
    }

    # Convert dictionary into a JSON object
    payload = json.dumps(payload)

    # Sends POST request
    response = requests.request("POST", url=url, headers=headers, data=payload)
    
    # If status is ok return success in json
    if response.status_code == 200:
        return response.json()
    # Returns error status code (ex: 400, 404, 500)
    else:
        return response.status_code



def SendMinimalOrder(
    # Used as headers to authorize and send your order
    token: str, # Your 'Integration Token' 

    store: str, # Name of the location (must be active) 

    device: str, # Name of the device to send to (originating device only)

    # Minimum required arguments to create an order in FreshKDS
    id: str, # ID of the order (must be unique) 

    name: str, # Name of customer or order

    mode: str, # Order type must be (For Here, ToGo, Pickup, DriveThru, Delivery, CurbSide)

    items: list[Item], # Items on the order must be of type 'Item' (see structs Item)

    terminal: str, # Name of the terminal that will accept the order

    time: str = str(datetime.now().isoformat()), # Time the order is place (must be in ISO 8601 format)
    
    # For requests
    headers: dict={}, 
):

    # Testing if all required items are filled in
    if id == None or name == None or time == None or mode == None or items == None or terminal == None:
        print("Could Not send order")
        return "Could not send order"
    
    # Adds your tokens into the headers and sets content type to application/json
    headers["x-integration-token"] = token
    headers["x-location-id"] = store
    headers["x-device-ids"] = device
    headers["Content-Type"] = "application/json"
    
    # Production URL for Fresh KDS
    url = "https://integrations-api.ftservices.cloud/integrators/kds-orders"

    payload = {
        "id": id,
        "name": name,
        "time": time,
        "mode": mode,
        "items": items,
        "terminal": terminal,}
    
        # Convert dictionary into a JSON object
    payload = json.dumps(payload)

    # Sends POST request
    response = requests.request("POST", url=url, headers=headers, data=payload)
    
    # If status is ok return success in json
    if response.status_code == 200:
        return response.json()
    # Returns error status code (ex: 400, 404, 500)
    else:
        return response.status_code
