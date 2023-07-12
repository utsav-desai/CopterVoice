from djitellopy import Tello
import time
import logging

Tello.LOGGER.setLevel(logging.DEBUG)

tello = Tello()


tello.connect()

time.sleep(3)

print('-----' * 20)
print('Taking off...')
print('-----' * 20)

tello.takeoff()

time.sleep(3)

print('Going left...')
print('-----' * 20)

tello.move_left(100)
time.sleep(3)

print('Landing...')
print('-----' * 20)

tello.land()
time.sleep(3)

print('All done')
print('-----' * 20)