import matplotlib.pyplot as plt
import numpy as np
import math

def degree_dist(degree, filename):
	plt.close()
	plt.plot(degree[1][:-1], degree[0], 'bo')
	plt.ylabel('number of vertices',fontsize=16)
	plt.xlabel('degree',fontsize=16)
	#plt.draw()
	plt.savefig(filename + '_degree.png')

def giant_phi(giant_cluster, filename):
	giant_cluster = np.array(giant_cluster)
	plt.close()
	plt.plot(giant_cluster[:, 1], giant_cluster[:, 0], 'bo')
	plt.plot(giant_cluster[:, 1], giant_cluster[:, 0] / giant_cluster[:, 1], 'ro')
	plt.ylabel('fraction of giant',fontsize=16)
	plt.xlabel('occupation',fontsize=16)
	#plt.draw()
	plt.savefig(filename + '_giant_phi.png')

def cluster_phi(number_cluster, filename):
	number_cluster = np.array(number_cluster)
	plt.close()
	plt.plot(number_cluster[:, 1], number_cluster[:, 0], 'bo')
	plt.ylabel('number of cluster',fontsize=16)
	plt.xlabel('occupation',fontsize=16)
	#plt.draw()
	plt.savefig(filename + '_cluster_phi.png')

def giant_k0(giant_cluster, filename):
	giant_cluster = np.array(giant_cluster)
	plt.close()
	plt.plot(giant_cluster[:, 2], giant_cluster[:, 0], 'bo')
	plt.plot(giant_cluster[:, 2], giant_cluster[:, 0], 'ro')
	plt.ylabel('fraction of giant',fontsize=16)
	plt.xlabel('max degree',fontsize=16)
	#plt.draw()
	plt.savefig(filename + '_giant_k0.png')


