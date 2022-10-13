import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from datetime import datetime
from app import app

import plotly.graph_objs as go

from FactoryData import FactoryData


process_names = [
    'indicateur_qualite',
    'indicateur_performance',
    'materiels',
    'production',
    'conditionnement',
    'panne1',
    'manufacturing_temp',
    'manufacturing_humi',
    'production_levels',
]

fdata = FactoryData(process_names)



layout = html.Div([
    # conteneur principale qui contient de l'ensemble de l'application
    html.Div(id='Div1', children=[
        # conteneur qui contient le numéro de cycle
        html.Div(className='indicator-box', children=[
            html.H4("Numéro de cycle"),
            daq.StopButton(id='nouveau_cycle', buttonText='nouveau cycle',style = {'margin-left':'10%','margin-top':'5%','margin-right':'10%'}),
            daq.LEDDisplay(
                id='num_cycle',
                value="124904",
                color='green',
                style = {'margin-left':'25%','margin-top':'5%'}
            ),
            html.Div(
                id='cycle_start'
            )
        ],style={'width': '33%', 'display': 'inline-block'}),

            html.Div(className='indicator-box', children=[
                html.H4("Button d'arret"),
                daq.StopButton(id='stop-button', buttonText='stop',style={'margin-left': '10%', 'margin-top': '5%','margin-bottom': '5%', 'margin-right': '10%'}),
            ], style={'width': '31%','margin-top' : '0%', 'display': 'inline-block'}),



        # conteneur qui contient les indicateurs de sécurité
        html.Div(className='indicator-box', id='safety-status', children=[
            html.H4("Contrôles de sécurité"),
            daq.Indicator(
                id='materiels',
                value='on',
                color='green',
                label='Matériels'
            ),
            daq.Indicator(
                id='production',
                value='on',
                color='orange',
                label='Production'
            ),
            daq.Indicator(
                id='conditionnement',
                value='on',
                color='red',
                label='Conditionnement'
            )
        ],style={'width': '31%', 'display': 'inline-block'}),
    ]),
    # conteneur qui contient le menu déroulant
    html.Div(id='app-content', children=[
    dcc.Dropdown(
        id='option',
        options=[
            {'label': 'Température', 'value': 'TEMP'},
            {'label': 'humidité', 'value': 'HUM'},
            {'label': 'KPI', 'value': 'KPI'},
            {'label': 'KQI', 'value': 'KQI'}
        ],
        value = 'HUM',
    ),
    # conteneuer qui contient le le graph de la page
    html.Div(className='indicator-box-graph', id='Div_graph', children=[
        html.H4(id='graph_titre', children = 'Niveaux de production'),
        dcc.Graph( id='production-graph',
            figure=go.Figure({ 'data': [{'x': [], 'y':[]}],  'layout': go.Layout(
                yaxis={ 'title': 'Valeur'},height=505)

            })),
            ]),
    # conteneur qui contient les indicateurs de qualité et de performance
    html.Div(
        className='indicator-box2',
        children=[
            html.Div(className='indicator-box', children=[
                html.H4('Indicateur clé de qualité'),
                daq.Gauge(
                    id='indicateur_qualite',
                    size=200,
                    min=0, max=10,
                    showCurrentValue=True,
                    color='red'
                )
            ]),
            html.Div(className='indicator-box', children=[
                html.H4('Indicateur clé de performance'),
                daq.Gauge(
                    id='indicateur_performance',
                    size=200,
                    min=0, max=10,
                    showCurrentValue=True,
                    color='blue'
                )
            ])
        ])
        ]
    ),
    # conteneur qui contient les indicateurs de valeurs de température
    html.Div(
        className='indicator-box',
        children=[
            html.H4("Mesure de température"),
            daq.Thermometer(
                id='manufacturing_temp',
                height=250,
                width=20,
                showCurrentValue=True,
                units="C",
                min=20, max=40,
                value=70,
                color='red'
            )
        ]
    ),
    # conteneur qui contient les indicateurs de valeurs d'humidité
    html.Div(
        className='indicator-box',
        children=[
            html.H4("Mesure de l'humidité"),
            daq.Tank(
                height=300,
                width=220,
                id='manufacturing_humi',
                showCurrentValue=True,
                units='%',
                min=30, max=72,
                value=70,
                color='#00BFFF'
            )
        ]
    ),
    #indicateur qui contient les 3 indicateur de detection de pannes
    html.Div(className='indicator-box1', children=[
        html.H4('Détection des pannes'),
        html.Div([
        daq.Indicator(
            id='my_indicator',
            value = False,
            label= 'Machine 1',
            color='green',
            size = 100),
        html.H2(id = 'machine1', children="En fonction",style= {'text-align': 'center','fontSize': 20})
        ],style={'width': '25%','display': 'inline-block'}),
        html.Div([
        daq.Indicator(
            id='my_indicator2',
            value = False,
            label= 'Machine 2',
            color='green',
            size = 100),
        html.H2(id = 'machine2', children="En fonction",style= {'text-align': 'center','fontSize': 20})
        ],style={'width': '25%','display': 'inline-block'}),
        html.Div([
            daq.Indicator(
                id='my_indicator3',
                value=False,
                label='Machine 3',
                color='green',
                size=100),
            html.H2(id='machine3', children="En fonction", style={'text-align': 'center', 'fontSize': 20})
        ], style={'width': '25%', 'display': 'inline-block'})

    ]),
    #dcc.Interval est un composant qui déclenchera périodiquement un callback
    dcc.Interval(
        id='mon_interval',
        n_intervals=0,
        interval=6*1000,
        disabled= False
    ),
    # composant utilisé pour stocker des données dans le navigateur
    dcc.Store(
        id='annotations-storage',
        data=[]
    )
])

