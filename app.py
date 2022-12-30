"""
Name:   Sarthak Kapaliya
Date:   30/12/2022
Desc:   This is a simple Flask app that uses the Azure Computer Vision API
        to extract text from an image. 
        The app is deployed on App Services
        of Microsoft Azure and can be accessed at https://frt-ocr-lab.azurewebsites.net/"""

# import the necessary packages
import requests
import sys
from flask import Flask, render_template, request
app = Flask(__name__)

# add your subscription key and endpoint url here
subscription_key = "a5f3e873a4d84af1b5483740dfc4e967"
vision_base_url = "https://ocrweb.cognitiveservices.azure.com/vision/v3.2/"
ocr_url = vision_base_url + "ocr"

def image_to_text(image_file, output_file):
    """
    Desc: Call the OCR API on a local image and save the text to a file
    Input: image_file: path to the image file, output_file: path to the output file
    Output: Make a request to the OCR API and save the text to a file from the image.
    """
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
    """
    Desc:   Call the image to text function on a local 
            image and we replce the jpg with txt for the
            output file.
    Input: image_file: path to the image file
    Output: Return the output from Image to text function"""
    image_to_text(image_file, image_file.replace(".jpg", ".txt"))


# Driver code for Azure OCR API
def OCR_fucntion(img_path):
    """Call the OCR API on a local image
    
    returns: text in the image"""
    ocr_text(img_path)
    text_path= img_path.replace(".jpg", ".txt")
    with open(text_path, 'r') as f:
        data = f.read()
        return data

# routes for the app
@app.route("/")
def main():
	return render_template("home.html")

# route for the home page of the app
@app.route("/templates/index", methods=['GET', 'POST'])
def index():
	return render_template("index.html")

# route for the output page of the app
@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
    """  
    Desc:   This function is called when the user uploads an image and
    clicks on the submit button. It calls the OCR function and returns the text in the image.
    Input:  The image file uploaded by the user    
    Output: Returns the text in the image
    """
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/" + img.filename	
        img.save(img_path)
        
        text = OCR_fucntion(img_path)

    return render_template("index.html", prediction = text, img_path = img_path)

# main function
if __name__ =='__main__':
	app.run(debug = True)
