import time
import os
import torch
from super_gradients.training import models
import cv2
import numpy as np
from webcolors import rgb_to_name
from scipy.spatial import KDTree
from webcolors import (hex_to_rgb)

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
yolo_nas_s = models.get("yolo_nas_s", pretrained_weights="coco").to(device)

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


def detect(img_path):
    # start = time.time()
    img_path = r'C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\images' + os.sep + img_path
    out = yolo_nas_s.predict(img_path)
    # print('Time:', time.time() - start)
    print(out)
    carBBox = []

    for image_prediction in out:
        image = image_prediction.image
        class_names = image_prediction.class_names
        labels = image_prediction.prediction.labels
        confidence = image_prediction.prediction.confidence
        bboxes = image_prediction.prediction.bboxes_xyxy


        for i, (label, conf, bbox) in enumerate(zip(labels, confidence, bboxes)):
            if label == 2.0:
                # print("prediction: ", i)
                # print("label_id: ", label)
                # print("label_name: ", class_names[int(label)])
                # print("confidence: ", conf)
                # print("bbox: ", bbox)
                # print("--" * 10)

                percentage = 40
                xCenter = int((bbox[1] + bbox[3])/2)
                yCenter = int((bbox[0] + bbox[2])/2)
                x1 = int(xCenter - (percentage / 100) * (bbox[3] - bbox[1]))
                x2 = int(xCenter + (percentage / 100) * (bbox[3] - bbox[1]))
                y1 = int(yCenter - (percentage / 100) * (bbox[2] - bbox[0]))
                y2 = int(yCenter + (percentage / 100) * (bbox[2] - bbox[0]))
                image = image[x1:x2, y1:y2]
                print(x1, x2, y1, y2)
                print(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                r, g, b = unique_count_app(np.average(image, axis = (0,1)))[::-1]
                color = convert_rgb_to_names((r, g, b))
                # print(color)
                carBBox.append((bbox, color))


    out.save("YOLO_NAS Output")
    return carBBox

if __name__ == '__main__':
    print(detect('final.png'))