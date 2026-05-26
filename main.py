from __future__ import annotations

import json
import time
import uuid
from datetime import datetime

import runtime_warnings

from env_config import get_device_id, get_integration_token, get_location_id, set_env_values
from order_templates import ORDER_OPTIONS, print_order_summary
from pyKDSAPI.structs import Item, Mods
from pyKDSAPI.utils import (
    build_order_payload,
    cancelLocalOrder,
    cancelOrder,
    customerArrivedNotification,
    discoverLocalDevices,
    estimatedArrivalUpdate,
    getDevices,
    getOrders,
    getOrganization,
    getStores,
    healthCheck,
    partialUpdateLocalOrder,
    partialUpdateOrder,
    sendKdsMessage,
    sendLocalOrder,
    updateLocalOrder,
    updateOrder,
)


def _choose_option(title: str, options: list[dict], formatter) -> dict:
    if not options:
        raise RuntimeError(f"No hay opciones disponibles para {title}")

    print(title)
    for index, option in enumerate(options, start=1):
        print(formatter(index, option))

    while True:
        selected = input("Selecciona un numero: ").strip()
        if selected.isdigit():
            index = int(selected)
            if 1 <= index <= len(options):
                return options[index - 1]
        print("Seleccion invalida. Intenta de nuevo.")


def _prompt_text(label: str, required: bool = True, default: str | None = None) -> str | None:
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        if not required:
            return None
        print("Este valor es requerido.")


def _prompt_int(label: str, default: int | None = None) -> int:
    while True:
        value = _prompt_text(label, required=default is None, default=str(default) if default is not None else None)
        try:
            return int(value)
        except (TypeError, ValueError):
            print("Ingresa un numero valido.")


def _prompt_bool(label: str) -> bool | None:
    value = input(f"{label} (s/n, Enter para omitir): ").strip().lower()
    if value in {"s", "si", "y", "yes"}:
        return True
    if value in {"n", "no"}:
        return False
    return None


def _print_response(response) -> None:
    print("Respuesta:")
    if isinstance(response, (dict, list)):
        print(json.dumps(response, indent=2, ensure_ascii=False))
    else:
        print(response)


def _sample_item(name: str = "Item actualizado desde main") -> Item:
    return Item(
        id=str(uuid.uuid4()),
        lineId=str(uuid.uuid4()),
        name=name,
        qty=1,
        mods=[Mods(id=str(uuid.uuid4()), name="Sin modificador", qty=1, components=[])],
        price="10.00",
        components=[],
        specialInstructions="Generado desde main.py",
    )


def _sample_order(order_id: str | None = None, name: str = "Orden desde main") -> dict:
    return build_order_payload(
        id=order_id or f"orden-{uuid.uuid4().hex[:6]}",
        name=name,
        mode="Pickup",
        terminal="main.py",
        time=datetime.now().isoformat(),
        items=[_sample_item()],
    )


def _resolve_location_and_device(token: str) -> tuple[dict, dict]:
    try:
        selected_store = {"id": get_location_id(), "name": "configurada"}
        selected_device = {"id": get_device_id(), "name": "configurado"}
        print(f"Usando location configurada: {selected_store['id']}")
        print(f"Usando device configurado: {selected_device['id']}")
        return selected_store, selected_device
    except RuntimeError:
        pass

    stores = getStores(token)
    if not isinstance(stores, list):
        raise RuntimeError(f"No fue posible obtener locations. Respuesta: {stores}")

    selected_store = _choose_option(
        "Locations disponibles:",
        stores,
        lambda index, option: f"{index}. {option['name']} ({option['id']})",
    )

    devices = getDevices(token, selected_store["id"])
    if not isinstance(devices, list):
        raise RuntimeError(f"No fue posible obtener devices. Respuesta: {devices}")

    selected_device = _choose_option(
        "Devices disponibles:",
        devices,
        lambda index, option: (
            f"{index}. {option['name']} ({option['id']}) - "
            f"online={option.get('isOnline')} type={option.get('type')}"
        ),
    )

    set_env_values(
        {
            "FRESH_KDS_LOCATION_ID": selected_store["id"],
            "FRESH_KDS_DEVICE_ID": selected_device["id"],
        }
    )
    return selected_store, selected_device


# Etiquetas de las acciones cloud/local. La clave es el id interno que esperan
# _run_cloud_option / _run_local_option (no cambia el enrutado).
ACTION_LABELS = {
    "12": "Health check API",
    "13": "Ver informacion completa de la marca",
    "14": "Ver locations",
    "15": "Ver devices de la location",
    "16": "Ver ordenes activas",
    "17": "Enviar mensaje a pantalla KDS",
    "18": "Cancelar orden",
    "19": "Actualizar orden parcial",
    "20": "Actualizar orden completa",
    "21": "Notificar que el cliente llego",
    "22": "Actualizar ETA del cliente",
    "23": "Descubrir pantallas en red local",
    "24": "Enviar orden local por TCP",
    "25": "Actualizar orden local completa",
    "26": "Actualizar orden local parcial",
    "27": "Cancelar orden local",
}


def _build_menu() -> list[tuple[str, str]]:
    """Devuelve [(numero_mostrado, id_interno)] con numeracion correlativa.

    El numero que ve el usuario es secuencial (1..N); el id interno conserva
    las claves de ORDER_OPTIONS y los numeros 12-27 que usa el enrutado.
    """
    action_ids = list(ORDER_OPTIONS) + [str(value) for value in range(12, 28)]
    return [(str(display), action_id) for display, action_id in enumerate(action_ids, start=1)]


