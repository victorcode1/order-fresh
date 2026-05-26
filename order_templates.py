from datetime import datetime, timedelta
import random
import uuid
from typing import Optional

from pyKDSAPI.structs import Costs, Item, Mods
from pyKDSAPI.utils import SendMinimalOrder, sendOrder


def _print_order_summary(result: dict) -> None:
    print(f"Orden enviada: {result['order_id']}")
    print(f"Cliente: {result['customer']}")
    print(f"Total items: {len(result['items'])}")
    for item in result["items"]:
        mods = item.get("mods", [])
        mod_name = mods[0].get("name", "Sin modificador") if mods else "Sin modificador"
        print(f" - {item['qty']} x {item['name']} [{mod_name}]")
    print("Respuesta del servidor:")
    print(result["response"])


def print_order_summary(result: dict) -> None:
    _print_order_summary(result)


def _new_order_id(prefix: str = "orden") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:6]}"


def _random_customer() -> str:
    return random.choice(["Luis", "Ana", "Carlos", "Maria", "Pedro", "Lucia", "Elena", "Javier"])


def _item(
    name: str,
    qty: int = 1,
    mod_name: str = "Sin modificador",
    price: str = "10.00",
    **extra_fields,
) -> Item:
    item = Item(
        lineId=str(uuid.uuid4()),
        name=name,
        qty=qty,
        mods=[{"name": mod_name, "qty": 1}],
        price=price,
        specialInstructions=extra_fields.pop("specialInstructions", ""),
    )
    item.update(extra_fields)
    return item


def _base_result(order_id: str, customer: str, items: list[Item], response) -> dict:
    return {
        "order_id": order_id,
        "customer": customer,
        "items": items,
        "response": response,
    }


def run_complete_order(token: str, location_id: str, device_id: str) -> dict:
    nombres_clientes = ["Luis", "Ana", "Carlos", "Maria", "Pedro", "Lucia", "Elena", "Javier"]
    productos = [
        "Hamburguesa Clasica",
        "Pizza Margarita",
        "Ensalada Cesar",
        "Sandwich de Pollo",
        "Wrap Vegetariano",
    ]
    modificadores = ["Sin cebolla", "Extra queso", "Sin tomate", "Pan sin gluten", "Sin mayonesa"]

    def generar_item() -> Item:
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
            specialInstructions=random.choice(["", "Sin condimentos", "Cocido bien", mod]),
        )

    order_id = f"orden-{uuid.uuid4().hex[:6]}"
    cliente = random.choice(nombres_clientes)
    items = [generar_item() for _ in range(random.randint(1, 3))]

    subtotal = round(random.uniform(15.0, 30.0), 2)
    tax = round(subtotal * 0.08, 2)
    total = subtotal + tax

    costs_obj = Costs(
        subtotal=f"{subtotal:.2f}",
        tax=f"{tax:.2f}",
        deliveryFee="0.00",
        surcharge="0.00",
        convenienceFee="0.00",
        tip="0.00",
        additionalFees=[],
        total=f"{total:.2f}",
        promoCodes=[],
    )

    response = sendOrder(
        token=token,
        store=location_id,
        device=device_id,
        id=order_id,
        name=f"{cliente} Cliente",
        mode=random.choice(["For Here", "ToGo", "Pickup", "DriveThru", "Delivery", "Curbside"]),
        items=items,
        terminal=random.choice(["Caja 1", "Terminal 2", "POS 3"]),
        time=datetime.now().isoformat(),
        phoneNumber=f"+569{random.randint(10000000, 99999999)}",
        optInForSms=random.choice([True, False]),
        deliveryAddress=random.choice(["Av. Falsa 123", "Calle Real 456", "Ruta 789"]),
        server=random.choice(["Mozo 1", "Camarera 2", "AutoServicio"]),
        pickupTime=datetime.now().isoformat(),
        specialInstructions=random.choice(["Agregar cubiertos", "Mesa con silla alta", "Sin cubiertos", ""]),
        customerArrivedUrl="https://example.com/arrived",
        vehicleModel=random.choice(["Toyota", "Ford", "Hyundai", ""]),
        vehicleColor=random.choice(["Rojo", "Negro", "Blanco", "Azul"]),
        retry={
            "notificationUrl": "https://example.com/notify",
            "expiration": datetime.now().isoformat(),
        },
        costs=costs_obj,
        deliveryservice={
            "name": random.choice(["UberEats", "Rappi", "PedidosYa"]),
            "orderId": f"TRK{random.randint(1000, 9999)}XYZ",
            "driverPhone": f"+569{random.randint(10000000, 99999999)}",
        },
        originSource=random.choice(["ThirdPartyVendor", "MobileApp", "WebKiosk"]),
    )

    return {
        "order_id": order_id,
        "customer": cliente,
        "items": items,
        "response": response,
    }


