from transformers import YolosImageProcessor, YolosForObjectDetection, logging
from PIL import Image, ImageDraw
import torch
import time
import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
import cv2
from webcolors import rgb_to_name
from scipy.spatial import KDTree
from webcolors import (hex_to_rgb)
# logging.set_verbosity_error()

warnings.filterwarnings('ignore')
os.environ['CURL_CA_BUNDLE'] = ''

def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1,a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]

def convert_rgb_to_names(rgb_tuple):
    
    # a dictionary of all the hex and their respective names in css3
    css3_db = {'#000000': 'black','#0000ff': 'blue', '#008000': 'green', '#ff0000': 'red', '#ffffff': 'white', '#ffff00': 'yellow'}
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

def detect(image):
    #img_path = image
    #image = Image.open(img_path)

    model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')

    image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

    inputs = image_processor(images=image, return_tensors="pt")
    # start = time.time()
    outputs = model(**inputs)
    # end = time.time()
    # print(end - start)

    # model predicts bounding boxes and corresponding COCO classes
    logits = outputs.logits
    bboxes = outputs.pred_boxes

    carBox = []
    # print results
    target_sizes = torch.tensor([image.size[::-1]])
    results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        # print(
        #     f"Detected {model.config.id2label[label.item()]} with confidence "
        #     f"{round(score.item(), 3)} at location {box}"
        # )
        # output = ImageDraw.Draw(image)
        # output.rectangle(box)
        # image.show()
        if model.config.id2label[label.item()] == 'car':
            img = np.asarray(image)
            percentage = 40
            xCenter = int((box[1] + box[3])/2)
            yCenter = int((box[0] + box[2])/2)
            x1 = int(xCenter - (percentage / 100) * (box[3] - box[1]))
            x2 = int(xCenter + (percentage / 100) * (box[3] - box[1]))
            y1 = int(yCenter - (percentage / 100) * (box[2] - box[0]))
            y2 = int(yCenter + (percentage / 100) * (box[2] - box[0]))
            img = img[x1:x2, y1:y2]
            # print(x1, x2, y1, y2)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
            r, g, b = unique_count_app(np.average(img, axis = (0,1)))[::-1]
            color = convert_rgb_to_names((r, g, b))

            # print((r, g, b))
            # cv2.imshow('output', img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            carBox.append((box, color))
    print('Car list', carBox)
    if carBox:
        return carBox
    else:
        return []

if __name__ == '__main__':
    print(detect('images/centering.png'))