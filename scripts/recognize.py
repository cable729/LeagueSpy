import os
import subprocess
import tempfile
import cv2

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

def text_from_cv2_image(image):
    (handle, input_name) = tempfile.mkstemp()
    cv2.imwrite(input_name + '.png', image)
    (handle, output_name) = tempfile.mkstemp()
    FNULL = open(os.devnull, 'w')
    return_code = subprocess.call([tesser_exe(), input_name + '.png', output_name, '-l', 'eng.matrx'], stderr=FNULL)
    return open(output_name + '.txt').read().rstrip('\n')    

def binarize(img):
    ret,thresh = cv2.threshold(img,127,255, cv2.THRESH_BINARY)
    return thresh

def get_cs(frame, index):
    img = binarize(frame.get_cs_img(index))
    return text_from_cv2_image(img)

def compare(show_errors = False):
    actual = [
            [99,53,92,98,4,93,56,80,81,13],
            [326,107,313,313,12,324,130,331,280,52],
            [433,129,415,474,28,492,158,455,402,74],
            [476,148,493,547,30,564,179,521,471,88],
            [551,186,569,683,43,656,202,652,550,105],
            [167,123,261,253,29,197,105,296,267,6]
        ]

    num_correct = 0
    num_screens = len(actual)
    for x in range(num_screens):
        screen = Frame('screens/screen' + str(x + 1) + '.png')
        for i in range(10):
            num = get_cs(screen, i)
            if not is_int(num) or int(num) != actual[x][i]:
                tabs = "\t\t" if len(num) <= 2 else "\t"
                print "WRONG [Screen {0}, Player {1}] '{2}'{3}({4})".format(x + 1, i, num, tabs, actual[x][i])
                if show_errors:
                    show_cv2_image(binarize(screen.get_cs_img(i)))
            else:
                num_correct += 1

    print "Correct: {0}/{1}\t({2})".format(num_correct, num_screens * 10, 10.0 * num_correct / num_screens)

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def generate_cs_imgs():
    for x in range(6):
        frame = Frame('screens/screen' + str(x + 1) + '.png')
        for i in range(10):
            img = binarize(frame._get_cs_img(i))
            cv2.imwrite('screens/cs/' + str(x * 10 + i) + ".png", img)