from dash import Dash, html, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_daq as daq
import pandas as pd

initial_consoles = ['COMET', 'OPERA', 'NGSC', 'TKTODS', 'TRIPS', 'MACS',
                    'CRIS', 'EKAS', 'AIMS', 'MARS']
rapid_console = ['PAX', 'CARGO', 'UC REPOSTIORY', 'MASTERS']
n_asa_console = ['ACCOUNTS PAYABLE', 'ACCOUNTS RECEIVABLE', 'GENERAL LEDGER', 'PETTY CASH']
'''
def header_colors():
    return {
        'bg_color': '#85002D',
        'font_color': 'white'
    }

def description():
    return 'AUDIT CONSOLE'

'''


def layout():
    return html.Div(
        id='audit-body',
        className='app-body',
        children=[
            html.Div(
                className='banner',
                children=[html.H2("Audit Console")]
            ),
            html.Br(),
            html.Div(
                id='audit-console-tabs',
                className='control-tabs',
                children=[
                    dcc.Tabs(id='audit-tabs', value='audit-val', children=[
                        dcc.Tab(
                            label='Audit Console',
                            value='audit-val',
                            children=html.Div(id='control-tab', children=[
                                html.Div(
                                    title='Audit Console',
                                    className='app-choose-block',
                                    children=(
                                        html.Div(className='controls-desc',
                                                 children=[html.H4(children='Select: ')]),
                                        html.Br(),
                                        html.Div(className='controls-console-desc', children='RAPID'),
                                        html.Br(),
                                        dcc.Dropdown(
                                            rapid_console,
                                            id='audit-rapid-val',
                                            multi=False,
                                            value=rapid_console[0]
                                        ),
                                        html.Hr(),
                                        html.Div(className='controls-console-desc', children='N_ASA'),
                                        html.Hr(),
                                        dcc.Dropdown(
                                            n_asa_console,
                                            id='audit-nasa-val',
                                            multi=False,
                                            value=n_asa_console[0]
                                        ),
                                        html.Br(),
                                        html.Hr(),
                                        html.Div(id='console_val1', className='controls-console-desc', children='COMET',
                                                 n_clicks=0),
                                        html.Hr(),
                                        html.Div(id='console_val2', className='controls-console-desc', children='OPERA',
                                                 n_clicks=0),
                                        html.Hr(),
                                        html.Div(id='console_val3', className='controls-console-desc', children='NGSC',
                                                 n_clicks=0),
                                        html.Hr(),
                                        html.Div(id='console_val4', className='controls-console-desc',
                                                 children='TKTODS', n_clicks=0),
                                        html.Hr(),
                                        html.Div(id='console_val5', className='controls-console-desc', children='TRIPS',
                                                 n_clicks=0),
                                        html.Hr(),
                                        html.Div(id='console_val6', className='controls-console-desc', children='MACS',
                                                 n_clicks=0),
                                        html.Hr(),
                                        html.Div(id='console_val7', className='controls-console-desc', children='CRIS',
                                                 n_clicks=0),
                                        html.Hr(),
                                        html.Div(id='console_val8', className='controls-console-desc', children='EKAS',
                                                 n_clicks=0),
                                        html.Hr(),
                                        html.Div(id='console_val9', className='controls-console-desc', children='AIMS',
                                                 n_clicks=0),
                                        html.Hr(),
                                        html.Div(id='console_val10', className='controls-console-desc', children='MARS',
                                                 n_clicks=0),
                                        html.Br()
                                    )
                                )
                            ])
                        )
                    ])
                ]),
            html.Div(id='audit-container'),
            dcc.Store(id='audit-sequence'),
            dcc.Store(id='audit-custom-color')
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
        State('audit-sequence', 'data')
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


# external_stylesheets = ['\assets\style.css']
#app_audit = Dash()
app_audit.layout = layout()
# callbacks(app_audit)
server = app_audit.server

if __name__ == '__main__':
    app_audit.run_server(debug=True)
