import requests
import numpy as np

# https://wiki.openstreetmap.org/wiki/Overpass_API
overpass_url = "http://overpass-api.de/api/interpreter"
# overpass_url = "https://overpass.kumi.systems/api/interpreter"
query_teplate =  """
[out:json];
 nwr(around:{distance},{lat},{lng});
out body;
"""

def ask_osm(query, url = overpass_url):
    result = requests.get(url, params={'data': query})
    if result.status_code != 200:
        return np.NaN
    else:
        return result.json()


def ask_osm_around_point(lat, lng, distance = 100, url = overpass_url):
    return ask_osm(query_teplate.format(distance = distance, lat=lat, lng=lng), url = url)


# for dataframe
# df.T.apply(ask_osm_around_point_df)
def ask_osm_around_point_df(df_row, distance = 100, url = overpass_url):
    return ask_osm_around_point(lat=df_row.lat, lng=df_row.lng, distance = distance, url = url)

# for np array of coords
# np.apply_along_axis(ask_osm_around_point_np, 1, coords)
def ask_osm_around_point_np(coord_row, distance = 100, lat_index = 0, lng_index = 1, url = overpass_url):
    return ask_osm_around_point(lat=coord_row[lat_index], lng=coord_row[lng_index], distance = distance, url = url)
