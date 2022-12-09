# import os
# import io
# import json 
# from msrest.authentication import CognitiveServicesCredentials
# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes,OperationStatusCodes
# import requests
# from PIL import Image,ImageDraw,ImageFont
# import time

# # loading Api key and endpoint
# credential = json.load(open('credential.json'))
# API_KEY = credential['API_KEY']
# ENDPOINT = credential['ENDPOINT']

# cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
# # 
# img_url = "https://preview.redd.it/hwbl11e5u33a1.jpg?width=2550&format=pjpg&auto=webp&s=9fd07d8e5334b2e3dd6d2094e3d746dea1c9f2c7"
# local_file  = "./test2.jpg" 
# # reading image
# # response = cv_client.read(url= img_url,language="en",raw=True)
# response = cv_client.read_in_stream(open(local_file,"rb"),language="en",raw=True)
# # get operation location
# operationLocation = response.headers["Operation-Location"]
# # grab the ID from the URL
# operation_id = operationLocation.split("/")[-1]
# time.sleep(5)
# result = cv_client.get_read_result(operation_id)
# # print result\
# print(result)
# print(result.status)
# print(result.analyze_result)

# # get text
# if result.status == OperationStatusCodes.succeeded:
#     for text_result in result.analyze_result.read_results:
#         for line in text_result.lines:
#             print(line.text)
#             print(line.bounding_box)

import requests
import sys
from flask import Flask, render_template, request
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
app = Flask(__name__)

subscription_key = "a5f3e873a4d84af1b5483740dfc4e967"
vision_base_url = "https://ocrweb.cognitiveservices.azure.com/vision/v3.2/"
ocr_url = vision_base_url + "ocr"

def image_to_text(image_file, output_file):
    image_data = open(image_file, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    response = requests.post(ocr_url, headers=headers, data=image_data)
    response.raise_for_status()
    analysis = response.json()

    regions = analysis["regions"]
    lines = [region["lines"] for region in regions][0]
    words = [line["words"] for line in lines]
    lines_words = []
    for line_words in words:
        w = [lw["text"] for lw in line_words]
        lines_words.append(w)

    with open(output_file, "w+",encoding="utf-8") as output:
        for lw in lines_words:
            output.write(' '.join(lw))
            output.write('\n')

def ocr_text(image_file):
    image_to_text(image_file, image_file.replace(".jpg", ".txt"))

# if __name__ == "__main__":
#     ocr_text("F:\IMP DOCUMENT\projects\OCR APP\IMG_06441.jpg")
def OCR_fucntion(img_path):
    """Call the OCR API on a local image
    
    returns: text in the image"""
    ocr_text(img_path)
    with open(img_path, "r") as f:
        data = f.read()
        return data

# routes
@app.route("/")
def main():
	return render_template("home.html")

@app.route("/templates/index", methods=['GET', 'POST'])
def index():
	return render_template("index.html")

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		text = OCR_fucntion(img_path)

	return render_template("index.html", prediction = text, img_path = img_path)

if __name__ =='__main__':
	app.run(debug = True)


