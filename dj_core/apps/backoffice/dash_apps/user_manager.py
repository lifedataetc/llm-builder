# from dash import dcc, html, Output, Input
# import dash_bootstrap_components as dbc
# from django_plotly_dash import DjangoDash
# import pandas as pd
# from dash import no_update as nup
#
# from apps.backoffice.models import Role
# from apps.utils.dag_helpers import get_infinite_grid, process_grid_filters
#
# external_css = '/static/assets/css/argon.css'
# # external_stylesheets = [external_css]
# app = DjangoDash('user_manager',)
# app.css.append_css({ "external_url" : external_css })
#
# org_cols = [dict(field='first_name', headerName='First Name', cellDataType='text'),
#             dict(field='last_name', headerName='Last Name', cellDataType='text'),
#             dict(field='email', headerName='Email', cellDataType='text'),
#             dict(field='user_type', headerName='Account Type', cellDataType='text'),]
# org_grid = get_infinite_grid('query_grid', org_cols, style={'height': 600}, selectable=True, selection_type='single',
#                          row_height=35)
#
# # admin_cols =
#
# @app.callback(
#     Output('query_grid', 'getRowsResponse'),
#     [Input('query_grid', 'getRowsRequest'),])
# def data_manager(request_ag, **kwargs):
#     try:
#         cc = kwargs['callback_context'].triggered[0]['prop_id']
#         user = kwargs['request'].user
#     except:
#         cc = ''
#     if cc == 'query_grid.getRowsRequest':
#         if request_ag:
#             if user.user_type == 1:
#                 qs = Role.objects.filter(user_type__in=[2, 3, 4]).values('first_name', 'last_name', 'email',
#                                                                          'user_type')
#                 dff = pd.DataFrame(qs)
#                 partial, lines = process_grid_filters(dff, request_ag)
#                 main_table_data = {'rowData': partial.to_dict('records'), 'rowCount': lines}
#                 return main_table_data
#
#     return nup
#
#
#
#
# layout = [html.Br(), org_grid]
# app.layout = html.Div(layout, className='col-md-10 container-fluid')