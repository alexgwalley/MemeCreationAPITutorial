#Author: Alexander Walley
#Description: This program provides the functionality for 
#the memegeneration by utilizing ronreiter-meme-generator
#Start-Date: Jan 10th, 2020
#Last Modified: Jan 10th, 2020

import random
import requests
import sys


generatorURL = "https://ronreiter-meme-generator.p.rapidapi.com/meme"

helpMessage = '''Possible functions:
make: <name> <top-text> <bottom-text> [imagePath]
add-image: <name> <image-path>
get-all-meme-names:'''

def toSpongeBob(text):
	t = list(text)
	for i in range(len(t)):
		t[i] = t[i].upper() if (random.random() > 0.5) else t[i].lower()
	return ''.join(t)

def getMeme(meme, topText, bottomText):

	headers = {
	    'x-rapidapi-host': "ronreiter-meme-generator.p.rapidapi.com",
	    'x-rapidapi-key': "030a4228c6msh9b3f95f5cae7068p13430ajsn796630acaee6"
	}

	random.seed(10)
	
	#TODO: Error-Checking

	topText = toSpongeBob(topText)
	bottomText = toSpongeBob(bottomText)

	querystring = {"font":"Impact","font_size":"50","meme":meme,"top":topText,"bottom":bottomText}

	response = requests.request("GET", generatorURL, headers=headers, params=querystring)

	return response

def saveResponseImage(response, imagePath):
	try:
		with open(imagePath, 'wb') as f:
		        for chunk in response:
		            f.write(chunk)	
		f.close()
		print("Image saved to path: {}".format(imagePath))
		return True
	except OSError:
		print("[Error]: Could not save image to file: {}".format(imagePath))
	except:
		print("[Error]: Error occured while saving image")
	return False

def loadImage(imagePath):
	file = open(imagePath, 'rb')
	contents = file.read()
	file.close()
	return contents

#function to print all current meme names
def getImageNames():
	url = "https://ronreiter-meme-generator.p.rapidapi.com/images"

	headers = {
   		'x-rapidapi-host': "ronreiter-meme-generator.p.rapidapi.com",
   		'x-rapidapi-key': "030a4228c6msh9b3f95f5cae7068p13430ajsn796630acaee6"
    }

	response = requests.request("GET", url, headers=headers)

	return response.text

def parseAddImage(argv):
	url = "https://ronreiter-meme-generator.p.rapidapi.com/images"

	if(len(argv) < 3):
		print("Usage: add-image <image-path> <name>")
		sys.exit()
	if(type(argv[1]) is not str):
		print("[Error]: Image path must be a string")
	if(type(argv[2]) is not str):
		print("[Error]: Image name must be a string")

	imagePath = argv[1]
	name = argv[2]

	headers = {
	    'x-rapidapi-host': "ronreiter-meme-generator.p.rapidapi.com",
	    'x-rapidapi-key': "030a4228c6msh9b3f95f5cae7068p13430ajsn796630acaee6",
	    'content-type': "multipart/form-data"
	}

	imageBytes = loadImage(argv[2])
	#Broken
	payload = {
		image:imageBytes
	}


	response = requests.request("POST", url, data=payload, headers=headers)

	print(response.status_code)


#parse make meme function
def parseMakeMeme(argv):
	imagePath = "response.jpeg"

	if(len(argv) < 5):
		print("Usage: python3 memeGenerator.py make <name> <top-text> <bottom-text>")
		sys.exit()

	if(type(argv[1]) is not str):
		print("[Error]: Name of meme must be a string, not {}".format(type))
		sys.exit()
	if(type(argv[2]) is not str):
		print("[Error]: Top Text of meme must be a string, not {}".format(type))
		sys.exit()
	if(type(argv[3]) is not str):
		print("[Error]: Bottom text of meme must be a string, not {}".format(type))
		sys.exit()
	if(len(argv) > 5):
		if(type(argv[5]) is str):
			imagePath = argv[5]
		else:
			print("[Error]: Image Path not valid")

	response = getMeme(argv[2], argv[3], argv[4])

	#Print the number of requests remaining
	print("Requests remaining: " + response.headers["x-ratelimit-requests-remaining"])

	saveResponseImage(response, imagePath)


def main():
	if(len(sys.argv) < 2):
		print("Usage: python3 memeGenerator.py <function> [function-arguments]")
		print("Use \"python3 memeGenerator.py -help\" to see possible options.")

	if(len(sys.argv) > 1 and sys.argv[1].lower() == "-help"):
		print(helpMessage)
	if(len(sys.argv) > 1 and sys.argv[1].lower() == "make"):
		parseMakeMeme(sys.argv)
	if(len(sys.argv) > 1 and sys.argv[1].lower() == "add-image"):
		parseAddImage(sys.argv)
	if(len(sys.argv) > 1 and sys.argv[1].lower() == "get-all-meme-names"):
		print(getImageNames())

if __name__ == "__main__":
	main()





