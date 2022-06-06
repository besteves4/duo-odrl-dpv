from multiprocessing import Value
from dash import Dash, html, dcc, Input, Output
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF

mondo = Graph()
mondo.parse("dash/assets/test.owl", format='application/rdf+xml')

g = Graph()
restrictions = Graph()
offer = Graph()
request =  Graph()

odrl = Namespace("http://www.w3.org/ns/odrl/2/")
g.namespace_manager.bind('odrl', URIRef('http://www.w3.org/ns/odrl/2/'))
request.namespace_manager.bind('odrl', URIRef('http://www.w3.org/ns/odrl/2/'))
offer.namespace_manager.bind('odrl', URIRef('http://www.w3.org/ns/odrl/2/'))

duodrl = Namespace("https://w3id.org/duodrl#")
g.namespace_manager.bind('duodrl', URIRef('https://w3id.org/duodrl#'))
request.namespace_manager.bind('duodrl', URIRef('https://w3id.org/duodrl#'))
offer.namespace_manager.bind('duodrl', URIRef('https://w3id.org/duodrl#'))

obo = Namespace("http://purl.obolibrary.org/obo/")
g.namespace_manager.bind('obo', URIRef('http://purl.obolibrary.org/obo/'))
request.namespace_manager.bind('obo', URIRef('http://purl.obolibrary.org/obo/'))
offer.namespace_manager.bind('obo', URIRef('http://purl.obolibrary.org/obo/'))

dpv = Namespace("https://w3id.org/dpv#")
g.namespace_manager.bind('dpv', URIRef('https://w3id.org/dpv#'))
request.namespace_manager.bind('dpv', URIRef('https://w3id.org/dpv#'))
offer.namespace_manager.bind('dpv', URIRef('https://w3id.org/dpv#'))

ex = Namespace("https://example.com/")

app = Dash(__name__)
app.layout = html.Div(
    className='wrapper',
    children=[
        html.H3('Policy editor', className='main-title'),
        html.P('DUODRL policies', className='paragraph-lead'),
        html.Div(
            className='card',
            children=[
                html.H3('Target dataset', className='card-title'),
                dcc.Input(
                    id="target_dataset",
                    type="url", size="40",
                    value="https://example.com/Dataset"
                ),
                html.Br(),html.Br(),
                html.H3('Data use permission', className='card-title'),
                dcc.Dropdown(
                    id='data_use_permission',
                    options=[
                        {'label': 'DUO_0000042 - General Research Use', 'value': 'GRU'},
                        {'label': 'DUO_0000006 - Health or Medical or Biomedical research', 'value': 'HMB'},
                        {'label': 'DUO_0000007 - Disease Specific research', 'value': 'DS'},
                        {'label': 'DUO_0000004 - No Restriction', 'value': 'NRES'},
                        {'label': 'DUO_0000011 - Population Origins or Ancestry research only', 'value': 'POA'}
                    ],
                    value='NRES'
                ),
                html.Br(),
                html.Div([
                    html.A("Search MONDO code", href="https://www.ebi.ac.uk/ols/ontologies/mondo", target="_blank",
                           id="MONDO-btn", className='card-button'),
                    dcc.Input(
                        id="MONDO-code",
                        type="text", size="45",
                        value="http://purl.obolibrary.org/obo/MONDO_0002082",
                        className='card-input'
                    ),
                ], style= {'display': 'inline-block'}),
                html.Br(),html.Br(),
                html.H3('Data use modifier', className='card-title'),
                dcc.Dropdown(
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
                        {'label': 'DUO_0000046 - non-commercial use only', 'value': 'DUO_0000046'},
                        {'label': 'DPV - offer to use dataset using Consent', 'value': 'dpv'}],
                    value = [],
                    multi=True
                ),
                html.Div([
                    dcc.Dropdown(
                        id = 'research_type',
                        options=[
                            {'label': 'Genetic studies research', 'value': 'GS'},
                            {'label': 'Methods development research', 'value': 'MDS'},
                            {'label': 'Population group research', 'value': 'PGR'},
                            {'label': 'Age category research', 'value': 'ACR'},
                            {'label': 'Gender category research', 'value': 'GCR'}
                        ],
                        value=''
                    )                    
                ], style= {'display': 'block'}),
                html.Div([
                    dcc.Input(
                        id="population-group",
                        type="text", size="45",
                        placeholder="Type a specific population group...",
                        className='card-input'
                    ),                  
                ], style= {'display': 'block'}),
                html.Div([
                    dcc.Input(
                        id="age-group",
                        type="text", size="45",
                        placeholder="Type a specific age...",
                        className='card-input'
                    ),                  
                ], style= {'display': 'block'}),
                html.Div([
                    dcc.Dropdown(
                        id = 'gender-group',
                        options=[
                            {'label': 'Female', 'value': 'Female'},
                            {'label': 'Male', 'value': 'Male'}
                        ],
                        value='Female'
                    )                   
                ], style= {'display': 'block'}),
                html.Div([
                    dcc.Input(
                        id="user-name",
                        type="text", size="45",
                        placeholder="Name",
                        className='card-input'
                    ),                 
                ], style= {'display': 'block'}),
                html.Div([
                    dcc.Input(
                        id="institution-name",
                        type="text", size="45",
                        placeholder="Name",
                        className='card-input'
                    ),                 
                ], style= {'display': 'block'}),
                html.Br(id='placeholder_1'),html.Br(id='placeholder_2'),
                html.Div(
                    id='button-div',
                    children=[
                        html.A("Generate offer", id="download-btn", className='card-button'),
                        html.Br(),html.Br()
                    ]
                )
            ]
        ),
        html.Div(
            className='card',
            children=[
                html.Pre(id='generated', className='card-text', children='')
            ]
        ),
        html.Br(),html.Br(),
        html.H3('Matching demo', className='main-title'),
        html.P('Matching an odrl:Request with the odrl:Offer defined above', className='paragraph-lead'),
        html.Div(
            className='card',
            children=[
                html.H3('DUO Request', className='card-title'),
                dcc.Dropdown(
                    id = 'request',
                    options=[
                        {'label': 'DUO_0000031 - Method development - investigation concerning development of methods, algorithms, software or analytical tools', 'value': 'MDS'},
                        {'label': 'DUO_0000032 - Population research - investigation concerning a specific population group', 'value': 'PR'},
                        {'label': 'DUO_0000033 - Ancestry research - investigation concerning ancestry or population origins', 'value': 'AR'},
                        {'label': 'DUO_0000034 - Age category research - investigation concerning specific age categories', 'value': 'ACR'},
                        {'label': 'DUO_0000035 - Gender category research - investigation concerning specific gender categories', 'value': 'GCR'},
                        {'label': 'DUO_0000036 - Research control - investigation concerning use of data as reference or control material', 'value': 'RC'},
                        {'label': 'DUO_0000037 - Biomedical research - investigation concerning health, medical, or biomedical research', 'value': 'BR'},
                        {'label': 'DUO_0000038 - Genetic research - biomedical research concerning genetics (i.e., the study of genes, genetic variations and heredity)', 'value': 'GR'},
                        {'label': 'DUO_0000039 - Drug development research - biomedical research concerning drug development', 'value': 'DDR'},
                        {'label': 'DUO_0000040 - Disease category research - biomedical research research concerning specific disease(s)', 'value': 'DCR'}
                    ],
                    value='BR'
                ),
                html.Br(),
                html.Div([
                    html.A("Search MONDO code", href="https://www.ebi.ac.uk/ols/ontologies/mondo", target="_blank",
                           id="MONDO-request-btn", className='card-button'),
                    dcc.Input(
                        id="request-disease",
                        type="text", size="45",
                        value="http://purl.obolibrary.org/obo/MONDO_0002082",
                        className='card-input'
                    ),
                ], style= {'display': 'inline-block'}),
                html.Div([
                    dcc.Input(
                        id="request-population",
                        type="text", size="45",
                        placeholder="Type a specific population group...",
                        className='card-input'
                    ),
                ], style= {'display': 'block'}),
                html.Div([
                    dcc.Input(
                        id="request-age",
                        type="text", size="45",
                        placeholder="Type a specific age...",
                        className='card-input'
                    ),
                ], style= {'display': 'block'}),
                html.Div([
                    dcc.Dropdown(
                        id = 'request-gender',
                        options=[
                            {'label': 'Female', 'value': 'Female'},
                            {'label': 'Male', 'value': 'Male'}
                        ],
                        value='Female'
                    )                   
                ], style= {'display': 'block'}),
                html.Br(id='placeholder_3'),html.Br(id='placeholder_4'),
                html.H3('Requester', className='card-title'),
                dcc.Dropdown(
                    id = 'requester',
                    options=[
                        {'label': 'Non profit organisation', 'value': 'NonProfitOrganisation'},
                        {'label': 'For profit organisation', 'value': 'ForProfitOrganisation'},
                        {'label': 'User', 'value': 'User'},
                        {'label': 'Institution', 'value': 'Institution'},
                    ],
                    value='NonProfitOrganisation'
                ),
                html.Br(),
                html.Div([
                    dcc.Input(
                        id="requester-name",
                        type="text", size="45",
                        placeholder="Name",
                        className='card-input'
                    ),
                ], style= {'display': 'block'}),
                html.Br(),html.Br(),
                html.Div(
                    id='match-div',
                    children=[
                        html.A("Match", id="match-btn", className='card-button'),
                        html.Br(),html.Br()
                    ]
                )
            ]
        ),
        html.Div(
            className='card',
            children=[
                html.Pre(id='matched', className='card-text', children='')
            ]
        )
    ]
)

