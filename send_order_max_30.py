from datetime import datetime
import random
import uuid
from pyKDSAPI.utils import SendMinimalOrder
from pyKDSAPI.structs import Item, Mods

# Datos REALES
token = '2cjIGIFIWNOd5qkt6yMg5wdoo546msuNZkepG1RJc8L2RVy6rWK1A2DmjdKxsmPjRSn1oBPoKCRW3HFrDQ7AVl'
location_id = '9943ab9c-dcbe-4d93-b902-92cdeabf771d'
device_id = 'b4d439c7-5c6a-421c-9365-f55b882dfc4a'

# Listas para generar datos aleatorios
nombres_clientes = ['Luis', 'Ana', 'Carlos', 'María', 'Pedro', 'Lucía', 'Elena', 'Javier']
productos = ['Hamburguesa Clásica', 'Pizza Margarita', 'Ensalada César', 'Sándwich de Pollo', 'Wrap Vegetariano', 'Tacos al Pastor', 'Nachos con Queso', 'Sopa de Pollo']
modificadores = ['Sin cebolla', 'Extra queso', 'Sin tomate', 'Pan sin gluten', 'Sin mayonesa', 'Salsa picante', 'Extra lechuga', 'Sin sal']

# Función para generar un ítem aleatorio
def generar_item():
    producto = random.choice(productos)
    mod_nombre = random.choice(modificadores)
    return Item(
        id=str(uuid.uuid4()),
        name=producto,
        qty=random.randint(1, 3),
        mods=[
            Mods(
                id=str(uuid.uuid4()),
                name=mod_nombre,
                components=[]
            )
        ],
        lineId=str(uuid.uuid4()),
        price=str(round(random.uniform(5.00, 15.00), 2)),
        components=[],
        specialInstructions=random.choice([mod_nombre, "", "Sin condimentos", "Entregar rápido", ""])
    )

# Generar nombre y pedido aleatorios
nombre_cliente = random.choice(nombres_clientes)
order_id = f'orden-{uuid.uuid4().hex[:6]}'

# ⚠️ Generar una cantidad aleatoria de ítems entre 1 y 30
cantidad_items = random.randint(1, 14)
items = [generar_item() for _ in range(cantidad_items)]

# Enviar la orden
response = SendMinimalOrder(
    token=token,
    store=location_id,
    device=device_id,
    id=order_id,
    name=f'{nombre_cliente} Cliente',
    mode='For Here',
    items=items,
    terminal='Caja 1',
    time=datetime.now().isoformat()
)

# Mostrar resumen
print(f"🧾 Orden enviada: {order_id}")
print(f"👤 Cliente: {nombre_cliente}")
print(f"📦 Total ítems: {len(items)}")
for i in items:
    mod = i['mods'][0]['name'] if i['mods'] else "Sin modificador"
    print(f" - {i['qty']} x {i['name']} [{mod}]")
print("📡 Respuesta del servidor:")
print(response)
