import networkx as nx
import sys

G = nx.read_edgelist(sys.argv[1], create_using = nx.Graph())

print(G.number_of_nodes())
print(G.number_of_edges())

print(G.nodes())

with open(sys.argv[2], 'r') as f:
  data = f.read().split('\n')
  data = [line.split('	') for line in data]
  data = data[:-1]
  
for node, comm in data:
  G.nodes[node]['comm'] = int(comm)
  G.nodes[node]['label'] = int(node)

nx.write_graphml(G, sys.argv[3] + '.graphml')
print('graphml')
