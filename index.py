# import libraries
import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output

import pandas as pd

# import app, tabs and dataset
from app import app
from tabs import tab1, tab2, tab3, tab_a
from database import data

# define the layout of app
app.layout = html.Div([
                  dcc.Tabs(id='tabs', value='tab-a', children=[
                  dcc.Tab(label='Analysis', value='tab-a'),
        	  dcc.Tab(label='Moving Average', value='tab-1'),
        	  dcc.Tab(label='Exponential Smoothing', value='tab-2'),
                  dcc.Tab(label='ARIMA', value='tab-3')
    ]),
    html.Div(id='tabs-content')
])

# decorator which will ensure that the updation function is called when the input changes
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])

# function which updates the dashboard based on the inputs  
def render_content(tab):
    if tab == 'tab-a':
       return tab_a.layout
    elif tab == 'tab-1':
       return tab1.layout
    elif tab == 'tab-2':
       return tab2.layout
    elif tab == 'tab-3':
       return tab3.layout

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='8050', debug=True)