@app.callback(
   [Output(component_id='MONDO-code', component_property='style'),
    Output(component_id='MONDO-btn', component_property='style')],
   Input(component_id='data_use_permission', component_property='value'))
def show_hide_element(visibility_state):
    if visibility_state == 'DS':
        return {'display': 'inline-block'}, {'display': 'inline-block'}
    else:
        return {'display': 'none'}, {'display': 'none'}

@app.callback(Output('placeholder_1', 'children'),
              [Input('data_use_permission', 'value'),
               Input('target_dataset', 'value'),
               Input('MONDO-code', 'value')])
def update_graph(permission, target, mondo_code):
    if permission == "GRU":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm')))
        g.set((BNode(value='perm'), odrl.target, URIRef(target)))
        g.set((BNode(value='perm'), odrl.constraint, BNode(value='perm_contraint')))
        g.set((BNode(value='perm_contraint'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='perm_contraint'), odrl.operator, odrl.isA))
        g.set((BNode(value='perm_contraint'), odrl.rightOperand, duodrl.GRU))
    elif permission == "HMB":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm')))
        g.set((BNode(value='perm'), odrl.target, URIRef(target)))
        g.set((BNode(value='perm'), odrl.constraint, BNode(value='perm_contraint')))
        g.set((BNode(value='perm_contraint'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='perm_contraint'), odrl.operator, odrl.isA))
        g.set((BNode(value='perm_contraint'), odrl.rightOperand, duodrl.HMB))
    elif permission == "POA":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm')))
        g.set((BNode(value='perm'), odrl.target, URIRef(target)))
        g.set((BNode(value='perm'), odrl.constraint, BNode(value='perm_contraint')))
        g.set((BNode(value='perm_contraint'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='perm_contraint'), odrl.operator, odrl.isA))
        g.set((BNode(value='perm_contraint'), odrl.rightOperand, duodrl.POA))
        g.add((ex.offer, odrl.prohibition, BNode(value='pro')))
        g.set((BNode(value='pro'), odrl.target, URIRef(target)))
        g.set((BNode(value='pro'), odrl.constraint, BNode(value='pro_contraint')))
        g.set((BNode(value='pro_contraint'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='pro_contraint'), odrl.operator, duodrl.isNotA))
        g.set((BNode(value='pro_contraint'), odrl.rightOperand, duodrl.POA))
    elif permission == "DS":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm')))
        g.set((BNode(value='perm'), odrl.target, URIRef(target)))
        g.set((BNode(value='perm'), odrl.constraint, BNode(value='perm_pur')))
        g.set((BNode(value='perm_pur'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='perm_pur'), odrl.operator, odrl.isA))
        g.set((BNode(value='perm_pur'), odrl.rightOperand, duodrl.DS))
        g.add((BNode(value='perm'), odrl.constraint, BNode(value='perm_mondo')))
        g.set((BNode(value='perm_mondo'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='perm_mondo'), odrl.operator, odrl.isA))
        g.set((BNode(value='perm_mondo'), odrl.rightOperand, obo.MONDO_0000001))
        g.add((BNode(value='perm'), odrl.constraint, BNode(value='perm_disease')))
        g.set((BNode(value='perm_disease'), odrl.leftOperand, odrl.purpose))
        g.set((BNode(value='perm_disease'), odrl.operator, odrl.isA))
        g.set((BNode(value='perm_disease'), odrl.rightOperand, URIRef(mondo_code)))
    elif permission == "NRES":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm_NRES')))
        g.set((BNode(value='perm_NRES'), odrl.target, URIRef(target)))
    return ;

