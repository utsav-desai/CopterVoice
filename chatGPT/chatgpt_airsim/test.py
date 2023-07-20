import threading
import time

def test():
    while True:
        print("Inside Test")
        time.sleep(2)
        
t1 = threading.Thread(target=test)
print("1")
print("2")
print("3")
print("4")
t1.start()
print("5")
time.sleep(2)
print(2)
print(2)