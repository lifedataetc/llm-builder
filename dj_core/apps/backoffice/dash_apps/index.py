from dash import dcc, html, Output, Input, ALL
from dash import no_update as nup
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash

external_css = 'static/assets/css/argon.css'
app = DjangoDash('index', external_stylesheets=[external_css])

pre_qual_card = html.Div([dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Manage Embeddings", className="card-title text-uppercase text-bold text-center mb-0"),
                html.P("Create vector database project", className="card-text text-center"),
                html.Div(dbc.Button(html.Span(['Go ', html.Span(className='ni ni-single-copy-04')]),
                                    id={'type':'rbtn', 'index':'vec_db_start'}), className='text-center')
            ])], style={"width": "18rem"},)], className='col-xl-3 col-md-6 col-sm-12')
user_manager_card = html.Div([dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Manager Users", className="card-title text-uppercase text-bold text-center mb-0"),
                html.P("Add or remove users for your organization", className="card-text text-center"),
                html.Div(dbc.Button(html.Span(['Go ', html.Span(className='ni ni-circle-08')]),
                                    id={'type':'rbtn', 'index':'user_manager'}), className='text-center')
            ])], style={"width": "18rem"},)], className='col-xl-3 col-md-6 col-sm-12')
org_manager_card = html.Div([dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Manager Orgs", className="card-title text-uppercase text-bold text-center mb-0"),
                html.P("Add, remove, and manage organizations", className="card-text text-center"),
                html.Div(dbc.Button(html.Span(['Go ', html.Span(className='ni ni-building')]),
                                    id={'type':'rbtn', 'index':'org_manager'}), className='text-center')
            ])], style={"width": "18rem"},)], className='col-xl-3 col-md-6 col-sm-12')
settings_card = html.Div([dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Settings", className="card-title text-uppercase text-bold text-center mb-0"),
                html.P("Manage settings", className="card-text text-center"),
                html.Div(dbc.Button(html.Span(['Go ', html.Span(className='ni ni-settings-gear-65')]),
                                    id={'type':'rbtn', 'index':'settings'}), className='text-center')
            ])], style={"width": "18rem"},)], className='col-xl-3 col-md-6 col-sm-12')

header = html.Div([
    html.Div([
        html.H1(id='user_header', className='text-white'), html.Hr(style={'border-color': 'lightgray'}),
        html.Div([html.Div(id='card_div', className='row')], className='header-body')
    ], className='container-fluid')])

@app.callback(
    [Output('card_div', 'children'),
    Output('user_header', 'children'),],
    [Input('init', 'children')]
)
def layout_maker(init, **kwargs):
    user = kwargs['request'].user
    cards = []
    user_header = f'Welcome, {user.first_name} (User Type: {user.user_type})'
    if user.user_type == 1:
        cards = [pre_qual_card, user_manager_card, org_manager_card, settings_card]
    return cards, user_header

@app.callback(
    Output('redirector', 'children'),
    [Input({'type': 'rbtn', 'index':ALL}, 'n_clicks'),],
    prevent_initial_call=True
)
def redirector(rbtn, **kwargs):
    try:
        trig = kwargs['callback_context'].triggered
        if len(trig) == 1:
            btn_idx = eval(trig[0]['prop_id'].split('.')[0])['index']
            return dcc.Location(pathname=f'{btn_idx}/', id='___')
        else:
            return nup
    except KeyError:
        return nup

app.layout = html.Div([header, html.Div(id='init', children=1, style={'display': 'none'}),
                       html.Div(id='redirector')], className='container-fluid col-md-11')