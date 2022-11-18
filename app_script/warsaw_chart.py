import pandas as pd
import geopandas as gpd
import plotly.express as px
from pymongo import MongoClient

MONGODB_CONNECTION_STRING = ""
client = MongoClient(MONGODB_CONNECTION_STRING)
client.server_info()['ok']
# Database Name
db = client["symbolsDB"]
# Collection Name
col = db["symbols"]

def warsaw_choro(WARTOSC, actual_date):
   district_geo = gpd.read_file("app_script/warsaw_geojson.geojson")
   df = pd.DataFrame(list(col.find()))
   df = df.loc[df['Date'] == actual_date]
   df2 = df.groupby('District', as_index=False)[WARTOSC].mean()
   min_value = df2[WARTOSC].min()
   max_value = df2[WARTOSC].max()
   fig = px.choropleth(df2, geojson=district_geo, locations='District',       
                           color=WARTOSC,
                           color_continuous_scale="Viridis",
                           range_color=(min_value, max_value),
                           featureidkey="properties.name",
                           projection="mercator"
                          )
   fig.update_geos(fitbounds="locations", visible=False)
   fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
   
   return fig

def warsaw_hist(WARTOSC, actual_date):
   df = pd.DataFrame(list(col.find()))
   df = df.loc[df['Date'] == actual_date]
   df = df.loc[~(df[WARTOSC] > 2000000),:]
   fig = px.histogram(df, x=WARTOSC)
   return fig

def warsaw_density(actual_date):
   df = pd.DataFrame(list(col.find()))
   df = df.loc[df['Date'] == actual_date]
   df = df.loc[~(df['Price in PLN'] > 2000000),:]
   fig = px.density_heatmap(df, y="District", x="Price in PLN")
   return fig

def warsaw_scatter(actual_date):
   df = pd.DataFrame(list(col.find()))
   df = df.loc[df['Date'] == actual_date]
   df = df.loc[~(df['Price in PLN'] > 2000000),:]
   fig = px.scatter(df, x="Apartment area", y="Price per meter", opacity=0.65,
                  trendline='ols', trendline_color_override='darkblue')
   return fig

def district_hist(WARTOSC, district_name):
   df = pd.DataFrame(list(col.find()))
   df = df.loc[df['District'] == district_name]
   df = df.loc[~(df[WARTOSC] > 2000000),:]
   fig = px.histogram(df, x=WARTOSC)
   return fig