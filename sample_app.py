import json
from dash import Dash, html, dcc, dash_table
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import mysql.connector
import dash_bootstrap_components as dbc
import pandas as pd

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    auth_plugin='mysql_native_password',
    password='mysqlparu',
    port='3306',
    database='indian_crimes'
)

cursor = mydb.cursor()

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

console_options = {0: 'crimes_commited_ipc'
    , 1: 'crimes_commited_sc'
    , 2: 'anti_corruption_cases'
    , 3: 'crimes_against_children'
    , 4: 'crimes_against_women'
    }

file_log = pd.read_csv(
    'https://gist.githubusercontent.com/pk2203/a625a323ce9e06416b31a7538d564e41/raw/98d1d9d8902401d7118da0d71d25af1c1338f4c8/sample_file_log.csv')
file_log = file_log[['Package ', 'Title', 'Data Description']]
file_log['id'] = [i for i in range(file_log.shape[0])]
file_log.set_index('id', inplace = True, drop=False)
user_log = pd.read_csv(
    'https://gist.githubusercontent.com/pk2203/e845ce82cf77a243d69ffad3346ea919/raw/c8c2f203b302aa38a137b817053b9e5e4e2602fe/UserLog.csv')
result_table = pd.DataFrame()

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                return name, operator_type[0].strip(), value

    return [None] * 3

def generate_col(col):
    res = []
    for x in col:
        res.append(list(x))
    res = [x for val in res for x in val]
    return res


def extract_data(table):
    cursor.execute('SELECT * from ' + table)
    data = [x for x in cursor]

    cursor.execute('select COLUMN_NAME from information_schema.columns where table_name = %s',
                   list([table]))
    columns = generate_col(cursor)

    df = pd.DataFrame(data, columns=columns)

    return df

