import os
import numpy as np
import pandas as pd
import torch
import torchvision
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import time

model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights='DEFAULT', progress = True, num_classes = 91, weights_backbone = 'DEFAULT')

def detect(img):

    # img_path = r'C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\images' + os.sep + img_path
    # img = Image.open(img_path)

    model.eval()

    np_img = np.array(img.convert("RGB"))

    transformed_img = torchvision.transforms.transforms.ToTensor()(torchvision.transforms.ToPILImage()(np_img))

    start = time.time()
    result = model([transformed_img])
    # print('Time taken:', time.time() - start)

    # print(result)

    COCO_INSTANCE_CATEGORY_NAMES = [
        '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
        'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
        'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
        'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
        'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
        'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
        'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
        'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
        'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
        'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

    car_id = 3
    car_boxes = [x.detach().numpy().tolist() for i, x in enumerate(result[0]['boxes']) if result[0]['labels'][i] == car_id]
    # print(car_boxes)


    try:
        x1, y1, x2, y2 = map(int, car_boxes[0])
    except:
        return []

    # sample_image_annotated = img.copy()
    # img_bbox = ImageDraw.Draw(sample_image_annotated)
    # img_bbox.rectangle([x1, y1, x2, y2], outline="red")
    # # sample_image_annotated.show()
    # sample_image_annotated.save('output.png', 'PNG')

    return [([x1, y1, x2, y2], 'None')]


if __name__ == '__main__':
    img_path = '/Users/utsavmdesai/Documents/Utsav/chatgpt_airsim/images/test-10.jpg'
    print(detect(img_path))
    