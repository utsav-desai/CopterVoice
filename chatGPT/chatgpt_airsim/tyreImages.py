from airsim_wrapper import *
import sys
sys.path.append(r'C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\GroundingDINO')
from GroundingDINO.inference_on_a_image import *
import cv2
import numpy as np

aw = AirSimWrapper()

def tyreAlign():
    print('-----' * 20)
    print('Running model.....')
    print('-----' * 20)

    aw.saveImage('tyreMain')

    boxes, labels = DINO(r'C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\images\tyreMain.png', 'car.tyre.')
    boxes = boxes.numpy()
    tyreBox = []
    for i in range(len(labels)):
        if labels[i].split('(')[0] == 'tyre':
            tyreBox.append(boxes[i])

    sorted(tyreBox,key=lambda x: x[0])

    start_position = aw.get_drone_position()
    for i, tyre in enumerate(tyreBox):
        centerX = int((tyre[0] * 256 + tyre[0] * 256 + tyre[2] * 256) / 2)
        centerY = int((tyre[1] * 144 + tyre[1] * 144 + tyre[3] * 144) / 2)

        xError = centerX - 128
        yError = centerY - 72

        distanceX = 0.01 * xError
        distanceY = 0.05 * yError

        print(distanceX, distanceY)

        current_position = aw.get_drone_position()
        target_position = [current_position[0] + distanceY, current_position[1] - distanceX, current_position[2] + 2]
        # print('Moving from', current_position, 'to', target_position)
        aw.fly_to(target_position, speed=1)
        aw.saveImage('cartyre' + str(i))
        aw.fly_to(start_position, speed=1)


    print('-----' * 20)
    print('Done.....')
    print('-----' * 20)


if __name__ == '__main__':
    aw.takeoff()
    current_position = aw.get_drone_position()
    target_position = [current_position[0] - 5, current_position[1] + 60, current_position[2]]
    aw.fly_to(target_position, speed=5)
    # tyreAlign()
    start_position = aw.get_drone_position()
    target_position = [start_position[0] + 3, start_position[1] - 2, start_position[2] + 1]
    aw.fly_to(target_position, speed=1)

    aw.fly_to(start_position, speed=1)

    start_position = aw.get_drone_position()
    target_position = [start_position[0] + 3, start_position[1] + 4, start_position[2] + 1]
    aw.fly_to(target_position, speed=1)