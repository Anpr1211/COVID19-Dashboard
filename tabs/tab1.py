# import libraries
import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html 
import pandas as pd
from dash.dependencies import Input, Output

from sklearn.metrics import mean_absolute_error
import numpy as np

# import app and dataset
from app import app 
from database import data

# read the dataset
df = data.df_confirmed

# function to calculate mean percentage error of the fits
def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100 
    
# dropdown options
countries = df.columns[:-1]
opts = [{'label' : i, 'value' : i} for i in countries]

# define the layout of the Moving Average tab
layout = html.Div([
		   html.Label("Choose a country"),    # label to provide information
             	   dcc.Dropdown(id = 'opt', options = opts, value='World'),    # dropdown of countries
                   dcc.Graph(id='plot'),    # plot
                   html.Div(id='mae'),      # to display the Mean Absolute Error
                   html.Div(id='mape'),     # to display the Mean Absolute Percentage Error
		   dcc.Slider(id='ma-slider', min=3, max=10, step=1, value=3, marks={i:str(i) for i in range(3, 11)}),    # slider to select the order of the MA model
                   html.Label("Select the window of Moving Average method")	# label to provide information
		 ])

# decorator which will ensure that the updation function is called when the input changes		 
@app.callback([Output('plot', 'figure'), Output('mae', 'children'), Output('mape', 'children')],
             [Input('opt', 'value'),
              Input('ma-slider', 'value')]
             )

# function which updates the dashboard based on the inputs             
def multi_output(input1, input2):
    
    # find the dataframe fitted with rolling mean of window size 'input2', by default 3
    data_ma = df.rolling(window=input2).mean()
    data_ma['Date'] = df['Date']               # add the 'Date' column
    
    # calculate the mean absolute error
    mae = np.round(mean_absolute_error(df[input1][input2:], data_ma[input1][input2:]), decimals=2)
    
    # calculate the mean absolute percentage error
    y_true = list(filter(lambda x:x>0, df[input1][input2:]))         # actual observations
    ma_fits = list(data_ma[input1][input2:])                         # dataframe of predicted observations
    y_pred = ma_fits[len(df[input1][input2:])-len(y_true):]          # predicted observations as an array
    mape = np.round(mean_absolute_percentage_error(y_true, y_pred), decimals=2)        # calculate MAPE
    
    # find out the 7-day forecast
    preds = list(data_ma[input1][-input2:])
    for t in range(7):
      length = len(preds)
      x = np.mean([preds[i] for i in range(length-input2,length)])
      preds.append(x)
    dates = pd.date_range(df['Date'][len(df)-1], periods = 8, closed='right')
    
    # line plot showing the observed/actual datapoints, fitted datapoints and forecasts
    fig = px.line(df, x='Date', y=input1, title='Number of COVID19 cases')
    fig['data'][0]['showlegend']=True
    fig['data'][0]['name']='Actual Values'
    fig.add_scatter(x=data_ma['Date'], y=data_ma[input1], mode='lines', name='Moving Average')
    fig.add_scatter(x=dates, y=preds, mode='lines', name='Forecasts')
   
    return fig,'Mean Absolute Error of the Fits: {}'.format(mae), 'Mean Absolute Percentage Error of the Fits: {}'.format(mape)


