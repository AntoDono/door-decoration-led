import time
import datetime

count = 0
identifier = datetime.datetime.now().second
while True:
    count+=1
    print(identifier)
    time.sleep(1)