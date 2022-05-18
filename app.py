import json
import cv2
import urllib.request
import numpy as np
import imutils
import easyocr
from flask import Flask, jsonify,request


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def home():
   
    return "MuvMeeOCR"


@app.route('/apitest/', methods=['GET'])
def get_api():
    #img = cv2.imread('/Users/kevin/muvmeeflask/images9644.jpeg')
    url = 'https://firebasestorage.googleapis.com/v0/b/muvmee-flutter.appspot.com/o/CaptureImg%2Fkeviniiz2543%40gmail.com%2Fimages5101.jpg?alt=media&token=5fb4908b-f7e2-4176-9fd6-28f69f0dec49' 
    #url = request.args.get('imgurl')
    with urllib.request.urlopen(url) as resp:
        img = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    blur = cv2.GaussianBlur(equalized, (5, 5), 1)
    # plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(bfilter, 30, 200)
    # plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    
# easyocr part
    reader = easyocr.Reader(['th'], gpu=False, download_enabled=False)
    result = reader.readtext(cropped_image,detail=0,paragraph=True)
    result

# string split
    result = result[0].split(sep=" ",maxsplit=5);
    if len(result) == 3:
        numberplate = result[0]+result[1]
        province = result[2]
    elif len(result) == 2:
        numberplate = result[0];
        province = result[1];

    return jsonify(numberplate,province)

@app.route('/apitest2/', methods=['GET','POST'])
def get_api2():
    #img = cv2.imread('/Users/kevin/muvmeeflask/images9644.jpeg')
    #url = 'https://firebasestorage.googleapis.com/v0/b/muvmee-flutter.appspot.com/o/CaptureImg%2Fkeviniiz2543%40gmail.com%2Fplate5.jpeg?alt=media&token=9fe87f31-0bec-4138-b4fa-b8879d58135d' 
    #url = request.args.get('imgurl')
    if request.method =='POST':
        data = json.loads(request.data)
        # result = request.data
        url = data["imgurl"]
    with urllib.request.urlopen(url) as resp:
        img = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    blur = cv2.GaussianBlur(equalized, (5, 5), 1)
    # plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(bfilter, 30, 200)
    # plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    
# easyocr part
    reader = easyocr.Reader(['th'], gpu=False, download_enabled=False)
    result = reader.readtext(cropped_image,detail=0,paragraph=True)
    result

# string split
    result = result[0].split(sep=" ",maxsplit=5);
    if len(result) == 3:
        numberplate = result[0]+result[1]
        province = result[2]
    elif len(result) == 2:
        numberplate = result[0];
        province = result[1];

    return jsonify(numberplate=numberplate,province=province),201

if __name__ == '__main__':
    app.run(debug=True)
