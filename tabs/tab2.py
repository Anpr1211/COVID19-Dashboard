# import libraries
import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html 
import pandas as pd
from dash.dependencies import Input, Output
from statsmodels.tsa.api import Holt
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

# define the layout of the Exponential Smoothing tab
layout = html.Div([
		   html.Label("Choose a country"),       # label to provide information
             	   dcc.Dropdown(id = 'opt-es', options = opts, value='World'),          # dropdown of countries
                   dcc.Graph(id='plot-es'),           # plot
                   html.Div(id='mae-es'),             # to display the Mean Absolute Error
                   html.Div(id='mape-es')             # to display the Mean Absolute Percentage Error
		 ])
	
# decorator which will ensure that the updation function is called when the input changes	
@app.callback([Output('plot-es', 'figure'), Output('mae-es', 'children'), Output('mape-es', 'children')],
             [Input('opt-es', 'value')]
             )

# function which updates the dashboard based on the inputs 
def multi_output(input1):
    
    model = Holt(df[input1]).fit()          # fit the Exponential Smoothing model
    exp_sm = model.fittedvalues             # fitted values of the model

    # calculate the mean absolute error
    mae = np.round(mean_absolute_error(df[input1], exp_sm), decimals=2)

    # calculate the mean absolute percentage error
    y_true = list(filter(lambda x:x>0, df[input1]))        # actual observations
    y_pred = exp_sm[len(df[input1])-len(y_true):]          # fitted/predicted observations
    mape = np.round(mean_absolute_percentage_error(y_true, y_pred), decimals=2)
    
    # find out the 7-day forecast
    preds = model.predict(start=len(df), end=len(df)+6)
    dates = pd.date_range(df['Date'][len(df)-1], periods = 8, closed='right')

     # line plot showing the observed/actual datapoints, fitted datapoints and forecasts
    fig = px.line(df, x='Date', y=input1, title='Number of COVID19 cases')
    fig['data'][0]['showlegend']=True
    fig['data'][0]['name']='Actual Values'
    fig.add_scatter(x=df['Date'], y=exp_sm, mode='lines', name='Exponential Smoother')
    fig.add_scatter(x=dates, y=preds, mode='lines', name='Forecasts')
   
    return fig,'Mean Absolute Error of the Fits: {}'.format(mae), 'Mean Absolute Percentage Error of the Fits: {}'.format(mape)


