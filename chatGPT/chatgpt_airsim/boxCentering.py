from telloWrapper import *
from tiny_yolo import *
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

aw = TelloWrapper()
aw.saveImage('centering')


def horizAlign(thresh, car_id):
    p = 0.06 #proportional constant
    d = -0.01 #differential constant
    direction = 1
    i = 0

    last_xError = 0


    while True:
        # input('Press Enter to move to move forward...')
        aw.saveImage('centering')
        # boxCoords = carBBox('centering.png')[1][0]  # assumption: just one car present in the frame
        boxCoords, _ = detect('centering.png')[car_id]
        xCenter = int((boxCoords[0] + boxCoords[2])/2)
        yCenter = int((boxCoords[1] + boxCoords[3])/2)

        xError = xCenter - 128  #current offset of bounding box from center
        yError = yCenter - 40  #current offset of bounding box from center
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
        

        if abs(xError) < thresh:
            print('X movement too low')
            distanceX = 0
        if abs(yError) < thresh + 35:
            print('Y movement too low')
            distanceY = 0
        print('To move:', distanceX, distanceY)
        current_position = aw.get_drone_position()
        target_position = [current_position[0], current_position[1] - distanceX, current_position[2] + distanceY]
        # print('Moving from', current_position, 'to', target_position)
        aw.fly_to(target_position, speed=1)


        last_xError = xError
        i += 1



def align(car_id):
    thresh = 20 #threshold limit on how accurate box needs centering(in pixels)
    targetPercentage = 80
    while True:
        horizAlign(thresh, car_id)

        last_coverage = 0
        closingDirection = 1
        closingp = 0.1
        
        while True:
            aw.saveImage('centering1')
            # boxCoords = carBBox('centering1.png')[1][0]  # assumption: just one car present in the frame
            boxCoords, _ = detect('centering.png')[car_id]
            yRange = abs(boxCoords[0] - boxCoords[2])
            coverage = (yRange / 256)*100
            print('Current coverage: ', coverage, '%')
            if coverage >= targetPercentage - 10:
                print('Completed Closing...')
                break
            if coverage < last_coverage:
                closingDirection = -1


            yError = coverage - targetPercentage
            distance = closingDirection*closingp*yError

            current_position = aw.get_drone_position()
            target_position = [current_position[0] - distance, current_position[1], current_position[2]]
            # print('Moving from', current_position, 'to', target_position)
            aw.fly_to(target_position, speed=1)
            horizAlign(thresh, car_id)

            last_coverage = coverage
        
        # boxCoords = carBBox('centering1.png')[1][0]  # assumption: just one car present in the frame
        boxCoords, _ = detect('centering.png')[car_id]
        xCenter = int((boxCoords[0] + boxCoords[2])/2)
        xError = xCenter - 128  #current offset of bounding box from center
        yCenter = int((boxCoords[1] + boxCoords[3])/2)
        yError = yCenter - 40  #current offset of bounding box from center
        yRange = abs(boxCoords[0] - boxCoords[2])
        coverage = (yRange / 256)*100
        targetPercentage  = min(targetPercentage + 5, 80)
        if abs(xError) < thresh and abs(yError) < thresh + 35 and coverage >= targetPercentage - 10:
            print('All set!!!')
            aw.saveImage('final')
            break

if __name__ == '__main__':
    aw.takeoff()
    # aw.set_yaw(30, 5)
    current_position = aw.get_drone_position()
    target_position = [current_position[0] + 2, current_position[1] + 10, current_position[2]]
    aw.fly_to(target_position, speed=2)
    align(0)