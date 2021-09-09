# Pillow-Face-Recognition
A program that makes use of the Pillow, OpenCV and Tesseract libraries to parse zip files with newspaper scans, and then create contact sheets with the photos of faces found in the scans that contain particular keywords


Look how easy it is to use:

    Run main.py.
    
The locations of the tesseract executable and frontalface xml may need adjusting depending on where on the operating system they are stored.

The program makes use of zip files. Each image scan in the file should contain a single newspaper page scan in jpg or png formats.

The program compiles a dictionary of data about each image. The program can be expanded with methods that make use of the data in the dictionary.

The data assembled are 
* filed_under: file name, 
* pillow_img: pillow object of the scan, 
* text: text extracted from the image,
* face_list: a list of numpy_arrays that locate the faces found in the image, 
* thumbnail_list: a list of pillow objects resized to thumbnail size

Support
-------

If you are having issues, please let us know.
We have a mailing list located at: bendbm@live.co.uk

License
-------

The project is licensed under the BSD license.
