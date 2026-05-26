# Order Fresh

Proyecto de pruebas para integrar Fresh KDS desde Python usando el wrapper local `pyKDSAPI` y un flujo principal interactivo con `main.py`.

## Requisitos

- Python 3.9 o superior.
- Dependencias del proyecto instaladas.
- Un token de integración válido de Fresh KDS.

## Instalación

Desde la raíz del proyecto:

```bash
pip3 install -r requirements.txt
```

Si `requirements.txt` no instala todo lo necesario en tu entorno, instala al menos:

```bash
pip3 install requests
```

## Configuración

La configuración ya no se hace editando cada script. Ahora se centraliza en `.env`.

Variables principales:

- `X_INTEGRATION_TOKEN`: token de integración activo.
- `FRESH_KDS_API_KEY`: alias del mismo token.
- `FRESH_KDS_LOCATION_ID`: location por defecto.
- `FRESH_KDS_DEVICE_ID`: device por defecto.

Ejemplo:

```env
X_INTEGRATION_TOKEN=TU_TOKEN
FRESH_KDS_API_KEY=TU_TOKEN
FRESH_KDS_LOCATION_ID=TU_LOCATION_ID
FRESH_KDS_DEVICE_ID=TU_DEVICE_ID
```

## Cliente gráfico web (app.py)

Además del CLI, hay un cliente gráfico en el navegador construido con Flask que
envuelve el mismo wrapper `pyKDSAPI` y reutiliza las plantillas de orden.

