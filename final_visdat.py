# -*- coding: utf-8 -*-
"""Final_Visdat.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wud8m7Sf74Med_bEvyQBC5TZTYpPeimx
"""

# import required libraries
import pandas as pd
import numpy as np

# read dataset
df = pd.read_csv('imdb_top_1000.csv')

# display dataset head
df.head()

# count dataset columns and rows
print("Columns: ", df.shape[1])
print("Rows: ", df.shape[0])

# display dataset general info
df.info()

# define a more compact version of previous dataset
df2 = df[['Series_Title', 'Released_Year', 'Genre', 'IMDB_Rating', 'No_of_Votes']]
df2['Released_Year'] = df2['Released_Year'].astype(int)
df2

# convert and scale object attribute to integer
from sklearn.preprocessing import LabelEncoder

labelEncoder = LabelEncoder()
labelEncoder.fit(df2['No_of_Votes'])
df2['No_of_Votes'] = labelEncoder.transform(df2['No_of_Votes'])

# further scaling of attribute
df2['No_of_Votes'] = [x / 25 for x in df2['No_of_Votes']]

# import required bokeh modules 
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show 
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.layouts import widgetbox, row
import random

# define data source for plot
source = ColumnDataSource(df2)

# file to save the model 
output_file("visdat_final.html") 
  
# color value for each points
N = 1000
a = np.random.random(size=N) * 100
b = np.random.random(size=N) * 100
colors = np.array([ [r, g, 150] for r, g in zip(50 + 2*a, 30 + 2*b) ], dtype = "uint8")

# define figure and points
fig = figure(x_axis_label = 'Year Released', 
    y_axis_label = 'Rating',
    title = 'TOP 1000 IMDB MOVIES (1920-2020)  |  %d Movies selected' % len(df2),
    height = 600, 
    width = 1000,
    tools = 'pan,box_zoom, hover, reset')

fig.circle(x = source.data['Released_Year'], 
    y = source.data['IMDB_Rating'],
    color = colors, 
    size = source.data['No_of_Votes'], 
    line_color = None, 
    alpha = 0.4,
    hover_color = 'white', 
    hover_alpha = 0.5)

# define method for selecting movies
def select_title():
    print('Selecting Title...')
    selected = df2[
        (df2.Released_Year >= min_year.value) &
        (df2.Released_Year <= max_year.value) &
        (df2.IMDB_Rating >= rating.value)
    ]
    if (genre.value != "All"):
        selected = selected[selected.Genre.str.contains(genre.value)==True]
    print('Title:', selected)
    return selected

# define method as a callback for widgets
def update_plot(attr, old, new):
    print('update')
    df3 = select_title()

    source.data = dict(
        Series_Title = df3['Series_Title'],
        Released_Year = df3['Released_Year'],
        Genre = df3['Genre'],
        IMDB_Rating = df3['IMDB_Rating'],
        No_of_Votes = df3['No_of_Votes'],
    )

    fig.renderers = []
    N = len(source.data['IMDB_Rating'])
    a = np.random.random(size=N) * 100
    b = np.random.random(size=N) * 100
    colors = np.array([ [r, g, 150] for r, g in zip(50 + 2*a, 30 + 2*b) ], dtype = "uint8")

    fig.title.text = 'TOP 1000 IMDB MOVIES (1920-2020)  |  %d Movies selected' % len(df3)
    fig.circle(x = source.data['Released_Year'], 
        y = source.data['IMDB_Rating'],
        color = colors, 
        size = source.data['No_of_Votes'], 
        line_color = None, 
        alpha = 0.4,
        hover_color = 'white', 
        hover_alpha = 0.5)

# making sliders and dropdown
min_year = Slider(title="Year released", start=1920, end=2020, value=1920, step=5)
min_year.on_change('value',update_plot)

max_year = Slider(title="End Year released", start=1920, end=2020, value=2020, step=5)
max_year.on_change('value',update_plot)

rating = Slider(title="Min Movie Rating", start=7.5, end=9, value=7.5, step=0.1)
rating.on_change('value',update_plot)

genre = Select(title="Genre", options=['All', 'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 
                                       'Drama', 'Family', 'Fantasy', 'Horror', 'Mystery', 'Romance', 
                                       'Sci-Fi', 'Sport', 'Thriller', 'Western'], value='All')
genre.on_change('value', update_plot)

# model settings and display
layout = row(widgetbox(min_year, max_year, rating, genre), fig)
curdoc().add_root(layout)
curdoc().title = 'Visdat Final'
curdoc().theme = 'dark_minimal'
show(layout)