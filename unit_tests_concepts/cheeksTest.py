from collections import OrderedDict
import numpy as np
import cv2
import dlib
import imutils

CHEEK_IDXS = OrderedDict([("left_cheek", (1,2,3,4,5,48,49,31)),
                        ("right_cheek", (11,12,13,14,15,35,53,54))
                         ])

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("data\\shape_predictor_68_face_landmarks.dat")

img = cv2.imread('data\\tom.jpg')
img = imutils.resize(img, width=600)

overlay = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

detections = detector(gray, 0)
for k,d in enumerate(detections):
    shape = predictor(gray, d)
    for (_, name) in enumerate(CHEEK_IDXS.keys()):
        pts = np.zeros((len(CHEEK_IDXS[name]), 2), np.int32)
        for i,j in enumerate(CHEEK_IDXS[name]):
            pts[i] = [shape.part(j).x, shape.part(j).y]

        pts = pts.reshape((-1,1,2))
        cv2.polylines(overlay,[pts],True,(0,255,0),thickness = 2)

    cv2.imshow("Image", overlay)
    cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
