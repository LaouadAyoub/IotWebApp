import dash


# Déclaration de l'application le meta_tags est responsable pour que l'application soit opérationnelle dans un smart_phone

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server
