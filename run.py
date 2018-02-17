import Entities
from datetime import datetime, timedelta
import time

d1 = datetime.now()
time.sleep(5)
d2 = datetime.now()
time_dif = (d2-d1)/timedelta(minutes=1)
print(time_dif)