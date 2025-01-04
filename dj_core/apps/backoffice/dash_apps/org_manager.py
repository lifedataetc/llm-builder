from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash

from apps.utils.dag_helpers import get_infinite_grid, process_grid_filters

external_css = 'static/assets/css/argon.css'
app = DjangoDash('org_manager', external_stylesheets=[external_css])

cols = []
grid = get_infinite_grid('query_grid', cols, style={'height': 600}, selectable=True, selection_type='single')

layout = []
app.layout = html.Div(layout, className='col-md-10')