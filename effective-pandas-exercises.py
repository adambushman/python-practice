import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


earthquakes = pd.read_csv('C:/Users/Adam Bushman/Documents/Earthquakes.csv/Earthquakes.csv')
cars = pd.read_csv('https://github.com/mattharrison/datasets/raw/master/data/vehicles.csv.zip')

eq_clean = (
    earthquakes
    .drop(['Unnamed: 0'], axis = 1)
    .assign(Year = pd.DatetimeIndex(earthquakes['Date'] + ' ' + earthquakes['Time']).year)
    .assign(Month = pd.DatetimeIndex(earthquakes['Date'] + ' ' + earthquakes['Time']).month)
)


# Magnitude frequencies
(eq_clean
    .assign(bins = pd.cut(earthquakes['mag'], 10))
    .groupby('bins')
    ['id'].count()
)


# Make a plot
(eq_clean
    .groupby('Year')
    .agg({'id': 'count', 'mag': 'max'})
    .reset_index()
    .query('Year < 2014')
    .plot(
        x = 'Year', 
        y = 'id', 
        s = 'mag', 
        c = 'red', 
        kind = 'scatter', 
        title = 'Earthquake Frequency by Year & Magnitude'
    )
)

plt.show()


# Practicing multiple conditions, sorts, and selections
(eq_clean
    .query('Year == 2012 & mag >= 7.0')
    .sort_values(['Date', 'mag'], ascending = [False, False])
    [['Date', 'place', 'mag']]
)

# Ands and ors in filtering
(eq_clean
    .query('(Year == 2012 & mag >= 7.0) | (Year == 2013 & mag < 6.5)')
    .sort_values(['Date', 'mag'], ascending = [False, False])
    [['Date', 'place', 'mag']]
)


# Practicing .loc[]
(eq_clean
    .loc[0:3]
)

(eq_clean
    .groupby('Year')
    .agg({'id': 'count', 'mag': 'max'})
    #.reset_index()
    .rename(columns = {'id': 'Freqency', 'mag': 'Max Magnitude'})
    .loc[[1990, 1995, 2000, 2005]]
)

# Another type of filtering with .loc[]
(eq_clean
    .loc[((eq_clean['mag'] > 8) & (eq_clean['depth'] < 30)) | (eq_clean['Month'] == 2)]
)

prices = pd.Series(
    [5.00, 1.41, 4.24, 6.82, 7.98], 
    index = ['Gum', 'Reeses', 'Almond Joy', 'Utah Truffle', 'See\'s']
)

(prices
    .mul(2.0)
    .loc[lambda i: (i > 10) | (i < 3)]
)


# Practicing with .iloc[]
(prices
    .loc['Almond Joy']
)
(prices
    .iloc[2]
)


(eq_clean
    .query('Year >= 1990 & Year < 2000')
    .groupby('Month')
    .agg({'id': 'count'})
    .rename(columns = {'id': 'Frequency'})
    .sort_values('Frequency', ascending = False)
    # .iloc[0:5] # Top 5; 0:4 doesn't work because of half-open interval
    # .head(5)
    # .iloc[-5:] # Bottom 5
    .tail(5)
)

