import requests
import json
import base64
import struct

url_get_challenge = "https://hackattic.com/challenges/help_me_unpack/problem?access_token="
url_submit_solution = "https://hackattic.com/challenges/help_me_unpack/solve?access_token="

chall = (requests.get(url_get_challenge)).text
load = json.loads(chall)
parsed = load['bytes']

chall_bytes = base64.b64decode(parsed)
raw_bytes = bytes(chall_bytes)

numbers = struct.unpack("iIhfd", raw_bytes[:24])
big_endian_double_solved = struct.unpack(">d", raw_bytes[24:])

print(numbers)

data = {
    "int": numbers[0],
    "uint": numbers[1],
    "short": numbers[2],
    "float": numbers[3],
    "double": numbers[4],
    "big_endian_double": big_endian_double_solved[0]
}

result = requests.post(url_submit_solution, json.dumps(data))
print(result.text)
