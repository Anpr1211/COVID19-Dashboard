# import libraries
import pandas as pd

# function to clean the data
def clean_data(df):
    
    df = df.drop(['Province/State', 'Lat', 'Long'], axis=1)                   # delete the unnecessary columns
    data = df.groupby('Country/Region').sum()                                 # add the no. of cases over countries
    data = data.T
    data.insert(0, 'World', list(df.sum()[1:]))                               # insert the entry for 'World'
    data['Date'] = data.index                                                 # add the Date column
    data['Date'] = pd.to_datetime(data['Date'])                               # convert to DateTime format
    data.index = range(len(data))                                             # change the index
    
    return data

# url from where the data is collected
url_confirmed = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

# reading the data
df_confirmed = clean_data(pd.read_csv(url_confirmed))
df_deaths = clean_data(pd.read_csv(url_deaths))
df_recovered = clean_data(pd.read_csv(url_recovered))
