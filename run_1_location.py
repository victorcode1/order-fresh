import requests

# Pone acá tu token de integración completo
headers = {
    "x-integration-token": "BH5yuMvuuQOfOrUUDSdpsZr4INBf8STUI8dt1YjeiyUHag5SaVuVAB2YYqd2PovCDEpq4EvIHppHSjRSVPkggB"
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
