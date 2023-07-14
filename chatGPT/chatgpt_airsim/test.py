import configparser
import os
from tiny_yolo import detect
from PIL import Image
# config = configparser.ConfigParser()
# config.read('chatgpt_airsim/settings.ini')
#
# images = config['images']['imageSaveFolder']
#
# print(images)

image = Image.open("images/test.jpg")


boxCoords, _ = detect(image)[0]
xCenter = int((boxCoords[0] + boxCoords[2])/2)
yCenter = int((boxCoords[1] + boxCoords[3])/2)


print(boxCoords)