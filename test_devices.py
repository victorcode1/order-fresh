import requests

headers = {
    "x-integration-token": "DjYHZnUEAJZp1hCg0MhAG6Tz6cbpzYey6fMgyIhpcnRgdqdGtQvMkRWog4kXYWn6L3WoXCf5YkfNQxYpIvFZmT"
}

location_id = "1d539473-6b19-4264-90d7-51223bb0d2e4"

resp = requests.get(f"https://integrations-api.ftservices.cloud/integrators/kds-information/locations/{location_id}/devices", headers=headers)

print("Status code:", resp.status_code)

try:
    print("Respuesta JSON:")
    print(resp.json())
except Exception as e:
    print("Error al interpretar JSON:", e)
    print("Texto crudo de la respuesta:")
    print(resp.text)
