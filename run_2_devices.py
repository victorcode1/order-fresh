import runtime_warnings

import requests
from env_config import get_integration_token

headers = {
    "x-integration-token": get_integration_token()
}

location_id = "40726afb-961f-498a-99d3-fb73f665f5fe"

resp = requests.get(f"https://integrations-api.ftservices.cloud/integrators/kds-information/locations/{location_id}/devices", headers=headers)

print("Status code:", resp.status_code)

try:
    print("Respuesta JSON:")
    print(resp.json())
except Exception as e:
    print("Error al interpretar JSON:", e)
    print("Texto crudo de la respuesta:")
    print(resp.text)
