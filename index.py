import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import dashboard, tableau

#Mise en page de l'application
app.layout = html.Div([
    #dcc location est un composant qui représente la barre de d'adresse dans le navigateur
    dcc.Location(id='url', refresh=False, pathname=''),
    html.Div([
        html.Div([html.H2("Bertrand Moise et Laouad Ayoub"),
                  html.H1('visualisation de données de production'),
                  html.Img(src='assets/univ.png'),
                  html.Img(src='assets/logo_final_final_bleu.png')], className="banner"),
        html.Br(),
        html.Br(),
        html.Div(className='mon_link',children=[
        #dcc link represent un lien ou on peut appuyer
        dcc.Link('Tableau de board||', href='/apps/dashboard',style={
        'fontSize': 30,
        'textAlign': 'left',
        'color': 'red',
        'borderColor':'black',
    }),
        dcc.Link('Données en temps réel', href='/apps/tableau',style={
        'fontSize': 30,
        'textAlign': 'left',
        'color': 'red'
    })],style={'border-style': 'dashed solid'})
    ], className="row"),
    html.Div(id='page-content', children=[])
])

# Cette page prend en entrée le lien de dcc location et nous rend une des page dans le div  page-content
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):

    # test sur le nom de l'url et retourner le layout d'une des applications
    if pathname == '/apps/dashboard':
        return dashboard.layout
    if pathname == '/apps/tableau':
        return tableau.layout
    else:
        #Sinon retourner un messeage
        return html.Div([html.Br(),html.H1("Bienvenue, Merci de choisir une page")])


#if __name__ == '__main__':
 #   app.run_server(debug=True)
if __name__ == '__main__':
    app.run_server(host = "172.18.20.90", debug=True)
