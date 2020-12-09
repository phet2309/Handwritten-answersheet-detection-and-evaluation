import cv2
import pytesseract as tess
from pytesseract import Output
import numpy as np
import random
import PIL.Image as Image
from autocorrect import Speller

def correct_sentence(p):
    p = p.strip().split('\n')
    lines=[]
    for i in p:
        if len(i)>0:
            lines.append(i)
    # print(l)
    #spell=Speller(lang='en')
    # lines = line.strip().split(' ')
    new_line = ""
    # similar_word = {}
    ans=[]
    for l in lines:
        l=l.strip().split(' ')
        for j in l:
            new_line += j + " "
            #new_line += spell(j) + " "
        ans.append(new_line)
        new_line=''
    # print(ans)
    return ans
    # # similar_word[l]=spell.candidates(l)
    # return new_line



def preprocess(image) :

# Method - 1
    ConcatenatedImage = np.concatenate((image, image, image, image, image, image), axis = 0)  # axis=0 is the concatenation at bottom
    ConcatenatedImage = Image.fromarray(ConcatenatedImage)
    #print('M-1:')
    #print(pytesseract.image_to_string(ConcatenatedImage))
# Method - 2
    image = cv2.fastNlMeansDenoisingColored(np.array(ConcatenatedImage))
    #print('M-2:')
    #print(pytesseract.image_to_string(image)) 
    Image.fromarray(image)
# Method - 3
    imageBorderRemoved = np.array(image)[40:310, 20:480]
    imageBorderRemoved = cv2.fastNlMeansDenoisingColored(imageBorderRemoved)
    Image.fromarray(imageBorderRemoved)
    #print('M-3:')
    #print(pytesseract.image_to_string(imageBorderRemoved))
# Method - 4
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    #print('M-4:')
    #print(pytesseract.image_to_string(gray))
    Image.fromarray(gray)
# Method - 5
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret1,th1 = cv2.threshold( gray,127,255,cv2.THRESH_BINARY)  #  global thresholding
    Image.fromarray(th1)
    #print('M-5:')
    #print(pytesseract.image_to_string(th1)) 
# Method - 6
    DenoisedImage = cv2.fastNlMeansDenoisingColored(np.array(image))
    grayDenoisedImage = cv2.cvtColor(DenoisedImage, cv2.COLOR_BGR2GRAY)
    th2 = cv2.adaptiveThreshold(grayDenoisedImage,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
    Image.fromarray(th2)
    #print('M-6:')
    #print(pytesseract.image_to_string(th2))
    return th2



def text_detection(path):
    # Load image, grayscale, Gaussian blur, adaptive threshold
    tess.pytesseract.tesseract_cmd = r'C:\Users\SATYAPRAKASH\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


    # path='D:\Sem5\Design Project\Mypart/test11.jpeg'
    img = cv2.imread(path)

    # img=preprocess(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    img = 255 - opening


    #target = pytesseract.image_to_string(img, lang='eng', config='--psm 6 --oem 3 -c tessedit_char_whitelist= ABCDEFGHIJKLNMOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz\\,\\.')
    # target=correct_sentence(target)
    target = tess.pytesseract.image_to_string(img)
    #a=correct_sentence(target)
    # for i in a:
        # print(i)
    return target
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
