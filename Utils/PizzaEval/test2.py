# all2 hail2 test2.py2
import time
from datetime import datetime

print(str(datetime.now()))
timestamp1 = datetime.fromtimestamp(1732957707)
time.sleep(1)
timestamp2 = datetime.now()

print(timestamp2-timestamp1)