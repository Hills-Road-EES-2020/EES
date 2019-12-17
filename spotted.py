from spotted_tf import SpottedTF
from spotted_tts import sayWord


# Test code (not to be used in the final version)
def main():
	tf = SpottedTF("Train/labels.txt", "Train/converted_model_quantized.tflite")
	
	result = tf.detect()
	sayWord(result)
	print(result)

# Main tester
main()
