import os
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output,State
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas_datareader.data as web
import plotly.graph_objects as go
import dash_table
import time
import sqlite3 as sqlite
from app import app







#app = dash.Dash(__name__)

layout = html.Div([

    html.Div(id='app_content',children=[
    dcc.Interval(
        id='mon_interval',
        n_intervals=0,
        interval=2 * 1000,
        #disabled=True
        ),
    html.Div(id="titre",children='Données', style={'color': 'green', 'fontSize': 50,'font-weight': 'bold', 'text-align': 'center'}),

    html.Br(),
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
    html.Div( id="output_table"),

]
)])

@app.callback(
    Output('output_table','children'),
    Output('titre','children'),
    [Input('mon_interval', 'n_intervals')],
    state=[State('option', 'value')]
)
def update(mon_interval,value):
    try:
        dbFile = "capteurs.db"
        conn = sqlite.connect(dbFile)
        df_humidity = pd.read_sql("SELECT * FROM humidity", conn)
        humi = df_humidity
        df_panne1 = pd.read_sql("SELECT * FROM panne1", conn)

        df_temperature = pd.read_sql("SELECT * FROM temperature", conn)
        temp = df_temperature
        if value == "HUM":
            df = humi
            df = df.iloc[::-1]
            df.columns = ['id', 'Horodatage', 'humidité']
            titre = "Données d'humidité"
        elif value == "TEMP":
            df = temp
            df = df.iloc[::-1]
            df.columns= ['id', 'Horodatage', 'temperature']
            titre = "Données de température"
        elif value == "STATH":

            humi = humi.iloc[:, 2]
            stat = humi.describe()
            df = pd.DataFrame({'Statistique': ['Nombre de données', 'La moyenne', 'La valeur de l écart type',
                                               'La valeur minimale', '25%', '50%', '75%', 'La valeur maximale'],
                               'Valeurs': stat})
            titre = "Statistique d'humidité"
        elif value == "STATT":
            print(temp)
            temp = temp.iloc[:, 2]
            stat = temp.describe()
            df = pd.DataFrame({'Statistique': ['Nombre de données', 'La valeur moyenne', 'La valeur de l écart type',
                                               'La valeur minimale'],
                               'Valeurs': stat})
            titre = "Statistique de température"

        elif value == "PANNE":
            df = df_panne1
            df = df.iloc[::-1]
            titre = "Historique des pannes"
            df.columns = ['id', 'Horodatage', 'Machine1']
        else:
            titre = "Veuiller sélectionner une valeur"

        data = df.to_dict('records')
        columns = [{"name": i, "id": i, } for i in (df.columns)]

        style_cell = dict(textAlign='left')
        style_header = dict(backgroundColor="paleturquoise",fontWeight= 'bold',fontSize = 30)
        style_data = dict(backgroundColor="lavender",fontSize = 20)

        tableau = dash_table.DataTable(data=data, columns=columns, style_cell=style_cell, style_header=style_header,
                                       style_data=style_data)
        return tableau, titre
    except:
        txt = html.H1("Saisissez le parametre à afficher")
        titre= "Rien à afficher"
        return txt,titre

#if __name__ == '__main__':
 #   app.server.run(debug=True)