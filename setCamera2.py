import cv2
import numpy
import numpy as np
import imutils
import os
import pytesseract as tess
from main import pageNo
from final import correct_sentence

from final import text_detection , correct_sentence
from time import sleep
#_________________________________________________________________________________
#prachi's work character recognition
tess.pytesseract.tesseract_cmd=r'C:\Users\SATYAPRAKASH\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
def text_rec(x):
    img = cv2.imread(x)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    target = tess.pytesseract.image_to_string(img , lang ="eng+eng1" )
    #target = pytesseract.image_to_string(img, lang='eng', config='--psm 6 --oem 3 -c tessedit_char_whitelist= ABCDEFGHIJKLNMOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz\\,\\.')
    #target = pytesseract.image_to_string(img, lang='eng', config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLNMOPQRSTUVWXYZ1234567890')
    #print(target)
    #a = correct_sentence(target)
    return target


def correct_sentence(p):
    p = p.strip().split('\n')
    lines = []
    for i in p:
        if len(i) > 0:
            lines.append(i)

    new_line = ""

    ans = []
    for l in lines:
        l = l.strip().split(' ')
        for j in l:
            new_line += j + " "
        ans.append(new_line)
        new_line = ''
    fin = ''
    for i in ans:
        fin += i + '\n'
    return fin

def final_file(id,q):
    f1=open("C:/Users/SATYAPRAKASH/PycharmProjects/Test/AnswerSheet/"+str(id)+'_Q'+str(q)+'.txt','r')
    s=f1.read()
    s=correct_sentence(s)
    f1.close()
    # print(s)
    f1=open("C:/Users/SATYAPRAKASH/PycharmProjects/Test/AnswerSheet/"+str(id)+'_Q'+str(q)+'.txt','w')
    f1.write(s)
    f1.close()




#_______________________________________________________________________________________
def get_answer(ID , QN):
    url = 'http://192.168.43.58:8080/video'
    cap = cv2.VideoCapture(1)  # cap is a camera object
    j = 0;
    #oldPage = 3425
    #newPage = 0;
    from matplotlib import pyplot as plt
    file1 = open("C:/Users/SATYAPRAKASH/PycharmProjects/Test/AnswerSheet/"+str(ID)+"_Q"+str(QN)+".txt", 'w')

    while True:
        ret, frame = cap.read()  # made a frame object
        blurred_frame = cv2.blur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)  # convert blurred_frame into hsv color

        lower_white = np.array([40, 0, 132])
        upper_white = np.array([145, 75, 245])

        mask = cv2.inRange(hsv, lower_white, upper_white)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        r, thresh = cv2.threshold(mask, 40, 255, 0)

        # check to see if we are using OpenCV 2.X or OpenCV 4
        if imutils.is_cv2() or imutils.is_cv4():
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # check to see if we are using OpenCV 3
        elif imutils.is_cv3():
            im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            area = cv2.contourArea(contour)
            # if area > 100:
            #     cv2.drawContours(frame, contours, -1, 255, 3)
            # find the biggest countour (c) by the area
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)

            # draw the biggest contour (c) in green
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            roi = frame[y + 10:y + h - 5, x + 10:x + w - 8]
            cv2.imshow("Roi", roi)  # show image

            if j % 150 == 0:
                cv2.imwrite("Frame" + str(j) + ".jpg", roi)
                content = text_rec("Frame" + str(j) + ".jpg")
                # content = text_detection("Frame"+str(j)+".jpg")
                # newPage = pageNo("Frame"+str(j)+".jpg")
                # if newPage==-1:
                #     continue
                print(content)
                file1.seek(0)
                file1.write(content)
                # for i in content:
                #     file1.write(i)
                #     file1.write("\n")
                #     print(i)

                # if newPage!=oldPage:
                #     print("page no = "+ str(newPage) )
                #     oldPage=newPage
                #     print(content)
                try:
                    os.remove("Frame" + str(j) + ".jpg")
                except:
                    pass
                break;

            j = j + 1

            # sleep(5)

        # show the images
        # cv2.imshow("Result", np.hstack([frame, res]))
        cv2.imshow("Roi", roi)  # show image
        # cv2.imshow("Frame", frame)  # show image
        # cv2.imshow("Mask", mask)  # show image
        # cv2.imshow("res", res)  # show image

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    file1.close()
    #final_file(ID , QN)
    cap.release()
    cv2.destroyAllWindows()




