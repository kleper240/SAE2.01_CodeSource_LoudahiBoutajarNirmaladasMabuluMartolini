import os
class ReseauMetro:
    def __init__(self):
        self.stations = {}
        self.lignes = {}

    def lire_fichier(self):
        
        with open("csv/stations.csv", "r", encoding="utf-8") as stations_file:
            # Ignorer la première ligne contenant les en-têtes
            next(stations_file)
            for line in stations_file:
                id, ligne, terminus, nom = line.strip().split(";")
                self.stations[int(id)] = [nom, int(terminus)]

                # Vérifier si la valeur de la ligne est numérique
                if ligne.isdigit():
                    # Ajouter la station à la liste de la ligne correspondante
                    if int(ligne) not in self.lignes:
                        self.lignes[int(ligne)] = []
                    self.lignes[int(ligne)].append(nom)

        with open("csv/relations.csv", "r", encoding="utf-8") as relations_file:
            # Ignorer la première ligne contenant les en-têtes
            next(relations_file)
            for line in relations_file:
                id1, id2, temps = line.strip().split(";")
                id1, id2, temps = int(id1), int(id2), int(temps)

                # Ajouter la relation entre les stations
                if id1 in self.stations and id2 in self.stations:
                    self.stations[id1].append((id2, temps))
                    self.stations[id2].append((id1, temps))

    def get_ligne(self, id):
        return self.lignes[id]
    
    def get_station(self, id:int):
        return self.stations[id]
            
    def get_correspondance(self, ligne1, ligne2):
        liste_correspondance = []
        for elem in self.lignes[int(ligne1)]:
            if elem in self.lignes[int(ligne2)]:
                liste_correspondance.append(elem)
        
        return liste_correspondance
    
    

    def algorithme_prim(self, station_depart):
        visites = set()
        arbre_couvrant_minimal = []
        infini = float('inf')

        distances = {station: infini for station in self.stations}
        distances[station_depart] = 0

        while len(visites) < len(self.stations):
            distance_min = infini
            station_min = None
            for station in self.stations:
                if station not in visites and distances[station] < distance_min:
                    distance_min = distances[station]
                    station_min = station

            if station_min is None:
                break

            visites.add(station_min)

            for voisin, temps in self.stations[station_min][2:]:
                if voisin not in visites and temps < distances[voisin]:
                    distances[voisin] = temps
                    arbre_couvrant_minimal.append((station_min, voisin, temps))
                    print(f"Added edge: {station_min} -> {voisin} (Temps: {temps})")

        print("Arbre couvrant minimal:")
        for edge in arbre_couvrant_minimal:
            print(f"{edge[0]} -> {edge[1]} (Temps: {edge[2]} secondes)")

        return arbre_couvrant_minimal

