import dash_ag_grid as dag
from dash import html
import pandas as pd

dtDefinitions = {
    'float':{
        'baseDataType': 'number', 'extendsDatatype': 'number', 'appendColumnTypes': True,
        'valueFormatter': {'function': "params.value == null ? '' : d3.format(',.2f')(params.value)"}
    }
}

operators = {
    "greaterThanOrEqual": "ge",
    "lessThanOrEqual": "le",
    "lessThan": "lt",
    "greaterThan": "gt",
    "notEqual": "ne",
    "equals": "eq",
}

def get_infinite_grid(table_id, cols, **kwargs):
    style = kwargs.get('style', {'height': 500})
    row_height = kwargs.get('row_height', 30)
    selectable = kwargs.get('selectable', False)
    selection_type = kwargs.get('selection_type', 'single')

    if not selectable:
        grid = html.Div([
            dag.AgGrid(id=table_id, style=style, rowModelType='infinite', columnDefs=cols,
                       dashGridOptions=dict(rowHeight=row_height, dataTypeDefinitions=dtDefinitions, rowBuffer=50,
                                            enableCellTextSelection=True, ensureDomOrder=True, maxBlocksInCache=2,
                                            cacheBlockSize=100, cacheOverflowSize=2, maxConcurrentDatasourceRequests=10,
                                            infiniteInitialRowCount=1), columnSize='responsiveSizeToFit',
                       className='ag-theme-quartz header-style-on-filter',
                       defaultColDef=dict(filter=True, sortable=True, resizable=True, wrapHeaderText=True,
                                          autoHeaderHeight=True))
        ])

    else:
        grid = html.Div([
            dag.AgGrid(id=table_id, style=style, rowModelType='infinite', columnDefs=cols,
                       dashGridOptions=dict(rowHeight=row_height, dataTypeDefinitions=dtDefinitions, rowBuffer=50,
                                            enableCellTextSelection=True, ensureDomOrder=True, maxBlocksInCache=2,
                                            cacheBlockSize=100, cacheOverflowSize=2, maxConcurrentDatasourceRequests=10,
                                            infiniteInitialRowCount=1, rowSelection=selection_type),
                       columnSize='responsiveSizeToFit',
                       className='ag-theme-quartz header-style-on-filter',
                       defaultColDef=dict(filter=True, sortable=True, resizable=True, wrapHeaderText=True,
                                          autoHeaderHeight=True,
                                          checkboxSelection=dict(function='params.column == params.api.getAllDisplayedColumns()[0]')),)
        ])

    return grid

def filter_df(dff, filter_model, col):
    # migrate this logic to Polars at some point
    if "filter" in filter_model:
        if filter_model["filterType"] == "date":
            crit1 = filter_model["dateFrom"]
            crit1 = pd.Series(crit1).astype(dff[col].dtype)[0]
            if "dateTo" in filter_model:
                crit2 = filter_model["dateTo"]
                crit2 = pd.Series(crit2).astype(dff[col].dtype)[0]
        else:
            crit1 = filter_model["filter"]
            crit1 = pd.Series(crit1).astype(dff[col].dtype)[0]
            if "filterTo" in filter_model:
                crit2 = filter_model["filterTo"]
                crit2 = pd.Series(crit2).astype(dff[col].dtype)[0]
    if "type" in filter_model:
        if filter_model["type"] == "contains":
            dff = dff.loc[dff[col].str.contains(crit1, case=False)]
        elif filter_model["type"] == "notContains":
            dff = dff.loc[~dff[col].str.contains(crit1, case=False)]
        elif filter_model["type"] == "startsWith":
            dff = dff.loc[dff[col].str.startswith(crit1)]
        elif filter_model["type"] == "notStartsWith":
            dff = dff.loc[~dff[col].str.startswith(crit1)]
        elif filter_model["type"] == "endsWith":
            dff = dff.loc[dff[col].str.endswith(crit1)]
        elif filter_model["type"] == "notEndsWith":
            dff = dff.loc[~dff[col].str.endswith(crit1)]
        elif filter_model["type"] == "inRange":
            if filter_model["filterType"] == "date":
                dff = dff.loc[
                    dff[col].astype("datetime64[ns]").between_time(crit1, crit2)
                ]
            else:
                dff = dff.loc[dff[col].between(crit1, crit2)]
        elif filter_model["type"] == "blank":
            dff = dff.loc[dff[col].isnull()]
        elif filter_model["type"] == "notBlank":
            dff = dff.loc[~dff[col].isnull()]
        elif filter_model["type"] == "true":
            dff = dff.loc[dff[col]]
        elif filter_model["type"] == "false":
            dff = dff.loc[~dff[col]]
        else:
            dff = dff.loc[getattr(dff[col], operators[filter_model["type"]])(crit1)]
    elif filter_model["filterType"] == "set":
        dff = dff.loc[dff[col].astype("string").isin(filter_model["values"])]
    return dff


def process_grid_filters(dff, request_ag):
    if request_ag['filterModel']:
        filters = request_ag['filterModel']
        for f in filters:
            try:
                if 'operator' in filters[f]:
                    if filters[f]['operator'] == 'AND':
                        dff = filter_df(dff, filters[f]['condition1'], f)
                        dff = filter_df(dff, filters[f]['condition2'], f)
                    else:
                        dff1 = filter_df(dff, filters[f]['condition1'], f)
                        dff2 = filter_df(dff, filters[f]['condition2'], f)
                        dff = pd.concat([dff1, dff2])
                else:
                    dff = filter_df(dff, filters[f], f)
            except:
                pass

    if request_ag['sortModel']:
        sorting = []
        asc = []
        for sort in request_ag['sortModel']:
            sorting.append(sort['colId'])
            if sort['sort'] == 'asc':
                asc.append(True)
            else:
                asc.append(False)
        dff = dff.sort_values(by=sorting, ascending=asc)

    lines = len(dff.index)
    if lines == 0:
        lines = 1

    return dff.iloc[request_ag['startRow']: request_ag['endRow']], lines
