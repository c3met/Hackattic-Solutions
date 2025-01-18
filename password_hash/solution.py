import requests
import json
import base64
from hashlib import sha256, pbkdf2_hmac
from Crypto.Protocol.KDF import scrypt
import hmac

url_get_challenge = "https://hackattic.com/challenges/password_hashing/problem?access_token="
url_submit_solution = "https://hackattic.com/challenges/password_hashing/solve?access_token="

chall = (requests.get(url_get_challenge)).text
load = json.loads(chall)

passw_parsed = load['password']
salt_parsed = base64.b64decode(load['salt'])
print("object: " + str(load))
print("salt parsed: " + str(salt_parsed))

pbkdf2_parsed = load['pbkdf2']
scrypt_parsed = load['scrypt']



pbkdf2_solved = pbkdf2_hmac(pbkdf2_parsed['hash'], passw_parsed.encode('utf-8'), salt_parsed, int(pbkdf2_parsed['rounds'])).hex()
sha256_solved = sha256(passw_parsed.encode('utf-8')).hexdigest()
hmac_solved = hmac.new(salt_parsed, msg=passw_parsed.encode('utf-8'), digestmod="sha256").hexdigest() 
scrypt_solved = scrypt(passw_parsed.encode('utf-8'), salt=salt_parsed, N=scrypt_parsed['N'], r=scrypt_parsed['r'], p=scrypt_parsed['p'], key_len=scrypt_parsed['buflen']).hex()



data = {
    "sha256": sha256_solved,
    "hmac": hmac_solved,
    "pbkdf2": pbkdf2_solved,
    "scrypt": scrypt_solved
}
print("Data final: " + str(data))

result = requests.post(url_submit_solution, json.dumps(data))
print("Result: " + result.text)
