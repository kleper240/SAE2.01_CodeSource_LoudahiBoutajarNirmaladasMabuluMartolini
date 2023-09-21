# Import des bibliothèques
import os
import folium
import pandas as pd
from ast import literal_eval

# Couleur des lignes de métro de Paris

table_couleurs = pd.read_table('.\data\color_metro_paris.txt', sep=',', header=None)

# Fichiers contenant la position des stations de métro et des lignes de Paris
fichier_stations = './data/emplacement-des-gares-idf.csv'
fichier_lignes = './data/traces-du-reseau-ferre-idf.csv'

# Nom du fichier de sortie de la carte
fichier_sortie = "paris_metro.html"

# Paris

m = folium.Map(location=[48.859553, 2.336332], 
               zoom_start=12.5, 
               control_scale=True, 
               prefer_canvas=True,
               tiles='CartoDB positron')

# Ajout des tuiles
folium.TileLayer('CartoDB positron').add_to(m)
folium.TileLayer('CartoDB dark_matter').add_to(m)


# Création d'un groupe de fonctionnalités (layer) pour chaque ligne de métro
groupe_ligne1 = folium.FeatureGroup(name='Ligne 1')
groupe_ligne2 = folium.FeatureGroup(name='Ligne 2')
groupe_ligne3 = folium.FeatureGroup(name='Ligne 3')
groupe_ligne3b = folium.FeatureGroup(name='Ligne 3b')
groupe_ligne4 = folium.FeatureGroup(name='Ligne 4')
groupe_ligne5 = folium.FeatureGroup(name='Ligne 5')
groupe_ligne6 = folium.FeatureGroup(name='Ligne 6')
groupe_ligne7 = folium.FeatureGroup(name='Ligne 7')
groupe_ligne7b = folium.FeatureGroup(name='Ligne 7b')
groupe_ligne8 = folium.FeatureGroup(name='Ligne 8')
groupe_ligne9 = folium.FeatureGroup(name='Ligne 9')
groupe_ligne10 = folium.FeatureGroup(name='Ligne 10')
groupe_ligne11 = folium.FeatureGroup(name='Ligne 11')
groupe_ligne12 = folium.FeatureGroup(name='Ligne 12')
groupe_ligne13 = folium.FeatureGroup(name='Ligne 13')
groupe_ligne14 = folium.FeatureGroup(name='Ligne 14')
groupe_rerA = folium.FeatureGroup(name='RER A')
groupe_rerB = folium.FeatureGroup(name='RER B')
groupe_rerC = folium.FeatureGroup(name='RER C')
groupe_rerD = folium.FeatureGroup(name='RER D')
groupe_rerE = folium.FeatureGroup(name='RER E')

# Et un dictionnaire associant une chaîne de ligne à un groupe
dictionnaire_groupes = {
    '1': groupe_ligne1,
    '2': groupe_ligne2,
    '3': groupe_ligne3,
    '3b': groupe_ligne3b,
    '4': groupe_ligne4,
    '5': groupe_ligne5,
    '6': groupe_ligne6,
    '7': groupe_ligne7,
    '7b': groupe_ligne7b,
    '8': groupe_ligne8,
    '9': groupe_ligne9,
    '10': groupe_ligne10,
    '11': groupe_ligne11,
    '12': groupe_ligne12,
    '13': groupe_ligne13,
    '14': groupe_ligne14,
    'A': groupe_rerA,
    'B': groupe_rerB,
    'C': groupe_rerC,
    'D': groupe_rerD,
    'E': groupe_rerE
}

# Récupération des lignes
df = pd.read_table(fichier_lignes, sep=';')
# Seulement les lignes de métro et RER
df_M = df.loc[(df['METRO']==1) | (df['RER']==1)]

for index, row in df_M.iterrows():
    # Nom de la ligne
    ligne_str = row['INDICE_LIG']
    # Obtention de la couleur correspondante
    couleur_ligne_metro = table_couleurs.iat[table_couleurs.loc[table_couleurs[0]==ligne_str].index.values[0],1]
    
    # Récupération des données de la ligne et formatage correct
    donnees = literal_eval(row['Geo Shape'])
    points = []
    for point in donnees['coordinates']:
        points.append(tuple([point[1], point[0]]))
    
    # Ajout dans le groupe correspondant
    folium.PolyLine(points, 
                    color=couleur_ligne_metro,
                    weight=2,
                    opacity=1).add_to(dictionnaire_groupes[ligne_str])

# Récupération des stations
df = pd.read_table(fichier_stations, sep=';')
# Seulement les stations de métro et RER
df_M = df.loc[(df['METRO']==1) | (df['RER']==1)]

for index, row in df_M.iterrows():
    # Lignes desservies par la station
    ligne_str = row['INDICE_LIG']
    
    # Nom de la station
    texte_popup = '{}'.format(row['NOM_GARE'].replace("'","\\'"))
    
    # Obtention de la couleur correspondante
    couleur_ligne_metro = table_couleurs.iat[table_couleurs.loc[table_couleurs[0]==ligne_str].index.values[0],1]
    couleur_remplissage_ligne_metro = couleur_ligne_metro
    # Rayon du marqueur
    rayon = 3

    # Ajout dans le groupe correspondant
    folium.CircleMarker(literal_eval(row['Geo Point']),
                        color=couleur_ligne_metro,
                        radius=rayon,
                        fill=True,
                        fill_color=couleur_remplissage_ligne_metro,
                        fill_opacity=1,
                        popup=texte_popup).add_to(dictionnaire_groupes[ligne_str])

# Ajout des groupes à la carte
groupe_ligne1.add_to(m)
groupe_ligne2.add_to(m)
groupe_ligne3.add_to(m)
groupe_ligne3b.add_to(m)
groupe_ligne4.add_to(m)
groupe_ligne5.add_to(m)
groupe_ligne6.add_to(m)
groupe_ligne7.add_to(m)
groupe_ligne7b.add_to(m)
groupe_ligne8.add_to(m)
groupe_ligne9.add_to(m)
groupe_ligne10.add_to(m)
groupe_ligne11.add_to(m)
groupe_ligne12.add_to(m)
groupe_ligne13.add_to(m)
groupe_ligne14.add_to(m)
groupe_rerA.add_to(m)
groupe_rerB.add_to(m)
groupe_rerC.add_to(m)
groupe_rerD.add_to(m)
groupe_rerE.add_to(m)

# Activation du contrôle des couches
folium.LayerControl().add_to(m)

m.save(fichier_sortie)