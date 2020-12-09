import cv2
import pytesseract
import os

def text_rec(x):
    img = cv2.imread(x)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    target = pytesseract.image_to_string(img, lang='eng', config='--psm 6 --oem 3 -c tessedit_char_whitelist= ABCDEFGHIJKLNMOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz\\,\\.')
    #target = pytesseract.image_to_string(img, lang='eng', config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLNMOPQRSTUVWXYZ1234567890')
    # print(target)
    # print("-----------")
    tp = ''
    for i in target:
        if ord(i) >= 48 and ord(i) <= 57:
            tp = tp + i
    if len(tp)==0:
        return -1
    return int(tp)

def pageNo(path):
    image = cv2.imread(path)
    #image = cv2.resize(image, (765, 1049))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    if len(cnts)==0:
        return -1
    # temp=cnts[len(cnts)-1]
    i = 0;
    # ROI_number = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)
            # if i==0:
            #     ROI = image[y:y+h, x:x+w]
            #     cv2.imwrite("PageNo" + str(i) + ".jpg", ROI)
            #     i=100;
            # ROI_number += 1
    ROI = image[y:y + h, x:x + w]
    cv2.imwrite("PageNo" + str(i) + ".jpg", ROI)
    retVal = text_rec("PageNo" + str(i) + ".jpg")

    try:
        os.remove("PageNo" + str(i) + ".jpg")
    except:
        pass
    return retVal