def layout():
    return html.Div(
        id='app-body',
        className='app-body_desc',
        children=[
            html.Div(
                id='banner',
                className='banner_desc',
                children=[html.H2("Query Console"), html.H5("Welcome PARVATHY KURUP")]
            ),
            html.Br(),
            html.Div(
                id='audit-controls',
                className='audit_control_desc',
                children=[
                    html.Div(
                        id='left-container',
                        className='left_container_desc',
                        children=[
                            dcc.Tabs(id='audit-tabs', className='audit_tabs_desc', children=[
                                dcc.Tab(
                                    label='Search New',
                                    id='search_new',
                                    children=[
                                        html.Div(
                                            id='search-new-container',
                                            className='search_new',
                                            children=[
                                                html.Br(),
                                                dbc.Container([
                                                    dcc.Markdown('### File Log'),
                                                    dbc.Label('Show number of rows:'),
                                                    dcc.Dropdown(
                                                        id='row_drop',
                                                        value=5,
                                                        clearable=False,
                                                        style={'width': '35%'},
                                                        options=[5, 10, 15, 20, 25]
                                                    ),
                                                    dash_table.DataTable(
                                                        id='file_log_table',
                                                        columns=[
                                                            {'name': 'Package ', 'id': 'Package ', 'type': 'text'},
                                                            {'name': 'Title', 'id': 'Title', 'type': 'text'},
                                                            {'name': 'Data Description', 'id': 'Data Description',
                                                             'type': 'text'}
                                                        ],
                                                        data=file_log.to_dict('records'),
                                                        filter_action='native',
                                                        page_size=10,
                                                        style_data={
                                                            'width': '150px', 'minWidth': '150px', 'maxwidth': '150px',
                                                            'overflow': 'hidden',
                                                            'textOverflow': 'ellipse', 'color': 'black'
                                                        }
                                                    ),
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.Dropdown(id='package_drop', options=[x for x in sorted(
                                                                file_log['Package '].unique())])
                                                        ], width=3)

                                                    ], justify='between', className='file_log'),

                                                ], fluid=True),
                                                html.Hr(),
                                                html.Button(
                                                    'Extract',
                                                    id='extract-button-val',
                                                    n_clicks=0,
                                                ),
                                            ]
                                        )]
                                ),
                                dcc.Tab(
                                    label='Extract New',
                                    id='extract_new',
                                    children=[
                                        dbc.Container([
                                            html.Div(
                                                id='directory-loc'),
                                            html.Hr(),
                                            html.Br(),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label('Show number of rows:'),
                                                    dcc.Dropdown(
                                                    id='row_tab_drop',
                                                    value=5,
                                                    clearable=False,
                                                    style={'width': '35%'},
                                                    options=[5, 10, 15, 20, 25]
                                                    )
                                                    ], width=3),
                                                dbc.Col([
                                                    dbc.Label('Number of records to load:'),
                                                    dcc.Input(
                                                        id = 'data_load',
                                                        type = 'number',
                                                        min=100
                                                    )
                                                ],width=3),
                                                dbc.Col([
                                                    dcc.Markdown('Filter queries with the following basic operators:'),
                                                    html.P([
                                                        ' [ge , >=], '
                                                          '[le , <= ], '
                                                          '[lt , <], '
                                                          '[gt , >], '
                                                          '[ne , !=], '
                                                          '[eq , =], '
                                                    ]),
                                                    html.P([
                                                        "Eg: eq GOA"
                                                    ]),
                                                    html.P([
                                                        "Eg: gt 30"
                                                    ])
                                                ])
                                            ]),
                                            html.Br(),
                                            html.Div(
                                                id='filter_data',
                                                className='filter_data',
                                                children=[
                                                    dbc.Label('Select the columns to filter:'),
                                                    dcc.Dropdown(
                                                        id='column_filter',
                                                        clearable=True,
                                                       # multi = True,
                                                        style={'width': '100%'}
                                                    ),
                                                    html.Br()
                                            ]),
                                            dcc.Store(id='orginal_data'),
                                            dcc.Store(id='final_data'),
                                            dash_table.DataTable(
                                                id='extracted_table',
                                                editable=True,
                                                filter_action="custom",
                                                filter_query='',
                                                sort_action="custom",
                                                sort_mode="multi",
                                                sort_by = [],
                                                column_selectable="single",
                                                selected_columns=[],
                                                page_action="custom",
                                                page_current=0,
                                                page_size=10,
                                                style_table={'overflowX': 'auto'},
                                                style_cell={
                                                    'width': '150px', 'minWidth': '150px', 'maxwidth': '150px',
                                                    'overflow': 'hidden',
                                                    'textOverflow': 'ellipse', 'color': 'black'
                                                }
                                            )

                                        ], fluid=True),
                                        html.Br(),
                                        dcc.Download(id='download_data'),
                                        html.Button(
                                            'Download',
                                            id='download-button-val',
                                            n_clicks=0,
                                            style={'position': 'center',
                                                   'display': 'inline-block',
                                                   'width': '160px',
                                                   'padding': '10px'}
                                        )

                                    ]
                                ),
                                dcc.Tab(
                                    label='User Log',
                                    id='user_log',
                                    children=[
                                        html.H5('List of Data Requests by PARVATHY KURUP: '),
                                        html.Br(),
                                        dash_table.DataTable(
                                            id='user_log_table',
                                            data=user_log.to_dict('records'),
                                            columns=[{'name': i, 'id': i} for i in user_log.columns],
                                            style_header={"backgroundColor": "rgb(224,97,97)",
                                                          "color": "white",
                                                          "textAlign": "center"}
                                        )
                                    ]
                                )
                            ])
                        ]
                    )
                ]
            )
        ]
    )


