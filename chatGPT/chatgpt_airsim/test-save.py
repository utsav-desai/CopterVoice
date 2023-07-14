import cv2
from djitellopy import Tello

tello = Tello()
tello.connect()

tello.streamoff()
tello.streamon()
frame_read = tello.get_frame_read()
print(tello.get_battery())
# tello.takeoff()

while True:
    img = frame_read.frame
    print(cv2.imwrite(r"picture.jpg", img))
    cv2.imshow("drone", img)

    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
#         tello.land()
        frame_read.stop()
        tello.streamoff()
        cv2.destroyAllWindows()
        
        break
# tello.land()

tello.streamoff()