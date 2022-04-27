from dash import Dash, html, dcc, Input, Output
from rdflib import Graph, Namespace, URIRef, BNode
from rdflib.namespace import RDF

g = Graph()

dpv = Namespace("https://w3id.org/dpv#")
g.namespace_manager.bind('dpv', URIRef('https://w3id.org/dpv#'))
odrl = Namespace("http://www.w3.org/ns/odrl/2/")
g.namespace_manager.bind('odrl', URIRef('http://www.w3.org/ns/odrl/2/'))
oac = Namespace("https://w3id.org/oac/")
g.namespace_manager.bind('oac', URIRef('https://w3id.org/oac/'))
ex = Namespace("https://example.com/")
g.namespace_manager.bind('ex', URIRef('https://example.com/'))

g.add((ex.ex1, RDF.type, odrl.Policy))
g.add((ex.ex1, odrl.permission, BNode(value='bn1')))
g.add((BNode(value='bn1'), RDF.type, odrl.Permission))
g.add((BNode(value='bn1'), odrl.action, oac.Processing))
g.add((BNode(value='bn1'), odrl.assigner, URIRef('https://example.com/JaneDoe')))
g.add((BNode(value='bn1'), odrl.target, URIRef('https://example.com/JaneDoe/resource1')))

app = Dash(__name__)
app.layout = html.Div(
    className='wrapper',
    children=[
        html.H3('Policy editor', className='main-title'),
        html.P('DUO-ODRL-DPV policies', className='paragraph-lead'),
        html.Div(
            className='card',
            children=[
                html.H3('Data use permission', className='card-title'),
                html.P('Select purpose:', className='card-text'),
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
                ], style= {'display': 'block'})
            ]
        ),
        html.Div(
            className='card',
            children=[
                html.H3('Data use modifier', className='card-title'),
                html.P('Select secondary data use restrictions:', className='card-text'),
                dcc.RadioItems(
                    id = 'GS',
                    options=[
                        {'label': 'Not specified', 'value': 'no'},
                        {'label': 'GS Permission', 'value': 'GSPermission'},
                        {'label': 'GS Prohibition', 'value': 'GSProhibition'}
                    ],
                    value='no'
                ),
                html.Br(id='placeholder'),html.Br(),
                html.Div(
                    id='button-div',
                    children=[
                        html.A("Generate policy", id="download-btn", className='card-button'),
                        html.Br(),html.Br(),
                        html.P(id='generated', className='card-text', children=''),
                    ]
                )
            ]
        )
    ]
)

@app.callback(
   Output(component_id='disease', component_property='style'),
   [Input(component_id='data_use_permission', component_property='value')])
def show_hide_element(visibility_state):
    if visibility_state == 'DS':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('placeholder', 'children'),
              [Input(component_id='data_use_permission', component_property='value')])
def update_graph(value):
    g.add((BNode(value='bn1'), odrl.constraint, BNode(value='c1')))
    g.add((BNode(value='c1'), odrl.leftOperand, oac.Purpose))
    g.add((BNode(value='c1'), odrl.operator, odrl.isA))
    if value == "NRES":
        g.set((BNode(value='c1'), odrl.rightOperand, dpv.Purpose))
    elif value == "GRU":
        g.set((BNode(value='c1'), odrl.rightOperand, dpv.ResearchAndDevelopment))

@app.callback(Output('generated', 'children'),
              [Input('download-btn', 'n_clicks')],
              prevent_initial_call=True)
def generate_policy(n_clicks):
    g.serialize(destination='dash/policy1.ttl', format='turtle')
    return "Success"

if __name__ == '__main__':
    app.run_server(debug=True)
    