from typing import TypedDict

class Accessibility(TypedDict):
    wheelChairAccess: bool # Value will be sent to supported integration (Apex Lockers)

class DeliveryService(TypedDict):
    name: str # Name of the service
    
    orderId: str # Delivery service order ID

    driverPhone: str # Delivery drivers phone number

class AdditionalFees(TypedDict):
    name: str # Name of the fee

    amount: str # Amount of the fee

class PromoCodes(TypedDict):
    name: str # Name of the code

    amount: str # Amount of Promo, value can include currency symbol

class Costs(TypedDict):
    subtotal: str # Subtotal of the order

    tax: str # Tax applied to the order

    deliveryFee: str # Delivery fee

    surcharge: str # Surcharge for the order

    convenienceFee: str # Convenicence fee applied to the order

    tip: str # Tip applied to the order

    additionalFees: list[AdditionalFees] # Any additional fees (see AdditionalFees)

    total: str # Total charge for the order

    promoCodes: list[PromoCodes] # Promotional codes to reduce order amount (see PromoCodes)


class Retry(TypedDict):
    notificationUrl: str # URL to post final success or failure upon expiration

    expiration: str # Time when the order will send your success or failure (ISO 8601 format)

class Components(TypedDict):
    name: str # Name of the component
    
    count: int # Quantity of the component to add onto the modifications

class Mods(TypedDict):
    id: str # ID of the modifier

    name: str # Name of the modifer
    
    components: list[Components] # List of components (see Components)

class Item(TypedDict):
    
    # Required to create an item
    id: str #ID of the item
    
    name: str # Name of the item
    
    qty: int # Quantity of the item ordered
    
    mods: list[Mods] # Modifier list (see Mods)

    # Optional fields for an item
    lineId: str # ID of the item on the order (used to update particular order item)

    price: str # Price of the item
    
    components: list[Components] # Components of the item (see Components)
    
    specialInstructions: str # Special instructions on the individual item (seperate from special instructions on the order)