@app.callback(Output('research_type', 'style'),
              Input('modifiers', 'value'))
def show_research_type(modifiers):
    if len(modifiers) < 1:
        return {'display': 'none'}
    else:
        for mod in modifiers:
            if mod == "DUO_0000012":
                return {'display': 'block'}
            else:
                return {'display': 'none'}

@app.callback(
   Output('population-group', 'style'),
   [Input('modifiers', 'value'),
    Input('research_type', 'value')])
def show_hide_element(modifiers, research_type):
    if len(modifiers) < 1:
        return {'display': 'none'}
    else:
        for mod in modifiers:
            if mod == "DUO_0000012" and research_type == "PGR":
                return {'display': 'block'}
            else:
                return {'display': 'none'}
            
@app.callback(
   Output('age-group', 'style'),
   [Input('modifiers', 'value'),
    Input('research_type', 'value')])
def show_hide_element(modifiers, research_type):
    if len(modifiers) < 1:
        return {'display': 'none'}
    else:
        for mod in modifiers:
            if mod == "DUO_0000012" and research_type == "ACR":
                return {'display': 'block'}
            else:
                return {'display': 'none'}
            
@app.callback(
   Output('gender-group', 'style'),
   [Input('modifiers', 'value'),
    Input('research_type', 'value')])
def show_hide_element(modifiers, research_type):
    if len(modifiers) < 1:
        return {'display': 'none'}
    else:
        for mod in modifiers:
            if mod == "DUO_0000012" and research_type == "GCR":
                return {'display': 'block'}
            else:
                return {'display': 'none'}
       
@app.callback(Output('user-name', 'style'),
              Input('modifiers', 'value'))
def show_research_type(modifiers):
    if len(modifiers) < 1:
        return {'display': 'none'}
    else:
        for mod in modifiers:
            if mod == "DUO_0000026":
                return {'display': 'block'}
            else:
                return {'display': 'none'}

@app.callback(Output('institution-name', 'style'),
              Input('modifiers', 'value'))
def show_research_type(modifiers):
    if len(modifiers) < 1:
        return {'display': 'none'}
    else:
        for mod in modifiers:
            if mod == "DUO_0000028":
                return {'display': 'block'}
            else:
                return {'display': 'none'}

@app.callback(Output('placeholder_2', 'children'),
              [Input('modifiers', 'value'),
               Input('target_dataset', 'value'),
               Input('research_type', 'value'),
               Input('user-name', 'value'),
               Input('institution-name', 'value'),
               Input('population-group', 'value'),
               Input('age-group', 'value'),
               Input('gender-group', 'value')])
