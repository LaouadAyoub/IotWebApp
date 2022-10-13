import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import dashboard, tableau

app.layout = html.Div([
    dcc.Location(id='url', refresh=False, pathname=''),
    html.Div([
        html.Div([html.H2("Bertrand Moise et Laouad Ayoub"),
                  html.H1('visualisation de données de production'),
                  html.Img(src='assets/univ.png'),
                  html.Img(src='assets/logo_final_final_bleu.png')], className="banner"),
        html.Br(),
        html.Br(),
        html.Div(className='mon_link',children=[
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


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/dashboard':
        return dashboard.layout
    if pathname == '/apps/tableau':
        return tableau.layout
    else:
        return html.Div([html.Br(),html.H1("Bienvenue, Merci de choisir une page")])


if __name__ == '__main__':
    app.run_server(host = "172.18.20.90", port=1883, debug=True)
