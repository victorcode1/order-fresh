import runtime_warnings

import requests
from env_config import get_integration_token

# Carga el token desde variables de entorno o desde .env
headers = {
    "x-integration-token": get_integration_token()
}

# Endpoint para obtener ubicaciones asociadas al token
resp = requests.get("https://integrations-api.ftservices.cloud/integrators/kds-information/locations", headers=headers)

print("Status code:", resp.status_code)

# Mostramos la respuesta del servidor
try:
    print("Respuesta JSON:")
    print(resp.json())
except Exception as e:
    print("Error al interpretar la respuesta como JSON:", e)
    print("Texto crudo de la respuesta:")
    print(resp.text)
