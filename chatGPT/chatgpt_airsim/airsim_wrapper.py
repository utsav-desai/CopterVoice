import airsim
import math
import numpy as np
import os
import io
from PIL import Image
import cv2
from FRCNN.FasterRCNN import *
import tensorflow as tf

objects_dict = {
    "mustang 1": "Dodge_SRT_Hellcat_Dodge_Challenger_Hellcat_SRT",
    "mustang 2": "Dodge_SRT_Hellcat_Dodge_Challenger_Hellcat_SRT2",
    "benz": "FbxScene_uploads_files_2787791_Mercedes+Benz+GLS+580"
}


class AirSimWrapper:
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)

    def takeoff(self):
        self.client.takeoffAsync().join()

    def land(self):
        self.client.landAsync().join()

    def get_drone_position(self):
        pose = self.client.simGetVehiclePose()
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val]

    def fly_to(self, point, speed = 2):
        if point[2] > 0:
            self.client.moveToPositionAsync(point[0], point[1], -point[2], speed).join()
        else:
            self.client.moveToPositionAsync(point[0], point[1], point[2], speed).join()

    def fly_path(self, points):
        airsim_points = []
        for point in points:
            if point[2] > 0:
                airsim_points.append(airsim.Vector3r(point[0], point[1], -point[2]))
            else:
                airsim_points.append(airsim.Vector3r(point[0], point[1], point[2]))
        self.client.moveOnPathAsync(airsim_points, 5, 120, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0), 20, 1).join()

    def set_yaw(self, yaw, yawRate = 3):
        self.client.rotateToYawAsync(yaw, yawRate).join()

    def get_yaw(self):
        orientation_quat = self.client.simGetVehiclePose().orientation
        yaw = airsim.to_eularian_angles(orientation_quat)[2]
        return yaw

    def get_position(self, object_name):
        query_string = objects_dict[object_name] + ".*"
        object_names_ue = []
        while len(object_names_ue) == 0:
            object_names_ue = self.client.simListSceneObjects(query_string)
        pose = self.client.simGetObjectPose(object_names_ue[0])
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val]
    
    def saveImage(self, filename):
        if not os.path.exists("'C:/Users/E080329/utsavtemp/PromptCraft-Robotics-main/chatgpt_airsim/images"):
        # If it doesn't exist, create it
            os.makedir("'C:/Users/E080329/utsavtemp/PromptCraft-Robotics-main/chatgpt_airsim/images")
        responses = self.client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
        response = responses[0]
        # get numpy array
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) 
        # reshape array to 4 channel image array H X W X 4
        img_rgb = img1d.reshape(response.height, response.width, 3)
        # original image is fliped vertically
        # img_rgb = np.flipud(img_rgb)
        # write to png 
        airsim.write_png(os.path.normpath('C:/Users/E080329/utsavtemp/PromptCraft-Robotics-main/chatgpt_airsim/images' + os.sep + filename + '.png'), img_rgb) 
    
    def carPose(self, img_path):
        model = tf.keras.models.load_model('car')

        img = tf.keras.utils.load_img(os.path.normpath('C:/Users/E080329/utsavtemp/PromptCraft-Robotics-main/chatgpt_airsim/images' + os.sep + img_path), target_size = (2510, 125))
        x = tf.keras.utils.img_to_array(img)
        x /= 255
        x = np.expand_dims(x, axis = 0)
        images = np.vstack([x])
        classes = model.predict(images, batch_size=10)
        print(np.argmax(classes[0]))
        print(classes[0])

        if np.argmax(classes[0]) == 0:
            return 'Back'
        elif np.argmax(classes[0]) == 1:
            return 'Front'
        elif np.argmax(classes[0]) == 2:
            return 'Side Left'
        elif np.argmax(classes[0]) == 3:
            return 'Side Right'


if __name__ == '__main__':
    aw = AirSimWrapper()
    print(aw.find_car_color())