from datetime import datetime
import random
import uuid
from pyKDSAPI.utils import sendOrder
from pyKDSAPI.structs import Item, Mods,Costs

# Datos reales
token = 'BH5yuMvuuQOfOrUUDSdpsZr4INBf8STUI8dt1YjeiyUHag5SaVuVAB2YYqd2PovCDEpq4EvIHppHSjRSVPkggB'
location_id = '687e1a74-03b4-4b6d-bdd9-3dc96193b813'
device_id = '14d5cdca-05de-4715-bbe1-4f52444dcc0e'

# Listas para generar valores aleatorios
nombres_clientes = ['Luis',  ]
productos = ['pollo']
modificadores = ['Sin cebolla', ]

# Generar ítems aleatorios
def generar_item():
    producto = random.choice(productos)
    mod = random.choice(modificadores)
    return Item(
        id=str(uuid.uuid4()),
        name=producto,
        qty=random.randint(1, 3),
        mods=[Mods(id=str(uuid.uuid4()), name=mod, components=[])],
        lineId=str(uuid.uuid4()),
        price=str(round(random.uniform(5.00, 20.00), 2)),
        components=[],
        specialInstructions=random.choice(["", "Sin condimentos", "Cocido bien", mod])
    )

# Datos del pedido
order_id = f'orden-{uuid.uuid4().hex[:6]}'
cliente = random.choice(nombres_clientes)
items = [generar_item() for _ in range(random.randint(1, 3))]

# Enviar orden usando todos los campos
response = sendOrder(
    token=token,
    store=location_id,
    device=device_id,
    id=order_id,
    name=f"{cliente} Cliente",
    mode=random.choice(["For Here", "ToGo", "Pickup", "DriveThru", "Delivery", "CurbSide"]),
    items=items,
    terminal=random.choice(["Caja 1", "Terminal 2", "POS 3"]),
    time=datetime.now().isoformat(),
    phoneNumber=f"+569{random.randint(10000000, 99999999)}",
    optInForSms=random.choice([True, False]),
    deliveryAddress=random.choice(["Av. Falsa 123", "Calle Real 456", "Ruta 789"]),
 server=random.choice(["Mozo 1", "Camarera 2", "AutoServicio"]),
# source=random.choice(["POS-System", "API-Integration", "WebOrder"]),
    pickupTime=datetime.now().isoformat(),
    specialInstructions=random.choice(["Agregar cubiertos", "Mesa con silla alta", "Sin cubiertos", ""]),
    customerArrivedUrl="https://example.com/arrived",
    vehicleModel=random.choice(["Toyota", "Ford", "Hyundai", ""]),
    vehicleColor=random.choice(["Rojo", "Negro", "Blanco", "Azul"]),
    retry={
        "notificationUrl": "https://example.com/notify",
        "expiration": datetime.now().isoformat()
    },
    costs={
        "subtotal": str(round(random.uniform(15.0, 30.0), 2)),
        "tax": str(round(random.uniform(1.0, 5.0), 2)),
        "deliveryFee": "0.00",
        "surcharge": "0.00",
        "convenienceFee": "0.00",
        "tip": "0.00",
        "additionalFees": [],
        "total": str(round(random.uniform(20.0, 40.0), 2)),
        "promoCodes": []
    },
    deliveryservice={
        "name": random.choice(["UberEats", "Rappi", "PedidosYa"]),
        "orderId": f"TRK{random.randint(1000, 9999)}XYZ",
        "driverPhone": f"+569{random.randint(10000000, 99999999)}"
    },
    # accessibility={
    #     "wheelChairAccess": random.choice([True, False])
    # },
    originSource=random.choice(["ThirdPartyVendor", "MobileApp", "WebKiosk"])
)

# Mostrar resultado
print(f"🧾 Orden enviada: {order_id}")
print(f"👤 Cliente: {cliente}")
print(f"📦 Total ítems: {len(items)}")
for i in items:
    mods = i.get('mods', [])
    mod_name = mods[0].get('name', 'Sin modificador') if mods else 'Sin modificador'
    print(f" - {i['qty']} x {i['name']} [{mod_name}]")

print("📡 Respuesta del servidor:")
print(response)
