import matplotlib.pyplot as plt
import numpy as np

n = 50
x = np.random.randn(n)
y = x * np.random.randn(n)
print(x)
print(y)

fig, ax = plt.subplots()
fit = np.polyfit(x, y, deg=1)
ax.plot(x, fit[0] * x + fit[1], color='red')
ax.scatter(x, y)

fig.show()
fig.savefig('haha.png')
