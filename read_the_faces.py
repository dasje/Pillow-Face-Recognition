import zipfile, pytesseract, cv2, numpy, math
from PIL import Image, ImageDraw, ImageFont

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
face_cascade = cv2.CascadeClassifier("C:/Users/Wottle of Bine/Documents/Python Projects/piiillow_test/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")

#open zip, reads files, convert to pillow objects, store as dictionary
# in list with file names as key
zip_file = zipfile.ZipFile('small_img.zip', mode='r')
file_list = zip_file.infolist()
zip_list = []
for file in file_list:
    temp_zip_obj = zip_file.open(file.filename, 'r')
    temp_img_obj = Image.open(temp_zip_obj)
    temp_img_obj = temp_img_obj.convert(mode = 'RGB')
    zip_list.append({'filed_under':file.filename, 'pillow_image':temp_img_obj})
print('zip open and loaded to dict')

# read text from each file
# append text as value to each dictionary
for dictionary in zip_list:
    text = pytesseract.image_to_string(dictionary['pillow_image'])
    dictionary.update({'text':text})
print('text is read and added to dictionary')


def keyword_present(keyword, dictionary): #look for keywords in dictionary[text], return true or false
    if keyword in dictionary['text']:
        return True
    else:
        return False


def contact_sheet(len_faces, file_name, faces): #create contact sheet
    font_thing = ImageFont.truetype("arial.ttf", 20)
    rows = math.ceil(len_faces / 5)
    height = rows * 128 + 64
    width = 640
    canvas = Image.new(mode = 'P', size = (width, height))
    contact = ImageDraw.Draw(canvas)
    contact.rectangle((0,0,639,64), fill = (255,255,255), outline = (0,0,0))
    contact.text((20,20), 'Results found in file {}'.format(file_name), font = font_thing)
    face_counter = 0
    for face in faces:
        if face_counter < 5:
            x, y = 0, face_counter * 128
            canvas.paste(face, box = (x, y))
            face_counter += 1
        elif face_counter >= 5:
            x, y = (face_counter - 5) * 128, 128
            canvas.paste(face, box = (x, y))
            face_counter += 1
    return canvas
    #must be 5x across and new images must be stacked below
    #must have title bar across top of image 'Results found in file {}'.format(filename)
    #paste faces into contact sheet


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
        face_list.append(cropped)
    return face_list

# run keyword search
for dictionary in zip_list:
    counter = 0
    keyword = keyword_present('Mark', dictionary)
    print('keyword function runs, produces: ',keyword)
    # if keyword found: filter faces, create contact sheet, add faces to contact sheet
    if keyword == True:
        faces = find_faces(dictionary['pillow_image'])
        len_faces = len(faces)
        contact = contact_sheet(len_faces, dictionary['filed_under'], faces)
        contact.save('{}.bmp'.format(dictionary['filed_under']), 'BMP')