def run_complete_copy_order(token: str, location_id: str, device_id: str) -> dict:
    nombres_clientes = ["Luis"]
    productos = ["pollo"]
    modificadores = ["Sin cebolla"]

    def generar_item() -> Item:
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
            specialInstructions=random.choice(["", "Sin condimentos", "Cocido bien", mod]),
        )

    order_id = f"orden-{uuid.uuid4().hex[:6]}"
    cliente = random.choice(nombres_clientes)
    items = [generar_item() for _ in range(random.randint(1, 3))]

    response = sendOrder(
        token=token,
        store=location_id,
        device=device_id,
        id=order_id,
        name=f"{cliente} Cliente",
        mode=random.choice(["For Here", "ToGo", "Pickup", "DriveThru", "Delivery", "Curbside"]),
        items=items,
        terminal=random.choice(["Caja 1", "Terminal 2", "POS 3"]),
        time=datetime.now().isoformat(),
        phoneNumber=f"+569{random.randint(10000000, 99999999)}",
        optInForSms=random.choice([True, False]),
        deliveryAddress=random.choice(["Av. Falsa 123", "Calle Real 456", "Ruta 789"]),
        server=random.choice(["Mozo 1", "Camarera 2", "AutoServicio"]),
        pickupTime=datetime.now().isoformat(),
        specialInstructions=random.choice(["Agregar cubiertos", "Mesa con silla alta", "Sin cubiertos", ""]),
        customerArrivedUrl="https://example.com/arrived",
        vehicleModel=random.choice(["Toyota", "Ford", "Hyundai", ""]),
        vehicleColor=random.choice(["Rojo", "Negro", "Blanco", "Azul"]),
        retry={
            "notificationUrl": "https://example.com/notify",
            "expiration": datetime.now().isoformat(),
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
            "promoCodes": [],
        },
        deliveryservice={
            "name": random.choice(["UberEats", "Rappi", "PedidosYa"]),
            "orderId": f"TRK{random.randint(1000, 9999)}XYZ",
            "driverPhone": f"+569{random.randint(10000000, 99999999)}",
        },
        originSource=random.choice(["ThirdPartyVendor", "MobileApp", "WebKiosk"]),
    )

    return {
        "order_id": order_id,
        "customer": cliente,
        "items": items,
        "response": response,
    }


def run_minimal_order(token: str, location_id: str, device_id: str, max_items: int, qty_choices: Optional[list[int]] = None) -> dict:
    nombres_clientes = ["Luis", "Ana", "Carlos", "Maria", "Pedro", "Lucia", "Elena", "Javier"]
    productos = [
        "Hamburguesa Clasica",
        "Pizza Margarita",
        "Ensalada Cesar",
        "Sandwich de Pollo",
        "Wrap Vegetariano",
        "Tacos al Pastor",
        "Nachos con Queso",
        "Sopa de Pollo",
    ]
    modificadores = [
        "Sin cebolla",
        "Extra queso",
        "Sin tomate",
        "Pan sin gluten",
        "Sin mayonesa",
        "Salsa picante",
        "Extra lechuga",
        "Sin sal",
    ]

    def generar_item() -> Item:
        producto = random.choice(productos)
        mod_nombre = random.choice(modificadores)
        qty = random.choice(qty_choices) if qty_choices else random.randint(1, 3)
        return Item(
            id=str(uuid.uuid4()),
            name=producto,
            qty=qty,
            mods=[Mods(id=str(uuid.uuid4()), name=mod_nombre, components=[])],
            lineId=str(uuid.uuid4()),
            price=str(round(random.uniform(5.00, 15.00), 2)),
            components=[],
            specialInstructions=random.choice([mod_nombre, "", "Sin condimentos", "Entregar rapido", ""]),
        )

    nombre_cliente = random.choice(nombres_clientes)
    order_id = f"orden-{uuid.uuid4().hex[:6]}"
    cantidad_items = random.randint(1, max_items)
    items = [generar_item() for _ in range(cantidad_items)]

    response = SendMinimalOrder(
        token=token,
        store=location_id,
        device=device_id,
        id=order_id,
        name=f"{nombre_cliente} Cliente",
        mode="For Here",
        items=items,
        terminal="Caja 1",
        time=datetime.now().isoformat(),
    )

    return {
        "order_id": order_id,
        "customer": nombre_cliente,
        "items": items,
        "response": response,
    }


