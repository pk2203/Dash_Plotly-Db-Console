from dash import Dash, html, dcc, dash_table, callback
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd

console_options = {
    'RAPID': ['PAX', 'CARGO', 'UC REPOSTIORY', 'MASTERS'],
    'N_ASA': ['ACCOUNTS PAYABLE', 'ACCOUNTS RECEIVABLE', 'GENERAL LEDGER', 'PETTY CASH'],
    'COMET': ['COMET'],
    'OPERA': ['OPERA'],
    'NGSC': ['NGSC'],
    'TKTODS': ['TKTODS'],
    'TRIPS': ['TRIPS'],
    'MACS': ['MACS'],
    'CRIS': ['CRIS'],
    'EKAS': ['EKAS'],
    'AIMS': ['AIMS'],
    'MARS': ['MARS']
}

file_log = pd.read_csv('https://gist.githubusercontent.com/pk2203/ecf0db94f489018ac337d33ef6aa69ac/raw/5e24aa20d64fe305fc20cd3faf38cfae8e215b32/file_log.csv')
file_log = file_log[['Directory', 'Sub-Folder', 'Packages', 'Data-Description']]
file_log.reset_index('id', inplace=True)
file_log.fillna(' ', inplace = True)

user_log = pd.read_csv('https://gist.githubusercontent.com/pk2203/e845ce82cf77a243d69ffad3346ea919/raw/c8c2f203b302aa38a137b817053b9e5e4e2602fe/UserLog.csv')


def layout():
    return html.Div(
        id='app-body',
        className='app-body_desc',
        children=[
            html.Div(
                id='banner',
                className='banner_desc',
                children=[html.H2("Audit Console"), html.H5("Welcome PARVATHY KURUP")]
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
                                                html.H2("Welcome to Audit Console: "),
                                                html.Hr(),
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
                                                            {'name': 'Directory', 'id': 'Directory', 'type': 'text'},
                                                            {'name': 'Sub-Folder', 'id': 'Sub-Folder', 'type': 'text'},
                                                            {'name': 'Packages', 'id': 'Packages', 'type': 'text'},
                                                            {'name': 'Data-Description', 'id': 'Data-Description','type': 'text'}
                                                        ],
                                                        data=file_log.to_dict('records'),
                                                        filter_action='native',
                                                        row_selectable='single',
                                                        selected_rows=[],
                                                        page_size=10,
                                                        style_data={
                                                            'width': '150px', 'minWidth': '150px', 'maxwidth': '150px',
                                                            'overflow': 'hidden',
                                                            'textOverflow': 'ellipse', 'color': 'black'
                                                        }
                                                    ),
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.Dropdown(id='directory_drop', options=[x for x in sorted(file_log['Directory'].unique())])
                                                        ], width=3),
                                                        dbc.Col((
                                                            dcc.Dropdown(id='subfolder_drop', options=[x for x in sorted(file_log['Sub-Folder'].unique())]
                                                                        ),
                                                        ), width=3),

                                                    ], justify='between', className='file_log'),

                                                ], fluid= True),
                                                html.Hr(),
                                                html.Button(
                                                    'Extract',
                                                    id='extract-button-val',
                                                    n_clicks=0,
                                                    style={'position': 'center',
                                                           'display': 'inline-block',
                                                           'width': '160px',
                                                           'padding': '10px'}
                                                ),
                                            ]
                                        )]
                                ),
                                dcc.Tab(
                                    label='Extract New',
                                    id= 'extract_new',

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
        Output('subfolder_drop', 'options'),
        Input('directory_drop', 'value')
    )
    def update_folder(selected_dir):
        if selected_dir is None:
            raise PreventUpdate
        return [{'label': i, 'value': i} for i in console_options[selected_dir]]

    @_app.callback(
        Output('subfolder_drop', 'value'),
        Input('subfolder_drop', 'options')
    )
    def disp_folder_val(console_options):
        if console_options[0]['value'] == '':
            raise PreventUpdate
        return console_options[0]['value']

    @_app.callback(
        [Output('file_log_table', 'data'),
         Output('file_log_table', 'page_size')],
        [Input('directory_drop', 'value'),
         Input('subfolder_drop', 'value'),
         Input('row_drop', 'value')]
    )
    def update_file_log(dir_val, sf_val, row_val):
        df = file_log.copy()

        if dir_val is None or sf_val is None or row_val is None:
            raise PreventUpdate

        if dir_val:
            df = df[df.Directory == dir_val]
        if sf_val:
            df = df[df['Sub-Folder'] == sf_val]

        return df.to_dict('records'), row_val

    @_app.callback(
        [Output('extract-button-val', 'n_clicks')],
        [Input('file_log_table','derived_virtual_row_ids'),
         Input('file_log_table','selected_row_ids'),
         Input('file_log_table', 'active_cell')]
    )
    def activate_extraction(row_ids, selected):

'''

app_audit = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app_audit.title = "Audit Console Prototype"
app_audit.layout = layout()
callbacks(app_audit)

if __name__ == '__main__':
    app_audit.run_server(debug=True)

'''