"""Cliente grafico web para Fresh KDS.

Sirve una interfaz en el navegador que envuelve el wrapper local pyKDSAPI
y reutiliza las plantillas de orden de order_templates.

Ejecutar:
    pip3 install -r requirements.txt
    python3 app.py

Luego abre http://localhost:5000
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

import runtime_warnings  # noqa: F401  (silencia warning de urllib3 al importar)

from flask import Flask, jsonify, render_template, request

from env_config import (
    get_device_id,
    get_integration_token,
    get_location_id,
    set_env_values,
)
from order_templates import ORDER_OPTIONS
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

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _token() -> str:
    return get_integration_token()


def _env_default(getter) -> str | None:
    try:
        return getter()
    except RuntimeError:
        return None


def _resolve(name: str, getter) -> str:
    """Toma el valor enviado por el cliente, o cae al de .env."""
    value = (request.values.get(name) or "").strip()
    if value:
        return value
    if request.is_json and request.json:
        body_value = (request.json.get(name) or "").strip()
        if body_value:
            return body_value
    fallback = _env_default(getter)
    if fallback:
        return fallback
    raise ValueError(f"Falta '{name}' y no hay valor por defecto en .env")


def _body() -> dict[str, Any]:
    return request.get_json(silent=True) or {}


def _ok(data: Any, **extra) -> Any:
    payload = {"ok": True, "data": data}
    payload.update(extra)
    return jsonify(payload)


def _fail(message: str, status: int = 400) -> Any:
    return jsonify({"ok": False, "error": message}), status


def _sample_item(name: str = "Item desde GUI") -> Item:
    return Item(
        id=str(uuid.uuid4()),
        lineId=str(uuid.uuid4()),
        name=name,
        qty=1,
        mods=[Mods(id=str(uuid.uuid4()), name="Sin modificador", qty=1, components=[])],
        price="10.00",
        components=[],
        specialInstructions="Generado desde la web app",
    )


def _sample_order(order_id: str | None = None, name: str = "Orden desde GUI") -> dict:
    return build_order_payload(
        id=order_id or f"orden-{uuid.uuid4().hex[:6]}",
        name=name,
        mode="Pickup",
        terminal="app.py",
        time=datetime.now().isoformat(),
        items=[_sample_item()],
    )


# ---------------------------------------------------------------------------
# Pagina
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------------------------------------------------------
# Configuracion / conexion
# ---------------------------------------------------------------------------
@app.get("/api/config")
def api_config():
    has_token = _env_default(_token) is not None
    return _ok(
        {
            "hasToken": has_token,
            "locationId": _env_default(get_location_id),
            "deviceId": _env_default(get_device_id),
            "templates": [
                {"key": key, "label": label} for key, (label, _) in ORDER_OPTIONS.items()
            ],
        }
    )


@app.post("/api/config")
def api_save_config():
    body = _body()
    values = {
        key: str(body[key]).strip()
        for key in ("FRESH_KDS_LOCATION_ID", "FRESH_KDS_DEVICE_ID")
        if body.get(key)
    }
    if not values:
        return _fail("No se enviaron valores para guardar")
    set_env_values(values)
    return _ok(values)


# ---------------------------------------------------------------------------
# Lectura cloud
# ---------------------------------------------------------------------------
@app.get("/api/health")
def api_health():
    return _ok(healthCheck(_token()))


@app.get("/api/organization")
def api_organization():
    return _ok(getOrganization(_token()))


@app.get("/api/locations")
def api_locations():
    return _ok(getStores(_token()))


@app.get("/api/devices")
def api_devices():
    location = _resolve("location", get_location_id)
    return _ok(getDevices(_token(), location))


@app.get("/api/orders")
def api_orders():
    location = _resolve("location", get_location_id)
    device = _resolve("device", get_device_id)
    return _ok(getOrders(_token(), location, device))


# ---------------------------------------------------------------------------
# Acciones cloud
# ---------------------------------------------------------------------------
@app.post("/api/send-order")
def api_send_order():
    body = _body()
    template = str(body.get("template", "")).strip()
    if template not in ORDER_OPTIONS:
        return _fail(f"Plantilla invalida: {template!r}")
    location = _resolve("location", get_location_id)
    device = _resolve("device", get_device_id)
    label, runner = ORDER_OPTIONS[template]
    result = runner(_token(), location, device)
    return _ok(
        {
            "label": label,
            "orderId": result.get("order_id"),
            "customer": result.get("customer"),
            "items": result.get("items"),
            "response": result.get("response"),
        }
    )


@app.post("/api/message")
def api_message():
    body = _body()
    message = str(body.get("message", "")).strip()
    if not message:
        return _fail("El mensaje es requerido")
    location = _resolve("location", get_location_id)
    device = _resolve("device", get_device_id)
    return _ok(sendKdsMessage(_token(), location, device, message))


@app.post("/api/cancel")
def api_cancel():
    body = _body()
    order_id = str(body.get("orderId", "")).strip()
    if not order_id:
        return _fail("orderId es requerido")
    location = _resolve("location", get_location_id)
    device = _resolve("device", get_device_id)
    return _ok(cancelOrder(_token(), location, device, order_id))


@app.post("/api/partial-update")
def api_partial_update():
    body = _body()
    order_id = str(body.get("orderId", "")).strip()
    if not order_id:
        return _fail("orderId es requerido")
    location = _resolve("location", get_location_id)
    device = _resolve("device", get_device_id)

    changes: dict[str, Any] = {}
    if body.get("name"):
        changes["name"] = str(body["name"]).strip()
    if body.get("specialInstructions"):
        changes["specialInstructions"] = str(body["specialInstructions"]).strip()
    if isinstance(body.get("priority"), bool):
        changes["priority"] = body["priority"]
    remove = str(body.get("itemsToRemove", "")).strip()
    if remove:
        changes["itemsToRemove"] = [x.strip() for x in remove.split(",") if x.strip()]

    return _ok(partialUpdateOrder(_token(), location, device, order_id, **changes))


@app.post("/api/full-update")
def api_full_update():
    body = _body()
    order_id = str(body.get("orderId", "")).strip()
    if not order_id:
        return _fail("orderId es requerido")
    name = str(body.get("name", "")).strip() or "Orden actualizada desde GUI"
    location = _resolve("location", get_location_id)
    device = _resolve("device", get_device_id)
    return _ok(updateOrder(_token(), location, device, _sample_order(order_id, name)))


@app.post("/api/customer-arrived")
def api_customer_arrived():
    body = _body()
    order_id = str(body.get("orderId", "")).strip()
    if not order_id:
        return _fail("orderId es requerido")
    location = _resolve("location", get_location_id)
    device = _resolve("device", get_device_id)
    return _ok(customerArrivedNotification(_token(), location, device, order_id))


@app.post("/api/eta")
def api_eta():
    body = _body()
    order_id = str(body.get("orderId", "")).strip()
    if not order_id:
        return _fail("orderId es requerido")
    try:
        minutes = int(body.get("minutes", 5))
    except (TypeError, ValueError):
        return _fail("minutes debe ser un numero")
    location = _resolve("location", get_location_id)
    device = _resolve("device", get_device_id)
    return _ok(estimatedArrivalUpdate(_token(), location, device, order_id, minutes))


# ---------------------------------------------------------------------------
# Red local (TCP / UDP)
# ---------------------------------------------------------------------------
@app.get("/api/local/discover")
def api_local_discover():
    try:
        timeout = float(request.values.get("timeout", 5))
    except (TypeError, ValueError):
        timeout = 5.0
    return _ok(discoverLocalDevices(timeout=timeout))


@app.post("/api/local/send")
def api_local_send():
    body = _body()
    ip = str(body.get("ip", "")).strip()
    if not ip:
        return _fail("ip es requerida")
    name = str(body.get("name", "")).strip() or "Orden local desde GUI"
    return _ok(sendLocalOrder(ip, _sample_order(name=name)))


@app.post("/api/local/update")
def api_local_update():
    body = _body()
    ip = str(body.get("ip", "")).strip()
    order_id = str(body.get("orderId", "")).strip()
    if not ip or not order_id:
        return _fail("ip y orderId son requeridos")
    name = str(body.get("name", "")).strip() or "Orden local actualizada"
    return _ok(updateLocalOrder(ip, _sample_order(order_id, name)))


@app.post("/api/local/partial")
def api_local_partial():
    body = _body()
    ip = str(body.get("ip", "")).strip()
    order_id = str(body.get("orderId", "")).strip()
    if not ip or not order_id:
        return _fail("ip y orderId son requeridos")
    changes: dict[str, Any] = {}
    if body.get("name"):
        changes["name"] = str(body["name"]).strip()
    if isinstance(body.get("priority"), bool):
        changes["priority"] = body["priority"]
    return _ok(partialUpdateLocalOrder(ip, order_id, **changes))


@app.post("/api/local/cancel")
def api_local_cancel():
    body = _body()
    ip = str(body.get("ip", "")).strip()
    order_id = str(body.get("orderId", "")).strip()
    if not ip or not order_id:
        return _fail("ip y orderId son requeridos")
    return _ok(cancelLocalOrder(ip, order_id))


# ---------------------------------------------------------------------------
# Manejo de errores
# ---------------------------------------------------------------------------
@app.errorhandler(ValueError)
def handle_value_error(error: ValueError):
    return _fail(str(error))


@app.errorhandler(Exception)
def handle_exception(error: Exception):
    return _fail(f"{type(error).__name__}: {error}", status=500)


if __name__ == "__main__":
    import os

    # El puerto 5000 suele estar ocupado en macOS por "AirPlay Receiver".
    # Usa 5001 por defecto; sobrescribe con la variable de entorno PORT.
    port = int(os.getenv("PORT", "5001"))
    app.run(host="127.0.0.1", port=port, debug=True)