# callback qui prend en entré le nombre de clicks sur le bouton
# et dans la sortie il retourne soit 'start' soit 'stop' et allume la
@app.callback(
     Output('stop-button', 'buttonText'),
     Input('stop-button', 'n_clicks')
)

def stop_production(n_clicks):
    # si on appuie pas sur le bouton on retourne "stop" par défaut
    if n_clicks is None:
        return "stop"
    elif int(n_clicks) % 2 == 1:
        fdata.send_data(1)
        return "start"
    elif int(n_clicks) % 2 == 0:
        fdata.send_data(0)
        return "stop"


# callback qui prend en entré le text du bouton
# et en retoure il arrete l'intervalle d'actualisation de sortie
@app.callback(
     #Output('mon_interval', 'disabled'),
     Output('mon_interval' ,'disabled'),
    Input('stop-button', 'buttonText')
    #state=[State('mon_interval', 'disabled')]
)

def stop(text):
    # si le text est start donc la production est en arret, on désactive l'intervalle de temps
    if text == 'start':
        print("text",text)
        return True
    elif text == 'stop':
        return False

# Deuxième intervalle responsable sur le comptage des cycles
# Il prend en entrée le bouton bleu et en sortie, il incrémente le numéro de cycle, et écrit le date du debut du cycle
# il ajoute aussi des marques sur le graph
@app.callback(
    [Output('num_cycle', 'value'),
     Output('annotations-storage', 'data'),
     Output('cycle_start', 'children')],
    [Input('nouveau_cycle', 'n_clicks')],
    state=[State('num_cycle', 'value'),
           State('annotations-storage', 'data'),
           State('production-graph', 'figure')]
)
def nouveau_cycle(_, nouveau_cycle, current_annotations, current_fig):

    # Déclaration d'une variable qui stocke le temps actuel
    timestamp = datetime.now().strftime('%H:%M:%S %D')
    # Si on a pas encore de valeur sur l'axe x du graph on ajoute pas un nouveau cycle vu qu'on est au debut
    if len(current_fig['data'][0]['x']) == 0:
        return nouveau_cycle, current_annotations, 'Cycle commencé le: {}'.format(timestamp)
    # creation des markers sur les derniers coordonnées de x et de y
    marker_x = current_fig['data'][0]['x'][-1]
    marker_y = current_fig['data'][0]['y'][-1]
    # les données des marques sont stocké dans le navigateur, et mise en place dans le dernier point de la navigation
    current_annotations.append({
        'x': marker_x,
        'y': marker_y,
        'text': 'Cycle no. {}'.format(str(int(nouveau_cycle) + 1)),
        'arrowhead': 0,
        'bgcolor'  : 'blue',
        'font': {'color': 'white'}
    })
    return str(int(nouveau_cycle) + 1), current_annotations, 'Cycle commencé le: {}'.format(timestamp)




