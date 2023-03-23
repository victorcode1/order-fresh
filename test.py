from pyKDSAPI.utils import getOrganization

heads = {'Content-Type':'application/json'}
token = "IuOjJi6uAMkEzybWjogaKYvh2J0KwVxyN7h3M3rgwAY0vlyztgB1kWo6V51V01rFh0nuirqHjutO6STCalnwzc"
x= getOrganization(token=token)

print(x)