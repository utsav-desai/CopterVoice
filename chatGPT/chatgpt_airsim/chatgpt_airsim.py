import re
import argparse
from tkinter.messagebox import QUESTION
from telloWrapper import *
from chatgpt import *
from boxCentering import *
from streamlit_combo_api_call import api_call
from tiny_yolo import *
import math
import numpy as np
import os
import json
import time
import configparser

#config = configparser.ConfigParser()
#config.read('./chatgpt_airsim/settings.ini')
#
#prompt = config['chatgpt']['prompt']
#sysprompt = config['chatgpt']['sysprompt']

prompt = "prompts/airsim_basic.txt"
sysprompt = "system_prompts/airsim_basic.txt"



# with open(args.sysprompt, "r") as f:
#     sysprompt = f.read()


code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)


def extract_python_code(content):
    code_blocks = code_block_regex.findall(content)
    if code_blocks:
        full_code = "\n".join(code_blocks)

        if full_code.startswith("python"):
            full_code = full_code[7:]

        return full_code
    else:
        return None

def simpleCommands(question):
    if question == 'takeoff':
        aw.takeoff()
        return True
    elif question == 'land':
        aw.land()
        return True
    return False





def main():

    print(f"Initializing AirSim...")
    aw = TelloWrapper()

    getAns(prompt)

    script = '''
        You are to help me simulating a drone in AirSim simulator. You can refer the AirSim documentation for any help.
        You are only allowed to use the functions which are provided in the documentation, and are not allowed to assume any functions by your own.
        If I ask you to do any task which needs a function which is not listed in the documentation and i have also not provided you the information on that function, you can ask me for clarity in the following format:
        
        'Function Clarification: Please specify the function which is to be used for the task:' and now add which ever task is confusing to you.
        You are supossed to remember all the previous conversion till the session ends, and should be able to communicate continuously without repeating informations again and again in every prompt.
        If you are clear about all the things listed above, confirm by printing:'I do understand your requirements.' No need to give takeoff commands everytime.

        Before checking the documentation, your first priority is to check if the below listed functions can accomplish the required task, if so use this functions:
        aw.takeoff(self): use to takeoff the drone
        aw.land(self): use to land the drone
        aw.get_drone_position(self): gives the (x, y, z) coordinates of the drone
        aw.fly_to(self, point, speed):moves the drone to given point(x, y, z) at given speed
        aw.fly_path(self, points): move along the path formed by points
        aw.set_yaw(yaw, yawRate): set the yaw to given value at given yaw rate
        aw.get_yaw(self): returns the yaw value
        aw.saveImage(self, filename): used to save what the drone is currently looking at with a given name-filename, Important:you should not provide the extension here
        align(): used to go close to the car after it's detection. No parameters should be given.
        detect(image_path): a car detection model, used to detect any car in the image. Input: image_path-path of the image in which the car is to be detected. Output: carBox - a list of tuples of the form (bounding_box, car_color), consisting of every car detected in the current frame. If no cars are found, an empty list is returned.
        api_call(image_path): used to get tyre dimensions. Input: image_path - name of the image for which tyre dimensions are to be found. Output: tyre_dimensions

        All the images have .png extension

        If the required function is not in the above list, refer documentation, but don't assume new functions by yourself.

        If the task cannot be completed by any of the functions above and any of the functions from the documentation, then you are supossed to tell me to do necessary steps to resolve the issue(like to add a new function to my code).

        Format of the required output:
        Paragraph 1: Details of the task(maximum 2 lines)
        Paragraph 2: Output a code command that achieves the desired goal.  (Take care to not to output more than one python code block)
        Paragraph 3: Reason explaining why the above code is correct( in no more than 3 lines)

        Whenever a task is given to you, you are supossed to stick to just do that task and not to make any other movements; i.e. you are not supossed ot make any assumptions.
        Although you are free to assume the speed values if not given specifically.

    '''

    getAns(script)




    colors = {'RED' : "\033[31m",
            'ENDC' : "\033[m",
            'GREEN' : "\033[32m",
            'YELLOW' : "\033[33m",
            'BLUE' : "\033[34m"} 
    while True:
        question = input(colors['GREEN'] + "AirSim> " + colors['ENDC'])

        if question == "quit" or question == "exit":
            break

        if question == "clear":
            os.system("cls")
            continue
        isSimple = simpleCommands(question)
        
        if isSimple:
            isSimple = False
            continue

        response = getAns(question)
        print(f"\n{response}\n")
        code = extract_python_code(response)
        if code is not None:
            print("Please wait while I run the code in AirSim...")
            try:
                exec(extract_python_code(response))
            except Exception as e:
                print(e)
            # print(code)
            # exec(code)
            print("Done!\n")
    
if __name__ == '__main__':
    main()