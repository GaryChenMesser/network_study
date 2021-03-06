import matplotlib.pyplot as plt
import numpy as np
import sys
import math

def node_edge(node, edge):
	log_node = np.array(map(math.log,map(float,node)))
	log_edge = np.array(map(math.log,map(float,edge)))
	print(log_node)
	print(log_edge)
	fit = np.polyfit(log_node, log_edge, deg=1)
	exp_fit = map(math.exp, fit[0] * log_node + fit[1])
	plt.close()
	plt.loglog(node, edge, 'bo')
	slope, = plt.loglog(node, exp_fit, color = 'red', label = 'slope = ' + str(fit[0]))
	plt.ylabel('edge',fontsize=16)
	plt.xlabel('node',fontsize=16)
	plt.legend(handles=[slope])
	plt.title(sys.argv[1].split('/')[-1].split('.')[0] + '(m=' + sys.argv[3] + ', c=' + sys.argv[4] + ')')
	plt.show()
	plt.savefig(sys.argv[1].split('/')[-1].split('.')[0] + '_' + sys.argv[3] + '_' + sys.argv[4] + '_dense.png')

def diameter(dia, time):
	plt.close()
	plt.plot(time, dia, 'bo')
	plt.ylabel('diameter',fontsize=16)
	plt.xlabel('node',fontsize=16)
	#plt.draw()
	plt.savefig(sys.argv[1].split('/')[-1].split('.')[0] + '_' + sys.argv[3] + '_' + sys.argv[4] + '_shrink.png')

def heat_dense(slope):
	_insert = int(sys.argv[6])
	_max = float(sys.argv[2])
	_min = float(sys.argv[3])
	row_labels = [format(_min + (_max - _min) / _insert / 2 * i, '.2f') for i in range(_insert * 2)]
	_max = float(sys.argv[4])
	_min = float(sys.argv[5])
	column_labels = [format(_min + (_max - _min) / _insert / 2 * i, '.2f') for i in range(_insert * 2)]
	fig, ax = plt.subplots()
	heatmap = ax.pcolor(slope, cmap='hot')

	#legend
	cbar = plt.colorbar(heatmap)
	#plt.imshow(slope, cmap='hot', interpolation='nearest')
	
	ax.set_yticklabels(row_labels, minor=False)
	ax.set_xticklabels(column_labels, minor=False)

	plt.savefig(sys.argv[1].split('/')[-1].split('.')[0] + '_' + sys.argv[2] + '_' + sys.argv[3] + '_heat.png')
	plt.show()

def heat_shrink(slope):
	_insert = int(sys.argv[6])
	_max = float(sys.argv[2])
	_min = float(sys.argv[3])
	row_labels = [format(_min + (_max - _min) / _insert / 2 * i, '.2f') for i in range(_insert * 2)]
	_max = float(sys.argv[4])
	_min = float(sys.argv[5])
	column_labels = [format(_min + (_max - _min) / _insert / 2 * i, '.2f') for i in range(_insert * 2)]
	fig, ax = plt.subplots()
	heatmap = ax.pcolor(slope, cmap='hot')

	#legend
	cbar = plt.colorbar(heatmap)
	#plt.imshow(slope, cmap='hot', interpolation='nearest')
	
	ax.set_yticklabels(row_labels, minor=False)
	ax.set_xticklabels(column_labels, minor=False)

	plt.savefig(sys.argv[1].split('/')[-1].split('.')[0] + '_' + sys.argv[2] + '_' + sys.argv[3] + '_shrink.png')
	plt.show()
