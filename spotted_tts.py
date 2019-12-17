import subprocess

def sayWord(whattosay):
	subprocess.run(['espeak',whattosay])