def run_delivery_handoff_order(token: str, location_id: str, device_id: str) -> dict:
    customer = _random_customer()
    order_id = _new_order_id("delivery")
    subtotal = 28.50
    items = [
        _item("Bowl de Pollo", 2, "Salsa aparte", "11.00"),
        _item("Limonada", 1, "Sin hielo", "4.50"),
    ]

    response = sendOrder(
        token=token,
        store=location_id,
        device=device_id,
        id=order_id,
        name=f"{customer} Delivery",
        mode="Delivery",
        items=items,
        terminal="Delivery App",
        time=datetime.now().isoformat(),
        phoneNumber=f"+569{random.randint(10000000, 99999999)}",
        optInForSms=True,
        deliveryAddress="Av. Principal 123, Torre B, Apto 402",
        deliveryHandoff=True,
        specialInstructions="Entregar en recepcion si el cliente no responde.",
        costs=Costs(
            subtotal=f"{subtotal:.2f}",
            tax="2.28",
            deliveryFee="3.50",
            surcharge="0.00",
            convenienceFee="1.00",
            tip="2.00",
            additionalFees=[],
            total="37.28",
            promoCodes=[],
        ),
        deliveryservice={
            "name": "DoorDash",
            "orderId": f"DD-{random.randint(10000, 99999)}",
            "driverPhone": f"+569{random.randint(10000000, 99999999)}",
        },
        originSource="DeliveryMarketplace",
    )
    return _base_result(order_id, customer, items, response)


def run_curbside_order(token: str, location_id: str, device_id: str) -> dict:
    customer = _random_customer()
    order_id = _new_order_id("curbside")
    pickup_time = datetime.now() + timedelta(minutes=12)
    items = [
        _item("Combo Hamburguesa", 1, "Extra queso", "14.50"),
        _item("Papas grandes", 1, "Sin sal", "4.00"),
    ]

    response = sendOrder(
        token=token,
        store=location_id,
        device=device_id,
        id=order_id,
        name=f"{customer} Curbside",
        mode="Curbside",
        items=items,
        terminal="Curbside POS",
        time=datetime.now().isoformat(),
        pickupTime=pickup_time.isoformat(),
        phoneNumber=f"+569{random.randint(10000000, 99999999)}",
        customerArrivedUrl="https://example.com/customer-arrived",
        vehicleModel=random.choice(["Toyota Corolla", "Honda Civic", "Ford Explorer"]),
        vehicleColor=random.choice(["Rojo", "Negro", "Blanco", "Azul"]),
        specialInstructions="Cliente espera en estacionamiento curbside.",
    )
    return _base_result(order_id, customer, items, response)


def run_priority_rush_order(token: str, location_id: str, device_id: str) -> dict:
    customer = _random_customer()
    order_id = _new_order_id("rush")
    items = [
        _item("Cafe Americano", 2, "Extra caliente", "3.50", specialInstructions="Preparar primero"),
        _item("Croissant", 2, "Calentar", "4.00"),
    ]

    response = sendOrder(
        token=token,
        store=location_id,
        device=device_id,
        id=order_id,
        name=f"{customer} PRIORIDAD",
        mode="ToGo",
        items=items,
        terminal="Caja Rapida",
        time=datetime.now().isoformat(),
        priority=True,
        prepTimeDuration="PT8M",
        checkNumber=f"CHK-{random.randint(100, 999)}",
        specialInstructions="Orden prioritaria. Cliente esperando en mostrador.",
        server="Supervisor",
    )
    return _base_result(order_id, customer, items, response)


def run_future_pickup_order(token: str, location_id: str, device_id: str) -> dict:
    customer = _random_customer()
    order_id = _new_order_id("pickup")
    pickup_time = datetime.now() + timedelta(minutes=35)
    items = [
        _item("Pizza Pepperoni", 1, "Extra queso", "18.00"),
        _item("Ensalada Familiar", 1, "Aderezo aparte", "9.50"),
    ]

    response = sendOrder(
        token=token,
        store=location_id,
        device=device_id,
        id=order_id,
        name=f"{customer} Pickup Futuro",
        mode="Pickup",
        items=items,
        terminal="Web Ordering",
        time=datetime.now().isoformat(),
        pickupTime=pickup_time.isoformat(),
        prepTimeDuration="PT20M",
        phoneNumber=f"+569{random.randint(10000000, 99999999)}",
        optInForSms=True,
        specialInstructions="No iniciar hasta que aplique el tiempo de preparacion.",
        source="OnlineOrdering",
    )
    return _base_result(order_id, customer, items, response)


