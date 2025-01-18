import requests
import json
import hashlib

get_challenge_url = "https://hackattic.com/challenges/mini_miner/problem?access_token="
submit_solution_url = "https://hackattic.com/challenges/mini_miner/solve?access_token="


chall = requests.get(get_challenge_url).text
load = json.loads(chall)

difficulty = load['difficulty']
block = load['block']
block['nonce'] = 0
unsolved = True

print(difficulty)
print(block)


while unsolved:
    serialized_block = json.dumps({"data": block["data"], "nonce": block["nonce"]}, 
                                       separators=(',', ':'), 
                                       sort_keys=True)
    hash = hashlib.sha256(serialized_block.encode("utf8")).hexdigest()
    bitHash = bin(int(hash, 16))[2:].zfill(256)
    
    if bitHash.startswith('0' * difficulty):
      data_solution = {
        "nonce": block['nonce']
      }
      result = requests.post(submit_solution_url, json.dumps(data_solution))
      print(result.text)
      unsolved = False
    else:
      block['nonce'] +=1

            