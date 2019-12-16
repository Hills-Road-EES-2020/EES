######## Webcam Object Detection Using Tensorflow-trained Classifier #########
#
# Author: FJI
# Date: 16/12/19
# Description: 
# This program uses a TensorFlow Lite object detection model to perform object 
# detection on an image or a folder full of images. It draws boxes and scores 
# around the objects of interest in each image.
#
# This code is based off the TensorFlow Lite image classification example at:
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py
#
# I added my own method of drawing boxes and labels using OpenCV.

# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util

from picamera import PiCamera
from time import sleep

class SpottedTF( ):
	def __init__(self, lables_path, model_path):
		# Load tensorflow
		pkg = importlib.util.find_spec('tensorflow')
		if pkg is None:
			from tflite_runtime.interpreter import Interpreter
		else:
			from tensorflow.lite.python.interpreter import Interpreter
		
		# Load the label map
		with open(lables_path, 'r') as f:
			self.labels = [line.strip() for line in f.readlines()]
		# Clean invalid values
		if self.labels[0] == '???':
			del(self.labels[0])
		
		# Load the Tensorflow Lite model.
		self.interpreter = Interpreter(model_path=model_path)

		self.interpreter.allocate_tensors()

		# Get model details
		self.input_details = self.interpreter.get_input_details()
		self.output_details = self.interpreter.get_output_details()
		self.height = self.input_details[0]['shape'][1]
		self.width = self.input_details[0]['shape'][2]

		self.floating_model = (self.input_details[0]['dtype'] == np.float32)

		input_mean = 127.5
		input_std = 127.5
		
		# Config camera
		self.camera = PiCamera()
		self.camera.resolution = (720, 720)
	
	def detect(self):
		# Take picture & save
		self.camera.start_preview()
		sleep(5)
		image_path = 'Capture/image.jpg'
		self.camera.capture(image_path)
		self.camera.stop_preview()
		
		# Run detection on the picture
		# Load image and resize to expected shape [1xHxWx3]
		image = cv2.imread(image_path)
		image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		imH, imW, _ = image.shape 
		image_resized = cv2.resize(image_rgb, (self.width, self.height))
		self.input_data = np.expand_dims(image_resized, axis=0)
		
		# Normalize pixel values if using a floating model (i.e. if model is non-quantized)
		if self.floating_model:
			input_data = (np.float32(input_data) - input_mean) / input_std

		# Perform the actual detection by running the model with the image as input
		self.interpreter.set_tensor(self.input_details[0]['index'],self.input_data)
		self.interpreter.invoke()

		# Retrieve detection results
		classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0] # Class index of detected objects
		scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0] # Confidence of detected objects
		#num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)



		# Pick the most probable result
		##for nth in range(0,len(classes)):
			##class_ = self.labels[int(classes[nth])]
			##score_ = scores[nth]
			##print("Class: " + class_ + " Score: " + str(score_))
			##print("   ")
		##print("Class: " + self.labels[int(classes[0])])
			
			
			
		# Return detected value (string)
		return self.labels[int(classes[0])]


def main():
	tf = SpottedTF("Sample_TFLite_model/labelmap.txt", "Sample_TFLite_model/detect.tflite")
	
	result = tf.detect()
	
	print(result)

# Main tester
main()
