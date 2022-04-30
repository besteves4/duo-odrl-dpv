from dash import Dash, html, dcc, Input, Output
from rdflib import Graph, Namespace, URIRef, BNode
from rdflib.namespace import RDF

g = Graph()

odrl = Namespace("http://www.w3.org/ns/odrl/2/")
g.namespace_manager.bind('odrl', URIRef('http://www.w3.org/ns/odrl/2/'))
duodrl = Namespace("https://w3id.org/duodrl#")
g.namespace_manager.bind('duodrl', URIRef('https://w3id.org/duodrl#'))
obo = Namespace("http://purl.obolibrary.org/obo/")
g.namespace_manager.bind('obo', URIRef('http://purl.obolibrary.org/obo/'))

ex = Namespace("https://example.com/")
g.namespace_manager.bind('ex', URIRef('https://example.com/'))

app = Dash(__name__)
app.layout = html.Div(
    className='wrapper',
    children=[
        html.H3('Policy editor', className='main-title'),
        html.P('DUODRL policies', className='paragraph-lead'),
        html.Div(
            className='card',
            children=[
                html.H3('Data use permission', className='card-title'),
                dcc.Dropdown(
                    id = 'data_use_permission',
                    options=[
                        {'label': 'DUO_0000042 - General Research Use', 'value': 'GRU'},
                        {'label': 'DUO_0000006 - Health or Medical or Biomedical research', 'value': 'HMB'},
                        {'label': 'DUO_0000007 - Disease Specific research', 'value': 'DS'},
                        {'label': 'DUO_0000004 - No Restriction', 'value': 'NRES'},
                        {'label': 'DUO_0000011 - Population Origins or Ancestry research only', 'value': 'POA'}
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
                        value=[]
                    )
                ], style= {'display': 'block'})
            ]
        ),
        html.Div(
            className='card',
            children=[
                html.H3('Data use modifier', className='card-title'),
                dcc.Checklist(
                    id = "modifiers",
                    options = [
                        {'label': 'DUO_0000012 - research specific restrictions', 'value': 'DUO_0000012'},
                        {'label': 'DUO_0000015 - no general methods research', 'value': 'DUO_0000015'},
                        {'label': 'DUO_0000016 - genetic studies only', 'value': 'DUO_0000016'},
                        {'label': 'DUO_0000018 - not for profit, non commercial use only', 'value': 'DUO_0000018'},
                        {'label': 'DUO_0000019 - publication required', 'value': 'DUO_0000019'},
                        {'label': 'DUO_0000020 - collaboration required', 'value': 'DUO_0000020'},
                        {'label': 'DUO_0000021 - ethics approval required', 'value': 'DUO_0000021'},
                        {'label': 'DUO_0000022 - geographical restriction', 'value': 'DUO_0000022'},
                        {'label': 'DUO_0000024 - publication moratorium', 'value': 'DUO_0000024'},
                        {'label': 'DUO_0000025 - time limit on use', 'value': 'DUO_0000025'},
                        {'label': 'DUO_0000026 - user specific restriction', 'value': 'DUO_0000026'},
                        {'label': 'DUO_0000027 - project specific restriction', 'value': 'DUO_0000027'},
                        {'label': 'DUO_0000028 - institution specific restriction', 'value': 'DUO_0000028'},
                        {'label': 'DUO_0000029 - return to database or resource', 'value': 'DUO_0000029'},
                        {'label': 'DUO_0000043 - clinical care use', 'value': 'DUO_0000043'},
                        {'label': 'DUO_0000044 - population origins or ancestry research prohibited', 'value': 'DUO_0000044'},
                        {'label': 'DUO_0000045 - not for profit organisation use only', 'value': 'DUO_0000045'},
                        {'label': 'DUO_0000046 - non-commercial use only', 'value': 'DUO_0000046'}],
                    value = [],
                    labelStyle={'display': 'block'},
                    style={"width":500, "overflow":"auto"},
                    inputStyle={"margin-right": "10px"}
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
    if value == "GRU":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm')))
        g.set((BNode(value='perm'), odrl.constraint, BNode(value='perm_contraint')))
        g.set((BNode(value='perm_contraint'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='perm_contraint'), odrl.operator, odrl.isA))
        g.set((BNode(value='perm_contraint'), odrl.rightOperand, duodrl.GRU))
    elif value == "HMB":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm')))
        g.set((BNode(value='perm'), odrl.target, duodrl.TemplateDataset))
        g.set((BNode(value='perm'), odrl.constraint, BNode(value='perm_contraint')))
        g.set((BNode(value='perm_contraint'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='perm_contraint'), odrl.operator, odrl.isA))
        g.set((BNode(value='perm_contraint'), odrl.rightOperand, duodrl.HMB))
    elif value == "POA":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm')))
        g.set((BNode(value='perm'), odrl.target, duodrl.TemplateDataset))
        g.set((BNode(value='perm'), odrl.constraint, BNode(value='perm_contraint')))
        g.set((BNode(value='perm_contraint'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='perm_contraint'), odrl.operator, odrl.isA))
        g.set((BNode(value='perm_contraint'), odrl.rightOperand, duodrl.POA))
        g.add((ex.offer, odrl.prohibition, BNode(value='pro')))
        g.set((BNode(value='pro'), odrl.target, duodrl.TemplateDataset))
        g.set((BNode(value='pro'), odrl.constraint, BNode(value='pro_contraint')))
        g.set((BNode(value='pro_contraint'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='pro_contraint'), odrl.operator, duodrl.isNotA))
        g.set((BNode(value='pro_contraint'), odrl.rightOperand, duodrl.POA))
    elif value == "DS":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm')))
        g.set((BNode(value='perm'), odrl.target, duodrl.TemplateDataset))
        g.set((BNode(value='perm'), odrl.constraint, BNode(value='perm_contraint')))
        g.set((BNode(value='perm_contraint'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='perm_contraint'), odrl.operator, odrl.isA))
        g.set((BNode(value='perm_contraint'), odrl.rightOperand, obo.MONDO_0000001))
    elif value == "NRES":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm')))
        g.set((BNode(value='perm'), odrl.target, duodrl.TemplateDataset)) 
    return ;

@app.callback(Output('generated', 'children'),
              Input('download-btn', 'n_clicks'),
              prevent_initial_call=True)
def generate_policy(n_clicks):
    g.serialize(destination='dash/offer.ttl', format='turtle')
    return "Success"

if __name__ == '__main__':
    app.run_server(debug=True)
    
