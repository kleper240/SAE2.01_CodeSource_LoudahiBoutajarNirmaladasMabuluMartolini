import csv
from flask import Flask, render_template, request
import Graph
import ReseauMetro
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avis.db'
db = SQLAlchemy(app)

IleDeFrance = ReseauMetro.ReseauMetro()
IleDeFrance.lire_fichier()
Graphe = Graph.Graph()

for i, j in IleDeFrance.stations.items():
    for k in range(2, len(j)):
        Graphe.add_edge(str(i), str(j[k][0]), j[k][1])

class Avis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    etoiles = db.Column(db.Integer)
    message = db.Column(db.Text)

@app.route('/')
def index(): 
    return render_template('index.html')
    
@app.route('/pluscourt', methods=['GET', 'POST'])
def plus_court():
    if request.method == 'POST':
        # Obtention des stations de départ et d'arrivée depuis le formulaire
        start_station = request.form['start_station']
        end_station = request.form['end_station']

        # Création du dictionnaire des noms de stations
        station_names = {}
        station_lines = {}
        with open('csv/stations.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                station_names[row['id']] = row['nom']
                station_lines[row['id']] = row['ligne']

        # Trouver le plus court chemin entre deux stations
        shortest_path = Graphe.bellman_ford(start_station, end_station)
        shortest_path_names = [station_names.get(station_id) for station_id in shortest_path[0]]
        shortest_path_duration = shortest_path[1]

        # Convertir la durée en minutes et secondes
        shortest_path_minutes = shortest_path_duration // 60
        shortest_path_seconds = shortest_path_duration % 60
        shortest_path_duration_str = f"{shortest_path_minutes} minutes {shortest_path_seconds} secondes"

        return render_template('plus_court.html', shortest_path=shortest_path_names,
                               shortest_path_duration=shortest_path_duration_str,
                               station_lines=station_lines)

    return render_template('plus_court.html')

@app.route('/tousleschemins', methods=['GET', 'POST'])
def tousleschemins():
    if request.method == 'POST':
        # Obtention des stations de départ et d'arrivée depuis le formulaire
        start_station = request.form['start_station']
        end_station = request.form['end_station']
        depth_limit = request.form['limit']
        # Création du dictionnaire des noms de stations
        station_names = {}
        station_lines = {}
        with open('csv/stations.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                station_names[row['id']] = row['nom']
                station_lines[row['id']] = row['ligne']
                
        
        paths = Graph.Graph.find_all_paths(Graphe, start_station, end_station, depth_limit)
        chemins = []
        for path in paths : 
            chemins.append([station_names.get(station_id) for station_id in path])
        return render_template('tous_les_chemins.html', paths = chemins)
    return render_template('tous_les_chemins.html')
    

@app.route('/comparerdeuxstations', methods=['GET', 'POST'])
def comparerdeuxstations():
    if request.method == 'POST':
        # Obtention des stations de départ et d'arrivée depuis le formulaire
        station1 = request.form['station1']
        station2 = request.form['station2']
        p = request.form['p']
        
        resultat_comparaison = Graphe.comparer_stations(station1, station2, p)
        resultats = []
        chaine_temp = ""
        for i in range(len(resultat_comparaison)):
            if resultat_comparaison[i] != ".":
                    chaine_temp += resultat_comparaison[i]
            else:
                resultats.append(chaine_temp)
                chaine_temp = ""
        
        return render_template('comparer_deux_stations.html', resultats = resultats)
    
    return render_template('comparer_deux_stations.html')

@app.route('/correspondancelignes', methods=['GET', 'POST'])
def correspondancelignes():
    if request.method == 'POST':
        # Obtention des lignes depuis le formulaire
        ligne1 = request.form['ligne1']
        ligne2 = request.form['ligne2']
        resultat = IleDeFrance.get_correspondance(ligne1, ligne2)
        
        return render_template('correspondance_lignes.html', resultat = resultat)
    
    return render_template('correspondance_lignes.html')

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'POST':
        depart = request.form['depart']
        destination = request.form['destination']

        graphe = Graphe.afficher_chemins_plus_courts(depart, destination)

        return render_template('graph.html', graph_html=graphe)
    
    return render_template('graph.html')


@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        etoiles = request.form['etoiles']
        message = request.form['message']
        avis = Avis(nom=nom, prenom=prenom, etoiles=etoiles, message=message)
        db.session.add(avis)
        db.session.commit()

    avis_list = Avis.query.all()
    return render_template('formulaire.html', avis_list=avis_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée la table "avis" si elle n'existe pas encore
    app.run(debug=True)
