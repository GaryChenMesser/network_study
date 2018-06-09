import graph_tool.all as gt
import numpy as np
import matplotlib

g = gt.collection.data["polblogs"]
g = gt.GraphView(g, vfilt=gt.label_largest_component(g))
'''
w = g.new_edge_property("double")
w.a = np.random.random(len(w.a)) * 42
ee, x = gt.eigenvector(g)
print(ee)
gt.graph_draw(g, pos=g.vp["pos"], vertex_fill_color=x,
              vertex_size=gt.prop_to_size(x, mi=5, ma=15),
              vcmap=matplotlib.cm.gist_heat,
              vorder=x, output="polblogs_eigenvector.pdf")
'''
prop = g.new_vertex_property("vector<int>")
print(prop[0])
prop[0] = [1,1]
print(prop[0])
prop[1] = [2,2]
print(prop[0])
print(prop[1])
