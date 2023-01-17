from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
# Need to use Python 3.8 or higher and Dash 2.2.0 or higher

df = pd.read_csv('https://gist.githubusercontent.com/pk2203/ecf0db94f489018ac337d33ef6aa69ac/raw/5e24aa20d64fe305fc20cd3faf38cfae8e215b32/file_log.csv')
df = df[['Directory', 'Sub-Folder', 'Packages', 'Data-Description']]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    dcc.Markdown('# DataTable Tips and Tricks', style={'textAlign':'center'}),

    dbc.Label("Show number of rows"),
    row_drop := dcc.Dropdown(value=10, clearable=False, style={'width':'35%'},
                             options=[10, 25, 50, 100]),

    my_table := dash_table.DataTable(
        columns=[
            {'name': 'Directory', 'id': 'directory', 'type': 'text'},
            {'name': 'Sub-Folder', 'id': 'subfolder', 'type': 'text'},
            {'name': 'Packages', 'id': 'packages', 'type': 'text'},
            {'name': 'Data-Description', 'id': 'datadesc', 'type': 'text'}
        ],
        data=df.to_dict('records'),
        filter_action='native',
        page_size=10,

        style_data={
            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        }
    ),
    dbc.Row([
        dbc.Col([
            directory_drop := dcc.Dropdown([x for x in sorted(df['Directory'].unique())])
        ], width=3),
        dbc.Col([
            subfolder_drop := dcc.Dropdown([x for x in sorted(df['Sub-Folder'].unique())], multi=True)
        ], width=3),

    ], justify="between", className='mt-3 mb-4'),

])

@callback(
    Output(my_table, 'data'),
    Output(my_table, 'page_size'),
    Input(directory_drop, 'value'),
    Input(subfolder_drop, 'value'),
    Input(row_drop, 'value')
)
def update_dropdown_options(dir_v, sub_v, row_v):
    dff = df.copy()

    if dir_v:
        dff = dff[dff.continent==dir_v]
    if sub_v:
        dff = dff[dff.country.isin(sub_v)]

    return dff.to_dict('records'), row_v
'''
if __name__ == '__main__':
    app.run_server(debug=True)
