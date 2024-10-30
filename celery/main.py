from tasks import add
import time

result = add.delay(4,4)

time.sleep(0.2)
print(result.ready())

