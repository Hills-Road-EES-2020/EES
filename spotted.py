from spotted_tf import SpottedTF
from spotted_tts import sayWord


# Test code (not to be used in the final version)
def main():
	tf = SpottedTF("Sample_TFLite_model/labelmap.txt", "Sample_TFLite_model/detect.tflite")
	
	result = tf.detect()
	sayWord(result)
	print(result)

# Main tester
main()
