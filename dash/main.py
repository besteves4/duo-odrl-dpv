from multiprocessing import Value
from dash import Dash, html, dcc, Input, Output
from rdflib import Graph, Namespace, URIRef, BNode
from rdflib.namespace import RDF

g = Graph()
restrictions = Graph()
request =  Graph()

odrl = Namespace("http://www.w3.org/ns/odrl/2/")
g.namespace_manager.bind('odrl', URIRef('http://www.w3.org/ns/odrl/2/'))
request.namespace_manager.bind('odrl', URIRef('http://www.w3.org/ns/odrl/2/'))

duodrl = Namespace("https://w3id.org/duodrl#")
g.namespace_manager.bind('duodrl', URIRef('https://w3id.org/duodrl#'))
request.namespace_manager.bind('duodrl', URIRef('https://w3id.org/duodrl#'))

obo = Namespace("http://purl.obolibrary.org/obo/")
g.namespace_manager.bind('obo', URIRef('http://purl.obolibrary.org/obo/'))
request.namespace_manager.bind('obo', URIRef('http://purl.obolibrary.org/obo/'))

dpv = Namespace("https://w3id.org/dpv#")
g.namespace_manager.bind('dpv', URIRef('https://w3id.org/dpv#'))
request.namespace_manager.bind('dpv', URIRef('https://w3id.org/dpv#'))

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
                    dcc.Dropdown(
                        id = 'disease',
                        options=[
                            {'label': 'Uveal Melanoma', 'value': 'uveal_melanoma'},
                            {'label': 'Melanoma', 'value': 'melanoma'},
                            {'label': 'Cancer', 'value': 'cancer'}
                        ],
                        value=''
                    )
                ], style= {'display': 'block'}),
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
                            {'label': 'Gender category research', 'value': 'GCS'}
                        ],
                        value=''
                    )
                ], style= {'display': 'block'}),
                html.Br(id='placeholder_1'),html.Br(id='placeholder_2'),
                html.Div(
                    id='button-div',
                    children=[
                        html.A("Generate policy", id="download-btn", className='card-button'),
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
        html.P('Matching odrl:Request with odrl:Offer', className='paragraph-lead'),
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
                    dcc.Dropdown(
                        id = 'request_disease',
                        options=[
                            {'label': 'Uveal Melanoma', 'value': 'uveal_melanoma'},
                            {'label': 'Melanoma', 'value': 'melanoma'},
                            {'label': 'Cancer', 'value': 'cancer'}
                        ],
                        value=''
                    )
                ], style= {'display': 'block'}),
                html.Br(id='placeholder_3'),html.Br(id='placeholder_4'),
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
   Output(component_id='disease', component_property='style'),
   [Input(component_id='data_use_permission', component_property='value')])
def show_hide_element(visibility_state):
    if visibility_state == 'DS':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('placeholder_1', 'children'),
              [Input('data_use_permission', 'value'),
               Input('target_dataset', 'value')])
def update_graph(permission, target):
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
    elif permission == "DS": # TODO: substitute TemplateDisease
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
        g.set((BNode(value='perm_disease'), odrl.rightOperand, duodrl.TemplateDisease))
    elif permission == "NRES":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm')))
        g.set((BNode(value='perm'), odrl.target, URIRef(target)))
    return ;

@app.callback(
   Output('research_type', 'style'),
   [Input('modifiers', 'value')])
def show_research_type(modifiers):
    if len(modifiers) < 1:
        return {'display': 'none'}
    else:
        for mod in modifiers:
            if mod == "DUO_0000012":
                return {'display': 'block'}
            else:
                return {'display': 'none'}

@app.callback(Output('placeholder_2', 'children'),
              [Input('modifiers', 'value'),
               Input('target_dataset', 'value'),
               Input('research_type', 'value'),])
