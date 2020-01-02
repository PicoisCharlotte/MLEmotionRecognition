from math import sqrt, pow
import cv2
import numpy as np
import dlib

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

not_emotion_smile_left = 0
not_emotion_smile_center = 0
not_emotion_smile_right = 0
not_emotion_eyebrow_left_center = 0
not_emotion_eyebrow_right_center = 0
not_emotion_eyebrow_center = 0
not_emotion_eyebrow_left = 0
not_emotion_eyebrow_right = 0

while True:


    def calculDist(x1, y1, x2, y2):
        return sqrt(pow((y2-y1), 2)+pow((x2-x1), 2))

    def isSmilling():
        return not_emotion_smile_left > smile_left_marge and not_emotion_smile_center < smile_center and not_emotion_smile_right > smile_right_marge

    def isSad():
        return not_emotion_smile_left < smile_left_marge and not_emotion_smile_right < smile_right_marge and not_emotion_eyebrow_left < eyebrow_left and not_emotion_eyebrow_right < eyebrow_right

    def isAngry():
        return not_emotion_eyebrow_left_center > eyebrow_left_center and not_emotion_eyebrow_right_center > eyebrow_right_center and not_emotion_eyebrow_center > eyebrow_center

    _,frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray) #detecte the faces
    #print(faces)
    for face in faces:
        #print(face) #affiche [(209, 185) (424, 400)] //[point at the top left, point at the top right]
        #use those point to draw a retangle where the face is
        #to extract the point do :
        x1 = face.left() #209
        y1 = face.top() #185
        x2 = face.right() #424
        y2 = face.bottom() #400
        #draw the rectangle : frame, point1, point2, color, thickness
        #cv2.rectangle(frame, (x1,y1), (x2, y2), (0,255,0), 3)
        landmarks = predictor(gray, face) #detecte the landmarks points
        #print(landmarks)#full_object_detection object



        smile_left = calculDist(landmarks.part(36).x, landmarks.part(36).y, landmarks.part(48).x, landmarks.part(48).y) * 1000
        smile_center = calculDist(landmarks.part(48).x, landmarks.part(48).y, landmarks.part(54).x, landmarks.part(54).y) * 1000
        smile_right = calculDist(landmarks.part(45).x, landmarks.part(45).y, landmarks.part(54).x, landmarks.part(54).y) * 1000

        eyebrow_left_center = calculDist(landmarks.part(21).x, landmarks.part(21).y, landmarks.part(31).x, landmarks.part(31).y) * 1000
        eyebrow_right_center = calculDist(landmarks.part(22).x, landmarks.part(22).y, landmarks.part(35).x, landmarks.part(35).y) * 1000
        eyebrow_center = calculDist(landmarks.part(21).x, landmarks.part(21).y, landmarks.part(22).x, landmarks.part(22).y) * 1000
        eyebrow_left = calculDist(landmarks.part(17).x, landmarks.part(17).y, landmarks.part(5).x, landmarks.part(5).y) * 1000
        eyebrow_right = calculDist(landmarks.part(26).x, landmarks.part(26).y, landmarks.part(11).x, landmarks.part(11).y) * 1000

        if not_emotion_smile_left == 0:
            not_emotion_smile_left = smile_left
        if not_emotion_smile_center == 0:
            not_emotion_smile_center = smile_center
        if not_emotion_smile_right == 0:
            not_emotion_smile_right = smile_right
        if not_emotion_eyebrow_left_center == 0:
            not_emotion_eyebrow_left_center = eyebrow_left_center
        if not_emotion_eyebrow_right_center == 0:
            not_emotion_eyebrow_right_center = eyebrow_right_center
        if not_emotion_eyebrow_center == 0:
            not_emotion_eyebrow_center = eyebrow_center
        if not_emotion_eyebrow_left == 0:
            not_emotion_eyebrow_left = eyebrow_left
        if not_emotion_eyebrow_right == 0:
            not_emotion_eyebrow_right = eyebrow_right

        smile_left_marge = smile_left + 5
        smile_right_marge = smile_right + 5

        """print("----------------------------------   EMOTION    --------------------------------------------")
        print(smile_left)
        print(smile_right)
        print(smile_center)
        print("----------------------------------   NOT EMOTION    --------------------------------------------")
        print(not_emotion_smile_left)
        print(not_emotion_smile_center)
        print(not_emotion_smile_center)"""


        if(isSmilling() and not isAngry() and not isSad()):
            print("SMILLING :)")
        elif(not isSmilling() and not isAngry() and isSad()):
            print("SAD :(")
        elif(not isSmilling() and isAngry() and not isSad()):
            print("ANGRY >:(")
        else:
            print("NOT EMOTION")




        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            #print(x,y)#print the x and y of point 0
            #draw the point : image, point, radius, color, thickness(-1 -> fill the circle)
            cv2.circle(frame, (x,y), 3, (0,0,255), -1)


    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
