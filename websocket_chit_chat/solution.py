import requests 
import json 
import websocket
from datetime import datetime 
import re

ws = websocket.WebSocket()

get_challenge_url = "https://hackattic.com/challenges/websocket_chit_chat/problem?access_token="
submit_solution_url = "https://hackattic.com/challenges/websocket_chit_chat/solve?access_token="


chall = requests.get(get_challenge_url).text
load = json.loads(chall)

token = load['token']
wsl_conn_url = f'wss://hackattic.com/_/ws/{token}'

start = datetime.now()

print(start)
print(wsl_conn_url)

def mapInterval(interval):
    if (interval < 1500):
        return 700
    if (interval < 2000):
        return 1500
    if (interval < 2500):
        return 2000
    if (interval < 3000):
        return 2500
    return 3000

def submit(message):
    message = re.findall(r'"(.*?)"', message)

    data = {
        "secret": message[0],
    }

    result = requests.post(submit_solution_url, json.dumps(data))
    print("Result: " + result.text)


def on_message(wsapp, message):
    global start
    print('Received: ', message)
    if (message == 'ping!'):

        interval = int((datetime.now() - start).total_seconds() * 1000) + 100
        interval = mapInterval(interval)

        wsapp.send(str(interval))
        print('Sent: ', interval)
        
        start = datetime.now()

    if ('congratulations' in message):
        submit(message)



wsapp = websocket.WebSocketApp(wsl_conn_url, on_message=on_message)
wsapp.run_forever()
