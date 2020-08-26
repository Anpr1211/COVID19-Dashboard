# import libraries
import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html 
import pandas as pd
from dash.dependencies import Input, Output

# import app and dataset
from app import app 
from database import data

# read the datasets
df_confirmed = data.df_confirmed
df_deaths = data.df_deaths
df_recovered = data.df_recovered

# making a dataframe which stores only the time series data for the countries
d = df_confirmed.iloc[-1, 1:-1]

# figure to plot the no. of confirmed cases on the world map for the countries
fig_map = px.scatter_geo(locations=d.index, locationmode='country names',
                     size=list(d.values), size_max = 60, projection="natural earth", text=d.index,
                     title = "No. of confirmed cases of COVID19 as on "+str(df_confirmed.iloc[-1, -1].date()))

fig_map.update_traces(hovertemplate="<b>%{text}</b> <br>Confirmed Cases: %{marker.size:,}")           # template of hovertext
    
# dropdown options
countries = df_confirmed.columns[:-1]
opts = [{'label' : i, 'value' : i} for i in countries]

# function to find the countries with the top 10 counts for the given dataframe
def find_top_10(df):
    
    d = df.iloc[-1, 1:-1].astype('int')
    
    top10 = d.nlargest(10)        
    
    return top10

# function to find the countries with the top 10 % counts for the given dataframe    
def find_top10_pct(df):
    
    confirmed = df_confirmed.iloc[-1, 1:-1].astype('int')
    
    d = df.iloc[-1, 1:-1].astype('int')

    pct = d.values/confirmed.values * 100
    
    data = pd.DataFrame(d)

    data['pct'] = pct

    top10_pct = data['pct'].nlargest(10)
    
    return top10_pct

# barplot for the countries with the highest number of confirmed cases   
fig1 = px.bar(x = find_top_10(df_confirmed).index, y=find_top_10(df_confirmed).values, title="Countries with the Highest Confirmed Cases")
fig1.update_traces(hovertemplate="<b>%{x}</b> <br>Confirmed Cases: %{y}")
fig1.update_layout(xaxis_title="Countries", yaxis_title="Values")

# barplot for the countries with the highest number of deaths  
fig2 = px.bar(x = find_top_10(df_deaths).index, y=find_top_10(df_deaths).values, title="Countries with the Highest No. of Deaths")
fig2.update_traces(hovertemplate="<b>%{x}</b> <br>No. of Deaths: %{y}")
fig2.update_layout(xaxis_title="Countries", yaxis_title="Values")

# barplot for the countries with the highest number of recoveries  
fig3 = px.bar(x = find_top_10(df_recovered).index, y=find_top_10(df_recovered).values, title="Countries with the Highest No. of Recoveries")
fig3.update_traces(hovertemplate="<b>%{x}</b> <br>No. of Recoveries: %{y}")
fig3.update_layout(xaxis_title="Countries", yaxis_title="Values")

# barplot for the countries with the worst death rate
fig4 = px.bar(x = find_top10_pct(df_deaths).index, y=find_top10_pct(df_deaths).values, title="Countries with the Worst Death Rate")
fig4.update_traces(hovertemplate="<b>%{x}</b> <br>Death Rate: %{y}")
fig4.update_layout(xaxis_title="Countries", yaxis_title="Values")

# barplot for the countries with the best recovery rate 
fig5 = px.bar(x = find_top10_pct(df_recovered).index, y=find_top10_pct(df_recovered).values, title="Countries with the Best Recovery Rate")
fig5.update_traces(hovertemplate="<b>%{x}</b> <br>Recovery Rate: %{y}")
fig5.update_layout(xaxis_title="Countries", yaxis_title="Values")

# define the layout of the Analysis tab
layout = html.Div([
                   dcc.Tabs(id='tabs-example', value='tab-1', children=[
                   dcc.Tab(label='Spread of COVID19', value='tab-1'),              # world map
                   dcc.Tab(label='Country wise Daily Change', value='tab-2'),      # time series plot for the given country
                   dcc.Tab(label='Highest Confirmed Cases', value='tab-3'),        # barplot for the countries with the highest number of confirmed cases  
                   dcc.Tab(label='Highest Deaths', value='tab-4'),                 # barplot for the countries with the highest number of deaths
                   dcc.Tab(label='Highest Recoveries', value='tab-5'),             # barplot for the countries with the highest number of recoveries  
                   dcc.Tab(label='Worst Death Rate', value='tab-6'),               # barplot for the countries with the worst death rate
                   dcc.Tab(label='Best Recovery Rate', value='tab-7')              # barplot for the countries with the best recovery rate 
                   ]),
                   html.Div(id='tabs-example-content')
                  ])

# decorator which will ensure that the updation function is called when the input changes
@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])

# function which updates the dashboard based on the inputs               		 
def render_content(tab):

    if tab == 'tab-1':
        return html.Div([
            dcc.Graph(id='map', figure=fig_map)
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Label("Choose a country"),
             	   dcc.Dropdown(id = 'opt', options = opts, value='World'),
             	   dcc.Graph(id='daily_change'),
        ])
    elif tab == 'tab-3':
        return html.Div([
            dcc.Graph(id='highest_confirmed_cases', figure=fig1)
        ])
    elif tab == 'tab-4':
        return html.Div([
            dcc.Graph(id='highest_deaths', figure=fig2)
        ])
    elif tab == 'tab-5':
        return html.Div([
            dcc.Graph(id='highest_recoveries', figure=fig3)
        ])
    elif tab == 'tab-6':
        return html.Div([
            dcc.Graph(id='worst_death_pct', figure=fig4)
        ])
    elif tab == 'tab-7':
        return html.Div([
            dcc.Graph(id='best_recovery_pct', figure=fig5)
        ])

# decorator which will ensure that the updation function is called when the dropdown input of daily_change tab changes
@app.callback(Output('daily_change', 'figure'),
             [Input('opt', 'value')]
             )	

# function which updates the dashboard based on the dropdown input of daily_change tab 	
def update_figure(input1): 
    
    # time series plot for given country
    fig = px.line(df_confirmed, x='Date', y=input1, title='Daily Change')
    fig['data'][0]['showlegend']=True
    fig['data'][0]['name']='Confirmed'

    fig.add_scatter(x=df_recovered['Date'], y=df_recovered[input1], mode='lines', name='Recovered')
    fig.add_scatter(x=df_deaths['Date'], y=df_deaths[input1], mode='lines', name='Deaths')
    
    return fig
