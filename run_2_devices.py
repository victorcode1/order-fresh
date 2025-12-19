import requests

headers = {
    "x-integration-token": "BH5yuMvuuQOfOrUUDSdpsZr4INBf8STUI8dt1YjeiyUHag5SaVuVAB2YYqd2PovCDEpq4EvIHppHSjRSVPkggB"
}

location_id = "687e1a74-03b4-4b6d-bdd9-3dc96193b813"

resp = requests.get(f"https://integrations-api.ftservices.cloud/integrators/kds-information/locations/{location_id}/devices", headers=headers)

print("Status code:", resp.status_code)

try:
    print("Respuesta JSON:")
    print(resp.json())
except Exception as e:
    print("Error al interpretar JSON:", e)
    print("Texto crudo de la respuesta:")
    print(resp.text)
