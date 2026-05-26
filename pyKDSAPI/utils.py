from __future__ import annotations

import json
import socket
import time as time_module
from datetime import datetime
from typing import Any, Iterable

import requests

from pyKDSAPI.structs import Item, Retry


PRODUCTION_BASE_URL = "https://integrations-api.ftservices.cloud"
SANDBOX_BASE_URL = "https://sandbox-integrations-api.ftservices.cloud"
DISCOVERY_PORT = 28000
LOCAL_KDS_PORT = 9104


def get_api_base_url(environment: str = "production", base_url: str | None = None) -> str:
    if base_url:
        return base_url.rstrip("/")
    if environment == "sandbox":
        return SANDBOX_BASE_URL
    return PRODUCTION_BASE_URL


def _format_device_ids(device_ids: str | Iterable[str]) -> str:
    if isinstance(device_ids, str):
        return device_ids
    return ",".join(device_ids)


def _build_headers(
    token: str,
    location_id: str | None = None,
    device_ids: str | Iterable[str] | None = None,
    content_type_json: bool = False,
    headers: dict[str, str] | None = None,
) -> dict[str, str]:
    request_headers = dict(headers or {})
    request_headers["x-integration-token"] = token
    if location_id is not None:
        request_headers["x-location-id"] = location_id
    if device_ids is not None:
        request_headers["x-device-ids"] = _format_device_ids(device_ids)
    if content_type_json:
        request_headers["Content-Type"] = "application/json"
    return request_headers


