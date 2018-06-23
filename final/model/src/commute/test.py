import time
import matplotlib.pyplot as plt
import numpy as np

class hash_random():
  def __init__(self):
    pass
  
  def init(self):
    self.seed = hash(time.time())
    self.temp = self.seed
  
  def output(self):
    if self.temp // 100 == 0:
      self.seed = abs(hash(str(self.seed)))
      self.temp = self.seed
    
    output = self.temp % 100
    self.temp //= 100
    
    return output

random = hash_random()
random.init()

start_time = time.time()
for i in range(10000):
  random.output()
print("elapsed time: {}".format(time.time() - start_time))

start_time = time.time()
for i in range(10000):
  np.random.random()
print("elapsed time: {}".format(time.time() - start_time))

his = [0 for i in range(100)]
for i in range(10000):
  his[random.output()] += 1
  #print("{} th, output = {}\n".format(i, random.output()))

plt.plot(his)
plt.show()
