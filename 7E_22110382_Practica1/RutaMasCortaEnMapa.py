import heapq
import networkx as nx
import matplotlib.pyplot as plt
'''
Algoritmo de Dijkstra (Búsqueda de ruta más corta en calles de una ciudad)
Este programa utiliza el algoritmo de Dijkstra para encontrar la ruta más 
corta entre dos ubicaciones en una ciudad. Se representa un mapa con nodos 
como puntos de interés (casa, supermercado, escuela, etc.) y aristas con pesos 
que indican la distancia o el tiempo de viaje. La ruta óptima se muestra en una 
gráfica resaltada en rojo.
'''
def dijkstra(graph, start, goal):
    queue = []
    heapq.heappush(queue, (0, start))  # (cost, node)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        if current_node == goal:
            path = []
            while current_node:
                path.append(current_node)
                current_node = predecessors[current_node]
            return path[::-1], distances[goal]
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    
    return None, float('inf')

def draw_graph(graph, path):
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    plt.title("Mapa de la ciudad con la ruta más corta resaltada")
    plt.show()

# Grafo representando calles de una ciudad
graph = {
    'Casa': {'Supermercado': 4, 'Escuela': 2},
    'Supermercado': {'Casa': 4, 'Parque': 5},
    'Escuela': {'Casa': 2, 'Parque': 8, 'Trabajo': 10},
    'Parque': {'Supermercado': 5, 'Escuela': 8, 'Trabajo': 2, 'Hospital': 6},
    'Trabajo': {'Escuela': 10, 'Parque': 2, 'Hospital': 3},
    'Hospital': {'Parque': 6, 'Trabajo': 3}
}

start, goal = 'Casa', 'Hospital'
path, cost = dijkstra(graph, start, goal)
print(f"La ruta más corta desde {start} hasta {goal} es: {path} con un tiempo estimado de {cost} minutos.")

draw_graph(graph, path)
