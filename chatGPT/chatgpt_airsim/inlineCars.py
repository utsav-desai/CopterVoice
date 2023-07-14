from airsim_wrapper import *
from boxCentering import align

aw = TelloWrapper()

carDistance = 20 #average distance between cars in centimeters

aw.takeoff()
i = 0
while(1):
    i += 1
    aw.saveImage('car' + str(i))
    print('-----'*3)
    print('Next loop...')
    # current_position = aw.get_drone_position()
    # target_position = [current_position[0], current_position[1] + 15, current_position[2]]
    # aw.fly_to(target_position, speed=2)
    aw.move('right', carDistance)
    try:
        print('Try 1...')
        align(0)
    except:
        try:
            print('Try 2...')
            # current_position = aw.get_drone_position()
            # target_position = [current_position[0] - 2, current_position[1] + 3, current_position[2]]
            # aw.fly_to(target_position, speed=2)
            aw.move('forward', 20)
            aw.move('right', 30)
            align(0)
        except:
            try:
                print('Try 3...')
                # current_position = aw.get_drone_position()
                # target_position = [current_position[0], current_position[1] + 3, current_position[2]]
                # aw.fly_to(target_position, speed=2)
                aw.move('right', 30)
                align(0)
            except:
                print('No car found in the frame')
                break
