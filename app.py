
import pandas as pd
import os
import plotly.io as pio
import plotly.graph_objects as go
import dash
from dash import dcc, html, dash_table, Input, Output
import base64

# External stylesheet
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Load logo image
image_filename = 'data/aei_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode()

# Set Plotly template
pio.templates.default = "plotly_white"

# Read data files
CURR_PATH = os.path.abspath(os.path.dirname(__file__))
budget_df = pd.read_csv(os.path.join(CURR_PATH, "data/budget_estimates.csv"))
poverty_df = pd.read_csv(os.path.join(CURR_PATH, "data/poverty_estimates.csv"))
dists_df = pd.read_csv(os.path.join(CURR_PATH, "data/dist_estimates.csv"))
params_df = pd.read_csv(os.path.join(CURR_PATH, "data/params_data.csv"))

# Primary content function
def make_content(base, reform, refund, ctc_c, u6_bonus, ps, tabs):
    def table_data_base(base, refund, ctc_c, u6_bonus, ps):
        if base == "cl":
            table_data_base = budget_df.loc[(budget_df["type"] == "CL")]
        elif base == "arpa":
            table_data_base = budget_df.loc[(budget_df["type"] == "ARPA")]
        elif base == "obbb":
            table_data_base = budget_df.loc[(budget_df["type"] == "OBBB")]
        return table_data_base

    output_table = table_data_base(base, refund, ctc_c, u6_bonus, ps)
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in output_table.columns],
        data=output_table.to_dict("records"),
        style_table={"overflowX": "auto"},
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=output_table['Year'], y=output_table['Cost'],
        name='Cost', marker_color='indianred'
    ))
    fig.update_layout(title="Budget Estimates", xaxis_title="Year", yaxis_title="Cost ($B)")
    return html.Div([dcc.Graph(figure=fig), table])

# App layout
app.layout = html.Div([
    html.H1("Child Tax Credit App"),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image), style={'height':'10%', 'width':'10%'}),
    html.Div([
        html.Label("Baseline:"),
        dcc.Dropdown(
            id='base-dropdown',
            options=[
                {'label': 'Current Law', 'value': 'cl'},
                {'label': 'ARPA', 'value': 'arpa'},
                {'label': 'OBBB', 'value': 'obbb'}
            ],
            value='cl'
        ),
    ]),
    html.Div(id='output-content')
])

# Callbacks
@app.callback(
    Output('output-content', 'children'),
    Input('base-dropdown', 'value')
)
def update_output(base):
    return make_content(base, None, None, None, None, None, None)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
