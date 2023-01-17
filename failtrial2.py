from dash import Dash, html, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_daq as daq
import pandas as pd

initial_consoles = ['COMET', 'OPERA', 'NGSC', 'TKTODS', 'TRIPS', 'MACS',
                    'CRIS', 'EKAS', 'AIMS', 'MARS']
rapid_console = ['PAX', 'CARGO', 'UC REPOSTIORY', 'MASTERS']
n_asa_console = ['ACCOUNTS PAYABLE', 'ACCOUNTS RECEIVABLE', 'GENERAL LEDGER', 'PETTY CASH']

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
                            dcc.Tabs(id='audit-tabs',className='audit_tabs_desc',children=[
                                dcc.Tab(
                                    label='Extract New',
                                    id='extract_new',
                                    children=[
                                        html.Div(
                                            id='extract-new-container',
                                            className='extract_new',
                                            children=[
                                                html.H2("Search: "),
                                                html.Hr(),
                                                html.Br(),
                                                html.Div(id='controls-audit', className='controls_console_desc',
                                                         children=[ html.Div(className='Rapid',children=[
                                                      html.H4('RAPID'),
                                                      dcc.Dropdown(
                                                          rapid_console,
                                                          id='audit-rapid-val',
                                                          multi=False,
                                                          searchable=False,
                                                          clearable=True
                                                )]),
                                                html.Br(),
                                                html.Div(className='N_asa',children=[
                                                    html.H4('N_ASA'),
                                                     dcc.Dropdown(
                                                          n_asa_console,
                                                          id='audit-nasa-val',
                                                          multi=False,
                                                          searchable=False,
                                                          clearable=True
                                                )]),
                                                html.Br(),
                                                html.Div(id='console_val1',n_clicks=0,
                                                         children=[html.H4('COMET')]),
                                                html.Br(),
                                                html.Div(id='console_val2',n_clicks=0,
                                                         children=[html.H4('OPERA')]),
                                                html.Br(),
                                                html.Div(id='console_val3',n_clicks=0,
                                                         children=[html.H4('NGSC')]),
                                                html.Br(),
                                                html.Div(id='console_val4',n_clicks=0,
                                                         children=[html.H4('TKTODS')]),
                                                html.Br(),
                                                html.Div(id='console_val5',n_clicks=0,
                                                         children=[html.H4('TRIPS')]),
                                                html.Br(),
                                                html.Div(id='console_val6',n_clicks=0,
                                                         children=[html.H4('MACS')]),
                                                html.Br(),
                                                html.Div(id='console_val7',n_clicks=0,
                                                         children=[html.H4('CRIS')]),
                                                html.Br(),
                                                html.Div(id='console_val8',n_clicks=0,
                                                         children=[html.H4('AIMS')]),
                                                html.Br(),
                                                html.Div(id='console_val9',n_clicks=0,
                                                         children=[html.H4('EKAS')]),
                                                html.Br(),
                                                html.Div(id='console_val10',n_clicks=0,
                                                         children=[html.H4('MARS')]),

                                            ])
                                    ])
                                ]),
                                dcc.Tab(
                                    label='View New'
                                ),
                                dcc.Tab(
                                    label='User Log'
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
        Output('audit-sequence', 'data'),
        [Input('audit-rapid-val', 'value'),
         Input('audit-nasa-val', 'value'),
         Input('console_val1', 'n_clicks'),
         Input('console_val2', 'n_clicks'),
         Input('console_val3', 'n_clicks'),
         Input('console_val3', 'n_clicks'),
         Input('console_val4', 'n_clicks'),
         Input('console_val5', 'n_clicks'),
         Input('console_val6', 'n_clicks'),
         Input('console_val7', 'n_clicks'),
         Input('console_val8', 'n_clicks'),
         Input('console_val9', 'n_clicks'),
         Input('console_val10', 'n_clicks'),
         ],
    )
    def add_sequence(rapid_val, nasa_val, cv1, cv2, cv3,
                     cv4, cv5, cv6, cv7, cv8, cv9, cv10, current):
        if rapid_val is None or nasa_val is None:
            raise PreventUpdate

        if cv1 is None or cv1 == 0:
            raise PreventUpdate
        if cv2 is None or cv1 == 0:
            raise PreventUpdate
        if cv3 is None or cv1 == 0:
            raise PreventUpdate
        if cv4 is None or cv1 == 0:
            raise PreventUpdate
        if cv5 is None or cv1 == 0:
            raise PreventUpdate
        if cv6 is None or cv1 == 0:
            raise PreventUpdate
        if cv7 is None or cv1 == 0:
            raise PreventUpdate
        if cv8 is None or cv1 == 0:
            raise PreventUpdate
        if cv9 is None or cv1 == 0:
            raise PreventUpdate
        if cv10 is None or cv1 == 0:
            raise PreventUpdate

        if current is None:
            current = {}

        return current

app_audit = Dash(__name__)
app_audit.layout = layout()

if __name__ == '__main__':
    app_audit.run_server(debug=True)