Instalación y ejecución (con entorno virtual recomendado):

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Luego abre [http://localhost:5001](http://localhost:5001).

> El puerto 5000 suele estar ocupado en macOS por "AirPlay Receiver", por eso
> el cliente usa el `5001` por defecto. Para cambiarlo: `PORT=8000 .venv/bin/python app.py`.

La interfaz lee `X_INTEGRATION_TOKEN`, `FRESH_KDS_LOCATION_ID` y
`FRESH_KDS_DEVICE_ID` desde `.env`, permite cambiar location/device desde la
barra superior y guardarlos de vuelta en `.env`. Cubre las mismas operaciones
del menú del CLI: enviar órdenes por plantilla, consultas (health, marca,
locations, devices, órdenes activas), acciones sobre una orden (cancelar,
update parcial/completa, cliente llegó, ETA), mensajes a pantalla y red local
TCP/UDP (discovery, enviar/actualizar/cancelar orden local). Las respuestas se
muestran en la consola lateral.

## Flujo principal (CLI)

El punto de entrada del CLI es `main.py`.

Ejecución:

```bash
python3 main.py
```

Comportamiento actual:

1. Lee el token desde `.env`.
2. Usa por defecto `FRESH_KDS_LOCATION_ID` y `FRESH_KDS_DEVICE_ID` si ya existen.
3. Si faltan, consulta la API, te deja elegir location y device, y los guarda en `.env`.
4. Solo te pide elegir qué script de envío ejecutar.

Opciones disponibles hoy en `main.py`:

1. Enviar orden: `send_order_complete copy.py`
2. Enviar orden: `send_order_complete.py`
3. Enviar orden: `send_order_max_3.py`
4. Enviar orden: `send_order_max_30.py`
5. Enviar orden: delivery con handoff + driver
6. Enviar orden: curbside con vehiculo + pickupTime
7. Enviar orden: rush order prioridad + prepTimeDuration
8. Enviar orden: pickup futuro con tiempo de preparacion
9. Enviar orden: mesa con cursos, asientos y covers
10. Enviar orden: orden con costos, fees y promoCodes
11. Enviar orden: orden enviada a todas las pantallas
12. Health check API
13. Ver informacion completa de la marca
14. Ver locations
15. Ver devices de la location
16. Ver ordenes activas
17. Enviar mensaje a pantalla KDS
18. Cancelar orden
19. Actualizar orden parcial
20. Actualizar orden completa
21. Notificar que el cliente llego
22. Actualizar ETA del cliente
23. Descubrir pantallas en red local
24. Enviar orden local por TCP
25. Actualizar orden local completa
26. Actualizar orden local parcial
27. Cancelar orden local
0. Salir

## Scripts disponibles

- `main.py`: launcher principal recomendado.
- `run_1_location.py`: consulta locations asociadas al token.
- `run_2_devices.py`: consulta devices de una location.
- `send_order_complete.py`: envía una orden completa con más campos.
- `send_order_complete copy.py`: variante reducida de orden completa.
- `send_order_max_3.py`: envía una orden mínima con hasta 3 ítems.
- `send_order_max_30.py`: envía una orden mínima con más ítems.

## Endpoints implementados

Rutas implementadas en `pyKDSAPI.utils` segun la documentacion de Fresh KDS:

- `GET /health`
- `GET /integrators/kds-information`
- `GET /integrators/kds-information/locations`
- `GET /integrators/kds-information/locations/{locationId}/devices`
- `GET /integrators/kds-orders/active`
- `POST /integrators/kds-orders`
- `PUT /integrators/kds-orders`
- `PUT /integrators/kds-orders/partial`
- `PUT /integrators/kds-orders/cancel`
- `POST /integrators/kds-notifications/customer-arrived`
- `POST /integrators/kds-notifications/estimated-arrival-update`
- `POST /integrators/kds-notifications/send-message`

Headers usados por la integración:

- `x-integration-token`
- `x-location-id`
- `x-device-ids`
- `Content-Type: application/json`

## Funciones nuevas del wrapper

El wrapper local `pyKDSAPI.utils` ahora cubre mas rutas de Fresh KDS:

- `healthCheck(token)`: valida que la API responda con el token.
- `createOrder(token, location_id, device_id, order)`: crea una orden con un payload ya armado.
- `updateOrder(token, location_id, device_id, order)`: actualiza una orden reenviando el payload completo.
- `partialUpdateOrder(token, location_id, device_id, order_id, **changes)`: actualiza solo campos puntuales.
- `cancelOrder(token, location_id, device_id, order_id)`: cancela una orden activa.
- `customerArrivedNotification(token, location_id, device_id, order_id)`: marca llegada de cliente.
- `estimatedArrivalUpdate(token, location_id, device_id, order_id, minutes)`: actualiza ETA.
- `sendKdsMessage(token, location_id, device_id, message)`: muestra un mensaje en pantalla KDS.
- `build_order_payload(...)` y `build_partial_order_payload(...)`: ayudan a construir payloads validos.

Ejemplo de update parcial:

```python
from pyKDSAPI.utils import partialUpdateOrder

response = partialUpdateOrder(
    token,
    location_id,
    device_id,
    "orden-123",
    name="Cliente actualizado",
    priority=True,
    itemsToRemove=["linea-2"],
)
print(response)
```

Para sandbox, pasa `environment="sandbox"` en cualquier funcion cloud:

```python
healthCheck(token, environment="sandbox")
```

## Red local TCP/UDP

Segun la documentacion local de Fresh KDS, los tablets emiten discovery UDP en el puerto `28000` y reciben ordenes TCP en el puerto `9104`. El wrapper agrega:

- `parseDiscoveryBroadcast(data)`: parsea un broadcast de 102 bytes a `application`, `version`, `ipAddress`, `identifier` y `name`.
- `discoverLocalDevices(timeout=5.0)`: escucha broadcasts y retorna pantallas encontradas.
- `sendLocalOrder(ip_address, order)`: envia `create-order` por TCP.
- `updateLocalOrder(ip_address, order)`: envia `update-order` por TCP.
- `partialUpdateLocalOrder(ip_address, order_id, **changes)`: envia `partial-update-order`.
- `cancelLocalOrder(ip_address, order_id)`: envia `cancel-order`.

Ejemplo local:

```python
from pyKDSAPI.utils import discoverLocalDevices, sendLocalOrder

devices = discoverLocalDevices(timeout=5)
screen = devices[0]
response = sendLocalOrder(screen["ipAddress"], order_payload)
print(response)
```

## Documentación útil

Guías encontradas de Fresh KDS:

- [Developer Guide de Fresh KDS](https://www.fresh.technology/kds/developer-guide)
- [API Introduction de Fresh KDS](https://fresh-technology.github.io/fresh.kds.docs.mobile-local-network-integration/docs/api/introduction/)

## Notas

- El proyecto silencia el warning de `urllib3` relacionado con LibreSSL para que no ensucie la salida.
- `.env` está ignorado por Git para no subir secretos.
- El wrapper local en `pyKDSAPI` implementa las rutas cloud principales y helpers para TCP/UDP local.
