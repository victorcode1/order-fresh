import requests

headers = {
    "x-integration-token": "sTOHqSylJUmA68pT5lkvxuKLSxpmcAVfIQQ8ybL6UiymiFQXzZjQyRXzN38RKqHI8YZNFuMIiXBIyJJ1lHi7OT"
}

location_id = "4f8e36ef-c1ec-4241-aa2a-e34b3324b8f9"

resp = requests.get(f"https://integrations-api.ftservices.cloud/integrators/kds-information/locations/{location_id}/devices", headers=headers)

print("Status code:", resp.status_code)

try:
    print("Respuesta JSON:")
    print(resp.json())
except Exception as e:
    print("Error al interpretar JSON:", e)
    print("Texto crudo de la respuesta:")
    print(resp.text)