def generate_policy(modifiers, target, research):
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
            elif research == "MDS":
                restrictions.set((BNode(value='DUO_0000012_perm_cons'), odrl.rightOperand, duodrl.MDS))
                restrictions.set((BNode(value='DUO_0000012_pro_cons'), odrl.rightOperand, duodrl.MDS))
            elif research == "GCS":
                restrictions.set((BNode(value='DUO_0000012_perm_cons'), odrl.rightOperand, duodrl.GenderCategoryResearch))
                restrictions.set((BNode(value='DUO_0000012_pro_cons'), odrl.rightOperand, duodrl.GenderCategoryResearch))            
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
            restrictions.add((BNode(value='DUO_0000025_perm_cons'), odrl.leftOperand, odrl.elapsedTime))
            restrictions.add((BNode(value='DUO_0000025_perm_cons'), odrl.operator, odrl.lteq))
            restrictions.add((BNode(value='DUO_0000025_perm_cons'), odrl.rightOperand, duodrl.TemplateTimeLimit))
        elif v == "DUO_0000026":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000026_perm')))
            restrictions.add((BNode(value='DUO_0000026_perm'), odrl.target, URIRef(target)))
            restrictions.add((BNode(value='DUO_0000026_perm'), odrl.assignee, BNode(value='DUO_0000026_perm_assignee')))
            restrictions.add((BNode(value='DUO_0000026_perm_assignee'), RDF.type, odrl.Party))
            restrictions.add((BNode(value='DUO_0000026_perm_assignee'), obo.DUO_0000010, duodrl.TemplateUser))
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
            restrictions.add((BNode(value='DUO_0000028_perm_assignee'), obo.DUO_0000010, duodrl.TemplateInstitution))
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
    for t in iter(restrictions):
        g.add(t)
    g.serialize(destination='dash/offer.ttl', format='turtle')
    a = g.serialize(format='turtle').decode("utf-8")
    g.remove((None, None, None))
    restrictions.remove((None, None, None))
    return a, '', []

@app.callback(
   Output(component_id='request_disease', component_property='style'),
   [Input(component_id='request', component_property='value')])
def show_hide_element(visibility_state):
    if visibility_state == 'DCR':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('placeholder_3', 'children'),
              [Input('request', 'value')])