def generate_policy(modifiers, target, research, user, institution, population, age, gender):
    for v in modifiers:
        if v == "DUO_0000012":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000012_perm')))
            restrictions.add((BNode(value='DUO_0000012_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000012_perm'), odrl.constraint, BNode(value='DUO_0000012_perm_cons')))
            restrictions.add((BNode(value='DUO_0000012_perm_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000012_perm_cons'), odrl.operator, odrl.isA))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000012_pro')))
            restrictions.add((BNode(value='DUO_0000012_pro'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000012_pro'), odrl.constraint, BNode(value='DUO_0000012_pro_cons')))
            restrictions.add((BNode(value='DUO_0000012_pro_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000012_pro_cons'), odrl.operator, duodrl.isNotA))
            
            if research == "GS":
                restrictions.set((BNode(value='DUO_0000012_perm_cons'), odrl.rightOperand, duodrl.GS))
                restrictions.set((BNode(value='DUO_0000012_pro_cons'), odrl.rightOperand, duodrl.GS))
                
                restrictions.remove((BNode(value='perm_value'), None, None))
                restrictions.remove((BNode(value='pro_value'), None, None))
                restrictions.remove((None, None, BNode(value='perm_value')))
                restrictions.remove((None, None, BNode(value='pro_value')))
            elif research == "MDS":
                restrictions.set((BNode(value='DUO_0000012_perm_cons'), odrl.rightOperand, duodrl.MDS))
                restrictions.set((BNode(value='DUO_0000012_pro_cons'), odrl.rightOperand, duodrl.MDS))
                
                restrictions.remove((BNode(value='perm_value'), None, None))
                restrictions.remove((BNode(value='pro_value'), None, None))
                restrictions.remove((None, None, BNode(value='perm_value')))
                restrictions.remove((None, None, BNode(value='pro_value')))
            elif research == "PGR":
                restrictions.set((BNode(value='DUO_0000012_perm_cons'), odrl.rightOperand, duodrl.PopulationGroupResearch))
                restrictions.set((BNode(value='DUO_0000012_pro_cons'), odrl.rightOperand, duodrl.PopulationGroupResearch))
                
                restrictions.add((BNode(value='DUO_0000012_perm'), odrl.constraint, BNode(value='perm_value')))
                restrictions.set((BNode(value='perm_value'), odrl.leftOperand, odrl.purpose))
                restrictions.set((BNode(value='perm_value'), odrl.operator, odrl.isA))
                restrictions.set((BNode(value='perm_value'), odrl.rightOperand, Literal(population)))
                
                restrictions.add((BNode(value='DUO_0000012_pro'), odrl.constraint, BNode(value='pro_value')))
                restrictions.set((BNode(value='pro_value'), odrl.leftOperand, odrl.purpose))
                restrictions.set((BNode(value='pro_value'), odrl.operator, duodrl.isNotA))
                restrictions.set((BNode(value='pro_value'), odrl.rightOperand, Literal(population)))
            elif research == "ACR":
                restrictions.set((BNode(value='DUO_0000012_perm_cons'), odrl.rightOperand, duodrl.AgeCategoryResearch))
                restrictions.set((BNode(value='DUO_0000012_pro_cons'), odrl.rightOperand, duodrl.AgeCategoryResearch))
                
                restrictions.add((BNode(value='DUO_0000012_perm'), odrl.constraint, BNode(value='perm_value')))
                restrictions.set((BNode(value='perm_value'), odrl.leftOperand, odrl.purpose))
                restrictions.set((BNode(value='perm_value'), odrl.operator, odrl.isA))
                restrictions.set((BNode(value='perm_value'), odrl.rightOperand, Literal(age)))
                
                restrictions.add((BNode(value='DUO_0000012_pro'), odrl.constraint, BNode(value='pro_value')))
                restrictions.set((BNode(value='pro_value'), odrl.leftOperand, odrl.purpose))
                restrictions.set((BNode(value='pro_value'), odrl.operator, duodrl.isNotA))
                restrictions.set((BNode(value='pro_value'), odrl.rightOperand, Literal(age)))
            elif research == "GCR":
                restrictions.set((BNode(value='DUO_0000012_perm_cons'), odrl.rightOperand, duodrl.GenderCategoryResearch))
                restrictions.set((BNode(value='DUO_0000012_pro_cons'), odrl.rightOperand, duodrl.GenderCategoryResearch))
                
                restrictions.add((BNode(value='DUO_0000012_perm'), odrl.constraint, BNode(value='perm_value')))
                restrictions.set((BNode(value='perm_value'), odrl.leftOperand, odrl.purpose))
                restrictions.set((BNode(value='perm_value'), odrl.operator, odrl.isA))
                restrictions.set((BNode(value='perm_value'), odrl.rightOperand, Literal(gender)))
                
                restrictions.add((BNode(value='DUO_0000012_pro'), odrl.constraint, BNode(value='pro_value')))
                restrictions.set((BNode(value='pro_value'), odrl.leftOperand, odrl.purpose))
                restrictions.set((BNode(value='pro_value'), odrl.operator, duodrl.isNotA))
                restrictions.set((BNode(value='pro_value'), odrl.rightOperand, Literal(gender)))
                           
        elif v == "DUO_0000015":
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000015_pro')))
            restrictions.add((BNode(value='DUO_0000015_pro'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000015_pro'), odrl.constraint, BNode(value='DUO_0000015_pro_cons')))
            restrictions.add((BNode(value='DUO_0000015_pro_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000015_pro_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000015_pro_cons'), odrl.rightOperand, duodrl.MDS))
        elif v == "DUO_0000016":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000016_perm')))
            restrictions.add((BNode(value='DUO_0000016_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000016_perm'), odrl.constraint, BNode(value='DUO_0000016_perm_cons')))
            restrictions.add((BNode(value='DUO_0000016_perm_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000016_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000016_perm_cons'), odrl.rightOperand, duodrl.GS))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000016_pro')))
            restrictions.add((BNode(value='DUO_0000016_pro'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000016_pro'), odrl.constraint, BNode(value='DUO_0000016_pro_cons')))
            restrictions.add((BNode(value='DUO_0000016_pro_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000016_pro_cons'), odrl.operator, duodrl.isNotA))
            restrictions.add((BNode(value='DUO_0000016_pro_cons'), odrl.rightOperand, duodrl.GS))
        elif v == "DUO_0000018":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000018_perm')))
            restrictions.add((BNode(value='DUO_0000018_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000018_perm'), odrl.constraint, BNode(value='DUO_0000018_perm_cons')))
            restrictions.add((BNode(value='DUO_0000018_perm_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000018_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000018_perm_cons'), odrl.rightOperand, duodrl.NCU))
            restrictions.add((BNode(value='DUO_0000018_perm'), odrl.assignee, BNode(value='DUO_0000018_perm_assignee')))
            restrictions.add((BNode(value='DUO_0000018_perm_assignee'), RDF.type, odrl.Party))
            restrictions.add((BNode(value='DUO_0000018_perm_assignee'), obo.DUO_0000010, duodrl.NonProfitOrganisation))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000018_pro')))
            restrictions.add((BNode(value='DUO_0000018_pro'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000018_pro'), odrl.constraint, BNode(value='DUO_0000018_pro_cons')))
            restrictions.add((BNode(value='DUO_0000018_pro_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000018_pro_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000018_pro_cons'), odrl.rightOperand, duodrl.NCU))
            restrictions.add((BNode(value='DUO_0000018_pro'), odrl.assignee, BNode(value='DUO_0000018_pro_assignee')))
            restrictions.add((BNode(value='DUO_0000018_pro_assignee'), RDF.type, odrl.Party))
            restrictions.add((BNode(value='DUO_0000018_pro_assignee'), obo.DUO_0000010, duodrl.ForProfitOrganisation))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000018_pro_2')))
            restrictions.add((BNode(value='DUO_0000018_pro_2'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000018_pro_2'), odrl.constraint, BNode(value='DUO_0000018_pro_2_cons')))
            restrictions.add((BNode(value='DUO_0000018_pro_2_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000018_pro_2_cons'), odrl.operator, duodrl.isNotA))
            restrictions.add((BNode(value='DUO_0000018_pro_2_cons'), odrl.rightOperand, duodrl.NCU))
            restrictions.add((BNode(value='DUO_0000018_pro_2'), odrl.assignee, BNode(value='DUO_0000018_pro_2_assignee')))
            restrictions.add((BNode(value='DUO_0000018_pro_2_assignee'), RDF.type, odrl.Party))
            restrictions.add((BNode(value='DUO_0000018_pro_2_assignee'), obo.DUO_0000010, duodrl.NonProfitOrganisation))
        elif v == "DUO_0000019":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000019_perm')))
            restrictions.add((BNode(value='DUO_0000019_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000019_perm'), odrl.duty, BNode(value='DUO_0000019_perm_duty')))
            restrictions.add((BNode(value='DUO_0000019_perm_duty'), odrl.action, odrl.distribute))
            restrictions.add((BNode(value='DUO_0000019_perm_duty'), odrl.output, duodrl.ResultsOfStudies))
        elif v == "DUO_0000020":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000020_perm')))
            restrictions.add((BNode(value='DUO_0000020_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000020_perm'), odrl.duty, BNode(value='DUO_0000020_perm_duty')))
            restrictions.add((BNode(value='DUO_0000020_perm_duty'), odrl.action, duodrl.CollaborateWithStudyPI))
            restrictions.add((BNode(value='DUO_0000020_perm_duty'), odrl.constraint, BNode(value='DUO_0000020_perm_duty_cons')))
            restrictions.add((BNode(value='DUO_0000020_perm_duty_cons'), odrl.leftOperand, odrl.event))
            restrictions.add((BNode(value='DUO_0000020_perm_duty_cons'), odrl.operator, odrl.lt))
            restrictions.add((BNode(value='DUO_0000020_perm_duty_cons'), odrl.rightOperand, odrl.policyUsage))
        elif v == "DUO_0000021":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000021_perm')))
            restrictions.add((BNode(value='DUO_0000021_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000021_perm'), odrl.duty, BNode(value='DUO_0000021_perm_duty')))
            restrictions.add((BNode(value='DUO_0000021_perm_duty'), odrl.action, duodrl.ProvideEthicalApproval))
        elif v == "DUO_0000022":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000022_perm')))
            restrictions.add((BNode(value='DUO_0000022_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000022_perm'), odrl.constraint, BNode(value='DUO_0000022_perm_cons')))
            restrictions.add((BNode(value='DUO_0000022_perm_cons'), odrl.leftOperand, odrl.spatial))
            restrictions.add((BNode(value='DUO_0000022_perm_cons'), odrl.operator, odrl.lteq))
            restrictions.add((BNode(value='DUO_0000022_perm_cons'), odrl.rightOperand, duodrl.TemplateLocation))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000022_pro')))
            restrictions.add((BNode(value='DUO_0000022_pro'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000022_pro'), odrl.constraint, BNode(value='DUO_0000022_pro_cons')))
            restrictions.add((BNode(value='DUO_0000022_pro_cons'), odrl.leftOperand, odrl.spatial))
            restrictions.add((BNode(value='DUO_0000022_pro_cons'), odrl.operator, odrl.gt))
            restrictions.add((BNode(value='DUO_0000022_pro_cons'), odrl.rightOperand, duodrl.TemplateLocation))
        elif v == "DUO_0000024":
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000024_pro')))
            restrictions.add((BNode(value='DUO_0000024_pro'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000024_pro'), odrl.action, odrl.distribute))
            restrictions.add((BNode(value='DUO_0000024_pro'), odrl.output, duodrl.ResultsOfStudies))
            restrictions.add((BNode(value='DUO_0000024_pro'), odrl.constraint, BNode(value='DUO_0000024_pro_cons')))
            restrictions.add((BNode(value='DUO_0000024_pro_cons'), odrl.leftOperand, odrl.dateTime))
            restrictions.add((BNode(value='DUO_0000024_pro_cons'), odrl.operator, odrl.lt))
            restrictions.add((BNode(value='DUO_0000024_pro_cons'), odrl.rightOperand, duodrl.TemplateStudyResultsPublicationDate))
        elif v == "DUO_0000025":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000025_perm')))
            restrictions.add((BNode(value='DUO_0000025_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000025_perm'), odrl.constraint, BNode(value='DUO_0000025_perm_cons')))
            restrictions.add((BNode(value='DUO_0000025_perm_cons'), odrl.leftOperand, odrl.dateTime))
            restrictions.add((BNode(value='DUO_0000025_perm_cons'), odrl.operator, odrl.lteq))
            restrictions.add((BNode(value='DUO_0000025_perm_cons'), odrl.rightOperand, duodrl.TemplateTimeLimit))
        elif v == "DUO_0000026":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000026_perm')))
            restrictions.add((BNode(value='DUO_0000026_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000026_perm'), odrl.assignee, BNode(value='DUO_0000026_perm_assignee')))
            restrictions.add((BNode(value='DUO_0000026_perm_assignee'), RDF.type, odrl.Party))
            restrictions.set((BNode(value='DUO_0000026_perm_assignee'), obo.DUO_0000010, Literal(user)))
        elif v == "DUO_0000027":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000027_perm')))
            restrictions.add((BNode(value='DUO_0000027_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000027_perm'), odrl.constraint, BNode(value='DUO_0000027_perm_cons')))
            restrictions.add((BNode(value='DUO_0000027_perm_cons'), odrl.leftOperand, duodrl.Project))
            restrictions.add((BNode(value='DUO_0000027_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000027_perm_cons'), odrl.rightOperand, duodrl.TemplateProject))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000027_pro')))
            restrictions.add((BNode(value='DUO_0000027_pro'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000027_pro'), odrl.constraint, BNode(value='DUO_0000027_pro_cons')))
            restrictions.add((BNode(value='DUO_0000027_pro_cons'), odrl.leftOperand, duodrl.Project))
            restrictions.add((BNode(value='DUO_0000027_pro_cons'), odrl.operator, duodrl.isNotA))
            restrictions.add((BNode(value='DUO_0000027_pro_cons'), odrl.rightOperand, duodrl.TemplateProject))
        elif v == "DUO_0000028":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000028_perm')))
            restrictions.add((BNode(value='DUO_0000028_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000028_perm'), odrl.assignee, BNode(value='DUO_0000028_perm_assignee')))
            restrictions.add((BNode(value='DUO_0000028_perm_assignee'), RDF.type, odrl.Party))
            restrictions.set((BNode(value='DUO_0000028_perm_assignee'), obo.DUO_0000010, Literal(institution)))
        elif v == "DUO_0000029":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000029_perm')))
            restrictions.add((BNode(value='DUO_0000029_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000029_perm'), odrl.duty, BNode(value='DUO_0000029_perm_duty')))
            restrictions.add((BNode(value='DUO_0000029_perm_duty'), odrl.action, duodrl.ReturnDerivedOrEnrichedData))
        elif v == "DUO_0000043":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000043_perm')))
            restrictions.add((BNode(value='DUO_0000043_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000043_perm'), odrl.constraint, BNode(value='DUO_0000043_perm_cons')))
            restrictions.add((BNode(value='DUO_0000043_perm_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000043_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000043_perm_cons'), odrl.rightOperand, duodrl.CC))
        elif v == "DUO_0000044":
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000044_pro')))
            restrictions.add((BNode(value='DUO_0000044_pro'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000044_pro'), odrl.constraint, BNode(value='DUO_0000044_pro_cons')))
            restrictions.add((BNode(value='DUO_0000044_pro_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000044_pro_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000044_pro_cons'), odrl.rightOperand, duodrl.POA))
        elif v == "DUO_0000045":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000045_perm')))
            restrictions.add((BNode(value='DUO_0000045_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000045_perm'), odrl.assignee, BNode(value='DUO_0000045_perm_assignee')))
            restrictions.add((BNode(value='DUO_0000045_perm_assignee'), RDF.type, odrl.Party))
            restrictions.add((BNode(value='DUO_0000045_perm_assignee'), obo.DUO_0000010, duodrl.NonProfitOrganisation))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000045_pro')))
            restrictions.add((BNode(value='DUO_0000045_pro'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000045_pro'), odrl.assignee, BNode(value='DUO_0000045_pro_assignee')))
            restrictions.add((BNode(value='DUO_0000045_pro_assignee'), RDF.type, odrl.Party))
            restrictions.add((BNode(value='DUO_0000045_pro_assignee'), obo.DUO_0000010, duodrl.ForProfitOrganisation))
        elif v == "DUO_0000046":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000046_perm')))
            restrictions.add((BNode(value='DUO_0000046_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000046_perm'), odrl.constraint, BNode(value='DUO_0000046_perm_cons')))
            restrictions.add((BNode(value='DUO_0000046_perm_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000046_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000046_perm_cons'), odrl.rightOperand, duodrl.NCU))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000046_pro')))
            restrictions.add((BNode(value='DUO_0000046_pro'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000046_pro'), odrl.constraint, BNode(value='DUO_0000046_pro_cons')))
            restrictions.add((BNode(value='DUO_0000046_pro_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000046_pro_cons'), odrl.operator, duodrl.isNotA))
            restrictions.add((BNode(value='DUO_0000046_pro_cons'), odrl.rightOperand, duodrl.NCU))
        elif v == "dpv":
            restrictions.add((ex.offer, odrl.permission, BNode(value='dpv_perm')))
            restrictions.add((BNode(value='dpv_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='dpv_perm'), odrl.constraint, BNode(value='dpv_perm_cons')))
            restrictions.add((BNode(value='dpv_perm_cons'), odrl.leftOperand, dpv.hasLegalBasis))
            restrictions.add((BNode(value='dpv_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='dpv_perm_cons'), odrl.rightOperand, dpv.Consent))
    return ;

@app.callback([Output('generated', 'children'),
               Output('data_use_permission', 'value'),
               Output('modifiers', 'value'),],
              [Input('download-btn', 'n_clicks')],
              prevent_initial_call=True)
def generate_policy(n_clicks):
    for res in iter(restrictions):
        g.add(res)
    offer.remove((None, None, None))
    for triple in iter(g):
        offer.add(triple)
    g.serialize(destination='dash/offer.ttl', format='turtle')
    a = g.serialize(format='turtle').decode("utf-8")
    g.remove((None, None, None))
    restrictions.remove((None, None, None))
    return a, '', []

@app.callback(
   [Output('request-disease', 'style'),
    Output('MONDO-request-btn', 'style')],
   Input('request', 'value'))
def show_hide_element(request):
    if request == 'DCR':
        return {'display': 'inline-block'}, {'display': 'inline-block'}
    else:
        return {'display': 'none'}, {'display': 'none'}

@app.callback(
   Output('request-population', 'style'),
   Input('request', 'value'))
def show_hide_element(request):
    if request == 'PR':
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    
@app.callback(
   Output('request-age', 'style'),
   Input('request', 'value'))
def show_hide_element(request):
    if request == 'ACR':
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    
@app.callback(
   Output('request-gender', 'style'),
   Input('request', 'value'))
def show_hide_element(request):
    if request == 'GCR':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
   Output('requester-name', 'style'),
   Input('requester', 'value'))
def show_hide_element(requester):
    if requester == 'User' or requester == 'Institution':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('placeholder_3', 'children'),
              [Input('request', 'value'),
               Input('request-disease', 'value'),
               Input('requester', 'value'),
               Input('requester-name', 'value'),
               Input('request-population', 'value'),
               Input('request-age', 'value'),
               Input('request-gender', 'value')])
def generate_request(value, disease, requester, name, population, age, gender):
    if value == "MDS":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='perm')))
        request.set((BNode(value='perm'), odrl.constraint, BNode(value='MD_perm_cons')))
        request.set((BNode(value='MD_perm_cons'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='MD_perm_cons'), odrl.operator, odrl.isA))
        request.set((BNode(value='MD_perm_cons'), odrl.rightOperand, duodrl.MDS))
    elif value == "PR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='perm')))
        request.set((BNode(value='perm'), odrl.constraint, BNode(value='PR_perm_pur')))
        request.set((BNode(value='PR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='PR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='PR_perm_pur'), odrl.rightOperand, duodrl.PopulationGroupResearch))
        request.add((BNode(value='perm'), odrl.constraint, BNode(value='PR_perm_group')))
        request.set((BNode(value='PR_perm_group'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='PR_perm_group'), odrl.operator, odrl.isA))
        request.set((BNode(value='PR_perm_group'), odrl.rightOperand, Literal(population)))
    elif value == "AR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='perm')))
        request.set((BNode(value='perm'), odrl.constraint, BNode(value='AR_perm_cons')))
        request.set((BNode(value='AR_perm_cons'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='AR_perm_cons'), odrl.operator, odrl.isA))
        request.set((BNode(value='AR_perm_cons'), odrl.rightOperand, duodrl.POA))
    elif value == "ACR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='perm')))
        request.set((BNode(value='perm'), odrl.constraint, BNode(value='ACR_perm_pur')))
        request.set((BNode(value='ACR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='ACR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='ACR_perm_pur'), odrl.rightOperand, duodrl.AgeCategoryResearch))
        request.add((BNode(value='perm'), odrl.constraint, BNode(value='ACR_perm_age')))
        request.set((BNode(value='ACR_perm_age'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='ACR_perm_age'), odrl.operator, odrl.isA))
        request.set((BNode(value='ACR_perm_age'), odrl.rightOperand, Literal(age)))
    elif value == "GCR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='perm')))
        request.set((BNode(value='perm'), odrl.constraint, BNode(value='GCR_perm_pur')))
        request.set((BNode(value='GCR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='GCR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='GCR_perm_pur'), odrl.rightOperand, duodrl.GenderCategoryResearch))
        request.add((BNode(value='perm'), odrl.constraint, BNode(value='GCR_perm_gender')))
        request.set((BNode(value='GCR_perm_gender'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='GCR_perm_gender'), odrl.operator, odrl.isA))
        request.set((BNode(value='GCR_perm_gender'), odrl.rightOperand, Literal(gender)))
    elif value == "RC":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='perm')))
        request.set((BNode(value='perm'), odrl.constraint, BNode(value='RC_perm_pur')))
        request.set((BNode(value='RC_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='RC_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='RC_perm_pur'), odrl.rightOperand, duodrl.ResearchControl))
    elif value == "BR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='perm')))
        request.set((BNode(value='perm'), odrl.constraint, BNode(value='BR_perm_pur')))
        request.set((BNode(value='BR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='BR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='BR_perm_pur'), odrl.rightOperand, duodrl.HMB))
    elif value == "GR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='perm')))
        request.set((BNode(value='perm'), odrl.constraint, BNode(value='GR_perm_pur')))
        request.set((BNode(value='GR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='GR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='GR_perm_pur'), odrl.rightOperand, duodrl.GS))
    elif value == "DDR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='perm')))
        request.set((BNode(value='perm'), odrl.constraint, BNode(value='DDR_perm_pur')))
        request.set((BNode(value='DDR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='DDR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='DDR_perm_pur'), odrl.rightOperand, duodrl.DrugDevelopment))
    elif value == "DCR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='perm')))
        request.set((BNode(value='perm'), odrl.constraint, BNode(value='DCR_perm_pur')))
        request.set((BNode(value='DCR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='DCR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='DCR_perm_pur'), odrl.rightOperand, duodrl.DS))
        request.add((BNode(value='perm'), odrl.constraint, BNode(value='DCR_perm_mondo')))
        request.set((BNode(value='DCR_perm_mondo'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='DCR_perm_mondo'), odrl.operator, odrl.isA))
        request.set((BNode(value='DCR_perm_mondo'), odrl.rightOperand, obo.MONDO_0000001))
        request.add((BNode(value='perm'), odrl.constraint, BNode(value='DCR_perm_disease')))
        request.set((BNode(value='DCR_perm_disease'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='DCR_perm_disease'), odrl.operator, odrl.isA))
        request.set((BNode(value='DCR_perm_disease'), odrl.rightOperand, URIRef(disease)))
        
    if requester == "NonProfitOrganisation":
        request.set((BNode(value='perm'), odrl.assignee, BNode(value='assignee')))
        request.set((BNode(value='assignee'), RDF.type, odrl.Party))
        request.set((BNode(value='assignee'), obo.DUO_0000010, duodrl.NonProfitOrganisation))
    elif requester == "ForProfitOrganisation":
        request.set((BNode(value='perm'), odrl.assignee, BNode(value='assignee')))
        request.set((BNode(value='assignee'), RDF.type, odrl.Party))
        request.set((BNode(value='assignee'), obo.DUO_0000010, duodrl.ForProfitOrganisation))
    elif requester == "User":
        request.set((BNode(value='perm'), odrl.assignee, BNode(value='assignee')))
        request.set((BNode(value='assignee'), RDF.type, odrl.Party))
        request.set((BNode(value='assignee'), obo.DUO_0000010, Literal(name)))
    elif requester == "Institution":
        request.set((BNode(value='perm'), odrl.assignee, BNode(value='assignee')))
        request.set((BNode(value='assignee'), RDF.type, odrl.Party))
        request.set((BNode(value='assignee'), obo.DUO_0000010, Literal(name)))
    return ;

@app.callback(Output('matched', 'children'),
              Input('match-btn', 'n_clicks'),
              prevent_initial_call=True)
def generate_match(n_clicks):
    for purpose_request in request.objects(predicate=odrl.rightOperand):
        if "Template" not in purpose_request and "MONDO_0000001" not in purpose_request and "https://w3id.org/duodrl#DS" not in purpose_request and "http" in purpose_request:
            # print(purpose_request)
            for prohibition in offer.objects(predicate=odrl.prohibition):
                for object_prohibition in offer.objects(subject=BNode(value=prohibition), predicate=odrl.constraint):
                    for purpose_assignee in request.objects(predicate=odrl.assignee):
                        get_offer_assignee = offer.value(subject=BNode(value=prohibition), predicate=odrl.assignee, object=None, default="no_assignee")
                        offer_assignee = offer.value(subject=BNode(value=get_offer_assignee), predicate=obo.DUO_0000010, object=None, default="no_assignee")
                        request_assignee = request.value(subject=BNode(value=purpose_assignee), predicate=obo.DUO_0000010, object=None, default="no_assignee")
                        
                        leftOperand_offer_prohibition = offer.value(subject=object_prohibition, predicate=odrl.leftOperand, object=None, default="no_prohibition")
                        operator_offer_prohibition = offer.value(subject=object_prohibition, predicate=odrl.operator, object=None, default="no_prohibition")
                        rightOperand_offer_prohibition = offer.value(subject=object_prohibition, predicate=odrl.rightOperand, object=None, default="no_prohibition")
                        
                        if "http" in rightOperand_offer_prohibition:
                            # print(rightOperand_offer_prohibition)
                            if "ForProfitOrganisation" in request_assignee and "ForProfitOrganisation" in offer_assignee and "isA" in operator_offer_prohibition and "NCU" in rightOperand_offer_prohibition and purpose_request==rightOperand_offer_prohibition:
                                return "Access denied"
                            elif "NonProfitOrganisation" in request_assignee and "NonProfitOrganisation" in offer_assignee and "isNotA" in operator_offer_prohibition and "NCU" in rightOperand_offer_prohibition and purpose_request!=rightOperand_offer_prohibition:
                                return "Access denied"
                            elif "NonProfitOrganisation" in request_assignee and "NonProfitOrganisation" in offer_assignee:
                                return "Access denied"
                            elif "ForProfitOrganisation" in request_assignee and "ForProfitOrganisation" in offer_assignee:
                                return "Access denied"
                            elif "purpose" in leftOperand_offer_prohibition and "isNotA" in operator_offer_prohibition and purpose_request!=rightOperand_offer_prohibition:
                                return "Access denied"
                            elif "purpose" in leftOperand_offer_prohibition and "isA" in operator_offer_prohibition and purpose_request==rightOperand_offer_prohibition:
                                return "Access denied"
                        
            access = ""
            duty = ""
            for permission in offer.objects(predicate=odrl.permission):
                constraint = offer.value(subject=BNode(value=permission), predicate=odrl.constraint, object=None, default="no_constraint")
                permission_duty = offer.value(subject=BNode(value=permission), predicate=odrl.duty, object=None, default="no_duty")
                assignee = offer.value(subject=BNode(value=permission), predicate=odrl.assignee, object=None, default="no_assignee")
                
                if constraint == "no_constraint" and permission_duty == "no_duty" and assignee == "no_assignee":
                    access = "Access authorized"
                elif constraint == "no_constraint" and permission_duty != "no_duty":
                    duty_action = offer.value(subject=BNode(value=permission_duty), predicate=odrl.action, object=None)
                    access = "Access authorized"
                    if "distribute" in duty_action:
                        duty = " and the requestor has a duty to make results of the study available to the larger scientific community"
                    elif "CollaborateWithStudyPI" in duty_action:
                        duty = " and the requestor has a duty to collaborate with the primary study investigator(s)"
                    elif "ProvideEthicalApproval" in duty_action:
                        duty = " and the requestor has a duty to provide documentation of local IRB/ERB approval"
                    elif "ReturnDerivedOrEnrichedData" in duty_action:
                        duty = " and the requestor has a duty to return derived/enriched data to the database/resource"
                elif constraint == "no_constraint" and assignee != "no_assignee":
                    offer_assignee = offer.value(subject=BNode(value=assignee), predicate=obo.DUO_0000010, object=None)
                    request_assignee = request.value(subject=BNode(value="assignee"), predicate=obo.DUO_0000010, object=None)
                    if "ForProfitOrganisation" not in request_assignee and "NonProfitOrganisation" not in request_assignee:
                        if request_assignee==offer_assignee:
                            access = "Access authorized"
                        else:
                            access = "Access denied"
                elif constraint != "no_constraint":
                    for object_permission in offer.objects(subject=BNode(value=permission), predicate=odrl.constraint):
                        leftOperand_offer_permission = offer.value(subject=object_permission, predicate=odrl.leftOperand, object=None)
                        operator_offer_permission = offer.value(subject=object_permission, predicate=odrl.operator, object=None)
                        rightOperand_offer_permission = offer.value(subject=object_permission, predicate=odrl.rightOperand, object=None)
                        
                        if assignee=="no_assignee":
                            if "purpose" in leftOperand_offer_permission and "isA" in operator_offer_permission and "Template" not in rightOperand_offer_permission and "MONDO_0000001" not in rightOperand_offer_permission and "https://w3id.org/duodrl#DS" not in rightOperand_offer_permission:
                                if "MONDO" in purpose_request:
                                    knows_query = "SELECT ?parent WHERE {<" + rightOperand_offer_permission + "> rdfs:subClassOf* ?parent }"
                                    results = mondo.query(knows_query)
                                    diseases = []
                                    for row in results:
                                        diseases.append(row.parent)
                                    if purpose_request in diseases:
                                        access = "Access authorized"
                                    elif "HMB" in rightOperand_offer_permission or "GRU" in rightOperand_offer_permission:
                                        access = "Access authorized"
                                elif purpose_request == rightOperand_offer_permission:
                                    if "PopulationGroupResearch" in purpose_request:
                                        population_offer = offer.value(subject=BNode(value='perm_value'), predicate=odrl.rightOperand, object=None)
                                        population_request = request.value(subject=BNode(value='PR_perm_group'), predicate=odrl.rightOperand, object=None)
                                        if population_offer == population_request:
                                            access = "Access authorized"
                                        else:
                                            access = "Access denied"
                                    elif "AgeCategoryResearch" in purpose_request:
                                        age_offer = offer.value(subject=BNode(value='perm_value'), predicate=odrl.rightOperand, object=None)
                                        age_request = request.value(subject=BNode(value='ACR_perm_age'), predicate=odrl.rightOperand, object=None)
                                        if age_offer == age_request:
                                            access = "Access authorized"
                                        else:
                                            access = "Access denied"
                                    elif "GenderCategoryResearch" in purpose_request:
                                        gender_offer = offer.value(subject=BNode(value='perm_value'), predicate=odrl.rightOperand, object=None)
                                        gender_request = request.value(subject=BNode(value='GCR_perm_gender'), predicate=odrl.rightOperand, object=None)
                                        if gender_offer == gender_request:
                                            access = "Access authorized"
                                        else:
                                            access = "Access denied"
                                    else:
                                        access = "Access authorized"
                                elif "MDS" in purpose_request:
                                    access = "Access authorized"
                                elif "ResearchControl" in purpose_request:
                                    if "HMB" in rightOperand_offer_permission or "GRU" in rightOperand_offer_permission:
                                        access = "Access authorized"
                                    else:
                                        access = "Access denied"
                                elif "POA" in purpose_request:
                                    if "GRU" in rightOperand_offer_permission:
                                        access = "Access authorized"
                                    else:
                                        access = "Access denied"
                                elif "HMB" in purpose_request:
                                    if "GRU" in rightOperand_offer_permission:
                                        access = "Access authorized"
                                    else:
                                        access = "Access denied"
                                else:
                                    access = "Access denied"
                        else:
                            offer_assignee = offer.value(subject=BNode(value=assignee), predicate=obo.DUO_0000010, object=None)
                            request_assignee = request.value(subject=BNode(value="assignee"), predicate=obo.DUO_0000010, object=None)
                            if "ForProfitOrganisation" not in request_assignee and "NonProfitOrganisation" not in request_assignee and request_assignee==offer_assignee:
                                if "purpose" in leftOperand_offer_permission and "isA" in operator_offer_permission and "Template" not in rightOperand_offer_permission and "MONDO_0000001" not in rightOperand_offer_permission and "https://w3id.org/duodrl#DS" not in rightOperand_offer_permission:
                                    if "MONDO" in purpose_request:
                                        knows_query = "SELECT ?parent WHERE {<" + rightOperand_offer_permission + "> rdfs:subClassOf* ?parent }"
                                        results = mondo.query(knows_query)
                                        diseases = []
                                        for row in results:
                                            diseases.append(row.parent)
                                        if purpose_request in diseases:
                                            access = "Access authorized"
                                        elif "HMB" in rightOperand_offer_permission or "GRU" in rightOperand_offer_permission:
                                            access = "Access authorized"
                                    elif purpose_request == rightOperand_offer_permission:
                                        if "PopulationGroupResearch" in purpose_request:
                                            population_offer = offer.value(subject=BNode(value='perm_value'), predicate=odrl.rightOperand, object=None)
                                            population_request = request.value(subject=BNode(value='PR_perm_group'), predicate=odrl.rightOperand, object=None)
                                            if population_offer == population_request:
                                                access = "Access authorized"
                                            else:
                                                access = "Access denied"
                                        elif "AgeCategoryResearch" in purpose_request:
                                            age_offer = offer.value(subject=BNode(value='perm_value'), predicate=odrl.rightOperand, object=None)
                                            age_request = request.value(subject=BNode(value='ACR_perm_age'), predicate=odrl.rightOperand, object=None)
                                            if age_offer == age_request:
                                                access = "Access authorized"
                                            else:
                                                access = "Access denied"
                                        elif "GenderCategoryResearch" in purpose_request:
                                            gender_offer = offer.value(subject=BNode(value='perm_value'), predicate=odrl.rightOperand, object=None)
                                            gender_request = request.value(subject=BNode(value='GCR_perm_gender'), predicate=odrl.rightOperand, object=None)
                                            if gender_offer == gender_request:
                                                access = "Access authorized"
                                            else:
                                                access = "Access denied"
                                        else:
                                            access = "Access authorized"
                                    elif "MDS" in purpose_request:
                                        access = "Access authorized"
                                    elif "ResearchControl" in purpose_request:
                                        if "HMB" in rightOperand_offer_permission or "GRU" in rightOperand_offer_permission:
                                            access = "Access authorized"
                                        else:
                                            access = "Access denied"
                                    elif "POA" in purpose_request:
                                        if "GRU" in rightOperand_offer_permission:
                                            access = "Access authorized"
                                        else:
                                            access = "Access denied"
                                    elif "HMB" in purpose_request:
                                        if "GRU" in rightOperand_offer_permission:
                                            access = "Access authorized"
                                        else:
                                            access = "Access denied"
                                    else:
                                        access = "Access denied"
            return access + duty
    return ;

if __name__ == '__main__':
    app.run_server(debug=True)
    