def _response_content(response: requests.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return response.text


def _error_response(response: requests.Response) -> dict[str, Any]:
    return {
        "status_code": response.status_code,
        "error": _response_content(response),
    }


def _request(
    method: str,
    path: str,
    token: str,
    location_id: str | None = None,
    device_ids: str | Iterable[str] | None = None,
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    environment: str = "production",
    base_url: str | None = None,
    timeout: int = 30,
) -> Any:
    url = f"{get_api_base_url(environment, base_url)}{path}"
    response = requests.request(
        method,
        url=url,
        headers=_build_headers(token, location_id, device_ids, payload is not None, headers),
        json=payload,
        timeout=timeout,
    )
    if response.ok:
        return _response_content(response)
    return _error_response(response)


def _compact(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value is not None}


def build_order_payload(
    id: str,
    name: str,
    mode: str,
    items: list[Item],
    terminal: str | None = None,
    time: str | None = None,
    phoneNumber: str | None = None,
    optInForSms: bool | None = None,
    deliveryAddress: str | None = None,
    deliveryHandoff: bool | None = None,
    server: str | None = None,
    source: str | None = None,
    pickupTime: str | None = None,
    specialInstructions: str | None = None,
    customerArrivedUrl: str | None = None,
    vehicleModel: str | None = None,
    vehicleColor: str | None = None,
    retry: Retry | None = None,
    costs: dict[str, Any] | None = None,
    deliveryService: dict[str, Any] | None = None,
    accessibility: dict[str, Any] | None = None,
    originSource: str | None = None,
    checkNumber: str | None = None,
    priority: bool | None = None,
    prepTimeDuration: str | None = None,
    covers: int | None = None,
    loyaltyMember: bool | None = None,
) -> dict[str, Any]:
    if not id or not name or not mode or items is None:
        raise ValueError("id, name, mode e items son requeridos")

    return _compact(
        {
            "id": id,
            "name": name,
            "time": time or datetime.now().isoformat(),
            "mode": mode,
            "items": items,
            "terminal": terminal,
            "phoneNumber": phoneNumber,
            "optInForSms": optInForSms,
            "deliveryAddress": deliveryAddress,
            "deliveryHandoff": deliveryHandoff,
            "server": server,
            "source": source,
            "pickupTime": pickupTime,
            "specialInstructions": specialInstructions,
            "customerArrivedUrl": customerArrivedUrl,
            "vehicleModel": vehicleModel,
            "vehicleColor": vehicleColor,
            "retry": retry,
            "costs": costs,
            "deliveryService": deliveryService,
            "accessibility": accessibility,
            "originSource": originSource,
            "checkNumber": checkNumber,
            "priority": priority,
            "prepTimeDuration": prepTimeDuration,
            "covers": covers,
            "loyaltyMember": loyaltyMember,
        }
    )


def build_partial_order_payload(
    id: str,
    name: str | None = None,
    mode: str | None = None,
    pickupTime: str | None = None,
    phoneNumber: str | None = None,
    server: str | None = None,
    specialInstructions: str | None = None,
    vehicleModel: str | None = None,
    vehicleColor: str | None = None,
    priority: bool | None = None,
    deliveryAddress: str | None = None,
    deliveryService: dict[str, Any] | None = None,
    costs: dict[str, Any] | None = None,
    originSource: str | None = None,
    checkNumber: str | None = None,
    deliveryHandoff: bool | None = None,
    prepTimeDuration: str | None = None,
    itemsToAdd: list[Item] | None = None,
    itemsToUpdate: list[Item] | None = None,
    itemsToRemove: list[str] | None = None,
    covers: int | None = None,
    loyaltyMember: bool | None = None,
) -> dict[str, Any]:
    if not id:
        raise ValueError("id es requerido")

    return _compact(
        {
            "id": id,
            "name": name,
            "mode": mode,
            "pickupTime": pickupTime,
            "phoneNumber": phoneNumber,
            "server": server,
            "specialInstructions": specialInstructions,
            "vehicleModel": vehicleModel,
            "vehicleColor": vehicleColor,
            "priority": priority,
            "deliveryAddress": deliveryAddress,
            "deliveryService": deliveryService,
            "costs": costs,
            "originSource": originSource,
            "checkNumber": checkNumber,
            "deliveryHandoff": deliveryHandoff,
            "prepTimeDuration": prepTimeDuration,
            "itemsToAdd": itemsToAdd,
            "itemsToUpdate": itemsToUpdate,
            "itemsToRemove": itemsToRemove,
            "covers": covers,
            "loyaltyMember": loyaltyMember,
        }
    )


def healthCheck(token: str, headers: dict[str, str] | None = None, **kwargs) -> Any:
    return _request("GET", "/health", token, headers=headers, **kwargs)


def getOrganization(
    token: str,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    **kwargs,
) -> Any:
    return _request("GET", "/integrators/kds-information", token, payload=payload, headers=headers, **kwargs)


def getStores(
    token: str,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    **kwargs,
) -> Any:
    return _request("GET", "/integrators/kds-information/locations", token, payload=payload, headers=headers, **kwargs)


def getDevices(
    token: str,
    store: str,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    **kwargs,
) -> Any:
    return _request(
        "GET",
        f"/integrators/kds-information/locations/{store}/devices",
        token,
        payload=payload,
        headers=headers,
        **kwargs,
    )


def getOrders(
    token: str,
    store: str,
    device: str | Iterable[str],
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    **kwargs,
) -> Any:
    return _request(
        "GET",
        "/integrators/kds-orders/active",
        token,
        location_id=store,
        device_ids=device,
        payload=payload,
        headers=headers,
        **kwargs,
    )


def sendOrder(
    token: str,
    store: str,
    device: str | Iterable[str],
    id: str,
    name: str,
    mode: str,
    items: list[Item],
    terminal: str,
    time: str | None = None,
    phoneNumber: str | None = None,
    optInForSms: bool | None = None,
    deliveryAddress: str | None = None,
    server: str | None = None,
    source: str | None = None,
    pickupTime: str | None = None,
    specialInstructions: str | None = None,
    customerArrivedUrl: str | None = None,
    vehicleModel: str | None = None,
    vehicleColor: str | None = None,
    retry: Retry | None = None,
    costs: dict[str, Any] | None = None,
    deliveryservice: dict[str, Any] | None = None,
    accessibility: dict[str, Any] | None = None,
    originSource: str | None = None,
    checkNumber: str | None = None,
    priority: bool | None = None,
    prepTimeDuration: str | None = None,
    covers: int | None = None,
    loyaltyMember: bool | None = None,
    deliveryHandoff: bool | None = None,
    headers: dict[str, str] | None = None,
    **kwargs,
) -> Any:
    payload = build_order_payload(
        id=id,
        name=name,
        time=time,
        mode=mode,
        items=items,
        terminal=terminal,
        phoneNumber=phoneNumber,
        optInForSms=optInForSms,
        deliveryAddress=deliveryAddress,
        deliveryHandoff=deliveryHandoff,
        server=server,
        source=source,
        pickupTime=pickupTime,
        specialInstructions=specialInstructions,
        customerArrivedUrl=customerArrivedUrl,
        vehicleModel=vehicleModel,
        vehicleColor=vehicleColor,
        retry=retry,
        costs=costs,
        deliveryService=deliveryservice,
        accessibility=accessibility,
        originSource=originSource,
        checkNumber=checkNumber,
        priority=priority,
        prepTimeDuration=prepTimeDuration,
        covers=covers,
        loyaltyMember=loyaltyMember,
    )
    return createOrder(token, store, device, payload, headers=headers, **kwargs)


def SendMinimalOrder(
    token: str,
    store: str,
    device: str | Iterable[str],
    id: str,
    name: str,
    mode: str,
    items: list[Item],
    terminal: str,
    time: str | None = None,
    headers: dict[str, str] | None = None,
    **kwargs,
) -> Any:
    return sendOrder(
        token=token,
        store=store,
        device=device,
        id=id,
        name=name,
        mode=mode,
        items=items,
        terminal=terminal,
        time=time,
        headers=headers,
        **kwargs,
    )


def createOrder(
    token: str,
    store: str,
    device: str | Iterable[str],
    order: dict[str, Any],
    headers: dict[str, str] | None = None,
    **kwargs,
) -> Any:
    return _request(
        "POST",
        "/integrators/kds-orders",
        token,
        location_id=store,
        device_ids=device,
        payload=order,
        headers=headers,
        **kwargs,
    )


def updateOrder(
    token: str,
    store: str,
    device: str | Iterable[str],
    order: dict[str, Any],
    headers: dict[str, str] | None = None,
    **kwargs,
) -> Any:
    return _request(
        "PUT",
        "/integrators/kds-orders",
        token,
        location_id=store,
        device_ids=device,
        payload=order,
        headers=headers,
        **kwargs,
    )


def partialUpdateOrder(
    token: str,
    store: str,
    device: str | Iterable[str],
    order_id: str,
    headers: dict[str, str] | None = None,
    **changes,
) -> Any:
    kwargs = {key: changes.pop(key) for key in ("environment", "base_url", "timeout") if key in changes}
    payload = build_partial_order_payload(order_id, **changes)
    return _request(
        "PUT",
        "/integrators/kds-orders/partial",
        token,
        location_id=store,
        device_ids=device,
        payload=payload,
        headers=headers,
        **kwargs,
    )


def cancelOrder(
    token: str,
    store: str,
    device: str | Iterable[str],
    order_id: str,
    headers: dict[str, str] | None = None,
    **kwargs,
) -> Any:
    return _request(
        "PUT",
        "/integrators/kds-orders/cancel",
        token,
        location_id=store,
        device_ids=device,
        payload={"id": order_id},
        headers=headers,
        **kwargs,
    )


def customerArrivedNotification(
    token: str,
    store: str,
    device: str | Iterable[str],
    order_id: str,
    retry: Retry | None = None,
    headers: dict[str, str] | None = None,
    **kwargs,
) -> Any:
    return _request(
        "POST",
        "/integrators/kds-notifications/customer-arrived",
        token,
        location_id=store,
        device_ids=device,
        payload=_compact({"id": order_id, "retry": retry}),
        headers=headers,
        **kwargs,
    )


def estimatedArrivalUpdate(
    token: str,
    store: str,
    device: str | Iterable[str],
    order_id: str,
    minutes: int,
    retry: Retry | None = None,
    headers: dict[str, str] | None = None,
    **kwargs,
) -> Any:
    return _request(
        "POST",
        "/integrators/kds-notifications/estimated-arrival-update",
        token,
        location_id=store,
        device_ids=device,
        payload=_compact({"id": order_id, "minutes": minutes, "retry": retry}),
        headers=headers,
        **kwargs,
    )


def sendKdsMessage(
    token: str,
    store: str,
    device: str | Iterable[str],
    message: str,
    headers: dict[str, str] | None = None,
    **kwargs,
) -> Any:
    if not message:
        raise ValueError("message es requerido")
    return _request(
        "POST",
        "/integrators/kds-notifications/send-message",
        token,
        location_id=store,
        device_ids=device,
        payload={"message": message},
        headers=headers,
        **kwargs,
    )


def _hex_to_ascii(hex_value: str) -> str:
    trimmed = hex_value
    while trimmed.endswith("00"):
        trimmed = trimmed[:-2]
    if not trimmed:
        return ""
    return bytes.fromhex(trimmed).decode("ascii", errors="ignore")


def _hex_to_ip(hex_value: str) -> str:
    trimmed = hex_value
    while trimmed.endswith("00"):
        trimmed = trimmed[:-2]
    octets = [str(int(trimmed[index : index + 2], 16)) for index in range(0, min(len(trimmed), 8), 2)]
    return ".".join(octets)


def parseDiscoveryBroadcast(data: bytes | str) -> dict[str, str]:
    hex_message = data.hex().upper() if isinstance(data, bytes) else data.upper()
    if len(hex_message) < 204:
        raise ValueError("El broadcast de Fresh KDS debe tener 102 bytes o 204 caracteres hex")

    return {
        "application": _hex_to_ascii(hex_message[0:24]),
        "version": _hex_to_ascii(hex_message[24:40]),
        "ipAddress": _hex_to_ip(hex_message[40:60]),
        "identifier": _hex_to_ascii(hex_message[60:100]),
        "name": _hex_to_ascii(hex_message[100:204]),
    }


def discoverLocalDevices(timeout: float = 5.0, port: int = DISCOVERY_PORT) -> list[dict[str, str]]:
    devices: dict[str, dict[str, str]] = {}
    deadline = time_module.time() + timeout

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", port))
        sock.settimeout(0.5)

        while time_module.time() < deadline:
            try:
                data, address = sock.recvfrom(1024)
            except socket.timeout:
                continue

            parsed = parseDiscoveryBroadcast(data)
            parsed["sourceAddress"] = address[0]
            devices[parsed["identifier"]] = parsed

    return list(devices.values())


def buildLocalCommand(command: str, order: dict[str, Any]) -> dict[str, Any]:
    if not command:
        raise ValueError("command es requerido")
    if not order:
        raise ValueError("order es requerido")
    return {"command": command, "order": order}


def sendLocalCommand(
    ip_address: str,
    command: str,
    order: dict[str, Any],
    port: int = LOCAL_KDS_PORT,
    timeout: float = 5.0,
) -> str:
    payload = json.dumps(buildLocalCommand(command, order)).encode("utf-8")
    with socket.create_connection((ip_address, port), timeout=timeout) as sock:
        sock.sendall(payload)
        sock.shutdown(socket.SHUT_WR)
        response = sock.recv(4096)
    return response.decode("utf-8", errors="replace")


def sendLocalOrder(ip_address: str, order: dict[str, Any], **kwargs) -> str:
    return sendLocalCommand(ip_address, "create-order", order, **kwargs)


def updateLocalOrder(ip_address: str, order: dict[str, Any], **kwargs) -> str:
    return sendLocalCommand(ip_address, "update-order", order, **kwargs)


def partialUpdateLocalOrder(ip_address: str, order_id: str, **changes) -> str:
    kwargs = {key: changes.pop(key) for key in ("port", "timeout") if key in changes}
    return sendLocalCommand(
        ip_address,
        "partial-update-order",
        build_partial_order_payload(order_id, **changes),
        **kwargs,
    )


def cancelLocalOrder(ip_address: str, order_id: str, **kwargs) -> str:
    return sendLocalCommand(ip_address, "cancel-order", {"id": order_id}, **kwargs)
