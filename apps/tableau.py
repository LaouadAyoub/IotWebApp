import pandas as pd
from dash.dependencies import Input, Output,State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import sqlite3 as sqlite
from app import app

layout = html.Div([
    # Déclaration d'un conteneur générique qui permet d'organiser le contenu
    html.Div(id='app_content',children=[
    #dcc.Interval est un composant qui déclenchera périodiquement un callback
    dcc.Interval(
        id='mon_interval',
        n_intervals=0,
        interval=2 * 1000,
        ),
    # un conteneur avec id titre qui contient le titre de graph
    html.Div(id="titre", style={'color': 'green', 'fontSize': 50,'font-weight': 'bold', 'text-align': 'center'}),

    html.Br(),
    # dcc dropdown est un menu déroulant avec les options des bases de données
    dcc.Dropdown(
        id='option',
        options=[
            {'label': 'Température', 'value': 'TEMP'},
            {'label': 'humidité', 'value': 'HUM'},
            {'label': 'Statistiques humidité', 'value': 'STATH'},
            {'label': 'Statistiques température', 'value': 'STATT'},
            {'label': 'Historique des pannes', 'value': 'PANNE'}
        ],
        value = 'HUM',
    ),
    html.Br(),
    # Le conteneur avec output_table est la sortie du callback ou on va retourner le tableau
    html.Div(id="output_table"),

]
)])

# Déclaration de la fonction de rappel qui s'actualise dans chaque intervalle de temps
# et prend en compte l'option du menu déroulant pour retourner une des table et modifier le titre de la page

@app.callback(
    Output('output_table','children'),
    Output('titre','children'),
    [Input('mon_interval', 'n_intervals')],
    state=[State('option', 'value')]
)
def update(mon_interval,value):
    try:
        #importation de de la base de données et déclaration des variable panda contenant la base de données
        # de température, d'humidité et de déclaration de panne
        dbFile = "capteurs.db"
        conn = sqlite.connect(dbFile)
        df_humidity = pd.read_sql("SELECT * FROM humidity", conn)
        humi = df_humidity
        df_panne1 = pd.read_sql("SELECT * FROM panne1", conn)
        panne1 = df_panne1
        df_temperature = pd.read_sql("SELECT * FROM temperature", conn)
        temp = df_temperature
        # la valeur retourné par le menu déroulant est Hum, on crée une variable panda on on met la base de données d'humidité
        if value == "HUM":
            df = humi
            #inversement de la base de données pour avoir la dérnière valeur au début
            df = df.iloc[::-1]
            # affectation des titres des colonnes
            df.columns = ['id', 'Horodatage', 'humidité']
            # affectation du titre
            titre = "Données d'humidité"
        # On fait la même chose pour la température
        elif value == "TEMP":
            df = temp
            df = df.iloc[::-1]
            df.columns= ['id', 'Horodatage', 'temperature']
            titre = "Données de température"
        # affichage des statistiques de l'humidité avec la fonction df.descrive de panda
        elif value == "STATH":
            # indexage des valeurs de l'humidité
            humi = humi.iloc[:, 2]
            # récupération des valeurs statistiques dans la variable stat
            stat = humi.describe()
            # création d'une variable panda avec des colonnes statistique et valeur, et mise en place des données avec la variable stat
            df = pd.DataFrame({'Statistique': ['Nombre de données', 'La moyenne', 'La valeur de l écart type',
                                               'La valeur minimale', '25%', '50%', '75%', 'La valeur maximale'],
                               'Valeurs': stat})

            titre = "Statistique d'humidité"
        # Le principe pour les statistiques de température
        elif value == "STATT":
            print(temp)
            temp = temp.iloc[:, 2]
            stat = temp.describe()
            df = pd.DataFrame({'Statistique': ['Nombre de données', 'La valeur moyenne', 'La valeur de l écart type',
                                               'La valeur minimale'],
                               'Valeurs': stat})
            titre = "Statistique de température"
        # affichage de l'historique des pannes  si la valeur du menu déroulant égale à panne
        elif value == "PANNE":
            df = panne1
            df = df.iloc[::-1]
            titre = "Historique des pannes"
            df.columns = ['id', 'Horodatage', 'Machine1']
        else:
            # si aucun de ces valeurs du menu déroulant est choisie, retourner un message
            titre = "Veuiller sélectionner une valeur"

        # convertit la variable panda à un dictionnaire
        data = df.to_dict('records')
        # déclaration d'un dictionnaire qui contient les colonne
        columns = [{"name": i, "id": i, } for i in (df.columns)]

        # ajouter des style pour notre tableau
        style_cell = dict(textAlign='left')
        style_header = dict(backgroundColor="paleturquoise",fontWeight= 'bold'
                            ,fontSize = 30)
        style_data = dict(backgroundColor="lavender",fontSize = 20)

        # déclaration d'une table Dash avec les dicitonnaires et style qu'on a créé
        tableau = dash_table.DataTable(data=data, columns=columns, style_cell=style_cell,
                                       style_header=style_header,
                                       style_data=style_data)
        # retourner le tableau créer et le titre de la page
        return tableau, titre
    except:
        # si il trouve une erreur dans le programmme il affiche un message
        txt = html.H1("Saisissez le parametre à afficher")
        titre= "Rien à afficher"
        return txt,titre
