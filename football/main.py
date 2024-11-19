import networkx as nx
import matplotlib.pyplot as plt

#load GML file
gml_file_path = 'football/football.gml'  
G = nx.read_gml(gml_file_path)

#create force-directed graph
pos = nx.spring_layout(G, k=0.15, iterations=20) #k affects spacing; can alter this if it looks ugly

#draw nodes and edges
plt.figure(figsize=(12, 12))  #can set figure size to whatever i want
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue', alpha=0.7)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color='gray')

#Draw the lables
nx.draw_networkx_labels(G, pos, font_size=10)

#show plot
plt.title('Force-Directed Graph of CFB games between FBS opponents')
plt.axis('off')  #turn off axis
plt.show()
