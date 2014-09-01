# import tesseract

# api = tesseract.TessBaseAPI()
# api.Init(".","eng",tesseract.OEM_DEFAULT)
# api.SetVariable("tessedit_char_whitelist", "0123456789")
# api.SetPageSegMode(tesseract.PSM_AUTO)

# mImgFile = "..\screens\scores\score0.png"
# mBuffer=open(mImgFile,"rb").read()
# result = tesseract.ProcessPagesBuffer(mBuffer,len(mBuffer),api)
# print "result(ProcessPagesBuffer)=",result
# api.End()
import os
import subprocess
import tempfile
import cv2
from PIL import Image, ImageEnhance

def pil_to_cv2(image):
    # source http://stackoverflow.com/a/14140796/264675
    pil_image = image.convert('RGB')
    open_cv_image = numpy.array(pil_image)
    # Convert RGB to BGR
    return open_cv_image[:, :, ::-1].copy()

def show_cv2_image(image):
    cv2.imshow('image', image)
    cv2.waitKey()

def tesser_exe():
    path = os.path.join(os.environ['Programfiles'], 'Tesseract-OCR', 'tesseract.exe')
    path32 = os.path.join(os.environ['Programfiles(x86)'], 'Tesseract-OCR', 'tesseract.exe')

    if os.path.exists(path):
        return path
    elif os.path.exists(path32):
        return path32
    else:
        raise NotImplementedError('You must first install tesseract from https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-setup-3.02.02.exe&can=2&q=')

def load_image(number):
    return Image.open('..\screens\scores\score' + str(number) + '.png')

def load_image_thresh(number):
    return load_image.point(lambda p: p > 170 and 255)

def load_image_blur_thresh(number):
    return load_image.filter(ImageFilter.GaussianBlur).point(lambda p: p > 170 and 255)

def compare_methods():
    for i in range(60):
        text1 = text_from_image(load_image_thresh(i))
        text2 = text_from_image(load_image_blur_thresh(i))
        print(str(i) + ":\n\t" + text1 + "\n\t" + text2)

def text_from_cv2_image(image):
    (handle, input_name) = tempfile.mkstemp()
    cv2.imwrite(input_name + '.png', image)
    (handle, output_name) = tempfile.mkstemp()
    FNULL = open(os.devnull, 'w')
    return_code = subprocess.call([tesser_exe(), input_name + '.png', output_name, '-l', 'eng.matrx'], stderr=FNULL)
    return open(output_name + '.txt').read().rstrip('\n')    

def thresh(img):
    ret,thresh4 = cv2.threshold(img,127,255, cv2.THRESH_TOZERO)
    return thresh4

def compare():
    actual = [
            [99,53,92,98,4,93,56,80,81,13],
            [326,107,313,313,12,324,130,331,280,52],
            [433,129,415,474,28,492,158,455,402,74],
            [476,148,493,547,30,564,179,521,471,88],
            [551,186,569,683,43,656,202,652,550,105],
            [167,123,261,253,29,197,105,296,267,6]
        ]

    correct = 0
    num_screens = len(actual)
    for x in range(num_screens):
        screen = Frame('screens/screen' + str(x + 1) + '.png')
        for i in range(10):
            num = get_cs(screen, i)
            is_correct = False if num == '' else int(num) == actual[x][i]
            if not is_correct:
                print '[' + str(x+1) + ',' + str(i) + ']', num, '\t(' + str(actual[x][i]) + ')'
                show_cv2_image(thresh(screen._get_cs_img(i)))
            else:
                correct += 1

    print "Correct: " + str(correct) + "/" + str(num_screens*10) + "\t(" + str(correct/(num_screens*10.0)) + "%)"

def get_cs(frame, index):
    img = thresh(frame._get_cs_img(index))
    return text_from_cv2_image(img)