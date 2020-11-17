
import requests
import urllib3
import random
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Select the number of participants per VideoRoom
#rooms = int(input("\n Enter the number of room: "))

rooms = int(sys.argv[1])

# Get transaction id
url = "https://janus-dev.maestroconference.com:8089/janus/info"
headers={ 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/85.0.4183.121 Safari/537.36'}
page = requests.get(url, headers=headers, verify=False)

response = page.json()
transaction = response['transaction']
print("\n Get transaction id: " + response['transaction'])

# Get session id
url = "https://janus-dev.maestroconference.com:8089/janus"
payload = { 
            "janus": "create", 
            "transaction": transaction }

page = requests.post(url, headers=headers, verify=False, json=payload)
response = page.json()
session = response['data']
print(" Get session id: " + str(session['id']))

# Get plugin handle
url = "https://janus-dev.maestroconference.com:8089/janus/"+ str(session['id'])
payload = {
            "janus" : "attach",
            "plugin" : "janus.plugin.videoroom",
            "transaction" : transaction  }

page = requests.post(url, headers=headers, verify=False, json=payload)
response = page.json()
plugin_handle = response['data']
print(" Get plugin handle: " + str(plugin_handle['id']) + "\n")

# Create video rooms
y = 0
i = 1
while y < rooms:
    url = "https://janus-dev.maestroconference.com:8089/janus/"+ str(session['id']) + '/' + str(plugin_handle['id'])
    payload = {
                "janus": "message",
                "transaction": transaction,
                    "body": {
                                "request" : "create",
                                "room" : 100 + i,
                                "permanent" : False,
                                "description" : "RoomTest " + str(i),
                                "secret" : "adminpwd",
                                "publishers" : 25,
                                "bitrate": 128000,
                                "fir_freq": 10,
                                "record": False
                            }
                }

    page = requests.post(url, headers=headers, verify=False, json=payload)
    response = page.json()
    print(" RoomTest " + str(i) +" "+ str(response['janus']))
    y = y + 1
    i = i + 1

# Video room listing
url = "https://janus-dev.maestroconference.com:8089/janus/"+ str(session['id']) + '/' + str(plugin_handle['id'])
payload = {
            "janus": "message",
            "transaction": transaction,
            "body": {
                "request" : "list" 
            } 
        }
page = requests.post(url, headers=headers, verify=False, json=payload)
response = page.json()
listing = response['plugindata']['data']['list']
print("\n Get list of rooms:")

y = 0
i = 0
while y == 0:
    try:
        if listing[i]['room']:
            print(" - " + listing[i]['description'])
            i = i + 1
    except IndexError:
        y = 1
