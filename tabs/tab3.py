# import libraries
import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html 
import pandas as pd
from dash.dependencies import Input, Output
import pmdarima as pm
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

# define the layout of the ARIMA tab
layout = html.Div([
	     	   html.Label("Choose a country"),              # label to provide information
             	   dcc.Dropdown(id = 'opt-ar', options = opts, value='World'),             # dropdown of countries
                   dcc.Graph(id='plot-ar'),                     # plot
                   html.Div(id='order-ar'),                     # to display the order of the ARIMA model
                   html.Div(id='mae-ar'),                       # to display the Mean Absolute Error
                   html.Div(id='mape-ar')                       # to display the Mean Absolute Percentage Error
		 ])

# decorator which will ensure that the updation function is called when the input changes	
@app.callback([Output('plot-ar', 'figure'), Output('order-ar', 'children'), Output('mae-ar', 'children'), Output('mape-ar', 'children')],
             [Input('opt-ar', 'value')]
             )
 
# function which updates the dashboard based on the inputs 
def multi_output(input1):
    
    # fit the ARIMA model by grid-searching the parameters
    model = pm.auto_arima(df[input1], max_d=4, scoring='mae', error_action='ignore')
    start = model.get_params()['order'][1]
    end = len(df)-1
    
    # fitted observations
    arima_fits = model.predict_in_sample(start=start, end=end)
    
    # order of the model
    order = model.get_params()['order']

    # calculate the mean absolute error
    mae = np.round(mean_absolute_error(df[input1][start:], arima_fits), decimals=2)

    # calculate the mean absolute percentage error
    y_true = list(filter(lambda x:x>0, df[input1][start:]))                   # actual observations
    y_pred = arima_fits[len(df[input1][start:])-len(y_true):]                 # fitted/predicted observations
    mape = np.round(mean_absolute_percentage_error(y_true, y_pred), decimals=2)             # calculate MAPE

    # find out the 7-day forecast
    preds = model.predict(n_periods=7)
    dates = pd.date_range(df['Date'][len(df)-1], periods = 8, closed='right')

    # line plot showing the observed/actual datapoints, fitted datapoints and forecasts
    fig = px.line(df, x='Date', y=input1, title='Number of COVID19 cases')
    fig['data'][0]['showlegend']=True
    fig['data'][0]['name']='Actual Values'
    fig.add_scatter(x=df['Date'], y=arima_fits, mode='lines', name='ARIMA Model')
    fig.add_scatter(x=dates, y=preds, mode='lines', name='Forecasts')
   
    return fig, 'Order of the Model: {}'.format(order), 'Mean Absolute Error of the Fits: {}'.format(mae), 'Mean Absolute Percentage Error of the Fits: {}'.format(mape)