def _show_menu(menu: list[tuple[str, str]]) -> None:
    print("\nQue quieres ejecutar?")
    for display_num, action_id in menu:
        if action_id in ORDER_OPTIONS:
            label = f"Enviar orden: {ORDER_OPTIONS[action_id][0]}"
        else:
            label = ACTION_LABELS[action_id]
        print(f"{display_num}. {label}")
    print("0. Salir")


def _run_send_order_option(selected: str, token: str, location_id: str, device_id: str) -> int:
    selected_label, selected_runner = ORDER_OPTIONS[selected]
    print(f"Ejecutando {selected_label}")
    result = selected_runner(token, location_id, device_id)
    print_order_summary(result)

    response = result.get("response")
    if isinstance(response, int) and response >= 400:
        print(f"El envio devolvio un error HTTP: {response}")
        return 1
    if isinstance(response, dict) and response.get("status_code", 0) >= 400:
        print(f"El envio devolvio un error HTTP: {response['status_code']}")
        return 1
    return 0


def _run_cloud_option(selected: str, token: str, location_id: str, device_id: str) -> int:
    if selected == "12":
        _print_response(healthCheck(token))
    elif selected == "13":
        _print_response(getOrganization(token))
    elif selected == "14":
        _print_response(getStores(token))
    elif selected == "15":
        _print_response(getDevices(token, location_id))
    elif selected == "16":
        _print_response(getOrders(token, location_id, device_id))
    elif selected == "17":
        message = _prompt_text("Mensaje para mostrar en KDS")
        _print_response(sendKdsMessage(token, location_id, device_id, message))
    elif selected == "18":
        order_id = _prompt_text("Order ID a cancelar")
        _print_response(cancelOrder(token, location_id, device_id, order_id))
    elif selected == "19":
        order_id = _prompt_text("Order ID a actualizar")
        changes = {
            "name": _prompt_text("Nuevo nombre de orden", required=False),
            "specialInstructions": _prompt_text("Nuevas instrucciones", required=False),
            "priority": _prompt_bool("Marcar prioridad"),
        }
        remove_line_ids = _prompt_text("LineIds a remover separados por coma", required=False)
        if remove_line_ids:
            changes["itemsToRemove"] = [line_id.strip() for line_id in remove_line_ids.split(",") if line_id.strip()]
        changes = {key: value for key, value in changes.items() if value is not None}
        _print_response(partialUpdateOrder(token, location_id, device_id, order_id, **changes))
    elif selected == "20":
        order_id = _prompt_text("Order ID existente a reemplazar/actualizar")
        name = _prompt_text("Nombre de la orden", default="Orden actualizada desde main")
        print("Esta opcion envia un payload completo de ejemplo para ese order ID.")
        _print_response(updateOrder(token, location_id, device_id, _sample_order(order_id, name)))
    elif selected == "21":
        order_id = _prompt_text("Order ID del cliente que llego")
        _print_response(customerArrivedNotification(token, location_id, device_id, order_id))
    elif selected == "22":
        order_id = _prompt_text("Order ID para actualizar ETA")
        minutes = _prompt_int("Minutos estimados", default=5)
        _print_response(estimatedArrivalUpdate(token, location_id, device_id, order_id, minutes))
    else:
        return 1
    return 0


def _run_local_option(selected: str) -> int:
    if selected == "23":
        timeout = _prompt_int("Segundos para escuchar UDP discovery", default=5)
        _print_response(discoverLocalDevices(timeout=timeout))
    elif selected == "24":
        ip_address = _prompt_text("IP de la pantalla KDS")
        order = _sample_order(name="Orden local desde main")
        _print_response(sendLocalOrder(ip_address, order))
    elif selected == "25":
        ip_address = _prompt_text("IP de la pantalla KDS")
        order_id = _prompt_text("Order ID existente")
        name = _prompt_text("Nombre de la orden", default="Orden local actualizada")
        _print_response(updateLocalOrder(ip_address, _sample_order(order_id, name)))
    elif selected == "26":
        ip_address = _prompt_text("IP de la pantalla KDS")
        order_id = _prompt_text("Order ID existente")
        name = _prompt_text("Nuevo nombre", required=False)
        priority = _prompt_bool("Marcar prioridad")
        changes = {key: value for key, value in {"name": name, "priority": priority}.items() if value is not None}
        _print_response(partialUpdateLocalOrder(ip_address, order_id, **changes))
    elif selected == "27":
        ip_address = _prompt_text("IP de la pantalla KDS")
        order_id = _prompt_text("Order ID a cancelar")
        _print_response(cancelLocalOrder(ip_address, order_id))
    else:
        return 1
    return 0


def main() -> int:
    try:
        token = get_integration_token()
        selected_store, selected_device = _resolve_location_and_device(token)
        location_id = selected_store["id"]
        device_id = selected_device["id"]

        menu = _build_menu()
        display_to_action = {display_num: action_id for display_num, action_id in menu}

        while True:
            _show_menu(menu)
            selected = input("Selecciona un numero: ").strip()

            if selected == "0":
                return 0

            action_id = display_to_action.get(selected)
            if action_id is None:
                print("Seleccion invalida. Intenta de nuevo.")
                continue

            if action_id in ORDER_OPTIONS:
                _run_send_order_option(action_id, token, location_id, device_id)
            elif action_id in {str(value) for value in range(12, 23)}:
                _run_cloud_option(action_id, token, location_id, device_id)
            elif action_id in {str(value) for value in range(23, 28)}:
                _run_local_option(action_id)

            time.sleep(0.2)
    except Exception as error:
        print(f"Se produjo un error durante la ejecucion: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
