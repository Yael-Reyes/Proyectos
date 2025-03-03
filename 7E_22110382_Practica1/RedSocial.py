from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
'''
Algoritmo BFS (Conexión en una red social)
Este código emplea el algoritmo de Búsqueda en Anchura (BFS) para determinar 
la conexión más corta entre dos personas dentro de una red social. Cada nodo 
representa a una persona y las conexiones indican relaciones de amistad. 
La salida del programa muestra el camino más eficiente para conectar a dos 
individuos dentro de la red y lo visualiza gráficamente.
'''
def bfs(graph, start, goal):
    queue = deque([[start]])  # Cola de rutas posibles
    visited = set()
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == goal:
            return path
        
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    
    return None

def draw_graph(graph, path):
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    
    pos = nx.spring_layout(G)
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    plt.title("Red social - Ruta más corta de conexión entre dos personas")
    plt.show()

# Grafo representando conexiones en una red social
social_network = {
    'Ana': ['Carlos', 'Beatriz'],
    'Carlos': ['Ana', 'David', 'Elena'],
    'Beatriz': ['Ana', 'David'],
    'David': ['Carlos', 'Beatriz', 'Elena', 'Fernando'],
    'Elena': ['Carlos', 'David', 'Fernando'],
    'Fernando': ['David', 'Elena']
}

start, goal = 'Ana', 'Fernando'
path = bfs(social_network, start, goal)
print(f"La conexión más corta entre {start} y {goal} es: {path}")

draw_graph(social_network, path)
