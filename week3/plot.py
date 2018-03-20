import powerlaw
import vis
import numpy
import sys

with open('temp.txt') as f:
	data = map(int, f.read().split(','))

# calculate exponent
results = powerlaw.Fit(data)
print(results.power_law.alpha)
print(results.power_law.xmin)

vis.plplot(numpy.array(data), results.power_law.xmin, results.power_law.alpha)

