from airsim_wrapper import *
from boxCentering import align

aw = AirSimWrapper()

aw.takeoff()
i = 0
while(1):
    i += 1
    aw.saveImage('car' + str(i))
    print('-----'*3)
    print('Next loop...')
    current_position = aw.get_drone_position()
    target_position = [current_position[0], current_position[1] + 15, current_position[2]]
    aw.fly_to(target_position, speed=2)
    try:
        print('Try 1...')
        align(0)
    except:
        try:
            print('Try 2...')
            current_position = aw.get_drone_position()
            target_position = [current_position[0] - 2, current_position[1] + 3, current_position[2]]
            aw.fly_to(target_position, speed=2)
            align(0)
        except:
            try:
                print('Try 3...')
                current_position = aw.get_drone_position()
                target_position = [current_position[0], current_position[1] + 3, current_position[2]]
                aw.fly_to(target_position, speed=2)
                align(0)
            except:
                print('No car found in the frame')
                break
