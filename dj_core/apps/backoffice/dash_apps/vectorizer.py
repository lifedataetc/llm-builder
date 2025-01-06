from dash import dcc, html, Output, Input, State
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import pandas as pd
from dash import no_update as nup

from apps.backoffice.models import Role
from apps.utils.dag_helpers import get_infinite_grid, process_grid_filters

external_css = '/static/assets/css/argon.css'
# external_stylesheets = [external_css, dbc.themes.BOOTSTRAP]
app = DjangoDash('vec_db_home')
app.css.append_css({ "external_url" : external_css })
# app.css.append_css({ "external_url" : dbc.themes.BOOTSTRAP })

intro_section = html.Div([html.Br(), html.H1('Manage Vector Databases', className='text-center'), html.Hr()])
new_section = html.Div([
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Create a New Vector DB",
                            className="card-title text-uppercase text-bold text-center mb-0"),
                    html.Br(),
                    html.Div(dbc.Button(html.Span(['Start ', html.Span(className='ni ni-bold-right')]),
                                        id='create_new_db'), className='text-center')
                ])], style={"width": "18rem"}, )
])
create_new_db = html.Div([
    dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Fullscreen modal")),
                dbc.ModalBody("Wow this thing takes up a lot of space..."),
            ],
            id="modal-fs",
            fullscreen=True,
        )
])

@app.callback(
    Output("modal-fs", "is_open"),
    Input("create_new_db", "n_clicks"),
    State("modal-fs", "is_open"),
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open

app.layout = html.Div([intro_section, new_section, create_new_db], className='col-md-10 container-fluid')