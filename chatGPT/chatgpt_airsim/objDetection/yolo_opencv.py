#############################################
# Object detection - YOLO - OpenCV
# Author : Arun Ponnusamy   (July 16, 2018)
# Website : http://www.arunponnusamy.com
############################################

import os
import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image',
                help = 'path to input image', default=r'C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\objDetection\tempCar1.jpg')
ap.add_argument('-c', '--config',
                help = 'path to yolo config file', default=r'C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\objDetection\yolov3.cfg')
ap.add_argument('-w', '--weights',
                help = 'path to yolo pre-trained weights', default=r'C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\objDetection\yolov3.weights')
ap.add_argument('-cl', '--classes',
                help = 'path to text file containing class names', default=r'C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\objDetection\yolov3.txt')
args = ap.parse_args()


def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

classes = None
with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# image = cv2.imread(args.image)
def carBBox(image):
    '''carBBox(image_path): a car detection model to detect any cars in the image whose path is image_path. 
        Input: Just the name of the image with extension
        Output: This function returns a tuple (image, BBox): image-original input image with bounding boxes added,
                                                     BBox-array of sub arrays; i_th sub array is of the form:[x1, y1, x2, y2], where (x1, y1) and (x2, y2) are the two diagonally opposite corners of the i_th object
    '''
    img_name = image[:-4]
    image = cv2.imread(r'C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\images' + os.sep + image)

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    

    with open(args.classes, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    

    net = cv2.dnn.readNet(args.weights, args.config)

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4


    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])


    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    BBox = []

    for i in indices:
        try:
            box = boxes[i]
        except:
            i = i[0]
            box = boxes[i]
        
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        # draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
        BBox.append([round(x), round(y), round(x + w), round(y + h)])

    # cv2.imshow("object detection", image)
    # cv2.waitKey(0)
        
    cv2.imwrite(r"C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\detectionOutputs"+ os.sep + img_name +".png", image)
    cv2.destroyAllWindows()
    # print('Detected', str(len(BBox)) + ' objects...', BBox)

    return(image, BBox)

if __name__ == '__main__':
    carBBox(r'C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\images\current_image.png')
