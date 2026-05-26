from typing import TypedDict, Union


class Accessibility(TypedDict, total=False):
    wheelChairAccess: bool


class DeliveryService(TypedDict, total=False):
    name: str
    orderId: str
    driverPhone: str


class AdditionalFees(TypedDict, total=False):
    name: str
    amount: str


class PromoCodes(TypedDict, total=False):
    name: str
    amount: str


class Costs(TypedDict, total=False):
    subtotal: str
    tax: str
    deliveryFee: str
    surcharge: str
    convenienceFee: str
    tip: str
    additionalFees: list[AdditionalFees]
    total: str
    promoCodes: list[PromoCodes]


class Retry(TypedDict, total=False):
    notificationUrl: str
    expiration: str


class Components(TypedDict, total=False):
    name: str
    count: int


class Modifier(TypedDict, total=False):
    name: str
    qty: int


class Mods(TypedDict, total=False):
    id: str
    name: str
    qty: int
    components: list[Components]


class ItemGroup(TypedDict, total=False):
    id: str
    name: str
    note: str


class Item(TypedDict, total=False):
    id: str
    lineId: str
    name: str
    qty: int
    price: str
    mods: Union[list[Mods], list[Modifier], list[str]]
    components: list[Components]
    specialInstructions: str
    course: str
    courseStatus: str
    seat: str
    itemGroup: ItemGroup


class PartialOrder(TypedDict, total=False):
    id: str
    name: str
    mode: str
    pickupTime: str
    phoneNumber: str
    server: str
    specialInstructions: str
    vehicleModel: str
    vehicleColor: str
    priority: bool
    deliveryAddress: str
    deliveryService: DeliveryService
    costs: Costs
    originSource: str
    checkNumber: str
    deliveryHandoff: bool
    prepTimeDuration: str
    itemsToAdd: list[Item]
    itemsToUpdate: list[Item]
    itemsToRemove: list[str]
    covers: int
    loyaltyMember: bool
