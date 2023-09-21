import Graph
import Station
import ReseauMetro


##################### Création de l'objet ResaeuMetro #####################
IleDeFrance = ReseauMetro.ReseauMetro()
IleDeFrance.lire_fichier()

##################### Affichage des stations des lignes #####################
# print(IleDeFrance.lignes)

##################### Correspondances entre deux lignes #####################
# print(IleDeFrance.stations)
# print(IleDeFrance.get_correspondance(6, 4))

##################### Créer un graphe avec les stations de metro #####################
Graphe = Graph.Graph()
for i,j in IleDeFrance.stations.items():
    for k in range(2,len(j)):
        Graphe.add_edge(str(i), str(j[k][0]), j[k][1])

# print(Graphe)


##################### Trouver tous les chemins possibles avec une limite de nombre de lignes #####################
start_node = '67'  # Nœud de départ
end_node = '212'  # Nœud de destination
depth_limit = 10  # Limite de profondeur

# paths = Graph.Graph.find_all_paths(Graphe, start_node, end_node, depth_limit)
# print(f"Les chemins possibles entre {start_node} et {end_node} sans dépasser une limite de {depth_limit} stations sont : ")
# for path in paths:  
#     print(path)


##################### Afficher le plus court chemin entre deux stations #####################
# print(f"le chemin le plus court entre {start_node} et {end_node} est {Graphe.bellman_ford(start_node, end_node)}")

# depart = "28"
# destination = "29"

# chemin_duree = Graphe.chemin_plus_court_duree(depart, destination)
# print(chemin_duree)


##################### Trouver chemin avec le moins de correspondance #####################
# chemin_correspondances = Graphe.chemin_moins_correspondances(depart, destination)
# print(chemin_correspondances)


# station = "67"
# stations_proches = Graphe.find_nearby_stations(station)
# print(f"Stations proches de {station} : {stations_proches}")

##################### Dire si deux stations sont reliées à une distance p #####################
# station1 = "28"
# station2 = "29"
# p = 3
# reliées = Graphe.are_stations_connected_p_distance(station1, station2, 1)
# print(f"Est-ce que {station1} et {station2} sont reliées à une distance de {p} ? {reliées}") 

##################### Comparer 2 stations A et B #####################
# station1 = "67"
# station2 = "212"
# p = 2
# résultat_comparaison = Graphe.comparer_stations(station1, station2, p)
# print(résultat_comparaison)


##################### Afficher ACM dans la console #####################
# acm = IleDeFrance.algorithme_prim(0)  





