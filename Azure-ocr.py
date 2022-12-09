import requests
import sys

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

if __name__ == "__main__":
    ocr_text("F:\IMP DOCUMENT\projects\OCR APP\IMG_06441.jpg")

