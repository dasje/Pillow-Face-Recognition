import numpy, cv2
from PIL import Image

face_cascade = cv2.CascadeClassifier("C:/Users/Wottle of Bine/Documents/Python Projects/piiillow_test/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")

def find_faces(image_for_faces):
    # filter faces from image
    # resize face images to thumbnail size
    image = image_for_faces.resize((1800,3150))
    image_np = numpy.asarray(image)
    image_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(image_gray) #correct numpy array, prints correct coordinates per face
    face_list = []
    for face in faces:
        box = (face[0], face[1], face[0]+face[2], face[1]+face[3]) #correctly produces numpy coordinates
        copy_image = image.copy()
        cropped = copy_image.crop(box = (box))
        cropped.thumbnail((128,128))
        print(type(cropped))
        face_list.append(cropped)
    return face_list

y = Image.open('famphoto.jpg')
z = y.convert('RGB')

x = find_faces(z)
print(x)