def callbacks(_app):
    @_app.callback(
        [Output('file_log_table', 'data'),
         Output('file_log_table', 'page_size')],
        [Input('package_drop', 'value'),
         Input('row_drop', 'value')]
    )
    def update_file_log(p_val, row_val):
        df = file_log.copy()

        if p_val is None or row_val is None:
            raise PreventUpdate

        if p_val:
            df = df[df['Package '] == p_val]

        return df.to_dict('records'), row_val

    @_app.callback(
        Output('extracted_table', 'page_size'),
        Input('row_tab_drop', 'value')
    )
    def update_page_size(row_val):
        if row_val is None:
            raise PreventUpdate
        else:
            return row_val

    @_app.callback(
        Output('directory-loc', 'children'),
        Input('extract-button-val', 'n_clicks'),
        State('file_log_table', 'active_cell')
    )
    def directory_log(n_clicks, active_cell):
        if n_clicks:
            active_row_id = active_cell['row_id'] if active_cell else None
            return html.H5(console_options[active_row_id])

    @_app.callback(
        Output('orginal_data','data'),
        Input('extract-button-val', 'n_clicks'),
        State('file_log_table', 'active_cell')
    )
    def update_Store(n_clicks, active_cell):
        if active_cell is None:
            raise PreventUpdate
        if n_clicks:
            row = active_cell['row_id']
            df = extract_data(console_options[row])
            res = df.to_json(date_format='iso', orient='split')
            return res
        else:
            raise PreventUpdate

    @_app.callback(
        Output('column_filter', 'options'),
        Input('extracted_table', 'selected_columns'),
        Input('orginal_data','data')
    )
    def dropdown_filters(selected_columns,data):
        if selected_columns:
            df = pd.read_json(data, orient='split')
            for i in selected_columns:
                if i not in df.columns:
                    raise PreventUpdate
                else:
                   return generate_col([sorted(df[i].unique())])
        else:
            raise PreventUpdate

    @_app.callback(
        [Output('extracted_table', 'data'),
         Output('final_data', 'data'),
         Output('extracted_table', 'columns'),
         Output('extracted_table','page_count')],
        [Input('extracted_table', 'selected_columns'),
         Input('column_filter', 'value'),
         Input('extracted_table','page_current'),
         Input('extracted_table','page_size'),
         Input('data_load','value'),
         Input('extracted_table','sort_by'),
         Input('extracted_table','filter_query'),
         Input('orginal_data','data')]
    )
    def activate_extraction(selected_columns,value,page_current,page_size,page_count,sort_by,filter,data):
        if data is None:
            raise PreventUpdate

        if data:
            df =  pd.read_json(data, orient='split')
            df_columns = [{'name': i, 'id': i, 'deletable': True, 'selectable': True} for i in df.columns]

            if selected_columns is not None and value is not None:
                for i in selected_columns:
                    if i not in df.columns:
                        raise PreventUpdate
                else:
                        df = df.loc[df[i]==value]
            else:
                df = df

            if len(sort_by):
                df = df.sort_values(
                    [col['column_id'] for col in sort_by],
                    ascending=[
                        col['direction'] == 'asc'
                        for col in sort_by
                    ]
                )
            else:
                df = df

            if filter:
                filtering_exp = filter.split(' && ')
                for filter_part in filtering_exp:
                    col_name, operator,filter_val = split_filter_part(filter_part)

                    if operator in ('eq','ne','lt','le','gt','ge'):
                        df = df.loc[getattr(df[col_name],operator)(filter_val)]
                    elif operator == 'contains':
                        df - df.loc[df[col_name].str.contains(filter_val)]
                    elif operator == 'datestartswith':
                        df = df.loc[df[col_name].str.contains(filter_val)]

            final = df.to_json(date_format='iso',orient='split')

            return df.iloc[page_current*page_size:(page_current+1)*page_size].to_dict('records'), final,df_columns,page_count

    @_app.callback(
        Output('data_load','max'),
        Output('data_load','value'),
        Input('row_tab_drop', 'value'),
        Input('orginal_data','data')
    )
    def data_loader(row_val,data):
        if data:
            df = pd.read_json(data, orient='split')
            if df.shape[0] > 1000:
                return int(1000/row_val), int(1000/row_val)
            else:
                return int(df.shape[0]/row_val),int(df.shape[0]/row_val)
        else:
            raise PreventUpdate

    @_app.callback(
        Output('download_data','data'),
        Input('download-button-val','n_clicks'),
        State('final_data', 'data'),
    )
    def download_data(n_clicks,table_data):
        if table_data is None:
            raise PreventUpdate
        if n_clicks:
            df = pd.read_json(table_data, orient='split')
            report_name = "export.csv"
            return dcc.send_data_frame(df.to_csv,report_name)
        else:
            raise PreventUpdate



app_sample = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app_sample.title = "Audit Console Prototype"
app_sample.layout = layout()
callbacks(app_sample)

if __name__ == '__main__':
    app_sample.run_server(debug=True)
