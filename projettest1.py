import sys
import os
import dlib
import glob

if len(sys.argv) != 4:
	print( len(sys.argv))
	exit()

predictor_path = sys.argv[1]
face_rec_model_path = sys.argv[2]
faces_folder_path = sys.argv[3]

print("1 " + predictor_path)
print("2 " + face_rec_model_path)
print("3 " + faces_folder_path)
