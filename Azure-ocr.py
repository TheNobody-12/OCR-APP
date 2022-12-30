"""
Name of author: Sarthak Kapaliya
Date: 30/12/2022 
Desc:   This is template for connecting 
        to Azure OCR API and getting the text
        from the image.
"""
import requests
# add your subscription key and endpoint url here 
subscription_key = 00000
vision_base_url = "Endpoint URL"
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

# Driver code
if __name__ == "__main__":
    ocr_text("img.jpg")