def generate_request(value):
    if value == "MDS":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='MD_perm')))
        request.set((BNode(value='MD_perm'), odrl.constraint, BNode(value='MD_perm_cons')))
        request.set((BNode(value='MD_perm_cons'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='MD_perm_cons'), odrl.operator, odrl.isA))
        request.set((BNode(value='MD_perm_cons'), odrl.rightOperand, duodrl.MDS))
    elif value == "PR": # TODO: field to substitute TemplatePopulationGroup
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='PR_perm')))
        request.set((BNode(value='PR_perm'), odrl.constraint, BNode(value='PR_perm_pur')))
        request.set((BNode(value='PR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='PR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='PR_perm_pur'), odrl.rightOperand, duodrl.PopulationGroupResearch))
        request.add((BNode(value='PR_perm'), odrl.constraint, BNode(value='PR_perm_group')))
        request.set((BNode(value='PR_perm_group'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='PR_perm_group'), odrl.operator, odrl.isA))
        request.set((BNode(value='PR_perm_group'), odrl.rightOperand, duodrl.TemplatePopulationGroup))
    elif value == "AR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='AR_perm')))
        request.set((BNode(value='AR_perm'), odrl.constraint, BNode(value='AR_perm_cons')))
        request.set((BNode(value='AR_perm_cons'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='AR_perm_cons'), odrl.operator, odrl.isA))
        request.set((BNode(value='AR_perm_cons'), odrl.rightOperand, duodrl.POA))
    elif value == "ACR": # TODO: field to substitute TemplateAgeCategory
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='ACR_perm')))
        request.set((BNode(value='ACR_perm'), odrl.constraint, BNode(value='ACR_perm_pur')))
        request.set((BNode(value='ACR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='ACR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='ACR_perm_pur'), odrl.rightOperand, duodrl.AgeCategoryResearch))
        request.add((BNode(value='ACR_perm'), odrl.constraint, BNode(value='ACR_perm_age')))
        request.set((BNode(value='ACR_perm_age'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='ACR_perm_age'), odrl.operator, odrl.isA))
        request.set((BNode(value='ACR_perm_age'), odrl.rightOperand, duodrl.TemplateAgeCategory))
    elif value == "GCR": # TODO: field to substitute TemplateGender
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='GCR_perm')))
        request.set((BNode(value='GCR_perm'), odrl.constraint, BNode(value='GCR_perm_pur')))
        request.set((BNode(value='GCR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='GCR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='GCR_perm_pur'), odrl.rightOperand, duodrl.GenderCategoryResearch))
        request.add((BNode(value='GCR_perm'), odrl.constraint, BNode(value='GCR_perm_gender')))
        request.set((BNode(value='GCR_perm_gender'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='GCR_perm_gender'), odrl.operator, odrl.isA))
        request.set((BNode(value='GCR_perm_gender'), odrl.rightOperand, duodrl.TemplateGender))
    elif value == "RC":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='RC_perm')))
        request.set((BNode(value='RC_perm'), odrl.constraint, BNode(value='RC_perm_pur')))
        request.set((BNode(value='RC_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='RC_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='RC_perm_pur'), odrl.rightOperand, duodrl.ResearchControl))
    elif value == "BR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='BR_perm')))
        request.set((BNode(value='BR_perm'), odrl.constraint, BNode(value='BR_perm_pur')))
        request.set((BNode(value='BR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='BR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='BR_perm_pur'), odrl.rightOperand, duodrl.HMB))
    elif value == "GR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='GR_perm')))
        request.set((BNode(value='GR_perm'), odrl.constraint, BNode(value='GR_perm_pur')))
        request.set((BNode(value='GR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='GR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='GR_perm_pur'), odrl.rightOperand, duodrl.GS))
    elif value == "DDR":
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='DDR_perm')))
        request.set((BNode(value='DDR_perm'), odrl.constraint, BNode(value='DDR_perm_pur')))
        request.set((BNode(value='DDR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='DDR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='DDR_perm_pur'), odrl.rightOperand, duodrl.DrugDevelopment))
    elif value == "DCR": # TODO: field to substitute TemplateDisease
        request.remove((None, None, None))
        request.set((ex.request, RDF.type, odrl.Request))
        request.set((ex.request, odrl.permission, BNode(value='DCR_perm')))
        request.set((BNode(value='DCR_perm'), odrl.constraint, BNode(value='DCR_perm_pur')))
        request.set((BNode(value='DCR_perm_pur'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='DCR_perm_pur'), odrl.operator, odrl.isA))
        request.set((BNode(value='DCR_perm_pur'), odrl.rightOperand, duodrl.DS))
        request.add((BNode(value='DCR_perm'), odrl.constraint, BNode(value='DCR_perm_mondo')))
        request.set((BNode(value='DCR_perm_mondo'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='DCR_perm_mondo'), odrl.operator, odrl.isA))
        request.set((BNode(value='DCR_perm_mondo'), odrl.rightOperand, obo.MONDO_0000001))
        request.add((BNode(value='DCR_perm'), odrl.constraint, BNode(value='DCR_perm_disease')))
        request.set((BNode(value='DCR_perm_disease'), odrl.leftOperand, odrl.purpose))
        request.set((BNode(value='DCR_perm_disease'), odrl.operator, odrl.isA))
        request.set((BNode(value='DCR_perm_disease'), odrl.rightOperand, duodrl.TemplateDisease))
    return ;

@app.callback(Output('matched', 'children'),
              [Input('match-btn', 'n_clicks')],
              prevent_initial_call=True)
def generate_match(n_clicks):
    r = request.serialize(format='turtle').decode("utf-8")
    return r

if __name__ == '__main__':
    app.run_server(debug=True)
    