# Sampling practice
(pd.Series(['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'HOU', 'GSW', 'IND', 'LAC', 'LAL'])
    .sample(
        4, 
        weights = [0.14, 0.14, 0.14, 0.125, 0.105, 0.09, 0.075, 0.06, 0.045, 0.03, 0.02, 0.015, 0.01, 0.005], 
        random_state = 9
    )
)

(eq_clean
    .sample(10, random_state = 10)
    [['Date', 'mag', 'place']]
)


# Reindex let's us filter with stuff that's not in the index without throwing an error
(eq_clean
    .reindex(['Hello', 2])
    .loc[eq_clean['Date'].isnull()]
)

eq_clean['Date'].reindex(['Hello', 2])


# Concatenating series
wins_2021 = pd.Series(
    [42, 56, 23, 12, 19, 63, 65, 12, 32, 45, 34, 37, 35, 22], 
    index = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'HOU', 'GSW', 'IND', 'LAC', 'LAL']
)

wins_2022 = pd.Series(
    wins_2021.sort_values(ascending = True).values, 
    index = wins_2021.index.sort_values(ascending = False)
)

wins_2022.head(5)

(pd.concat(
    [wins_2021, wins_2022], 
    axis = 1, 
    keys = ['wins_2021', 'wins_2022']
)
    .assign(wins_increase = wins_2022 - wins_2021)
    .sort_values('wins_increase', ascending = False)
)


# Joining/merging dataframes

wins_2021_df = pd.DataFrame({
    'team': ['ATL', 'BKN', 'BOS', 'CHI', 'CLE', 'DAL', 'DEN', 'HOU', 'GSW', 'LAC', 'LAL'], 
    'wins': [12, 19, 63, 65, 12, 32, 45, 34, 37, 35, 22]
})

wins_2022_df = pd.DataFrame({
    'team': ['ATL', 'BOS', 'CHA', 'CLE', 'DAL', 'DEN', 'DET', 'HOU', 'GSW', 'IND', 'LAL'], 
    'wins': [42, 56, 23, 12, 65, 12, 32, 45, 37, 35, 22]
})


wins_comps = (
    pd.merge(
        wins_2021_df, 
        wins_2022_df, 
        how = "inner", 
        on = "team"
    )
    .assign(wins_increase = lambda df: df['wins_x'] - df['wins_y'])
    .sort_values('wins_increase', ascending = False)
)


# Pivoting

## Wide to long
(wins_comps
    .melt(id_vars = ['team'], value_vars = ['wins_x', 'wins_y'], var_name = 'years', value_name = 'wins')
)
## Long to wide
(wins_comps
    .pivot()
)


place = eq_clean['place']

ids = (place
    .astype('string')
    .str.lower()
    .str.find('chile')
    .loc[lambda p: p > -1]
)

make = cars['make']

(make
    .astype('string')
    .str.extract(r'ea?')
    #.loc[lambda m: m > -1]
)

ages = pd.Series(
    pd.Series(['18-34', '35-52', '53-64']).sample(40, random_state = 8, replace = True).values
)

(ages
    .str.split('-', expand = True)
    .astype(int)
    .mean(axis = 1)
    .mean(axis = 0)
)

(pd.concat([wins_2022_df, wins_2021_df], axis=0)
    .reset_index()
    .groupby('team')
    .agg({'wins': 'mean'})
    .sort_values('wins', ascending = False)
)

(eq_clean
    .Year
    .value_counts()
    .sort_values(ascending = False)
    .head(5)
)


# Merging/joining
(
    pd.merge(
        wins_2021_df, 
        wins_2022_df, 
        how = "inner", 
        on = "team"
    )
    .mean(axis=1)
)

car_makes = cars["make"]

# String replacement

(car_makes
    .str.replace('A', 'AA')
)

# All manufacturers with consecutive letters
(car_makes
    .loc[(car_makes
        .replace(r'([a-z])\1+', '*', regex = True)
        .str.find('*')
        .gt(-1)
    )]
    .unique()
)

(car_makes
    .loc[(car_makes
        .str.find(' ')
        .gt(-1)
    )]
    .str.cat(sep = ',')
)

(car_makes
    .str.wrap(5)
)


# Earthquake dates and times
eqs = earthquakes["Date"] + " " + earthquakes["Time"]
eqs_upd = earthquakes["updated"]

eqs.head()
eqs_upd.head()

eqs_dt = pd.to_datetime(eqs, utc = True)
eqs_dt_upd = pd.to_datetime(eqs_upd, utc = True)

eqs_dt_upd.dt.tz_convert('America/Denver')


eqs_dt_upd.dt.strftime('%b %d, %Y')

(eqs_dt_upd
    .loc[eqs_dt_upd.dt.is_leap_year]
)


# Dates as index

url = 'https://github.com/mattharrison/datasets/raw/master/data/alta-noaa-1980-2019.csv'
alta_df = pd.read_csv(url)

dates = pd.to_datetime(alta_df.DATE)

snow = (
    alta_df
    .SNOW
    .rename(dates)
)

snow.head()

winter = (snow.index.quarter == 1) | (snow.index.quarter == 4)

snow_clean = (snow
    .where(~(winter & snow.isna()), snow.interpolate())
    .where(~(~winter & snow.isna()), 0)
)

(snow_clean
    .rolling(7)
    .mean()
    .dropna()
)

(snow_clean
    .resample('AS')
    .sum()
    .plot(
        x = 'index', 
        y = 'SNOW', 
        c = 'blue', 
        kind = 'line', 
        title = 'Historical Monthly Snowfall at Alta'
    )
)

plt.show()


(snow_clean
    .div(snow_clean
        .resample('QS')
        .transform('sum')
    )
    .mul(100)
    .fillna(0)
    .sort_values(ascending = False)
    .head(10)
)

(snow_clean
    .loc['2017-10-01':'2018-03-31']
    .div(snow_clean
        .resample('YS')
        .transform('sum')
    )
    .fillna(0)
    .sort_values(ascending = False)
    .head(10)
)

def christmas(idx):
    year = idx.year
    month = idx.month
    return year.where((month == 12), year + 1)

(snow_clean
    .groupby(christmas)
    .sum()
    .sort_values(ascending = False)
    .head
)


# Cumulative Snow Comparison
(
    snow_clean
    .loc['2010-07-01':'2011-06-30']
    .cumsum()
    .reset_index()
    .SNOW
    .rename('2010')
    .plot(
        x = 'index', 
        y = 'SNOW', 
        c = 'green', 
        kind = 'line', 
    )
)
(
    snow_clean
    .loc['1994-07-01':'1995-06-30']
    .cumsum()
    .reset_index()
    .SNOW
    .rename('1994')
    .plot(
        x = 'index', 
        y = 'SNOW', 
        c = 'blue', 
        kind = 'line', 
        title = 'Cumulative Season Snow Comparison'
    )
)

plt.legend(loc = 'upper right')
plt.show()