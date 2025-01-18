import requests 
import json
import numpy
import cv2

get_challenge_url = "https://hackattic.com/challenges/basic_face_detection/problem?access_token="
submit_solution_url = "https://hackattic.com/challenges/basic_face_detection/solve?access_token="


chall = requests.get(get_challenge_url).text
load = json.loads(chall)
image_url = load["image_url"]

nparr = numpy.frombuffer(requests.get(image_url).content, numpy.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

faces = face_classifier.detectMultiScale(
    gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
)


def find_grid_from_px(i):
    if i <= 100:
        return 0
    elif i <= 200:
        return 1
    elif i <= 300:
        return 2
    elif i <= 400:
        return 3
    elif i <= 500:
        return 4
    elif i <= 600:
        return 5
    elif i <= 700:
        return 6
    elif i <= 800:
        return 7

def sort_face_locations():
    output_arr = []

    for face in faces:
        output_arr.append([find_grid_from_px(face[0]), find_grid_from_px(face[1])])

    return output_arr

out = {
    "face_tiles": sort_face_locations()
}

print(out)

result = requests.post(submit_solution_url, json.dumps(out))
print(result.text)