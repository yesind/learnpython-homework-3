from collections import Counter 
from geopy.distance import geodesic
from math import radians, cos
import pandas as pd


stations = pd.read_csv(
    open('bus_stops.csv', 'r', encoding='cp1251'),
    sep=';'
)

list_stations = stations["PlaceDescription"]

stations["PlaceDescription"].head()
res_list=[]
for station in list_stations:
    res_list.append(str(station).split(',')[0])

streets = Counter(res_list)
res=sorted(streets.items(), key=lambda item: item[1], reverse=True)
print(res)

#######################
print('-----------------------')

metro_stations = pd.read_csv(
    open('metro_stops.csv', 'r', encoding='cp1251'),
    sep=';'
)
closed_stations = metro_stations.loc[metro_stations['ObjectStatus'] == 'временно закрыт']['NameOfStation'].tolist()
print(set(closed_stations))

#######################
print('-----------------------')
metro_stations["lat_lon"]=metro_stations[["Latitude_WGS84","Longitude_WGS84"]].apply(tuple,axis=1)
metro_stations["name_lat_lon"]=metro_stations[["NameOfStation","lat_lon"]].apply(tuple,axis=1)

stations["lat_lon"]=stations[["Latitude_WGS84","Longitude_WGS84"]].apply(tuple,axis=1)

radius=500
station_metro_list=[]
for metro_name, metro_exit in metro_stations["name_lat_lon"].to_list()[1:]:
    for bus_stop in stations["lat_lon"].to_list()[1:]:
        if (float(metro_exit[1])-radius/111000<float(bus_stop[1])<float(metro_exit[1])+radius/111000 and 
            float(metro_exit[0])-radius/(111000*cos(radians(float(metro_exit[0]))))<float(bus_stop[0])<float(metro_exit[0])+radius/(111000*cos(radians(float(metro_exit[0]))))):
            if geodesic(metro_exit, bus_stop).m<=radius:
                station_metro_list.append(metro_name)


res_dic = Counter(station_metro_list)
final_dict = {key:value for key, value in res_dic.items() if value == max(res_dic.values())}
print(final_dict)