# callback des mesures
# chaque intervalle de temps, ici 6 secondes, le graph reçoit une liste des données de la classe FactoryData
# il prend en compte la valeur du menu déroulant, l'état actuel du graph
@app.callback(
    [Output('indicateur_qualite', 'value'),
     Output('indicateur_performance', 'value'),
     Output('materiels', 'color'),
     Output('production', 'color'),
     Output('conditionnement', 'color'),
     Output('my_indicator', 'color'),
     Output('manufacturing_temp', 'value'),
     Output('manufacturing_humi', 'value'),
     Output('production-graph', 'figure'),
     Output('graph_titre', 'children')
     ],
    [Input('mon_interval', 'n_intervals')],
    state=[State('option', 'value'),
        State('production-graph', 'figure'),
           State('annotations-storage', 'data')]
)


def update_stats(n_intervals,value, current_fig, current_annotations):
    
    # stats utilise l'objet fdata avec la fonction get_data pour récuperer une lise de 9 valeurs contenant les variable
    stats = [fdata.get_data()[pname] for pname in process_names]
    current_data = current_fig['data'][0]

    #Condition du choix de la valeur d'optio
    if value=="HUM":
        valeur=stats[-2]
        titre = "Valeur d'humidité"
    elif value=="TEMP":
        valeur=stats[-3]
        titre = "Valeur de température"
    elif value=="KPI":
        valeur=stats[0]
        titre = "Valeur de KPI"
    else:
        valeur=0
        titre = "Veuiller sélectionner une valeur"

    # créer un dictionnaire de données,
    # On ajoute à les nouveaux prochain intervalle
    new_data = [{'x': current_data['x'].append(n_intervals),
                 # on ajoute la variable valeur à notre axe y
                 'y': current_data['y'].append(
                     valeur
                     if len(current_data['y']) > 0
                     else valeur

                 )}]
    
    # stockage de la même mise en page
    current_fig['layout'].update(annotations=current_annotations)
    #mise à jour du graph avec les nouvelle valeur de nos nouvelles données new data
    current_fig.update(
        figure=go.Figure(
            data=new_data,
    ))
    # on crée une nouvelle fig depuis la mise a jour de la dernière
    fig = go.Figure(current_fig)


    #on enleve la dernière valeur de stat et on mets à sa place sa figure, de cette façon, 
    # la figure se rend directement à notre graph
    stats = stats[:-1]
    stats.append(fig)
    # finalement on ajoute le titre du graph pour l'affecter au div graph_titre
    stats.append(titre)
    return stats


#Dernier callback responsable sur les 3 indicateurs de panne,
# il prend en entré la couleur de l'indicateur, si l'indicateur est rouge, le div en bas devien "en panne"
# si il est en vert il devient "en fonction"
@app.callback(
    Output('machine1', 'children'),
    [Input('my_indicator', 'color')])

def panne(col):
    green = 'green'
    red = 'red'
    if col == green:
        return 'En fonction'
    elif col == red:
        return 'En panne'
