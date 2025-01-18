import requests
import json
import cv2
import numpy

get_challenge_url = "https://hackattic.com/challenges/reading_qr/problem?access_token="
submit_solution_url = "https://hackattic.com/challenges/reading_qr/solve?access_token="

detector = cv2.QRCodeDetector()

chall = requests.get(get_challenge_url).text
load = json.loads(chall)
img_url = load['image_url']

nparr = numpy.frombuffer(requests.get(img_url).content, numpy.uint8)
qr_code = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

data, bbox, straight_qrcode = detector.detectAndDecode(qr_code)

print(data)

data_solution = {
    "code": data
}

result = requests.post(submit_solution_url, json.dumps(data_solution))
print(result.text)
