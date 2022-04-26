from dash import Dash, html, dcc, Input, Output
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

app.layout = html.Div(children=[
    html.H3('Dash App'),
    html.H4('Data use permission'),
    dcc.Dropdown(
        id = 'data_use_permission',
        options=[
            {'label': 'General Research Use', 'value': 'GRU'},
            {'label': 'Health or Medical or Biomedical research', 'value': 'HMB'},
            {'label': 'Disease Specific research', 'value': 'DS'},
            {'label': 'No Restriction', 'value': 'NRES'},
            {'label': 'Population Origins or Ancestry research only', 'value': 'POA'}
        ],
        value='NRES'
    ),
    html.Div([
        dcc.Dropdown(
            id = 'disease',
            options=[
                {'label': 'Uveal Melanoma', 'value': 'uveal_melanoma'},
                {'label': 'Melanoma', 'value': 'melanoma'},
                {'label': 'Cancer', 'value': 'cancer'}
            ],
            value=[],
            multi=True
        )
    ], style= {'display': 'block'}),
    html.H4('Data use modifier')
])

@app.callback(
   Output(component_id='disease', component_property='style'),
   [Input(component_id='data_use_permission', component_property='value')])

def show_hide_element(visibility_state):
    if visibility_state == 'DS':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True)
