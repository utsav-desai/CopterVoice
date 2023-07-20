from djitellopy import Tello
import math
import numpy as np
import os
import io
import time
from PIL import Image
import cv2
import threading
import logging

stopThreads = False
Tello.LOGGER.setLevel(logging.ERROR)
class TelloWrapper:
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.tello.streamoff()
        self.tello.streamon()
     #   self.keepAliveThread = threading.Thread(target=self.keepalive,args=(self.tello,))

    def takeoff(self):
        self.tello.takeoff()
        self.tello.rotate_clockwise(0)
 #       global stopThreads 
 #       stopThreads = False
 #       self.keepAliveThread.start()
 #       
 #
 #   def keepalive(self, tello):
 #       global stopThreads
 #       while True:
 #           time.sleep(10)
 #           tello.rotate_clockwise(c0)
 #           if stopThreads:
 #               break
 

    def land(self):
        global stopThreads 
        stopThreads = True
        self.keepAliveThread.join()
        print('Keep Alive Stop')
        self.tello.land()

    def move(self, direction, distance):
        '''
            direction: 'forward', 'back', 'right', 'left', 'up', 'down' to specify in which direction to move...
            distance: distance to move in centimeters
        '''
        distance = int(distance)
        distance = max(20, distance)
        if direction == 'up':
            self.tello.move_up(distance)
        elif direction == 'down':
            self.tello.move_down(distance)
        elif direction == 'forward':
            self.tello.move_forward(distance)
        elif direction == 'back':
            self.tello.move_back(distance)
        elif direction == 'right':
            self.tello.move_right(distance)
        elif direction == 'left':
            self.tello.move_left(distance)

    def rotate(self, direction, angle):
        '''
            direction: 'clockwise', 'counter_clockwise' specify the direction to rotate
            angle: amount to rotate in given direction in degrees
        '''
        if angle == 0:
            print("Hovering")
        if direction == 'clockwise':
            self.tello.rotate_clockwise(angle)
        elif direction == 'counter_clockwise':
            self.tello.rotate_counter_clockwise(angle)

    def saveImage(self, filename):
        if not os.path.exists("images"):
        # If it doesn't exist, create it
            os.makedirs("images")
        self.tello.streamoff()
        self.tello.streamon()
        frame_read = self.tello.get_frame_read()
        image = cv2.cvtColor(frame_read.frame,cv2.COLOR_BGR2RGB)
        cv2.imwrite('images' + os.sep + filename + '.jpg',image)
        print('Saved image: ', 'images' + os.sep + filename + '.jpg')
    
    def get_frame(self):
        frame_read = self.tello.get_frame_read()
        while frame_read.frame.shape !=(720,960,3):
            frame_read = self.tello.get_frame_read()
       #cv2.imshow('output', frame_read.frame)
       #cv2.waitKey(0)
       #cv2.destroyAllWindows()
        return Image.fromarray(frame_read.frame)
        
    def streamReset(self):
        self.tello.streamoff()
        self.tello.streamon()
    
    def get_yaw(self) -> int:
        """Get yaw in degree
        Returns:
            int: yaw in degree
        """
        return self.tello.get_state_field('yaw')
    
    def get_height(self) -> int:
        """Get current height in cm
        Returns:
            int: height in cm
        """
        return self.tello.get_state_field('h')
    
    def get_battery(self) -> int:
        """Get current battery percentage
        Returns:
            int: 0-100
        """
        return self.tello.get_state_field('bat')
    
    def send_keepalive(self):
        """Send a keepalive packet to prevent the drone from landing after 15s
        """
        self.tello.send_control_command("keepalive")

    def turn_motor_on(self):
        """Turn on motors without flying (mainly for cooling)
        """
        self.tello.send_control_command("motoron")

    def turn_motor_off(self):
        """Turns off the motor cooling mode
        """
        self.tello.send_control_command("motoroff")


if __name__ == '__main__':
    aw = TelloWrapper()
    aw.saveImage("si")
    
    
    