import requests
import base64
import json

client_id = "242509dc-1710-4fb3-b19c-0fa3ce113fe6"              #this has to be taken from Admin>External Applications
client_secret = "5591622"   #this has to be taken from Admin>External Applications (only visible when adding new application registrations

# Encode the client ID and client secret
authorization = base64.b64encode(bytes(client_id + ":" + client_secret, "ISO-8859-1")).decode("ascii")



headers = {
    "Authorization": f"Basic {authorization}",
    "Content-Type": "application/x-www-form-urlencoded"
}
body = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "OR.Queues"

}

response = requests.post("https://cloud.uipath.com/identity_/connect/token", data=body, headers=headers, verify=False)

print(response.text)
print(response.json()["access_token"])