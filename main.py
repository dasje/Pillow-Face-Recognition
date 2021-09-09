import zipfile
import pytesseract
import cv2
import numpy
import math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
face_cascade = cv2.CascadeClassifier(
    "C:/Users/nvcmm/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml"
)


def create_contact_sheet(img_dictionary, name):
    """Creates a contact sheet of faces found on the pages where a particular word or name appears.
    The dictionary is a python dictionary the information for images to be sorted: and will need entries for
    thumbnail_list and filed_under:
    a list of pillow objects of size 64/64
    the name of the file the objects were originally pulled from."""
    number_of_rows = math.ceil(len(img_dictionary['thumbnail_list']) / 5)
    canvas = Image.new('P', (640, number_of_rows * 128 + 64))
    draw_space = ImageDraw.Draw(canvas)
    draw_space.rectangle((0, 0, 639, 64), fill=(255, 255, 255), outline=(0, 0, 0))
    font_thing = ImageFont.truetype("arial.ttf", 20)
    if name:
        draw_space.text((20, 20), 'Results found in file {}'.format(img_dictionary['filed_under']), font=font_thing)
        thumbnail_counter = 0
        for thumbnail in img_dictionary['thumbnail_list']:
            if thumbnail_counter < 5:
                x, y = thumbnail_counter * 128, 64
                canvas.paste(thumbnail, (x, y))
                thumbnail_counter += 1
            elif thumbnail_counter >= 5:
                x, y = (thumbnail_counter - 5) * 128, 196
                canvas.paste(thumbnail, (x, y))
                thumbnail_counter += 1
    else:
        draw_space.text((20, 20), 'No results found in file {}'.format(img_dictionary['filed_under']), font=font_thing)
    return canvas


# open zip, reads files, convert to pillow objects, store as dictionary
# in list with file names as key
zip_file = zipfile.ZipFile(input('Please give the location of the zip you would like to use: '), mode='r')
file_list = zip_file.infolist()
zip_list = []
for file in file_list:
    temp_zip_obj = zip_file.open(file.filename, 'r')
    temp_img_obj = Image.open(temp_zip_obj)
    temp_img_obj = temp_img_obj.convert(mode='RGB')
    zip_list.append({'filed_under': file.filename, 'pillow_image': temp_img_obj})
print('zip open and loaded to dict')

# read text from each file
# append text as value to each dictionary
text_list = []
for dictionary in zip_list:
    text = pytesseract.image_to_string(dictionary['pillow_image'])
    text_list.append(text)
    dictionary.update({'text': text})
print('text is read and added to dictionary')

# read faces from each file
# append faces as list to each dictionary
# filter faces from image
# resize face images to thumbnail size
for dictionary in zip_list:
    image = dictionary['pillow_image']
    enhancer = ImageEnhance.Contrast(image)
    enhancer.enhance(0.0)
    sizes = image.size
    image = image.resize((int(sizes[0]/3), int(sizes[1]/3)))
    image_np = numpy.asarray(image)
    image_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(image_gray)  # correct numpy array, prints correct coordinates per face
    dictionary.update({'face_list': faces})

    thumbnail_list = []
    new_image = dictionary['pillow_image']
    sizes = new_image.size
    new_image = new_image.resize((int(sizes[0]/3), int(sizes[1]/3)))

    for face in dictionary['face_list']:
        x, y, a, b = face[0], face[1], face[2], face[3]
        copy_image = new_image.copy()
        box = (x, y, x+a, y+b)
        cropped = copy_image.crop(box)
        resized = cropped.resize((128, 128))
        thumbnail_list.append(resized)
    dictionary.update({'thumbnail_list': thumbnail_list})

print('faces and thumbnails added to dictionary')

name_request = input('What word are we searching for?: ')
for dictionary in zip_list:
    name_present = None
    if name_request in dictionary['text']:
        name_present = True
    else:
        name_present = False
    final_contact = create_contact_sheet(dictionary, name_present)
    final_contact.show()
    final_contact.save('{}'.format(dictionary['filed_under']))
