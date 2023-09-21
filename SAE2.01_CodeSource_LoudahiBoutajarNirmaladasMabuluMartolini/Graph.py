import math
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go


class Graph:
    def __init__(self, directed=False):
        self._edges = dict()
        self._isDirected = directed

    def __len__(self):
        return len(self._edges)

    def __iter__(self):
        return iter(self._edges.keys())

    def __getitem__(self, node):
        return self._edges[node]

    def add_node(self, s):
        if s not in self._edges:
            self._edges[s] = []

    def add_edge(self, source, target, weight=None):
        self.add_node(source)
        self.add_node(target)
        if (source, weight) not in self._edges[target]:
                self._edges[target].append((source, weight))
        # si le graphe est non orienté
        if not self._isDirected:
            if (source, weight) not in self._edges[target]:
                self._edges[target].append((source, weight))
                
    

    def __str__(self):
        s = ""
        for (n, out) in self._edges.items():
            s += n.__str__() + " -> " + out.__str__() + "\n"
        return s

    def bellman_ford(self, start, destination):
        dist = dict()
        pred = dict()

        for n in self:
            dist[n] = math.inf
            pred[n] = None
        dist[start] = 0

        for k in range(0, len(self) - 1):
            for u in self._edges:
                for (v, w) in self[u]:
                    if dist[v] > dist[u] + w:
                        dist[v] = dist[u] + w
                        pred[v] = u

        # Vérification de la présence d'un cycle négatif
        for u in self._edges:
            for (v, w) in self[u]:
                if dist[v] > dist[u] + w:
                    return None

        # Retourner le chemin et la distance
        path = [destination]
        node = destination
        while pred[node] is not None:
            path.append(pred[node])
            node = pred[node]
        path.reverse()
        return path, dist[destination]

    def find_all_paths(graph, start, end, depth_limit):
        visited = set()
        paths = set()
        def ldfs(current_node, current_path, depth):
            visited.add(current_node)
            current_path.append(current_node)

            if current_node == end:
                paths.add(tuple(current_path[:]))
            elif int(depth) < int(depth_limit):
                for neighbor, _ in graph[current_node]:
                    if neighbor not in visited and neighbor not in current_path:
                        ldfs(neighbor, current_path, depth + 1)
            current_path.pop()
            visited.remove(current_node)

        ldfs(start, [], 0)
        return [list(path) for path in paths]

    def find_all_paths_time_limit(graph, start, end, time_limit):
        visited = set()
        paths = set()
        

    def find_nearby_stations(self, station):
        if station not in self._edges:
            return []
        return [node for node in self._edges[station]]

    def are_stations_connected_p_distance(self, station1, station2, p):
        if station1 not in self._edges or station2 not in self._edges:
            return False
        visités = set()
        file = deque([(station1, 0)])
        while file:
            station_courante, distance = file.popleft()
            visités.add(station_courante)
            if distance == p and station_courante == station2:
                return True
            if int(distance) < int(p):
                for voisin, _ in self._edges[station_courante]:
                    if voisin not in visités:
                        file.append((voisin, distance + 1))
        return False

    def comparer_stations(self, station1, station2, p):
        if station1 not in self._edges or station2 not in self._edges:
            return "Stations non trouvées dans le graphe."

        def obtenir_nombre_correspondances(station):
            count = 0
            visités = set()
            file = deque([(station, 0)])
            while file:
                station_courante, distance = file.popleft()
                visités.add(station_courante)
                if distance == p:
                    count += 1
                if int(distance) < int(p):
                    for voisin, _ in self._edges[station_courante]:
                        if voisin not in visités:
                            file.append((voisin, distance + 1))
            return count

        def obtenir_temps_terminus(station):
            if station not in self._edges:
                return math.inf
            visités = set()
            file = deque([(station, 0)])
            while file:
                station_courante, temps = file.popleft()
                visités.add(station_courante)
                if len(self._edges[station_courante]) == 1:
                    return temps
                for voisin, _ in self._edges[station_courante]:
                    if voisin not in visités:
                        file.append((voisin, temps + 1))
            return math.inf

        station1_accessible = self.bellman_ford(station1, station2)
        station2_accessible = self.bellman_ford(station2, station1)
        station1_central = obtenir_nombre_correspondances(station1)
        station2_central = obtenir_nombre_correspondances(station2)
        station1_terminal = obtenir_temps_terminus(station1)
        station2_terminal = obtenir_temps_terminus(station2)

        résultat = f"Comparaison entre {station1} et {station2} :\n"
        résultat += f"{station1} est {'accessible' if station1_accessible else 'non accessible'} depuis {station2}.\n"
        résultat += f"{station1} a {station1_central} correspondances dans un rayon de {p} stations avec la station {station2}.\n"
        résultat += f"{station1} est {'plus' if station1_terminal < station2_terminal else 'moins'} proche d'un terminus que {station2}.\n"


        return résultat


    def dessiner_graphe(self):
        G = nx.Graph()
        for sommet in self._aretes:
            G.add_node(sommet)
            for voisin, _ in self._aretes[sommet]:
                G.add_edge(sommet, voisin)

        nx.draw(G, with_labels=True)
        plt.show()

    def chemin_plus_court_duree(self, depart, destination):
        chemin, duree = self.bellman_ford(depart, destination)
        if chemin is None:
            return "Il n'existe pas de chemin entre les stations."

        return f"Chemin le plus court en durée : {chemin}, durée totale : {duree} unités de temps."

    def chemin_moins_correspondances(self, depart, destination):
        chemins = self.find_all_paths_time_limit(depart, destination, len(self) - 1)
        if not chemins:
            return "Il n'existe pas de chemin entre les stations."

        min_correspondances = min(len(chemin) - 1 for chemin in chemins)
        chemins_moins_correspondances = [chemin for chemin in chemins if len(chemin) - 1 == min_correspondances]

        return f"Chemins utilisant le moins de correspondances : {chemins_moins_correspondances}, nombre de correspondances : {min_correspondances}."


    def afficher_chemins_plus_courts(self, depart, destination):
        G = nx.Graph()

        for sommet in self:
            G.add_node(sommet)

        for sommet in self:
            for voisin, poids in self[sommet]:
                G.add_edge(sommet, voisin, weight=poids)

        pos = nx.spring_layout(G)

        chemins_duree = self.bellman_ford(depart, destination)
        chemins_correspondances_moins = self.chemin_moins_correspondances(depart, destination)

        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5, color='gray'),
            hoverinfo='none',
            mode='lines')

        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color=[],
                size=10,
                line_width=2))

        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            node_trace['text'] += tuple([node])
            node_trace['marker']['color'] += tuple(['red' if node == depart or node == destination else 'lightgray'])

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        data = [edge_trace, node_trace]

        layout = go.Layout(
            title='<br>Graph des Stations de Métro',
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

        fig = go.Figure(data=data, layout=layout)
        fig.show()
        
if __name__ == "__main__":

    G = Graph()
    G.add_edge("s", "a", 10)
    G.add_edge("s", "e", 8)
    G.add_edge("e", "d", 1)
    G.add_edge("d", "a", 4)
    G.add_edge("d", "c", 1)
    G.add_edge("c", "b", 2)
    G.add_edge("b", "a", 1)
    G.add_edge("a", "c", 2)

    print(G)
    # print(Graph.find_all_paths(G, "a", "e"))

    # Exemple d'utilisation
    graph = Graph()
    # Ajoutez les arêtes de votre réseau de métro à l'objet graph

    # start_node = 'a'  # Nœud de départ
    # end_node = 'e'  # Nœud de destination
    # depth_limit = 5  # Limite de profondeur

    # paths = Graph.find_all_paths(G, start_node, end_node, depth_limit)
    # for path in paths:
    #     print(path)

    G = Graph()
    # Ajoutez les arêtes de votre réseau de métro à l'objet graph

    # Analyse 1-distance : stations proches d'une station donnée
    station = "a"
    nearby_stations = G.find_nearby_stations(station)
    print(f"Stations nearby {station}: {nearby_stations}")

    # Dire si deux stations sont reliées à p-distance
    station1 = "a"
    station2 = "e"
    p = 3
    connected = G.are_stations_connected_p_distance(station1, station2, p)
    print(f"Are {station1} and {station2} connected at {p}-distance? {connected}")

    # Comparer 2 stations A et B
    station1 = "a"
    station2 = "b"
    p = 2
    comparison_result = G.compare_stations(station1, station2, p)
    print(comparison_result)