def run_dine_in_courses_order(token: str, location_id: str, device_id: str) -> dict:
    customer = _random_customer()
    order_id = _new_order_id("table")
    table_group = {"id": "mesa-12", "name": "Mesa 12", "note": "Cumpleanos"}
    items = [
        _item(
            "Entrada Nachos",
            1,
            "Jalapenos aparte",
            "8.50",
            course="Entrada",
            courseStatus="Fired",
            seat="1",
            itemGroup=table_group,
        ),
        _item(
            "Ribeye",
            1,
            "Termino medio",
            "26.00",
            course="Principal",
            courseStatus="Hold",
            seat="1",
            itemGroup=table_group,
        ),
        _item(
            "Pasta Alfredo",
            1,
            "Sin champinones",
            "17.00",
            course="Principal",
            courseStatus="Hold",
            seat="2",
            itemGroup=table_group,
        ),
    ]

    response = sendOrder(
        token=token,
        store=location_id,
        device=device_id,
        id=order_id,
        name=f"Mesa 12 - {customer}",
        mode="For Here",
        items=items,
        terminal="POS Salon",
        time=datetime.now().isoformat(),
        server="Mesero 4",
        covers=2,
        checkNumber=f"M12-{random.randint(100, 999)}",
        specialInstructions="Enviar platos principales despues de entrada.",
    )
    return _base_result(order_id, customer, items, response)


def run_costs_promos_order(token: str, location_id: str, device_id: str) -> dict:
    customer = _random_customer()
    order_id = _new_order_id("promo")
    items = [
        _item("Sandwich Club", 2, "Sin tomate", "12.00"),
        _item("Sopa del dia", 2, "Sin sal", "6.00"),
    ]
    subtotal = 36.00
    tax = 2.88
    total = 34.38

    response = sendOrder(
        token=token,
        store=location_id,
        device=device_id,
        id=order_id,
        name=f"{customer} Promo",
        mode="ToGo",
        items=items,
        terminal="Caja 2",
        time=datetime.now().isoformat(),
        loyaltyMember=True,
        costs=Costs(
            subtotal=f"{subtotal:.2f}",
            tax=f"{tax:.2f}",
            deliveryFee="0.00",
            surcharge="0.00",
            convenienceFee="1.50",
            tip="0.00",
            additionalFees=[{"name": "Eco packaging", "amount": "0.50"}],
            total=f"{total:.2f}",
            promoCodes=[{"name": "LUNCH10", "amount": "-6.00"}],
        ),
        specialInstructions="Aplicar promo y confirmar empaque.",
    )
    return _base_result(order_id, customer, items, response)


def run_all_devices_order(token: str, location_id: str, device_id: str) -> dict:
    customer = _random_customer()
    order_id = _new_order_id("all")
    items = [
        _item("Orden visible en todas las pantallas", 1, "Prueba all devices", "1.00"),
    ]

    response = SendMinimalOrder(
        token=token,
        store=location_id,
        device="all",
        id=order_id,
        name=f"{customer} All Devices",
        mode="For Here",
        items=items,
        terminal="main.py",
        time=datetime.now().isoformat(),
    )
    return _base_result(order_id, customer, items, response)


ORDER_OPTIONS = {
    "1": ("send_order_complete copy.py", run_complete_copy_order),
    "2": ("send_order_complete.py", run_complete_order),
    "3": ("send_order_max_3.py", lambda token, location_id, device_id: run_minimal_order(token, location_id, device_id, 3, [1, 3])),
    "4": ("send_order_max_30.py", lambda token, location_id, device_id: run_minimal_order(token, location_id, device_id, 14)),
    "5": ("delivery con handoff + driver", run_delivery_handoff_order),
    "6": ("curbside con vehiculo + pickupTime", run_curbside_order),
    "7": ("rush order prioridad + prepTimeDuration", run_priority_rush_order),
    "8": ("pickup futuro con tiempo de preparacion", run_future_pickup_order),
    "9": ("mesa con cursos, asientos y covers", run_dine_in_courses_order),
    "10": ("orden con costos, fees y promoCodes", run_costs_promos_order),
    "11": ("orden enviada a todas las pantallas", run_all_devices_order),
}
