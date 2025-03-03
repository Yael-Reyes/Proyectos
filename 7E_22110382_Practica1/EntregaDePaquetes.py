import heapq
import networkx as nx
import matplotlib.pyplot as plt
'''
Algoritmo A (Optimización de entregas de paquetes)
Este programa usa el algoritmo A* para calcular la ruta óptima de un 
servicio de entrega de paquetes desde un almacén hasta un destino. 
La heurística aplicada permite mejorar la búsqueda en función de la 
distancia estimada restante. El resultado muestra el mejor camino en 
términos de eficiencia y se representa visualmente en un grafo.
'''
def a_star(graph, start, goal, heuristic):
    queue = []
    heapq.heappush(queue, (0, start))  # (cost, node)
    g_costs = {node: float('inf') for node in graph}
    g_costs[start] = 0
    predecessors = {node: None for node in graph}
    
    while queue:
        current_cost, current_node = heapq.heappop(queue)
        
        if current_node == goal:
            path = []
            while current_node:
                path.append(current_node)
                current_node = predecessors[current_node]
            return path[::-1]
        
        for neighbor, weight in graph[current_node].items():
            g_cost = g_costs[current_node] + weight
            f_cost = g_cost + heuristic[neighbor]
            
            if g_cost < g_costs[neighbor]:
                g_costs[neighbor] = g_cost
                predecessors[neighbor] = current_node
                heapq.heappush(queue, (f_cost, neighbor))
    
    return None

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
    
    plt.title("Entrega de paquetes - Ruta óptima")
    plt.show()

# Grafo representando una red de entrega de paquetes
delivery_map = {
    'Almacén': {'A': 2, 'B': 4},
    'A': {'Almacén': 2, 'C': 5, 'D': 10},
    'B': {'Almacén': 4, 'D': 3},
    'C': {'A': 5, 'Destino': 8},
    'D': {'A': 10, 'B': 3, 'Destino': 4},
    'Destino': {'C': 8, 'D': 4}
}

heuristic = {
    'Almacén': 10, 'A': 7, 'B': 5, 'C': 3, 'D': 2, 'Destino': 0
}

start, goal = 'Almacén', 'Destino'
path = a_star(delivery_map, start, goal, heuristic)
print(f"La mejor ruta de entrega desde {start} hasta {goal} es: {path}")

draw_graph(delivery_map, path)
