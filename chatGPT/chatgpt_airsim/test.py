import configparser
import os

config = configparser.ConfigParser()
config.read('chatgpt_airsim/settings.ini')

images = config['images']['imageSaveFolder']

print(images)