from spotted_tf import SpottedTF


# Test code (not to be used in the final version)
def main():
	tf = SpottedTF("Sample_TFLite_model/labelmap.txt", "Sample_TFLite_model/detect.tflite")
	
	result = tf.detect()
	
	print(result)

# Main tester
main()
