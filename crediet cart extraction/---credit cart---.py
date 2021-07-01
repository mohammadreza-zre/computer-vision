import imutils
import numpy as np
from imutils import contours
import cv2
import os
import pytesseract
from PIL import Image


path = 'C:\\Users\\Lenovo\\Desktop\\project2\\card2.jpg'
image = cv2.imread(path)
image = imutils.resize(image , height=400)
image = cv2.rotate(image , cv2.ROTATE_180)


rotate = cv2.rotate(image , cv2.ROTATE_180)
gray = cv2.cvtColor(rotate, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)


# canny = cv2.Canny(gray , 50,200)
thresh = cv2.adaptiveThreshold(gray , 255 , cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY_INV , 7 , C=2)
# kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (2,6))
erode = cv2.erode(thresh ,(3,3), iterations=1)
# kerrnel = cv2.getStructuringElement(cv2.MORPH_DILATE , (20,4))
dilate = cv2.dilate(erode , (3,3) , iterations=3)
# cv2_imshow(dilate)


cnts = cv2.findContours(dilate.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
c = cnts

for (i,c) in enumerate(cnts) :
    if i==1 : break
  # peri = cv2.arcLength(c, True)
  # approx = cv2.approxPolyDP(c, 0.0001 * peri, True)
  # print(len(approx))
  # cv2.drawContours(rotate, [approx], -1, (0, 255, 0), 2)
    (x,y,w,h)=cv2.boundingRect(c)
    cv2.rectangle(rotate , (x,y) , (x+w , y+h) , (0,200,0) , 2)
source = np.float32([[x,y] , [x,y+h] , [x+w , y] , [x+w , y+h]])
cart = np.zeros((210,340) , dtype = 'uint8')
dest = np.float32([[0,0] ,[0,210],[340,0],[340,210]])

M = cv2.getPerspectiveTransform(source , dest)
result = cv2.warpPerspective(rotate , M , (340,210))


# if dnn_superres doesn't work first (pip uninstall opencv-python) next (pip install opencv-contrib-python)

# !pip uninstall opencv-pythony
# !pip uninstall opencv-contrib-python
# !pip install --upgrade opencv-python
# !pip install --upgrade opencv-contrib-python
# cv2.__version__
# !pip install opencv-contrib-python==4.3.0.36

result_1 = imutils.resize(result , height=700)
test=result_1.copy()
kernel = np.array([[-1,-1,-1], [-1,7.8,-1], [-1,-1,-1]])
sharped = cv2.filter2D(result_1, -1, kernel)

gray = cv2.cvtColor(sharped , cv2.COLOR_BGR2GRAY)
gus = cv2.GaussianBlur(gray , (5,5) , -1)
adapt = cv2.adaptiveThreshold(gus , 255 ,
                              thresholdType=cv2.THRESH_BINARY_INV ,
                              adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C ,
                              blockSize= 25,
                              C=11)
erode = cv2.erode(adapt , (3,3) , iterations=3)
# sobel_y = cv2.Sobel(adapt , ddepth=0 , dx=0,dy=1 , ksize=1)
#blur_1 = cv2.medianBlur(thresh , 1)
ker = cv2.getStructuringElement(cv2.MORPH_DILATE , (30,8))
dil = cv2.dilate(erode , ker , iterations=5)
# cv2.imshow('sharp' , dil)
'''# boerder off carts is empty from information'''
# cv2.imwrite("C:\\Users\\Lenovo\\Desktop\\project2\\result_4_2.jpg" , dil[198: , 85:1048])
# cv2.waitKey(0)



cnts = cv2.findContours(dil[198: , 85:1048] , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# print(len(cnts)) # == 5
# # cnts = contours.sort_contours(cnts,method="bottom-to-top")
cnts = sorted(cnts , key = cv2.contourArea , reverse=True)[:5]

gray_pieces = []
for (i,c) in enumerate(cnts):
    if i==5 : break
    (x,y,w,h) = cv2.boundingRect(c)
    # +85 for return the dimantions to the original siz
    # -20,+20 for confidence distance and conflict
    cv2.rectangle(test , (x+85-20,y+198) , (x+85+20+w,y+198+h) , (0,0,255) , 2)
    c = test[y+198+3:y+198-3+h , x+85-20:x+85+20+w]
    gray = cv2.cvtColor(c , cv2.COLOR_BGR2GRAY)
    gray_pieces.append(gray)
# cv2.imshow('test' , test)
# cv2.imwrite("C:\\Users\\Lenovo\\Desktop\\project2\\result2.jpg" ,test)
# cv2.waitKey(0)



for (i,c) in enumerate(gray_pieces) :
    c = cv2.GaussianBlur(c , (3,3) , -1)
    c = cv2.adaptiveThreshold(c , 200 , cv2.THRESH_BINARY_INV , cv2.ADAPTIVE_THRESH_MEAN_C , blockSize=29, C=9)

    c = cv2.dilate(c ,(1,1) , iterations=5)
    c = cv2.erode(c, (10,1), iterations=2)



    # _,c = cv2.threshold(c , 0 , 255 , cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    # c = cv2.erode(c , (5,3) , iterations=1)
    # c = cv2.morphologyEx(c , cv2.MORPH_CLOSE, kernel=(5,5) , iterations=4)

    # cv2.imwrite(f"C:\\Users\\Lenovo\\Desktop\\project2\\piece_gray{i}.jpg" ,c)
    # cv2.imshow("c" , c)
    # cv2.waitKey(500)

stop_alphabets = ['1' , '2' ,'3' ,'4' ,'5' ,'6' ,'7', '8', '9' ,'0','!','@','#','$','%','^','&','*','(',')','_','+',
                  '=','-',']','[','}','}','~','`','?','/','<','>',',','z','x','c','v','b','n','m','.','a','s','d','f',
                  'g','h','j','k','l','q','w','e','r','t','y','u','i','o','p','|',':',';','Q','E','R','T','Y','U','I','O','P'
                  ,'A','S','D','F','G','H','J','K','L',';','Z','X','C','V','B','N','M',]
continue_alphabrt = ['ض','ص','ث','ق','ف','غ','ع','ه','خ','ح','ج','چ','پ','گ','ک','م','ن','ت','ا','ل','ب','ی','س','ش','ظ','ط','ز',
                     'ر','ذ','د','ئ','و','أ','ؤ','ژ','ي','ة','إ','أ','ء','آ','ۀ']
numbers = ['1' , '2' ,'3' ,'4' ,'5' ,'6' ,'7', '8', '9' ,'0']
cart_number= ""
name = ""

pytesseract.pytesseract.tesseract_cmd = 'C:\\UsersLenovo\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'
for i in range(5):
    c = Image.open(f"C:\\Users\\Lenovo\\Desktop\\project2\\piece_gray{i}.jpg")
    text = pytesseract.image_to_string(c , lang='fas+eng')
    parts = text.split()
    alphabets_parts = []
# '''-------------------------------------------------------'''
    if len(parts) >= 4 :
        for j in range(4):
            # part
            part = parts[j].split()
            alphabet_part = []
            for k in range(len(part[0])):
                # alphabet
                alphabet = part[0][k]
                alphabet_part.append(alphabet)

            for Q in alphabet_part :
                if Q in numbers :
                    cart_number += Q
        print("****************************")
        print(f'Cart number : {cart_number}')



# '''-------------------------------------------------------'''




    else :
        for j in range(len(parts)):
            # part
            part = parts[j].split()
            alphabet_part = []
            for k in range(len(part[0])):
                # alphabet
                alphabet = part[0][k]
                alphabet_part.append(alphabet)
            if "R" in alphabet_part:
                alphabet_part[0] = 'I'
                Shaba = ''
                for G in alphabet_part:
                    Shaba += G
                print("****************************")
                print(f'Shaba number : {Shaba}')
            elif "/" in alphabet_part :
                print("****************************")
                print(f'Expiration date : {parts[j]}')
            elif len(alphabet_part) == 3 :
                for N in alphabet_part:
                    if N not in numbers :
                        pass
                    else:
                        print("****************************")
                        print(f'CVV2 : {parts[j]}')
                        break




# '''-------------------------------------------------------'''






for i in range(5):
    c = Image.open(f"C:\\Users\\Lenovo\\Desktop\\project2\\piece_gray{i}.jpg")
    text = pytesseract.image_to_string(c , lang='fas+eng')
    parts = text.split()
    alphabets_parts = []

    if len(parts) == 2 :
        alphabet_part = []

        for j in range(2):
            # part
            part = parts[j].split()

            for k in range(len(part[0])):
                # alphabet
                alphabet = part[0][k]
                alphabet_part.append(alphabet)
        for T in alphabet_part :
            if T in continue_alphabrt :
                name += T
            else:
                break

print("****************************")
print(f'Owner name : {name}')



banks = {
    '603799' : "بانک ملی ایران" ,
    '589210' : "بانک سپه" ,
    '627648' : "بانک توسعه صادرا" ,
    '627961' : "بانک صنعت و معدن" ,
    '603770' : "بانک کشاورزی" ,
    '628023' : "بانک مسکن" ,
    '627760' : "پست بانک ایران" ,
    '502908' : "بانک توسعه تعاون" ,
    '627412' : "بانک اقتصاد نوین" ,
    '622106' : "بانک پارسیان" ,
    '502229' : "بانک پاسارگاد" ,
    '627488' : "بانک کارآفری" ,
    '621986' : "بانک سامان" ,
    '639346' : "بانک سینا" ,
    '639607' : "بانک سرمایه" ,
    '636214' : "بانک تات" ,
    '502806' : "بانک شهر" ,
    '502938' : "بانک دی" ,
    '603769' : "بانک صادرات " ,
    '610433' : "بانک ملت " ,
    '627353' : "بانک تجارت " ,
    '589463' : "بانک رفاه" ,
    '627381' : "بانک انصار" ,
    '639370' : "بانک مهر اقتصاد" ,
        }


bank_id = cart_number[:6]
print("****************************")
print(f'Bank name : {banks[bank_id]}')
print("****************************")

# for text in texts :

# a = texts[1].split()[0]
# alphabets_final=[]
# sections = []
# for text in texts :
#     #sent
#     text_1 = text.split()
#     alphabets_sent = []
#     for j in range(len(text_1)):
#         #part
#         text_2 = text_1[j].split()
#         alphabet_part = []
#         for k in range(len(text_2[0])):
#             # alphabet
#             alphabet=text_2[0][k]
#             alphabet_part.append(alphabet)
#
#
#
#
#         if "R" in alphabet_part :
#             print(f'shaba number : {text_1[j]}')
#         elif "/" in alphabet_part :
#             print(f'expired date : {text_1[j]}')
#         elif len(alphabet_part) ==3 :
#             for N in alphabet_part:
#                 if N not in numbers :
#                     pass
#                 else:
#                     print(f'CVV2 : {text_1[j]}')
#                     break
#         elif len(text)==4:
#             for part in text :
#                 for N in part :
#                     if N in numbers:
#                         cart_namber.append(N)
#             print(cart_namber)
#
#
#
#



# # from cv2.cv2 import dnn_superres
#
#
# '''
# EDSR_x4.pb
# ESPCN_x4.pb
# FSRCNN_x3.pb
# LapSRN_x8.pb
# '''
# model = {'a' : "C:\\Users\\Lenovo\\Downloads\resolution_dnn\\EDSR_x4.pb",
#          'b' : "C:\\Users\\Lenovo\\Downloads\resolution_dnn\\ESPCN_x4.pb",
#          'c' : "C:\\Users\\Lenovo\\Downloads\resolution_dnn\\FSRCNN_x4.pb",
#          'd' : "C:\\Users\\Lenovo\\Downloads\resolution_dnn\\LapSRN_x8.pb"}
# d = "C:\\Users\\Lenovo\\Downloads\resolution_dnn\\LapSRN_x8.pb"
# # for x in model.values():
# #   modelName = x.split(os.path.sep)[-1].split("_")[0].lower()
# #   modelScale= x.split("_x")[-1]
# #   modelScale = int(modelScale[:modelScale.find(".")])
# #   sr = cv2.dnn_superres.DnnSuperResImpl_create()
# #   sr.readModel(x)
# #   sr.setModel(modelName, modelScale)
# #   upscaled = sr.upsample(result)
# #   print(x)
# #   cv2_imshow(upscaled)
# print("B ...")
# modelName = d.split(os.path.sep)[-1].split("_")[0].lower()
# modelScale= d.split("_x")[-1]
# modelScale = int(modelScale[:modelScale.find(".")])
# print("C ...")
# sr = cv2.dnn_superres.DnnSuperResImpl_create()
# sr.readModel(d)
# sr.setModel(modelName, modelScale)
# print("D ...")
# upscaled = sr.upsample(result)
# (h_r , w_r) = result.shape[:2]
# cv2.imshow('upscaled',upscaled)
# test = upscaled.copy()


# cv2.imshow('test' , test)
# cv2.imwrite("C:\\Users\\Lenovo\\Desktop\\project\\test.jpg", test)
#


















