import requests
import json 

http_proxies = [
]

get_challenge_url = "https://hackattic.com/challenges/a_global_presence/problem?access_token="
submit_solution_url = "https://hackattic.com/challenges/a_global_presence/solve?access_token="


chall = requests.get(get_challenge_url).text
load = json.loads(chall)

presence_url = f'https://hackattic.com/_/presence/{load['presence_token']}'
print("Presence URL: " + presence_url)


for i in http_proxies:
    try:

        proxies = {
            "http": i,
            "https": i
        }

        res = requests.get(presence_url, proxies=proxies, timeout=3)
        print("Response status:", res.text)

        response_codes = res.text.split(",")
        if len(response_codes) > 7:
            result = requests.post(submit_solution_url, json.dumps({}))
            print(result.text)


    except requests.exceptions.RequestException:
        print(i)
        continue


