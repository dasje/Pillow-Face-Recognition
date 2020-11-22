import numpy, cv2
from PIL import Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "/haarcascade_fontalface_default.xml")

thing = Image.open('famphoto.jpg')
thing = thing.convert('RGB')

def find_faces(image_for_faces):
    image = image_for_faces
    image = numpy.asarray(image)
    print(image)
    print(type(image))
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(image_gray)
    print(type(image_gray))
    cv2.imshow('face, hopefully', image_gray)
    faces = face_cascade.detectMultiScale(image_gray)
    return faces

faces = find_faces(thing)