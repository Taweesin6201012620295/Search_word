import io
import csv
from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster
import pandas as pd
import plotly.express as px
from datetime import datetime, date

def geopy():

    geolocator = Nominatim(user_agent="sample app")
    name = 'โควิด19'

    headers = ['Address', 'Lat', 'Lon']
    file_name = str(name)+'_map.csv'
    pan = pd.read_csv(str(name)+'_Data.csv')

    for i in pan['places']:
        try:
            if str(i) != 'nan':
                data = geolocator.geocode(str(i))
                data.raw.get("lat"), data.raw.get("lon")
                data.point.latitude, data.point.longitude

                csvfile = open(file_name, 'r', newline='', encoding='utf-8')
                csvfile = open(file_name, 'a', newline='', encoding='utf-8')
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                article = (i, data.point.latitude, data.point.longitude)
                writer.writerow( {'Address':article[0], 'Lat':article[1], 'Lon':article[2]} )
                csvfile.close()
                print("2")

        except FileNotFoundError:
            csvfile = open(file_name, 'w', newline='', encoding='utf-8')
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            article = (i, data.point.latitude, data.point.longitude)
            writer.writerow( {'Address':article[0], 'Lat':article[1], 'Lon':article[2]} )
            csvfile.close()
            print("1")

        except AttributeError:
            print('3')
            pass

def plotly():

    name = 'โควิด19'
    df = pd.read_csv(str(name)+'_map.csv')

    fig = px.scatter_geo(df, 
                        # longitude is taken from the df["lon"] columns and latitude from df["lat"]
                        lon="Lon", 
                        lat="Lat", 
                        # choose the map chart's projection
                        projection="natural earth",
                        # columns which is in bold in the pop up
                        hover_name = "Address",
                        # format of the popup not to display these columns' data
                        hover_data = {"Address":False,
                                    "Lon": False,
                                    "Lat": False})

    # scatter_geo allow to change the map date based on the information from the df dataframe, but we can separately specify the values that are common to all
    # change the size of the markers to 25 and color to red
    fig.update_traces(marker=dict(size=25, color="red"))
    # fit the map to surround the points
    fig.update_geos(fitbounds="locations", showcountries = True)
    # add title
    fig.update_layout(title = 'Your customers')
    fig.write_image(f"C:/Users/Lenovo/Desktop/New folder/{name}_map.png")
    fig.show()

if __name__ == "__main__":
    start = datetime.now()
    #geopy()
    plotly()
    finish = datetime.now()
    print(finish - start)