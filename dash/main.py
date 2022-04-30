from dash import Dash, html, dcc, Input, Output
from rdflib import Graph, Namespace, URIRef, BNode
from rdflib.namespace import RDF

g = Graph()
restrictions = Graph()

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
                        value=''
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
                html.Br(id='placeholder_1'),html.Br(id='placeholder_2'),
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

@app.callback(Output('placeholder_1', 'children'),
              [Input(component_id='data_use_permission', component_property='value')])
def update_graph(value):
    if value == "GRU":
        g.remove((None, None, None))
        g.set((ex.offer, RDF.type, odrl.Offer))
        g.set((ex.offer, odrl.permission, BNode(value='perm')))
        g.set((BNode(value='perm'), odrl.target, duodrl.TemplateDataset))
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

@app.callback(Output('placeholder_2', 'children'),
              [Input('modifiers', 'value')])
def generate_policy(value):
    for v in value:
        if v == "DUO_0000012":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000012_perm')))
            restrictions.add((BNode(value='DUO_0000012_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000012_perm'), odrl.constraint, BNode(value='DUO_0000012_perm_cons')))
            restrictions.add((BNode(value='DUO_0000012_perm_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000012_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000012_perm_cons'), odrl.rightOperand, duodrl.TemplateResearch))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000012_pro')))
            restrictions.add((BNode(value='DUO_0000012_pro'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000012_pro'), odrl.constraint, BNode(value='DUO_0000012_pro_cons')))
            restrictions.add((BNode(value='DUO_0000012_pro_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000012_pro_cons'), odrl.operator, duodrl.isNotA))
            restrictions.add((BNode(value='DUO_0000012_pro_cons'), odrl.rightOperand, duodrl.TemplateResearch))
        elif v == "DUO_0000015":
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000015_pro')))
            restrictions.add((BNode(value='DUO_0000015_pro'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000015_pro'), odrl.constraint, BNode(value='DUO_0000015_pro_cons')))
            restrictions.add((BNode(value='DUO_0000015_pro_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000015_pro_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000015_pro_cons'), odrl.rightOperand, duodrl.MDS))
        elif v == "DUO_0000016":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000016_perm')))
            restrictions.add((BNode(value='DUO_0000016_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000016_perm'), odrl.constraint, BNode(value='DUO_0000016_perm_cons')))
            restrictions.add((BNode(value='DUO_0000016_perm_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000016_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000016_perm_cons'), odrl.rightOperand, duodrl.GS))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000016_pro')))
            restrictions.add((BNode(value='DUO_0000016_pro'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000016_pro'), odrl.constraint, BNode(value='DUO_0000016_pro_cons')))
            restrictions.add((BNode(value='DUO_0000016_pro'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000016_pro'), odrl.operator, duodrl.isNotA))
            restrictions.add((BNode(value='DUO_0000016_pro'), odrl.rightOperand, duodrl.GS))
        elif v == "DUO_0000018":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000018_perm')))
            restrictions.add((BNode(value='DUO_0000018_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000018_perm'), odrl.constraint, BNode(value='DUO_0000018_perm_cons')))
            restrictions.add((BNode(value='DUO_0000018_perm_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000018_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000018_perm_cons'), odrl.rightOperand, duodrl.NCU))
            restrictions.add((BNode(value='DUO_0000018_perm'), odrl.assignee, BNode(value='DUO_0000018_perm_assignee')))
            restrictions.add((BNode(value='DUO_0000018_perm_assignee'), RDF.type, odrl.Party))
            restrictions.add((BNode(value='DUO_0000018_perm_assignee'), obo.DUO_0000010, duodrl.NonProfitOrganisation))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000018_pro')))
            restrictions.add((BNode(value='DUO_0000018_pro'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000018_pro'), odrl.constraint, BNode(value='DUO_0000018_pro_cons')))
            restrictions.add((BNode(value='DUO_0000018_pro_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000018_pro_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000018_pro_cons'), odrl.rightOperand, duodrl.NCU))
            restrictions.add((BNode(value='DUO_0000018_pro'), odrl.assignee, BNode(value='DUO_0000018_pro_assignee')))
            restrictions.add((BNode(value='DUO_0000018_pro_assignee'), RDF.type, odrl.Party))
            restrictions.add((BNode(value='DUO_0000018_pro_assignee'), obo.DUO_0000010, duodrl.ForProfitOrganisation))
        elif v == "DUO_0000019":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000019_perm')))
            restrictions.add((BNode(value='DUO_0000019_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000019_perm'), odrl.duty, BNode(value='DUO_0000019_perm_duty')))
            restrictions.add((BNode(value='DUO_0000019_perm_duty'), odrl.action, odrl.distribute))
            restrictions.add((BNode(value='DUO_0000019_perm_duty'), odrl.output, duodrl.ResultsOfStudies))
        elif v == "DUO_0000020":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000020_perm')))
            restrictions.add((BNode(value='DUO_0000020_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000020_perm'), odrl.duty, BNode(value='DUO_0000020_perm_duty')))
            restrictions.add((BNode(value='DUO_0000020_perm_duty'), odrl.action, duodrl.CollaborateWithStudyPI))
        elif v == "DUO_0000021":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000021_perm')))
            restrictions.add((BNode(value='DUO_0000021_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000021_perm'), odrl.duty, BNode(value='DUO_0000021_perm_duty')))
            restrictions.add((BNode(value='DUO_0000021_perm_duty'), odrl.action, duodrl.ProvideEthicalApproval))
        elif v == "DUO_0000022":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000022_perm')))
            restrictions.add((BNode(value='DUO_0000022_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000022_perm'), odrl.constraint, BNode(value='DUO_0000022_perm_cons')))
            restrictions.add((BNode(value='DUO_0000022_perm_cons'), odrl.leftOperand, odrl.spatial))
            restrictions.add((BNode(value='DUO_0000022_perm_cons'), odrl.operator, odrl.eq))
            restrictions.add((BNode(value='DUO_0000022_perm_cons'), odrl.rightOperand, duodrl.TemplateLocation))
        elif v == "DUO_0000024":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000024_perm')))
            restrictions.add((BNode(value='DUO_0000024_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000024_perm'), odrl.duty, BNode(value='DUO_0000024_perm_duty')))
            restrictions.add((BNode(value='DUO_0000024_perm_duty'), odrl.action, odrl.distribute))
            restrictions.add((BNode(value='DUO_0000024_perm_duty'), odrl.output, duodrl.ResultsOfStudies))
            restrictions.add((BNode(value='DUO_0000024_perm_duty'), odrl.constraint, BNode(value='DUO_0000024_perm_cons')))
            restrictions.add((BNode(value='DUO_0000024_perm_cons'), odrl.leftOperand, odrl.dateTime))
            restrictions.add((BNode(value='DUO_0000024_perm_cons'), odrl.operator, odrl.gteq))
            restrictions.add((BNode(value='DUO_0000024_perm_cons'), odrl.rightOperand, duodrl.TemplateStudyResultsPublicationDate))
        elif v == "DUO_0000025":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000025_perm')))
            restrictions.add((BNode(value='DUO_0000025_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000025_perm'), odrl.constraint, BNode(value='DUO_0000025_perm_cons')))
            restrictions.add((BNode(value='DUO_0000025_perm_cons'), odrl.leftOperand, odrl.elapsedTime))
            restrictions.add((BNode(value='DUO_0000025_perm_cons'), odrl.operator, odrl.lteq))
            restrictions.add((BNode(value='DUO_0000025_perm_cons'), odrl.rightOperand, duodrl.TemplateTimeLimit))
        elif v == "DUO_0000026":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000026_perm')))
            restrictions.add((BNode(value='DUO_0000026_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000026_perm'), odrl.assignee, BNode(value='DUO_0000026_perm_assignee')))
            restrictions.add((BNode(value='DUO_0000026_perm_assignee'), RDF.type, odrl.Party))
            restrictions.add((BNode(value='DUO_0000026_perm_assignee'), obo.DUO_0000010, duodrl.TemplateUser))
        elif v == "DUO_0000027":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000027_perm')))
            restrictions.add((BNode(value='DUO_0000027_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000027_perm'), odrl.constraint, BNode(value='DUO_0000027_perm_cons')))
            restrictions.add((BNode(value='DUO_0000027_perm_cons'), odrl.leftOperand, duodrl.Project))
            restrictions.add((BNode(value='DUO_0000027_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000027_perm_cons'), odrl.rightOperand, duodrl.TemplateProject))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000027_pro')))
            restrictions.add((BNode(value='DUO_0000027_pro'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000027_pro'), odrl.constraint, BNode(value='DUO_0000027_pro_cons')))
            restrictions.add((BNode(value='DUO_0000027_pro_cons'), odrl.leftOperand, duodrl.Project))
            restrictions.add((BNode(value='DUO_0000027_pro_cons'), odrl.operator, duodrl.isNotA))
            restrictions.add((BNode(value='DUO_0000027_pro_cons'), odrl.rightOperand, duodrl.TemplateProject))
        elif v == "DUO_0000028":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000028_perm')))
            restrictions.add((BNode(value='DUO_0000028_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000028_perm'), odrl.assignee, BNode(value='DUO_0000028_perm_assignee')))
            restrictions.add((BNode(value='DUO_0000028_perm_assignee'), RDF.type, odrl.Party))
            restrictions.add((BNode(value='DUO_0000028_perm_assignee'), obo.DUO_0000010, duodrl.TemplateInstitution))
        elif v == "DUO_0000029":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000029_perm')))
            restrictions.add((BNode(value='DUO_0000029_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000029_perm'), odrl.duty, BNode(value='DUO_0000029_perm_duty')))
            restrictions.add((BNode(value='DUO_0000029_perm_duty'), odrl.action, duodrl.ReturnDerivedOrEnrichedData))
        elif v == "DUO_0000043":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000043_perm')))
            restrictions.add((BNode(value='DUO_0000043_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000043_perm'), odrl.constraint, BNode(value='DUO_0000043_perm_cons')))
            restrictions.add((BNode(value='DUO_0000043_perm_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000043_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000043_perm_cons'), odrl.rightOperand, duodrl.CC))
        elif v == "DUO_0000044":
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000044_pro')))
            restrictions.add((BNode(value='DUO_0000044_pro'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000044_pro'), odrl.constraint, BNode(value='DUO_0000044_pro_cons')))
            restrictions.add((BNode(value='DUO_0000044_pro_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000044_pro_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000044_pro_cons'), odrl.rightOperand, duodrl.POA))
        elif v == "DUO_0000045":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000045_perm')))
            restrictions.add((BNode(value='DUO_0000045_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000045_perm'), odrl.assignee, BNode(value='DUO_0000045_perm_assignee')))
            restrictions.add((BNode(value='DUO_0000045_perm_assignee'), RDF.type, odrl.Party))
            restrictions.add((BNode(value='DUO_0000045_perm_assignee'), obo.DUO_0000010, duodrl.NonProfitOrganisation))
        elif v == "DUO_0000046":
            restrictions.add((ex.offer, odrl.permission, BNode(value='DUO_0000046_perm')))
            restrictions.add((BNode(value='DUO_0000046_perm'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000046_perm'), odrl.constraint, BNode(value='DUO_0000046_perm_cons')))
            restrictions.add((BNode(value='DUO_0000046_perm_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000046_perm_cons'), odrl.operator, odrl.isA))
            restrictions.add((BNode(value='DUO_0000046_perm_cons'), odrl.rightOperand, duodrl.NCU))
            
            restrictions.add((ex.offer, odrl.prohibition, BNode(value='DUO_0000046_pro')))
            restrictions.add((BNode(value='DUO_0000046_pro'), odrl.target, duodrl.TemplateDataset))
            restrictions.add((BNode(value='DUO_0000046_pro'), odrl.constraint, BNode(value='DUO_0000046_pro_cons')))
            restrictions.add((BNode(value='DUO_0000046_pro_cons'), odrl.leftOperand, odrl.purpose))
            restrictions.add((BNode(value='DUO_0000046_pro_cons'), odrl.operator, duodrl.isNotA))
            restrictions.add((BNode(value='DUO_0000046_pro_cons'), odrl.rightOperand, duodrl.NCU))
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
    g.remove((None, None, None))
    restrictions.remove((None, None, None))
    return "Success", '', []

if __name__ == '__main__':
    app.run_server(debug=True)
    
