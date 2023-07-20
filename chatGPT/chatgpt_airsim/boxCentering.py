from telloWrapper import *
from djitellopy import Tello
# from tiny_yolo import *
from PIL import Image
import numpy as np
import logging
from FasterRCNN import detect


Tello.LOGGER.setLevel(logging.ERROR)
# import keyboard
# from yolonas import *

#todo: sort car list by x coordinate

'''
first save image by calling saveImage function;
get bounding box coordinates from carBBox function;
define penalty based on the center distance(similar to a pid controller)
move the drone left/right based on the BBox center
run a while loop on this until center is within a certain threshold
image size: 256x144
'''

def displayOutput(frame,bbox):
    print('Display')
    image = np.array(frame)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if len(bbox) != 0:
        # bbox , _= bbox[0]
        start_point = (int(bbox[0]),int(bbox[1]))
        end_point = (int(bbox[2]),int(bbox[3]))

        image = cv2.rectangle(image,start_point,end_point,(0,255,0),2)
    cv2.imwrite('out' + str(time.time()) + '.jpg', image)
    cv2.startWindowThread()
    cv2.namedWindow("BB", cv2.WINDOW_NORMAL)
    cv2.imshow("BB",image)
    cv2.waitKey(1)
    

def horizAlign(aw, thresh, car_id):
    p = 0.15 #proportional constant
    d = -0.01 #differential constant
    direction = 1
    i = 0

    last_xError = 0

    count=0
    display = True
    while True:  
        # input('Press Enter to move to move forward...')
        # aw.saveImage('centering')
        aw.streamReset()
        frame = aw.get_frame()
        #image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB())
    
        
        count+=1
        print("------------------------------------")
        # aw.saveImage("test-"+str(count))
        boxCoords = detect(frame)
        # if display == True:
        #     displayOutput(frame,boxCoords)
        print(len(boxCoords),"----")
        if len(boxCoords)==0:
            # aw.move("forward", 20)
            continue
        boxCoords, _ = boxCoords[car_id]
        # displayOutput(frame,boxCoords)
        xCenter = int((boxCoords[0] + boxCoords[2])/2)
        yCenter = int((boxCoords[1] + boxCoords[3])/2)

        xError = xCenter - 480  #current offset of bounding box from center
        yError = yCenter - 360  #current offset of bounding box from center
        # print(abs(last_xError), abs(xError))
        if i >= 1:
            if abs(last_xError) < abs(xError):
                print('Changing direction...')
                direction = -1 * direction
        distanceX = direction*p*xError
        distanceY = p*yError

        
        

        print('Current horizontal error: ', xError)
        print('Current vertical error: ', yError)
        if abs(xError) <= thresh and abs(yError) <= thresh + 35: #reached reasonable close to center
            print('Completed centering...')
            break
        

        if abs(distanceX) > 20:
            
            if distanceX<0:
                aw.move('left', -1*distanceX)
            else:
                aw.move("right",distanceX)
            # time.sleep(5)
        if abs(distanceY) > 20:
            
            if distanceY<0:
                aw.move('up', -1*distanceY)
            else:
                aw.move("down",distanceY)
            # time.sleep(5)
        print('To move:', distanceX, distanceY)
        # current_position = aw.get_drone_position()
        # target_position = [current_position[0], current_position[1] - distanceX, current_position[2] + distanceY]
        # # print('Moving from', current_position, 'to', target_position)
        # aw.fly_to(target_position, speed=1)
        #aw.move('right', distanceX)
        #aw.move('down', distanceY)


        last_xError = xError
        i += 1
    aw.saveImage("Aligned")



def align(aw, car_id):
    thresh = 100 #threshold limit on how accurate box needs centering(in pixels)
    targetPercentage = 70
    while True:
        horizAlign(aw, thresh, car_id)
        last_coverage = 0
        closingDirection = 1
        closingp = 1.5
        count = 0
        while True:
            frame = aw.get_frame()
            print("------------------------------------")
            aw.saveImage("test-"+str(count))
            count+=1
            boxCoords= detect(frame)

            if len(boxCoords)==0:
                # aw.move("forward",40)
                continue
            boxCoords, _ = boxCoords[car_id]
            yRange = abs(boxCoords[0] - boxCoords[2])
            coverage = (yRange / 960)*100
            print('Current coverage: ', coverage, '%')
            if coverage >= targetPercentage:
                print('Completed Closing...')
                break
            if coverage < last_coverage:
                closingDirection = -1


            yError = targetPercentage-coverage
            distance = closingDirection*closingp*yError

            # current_position = aw.get_drone_position()
            # target_position = [current_position[0] - distance, current_position[1], current_position[2]]
            # print('Moving from', current_position, 'to', target_position)
            # aw.fly_to(target_position, speed=1)
            
            aw.move('forward', max(20, abs(distance)))
            print('Move forward by', distance, 'cms')
            horizAlign(aw, thresh, car_id)

            last_coverage = coverage
        if coverage >= targetPercentage:
            break
        
        # boxCoords = carBBox('centering1.png')[1][0]  # assumption: just one car present in the frame
        boxCoords= detect(frame)
        if len(boxCoords)==0:
            continue
        
        boxCoords, _ = boxCoords[car_id]
        xCenter = int((boxCoords[0] + boxCoords[2])/2)
        xError = xCenter - 480  #current offset of bounding box from center
        yCenter = int((boxCoords[1] + boxCoords[3])/2)
        yError = yCenter - 360  #current offset of bounding box from center
        yRange = abs(boxCoords[0] - boxCoords[2])
        coverage = (yRange / 256)*100
        # targetPercentage  = min(targetPercentage + 5, 80)
        if abs(xError) < thresh and abs(yError) < thresh -100 and coverage >= targetPercentage:
            # start_point = (boxCoords[0], boxCoords[1])
            # end_point = (boxCoords[2], boxCoords[3])

            # image = cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 2)
            # cv2.imshow('Aligned', image)
            print('All set!!!')
            aw.saveImage('final')
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    aw = TelloWrapper()
    # aw.saveImage("test")
    print('-----' * 10)
    print('Battery Remaining:', aw.get_battery())
    print('-----' * 10)
    aw.takeoff()
    # time.sleep(5)
    # aw.move('up',60)
    # aw.set_yaw(30, 5)
    # current_position = aw.get_drone_position()
    # target_position = [current_position[0] + 2, current_position[1] + 10, current_position[2]]
    # aw.fly_to(target_position, speed=2)
    align(aw,0)