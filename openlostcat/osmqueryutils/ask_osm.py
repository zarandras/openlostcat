import requests
import numpy as np

overpass_url = "http://overpass-api.de/api/interpreter"
# overpass_url = "https://overpass.kumi.systems/api/interpreter"
query_teplate =  """
[out:json];
 nwr(around:{distance},{lat},{lon});
out body;
"""

def ask_osm(query, url = overpass_url):
    tmp = requests.get(url, params={'data': query})
    if tmp.status_code != 200:
        return np.NaN
    else:
        return tmp.json()


def ask_osm_around_point(lat, lng, distance = 100, url = overpass_url):
    return ask_osm(query_teplate.format(distance = distance, lat=lat, lon=lng), url = url)


# for dataframe
# df.T.apply(ask_osm_around_point_df)
def ask_osm_around_point_df(df, distance = 100, url = overpass_url):
    return ask_osm_around_point(lat=df.lat, lng=df.lng, distance = distance, url = url)

# for np array of coords
# np.apply_along_axis(ask_osm_around_point_np, 1, coords)
def ask_osm_around_point_np(coord, distance = 100, url = overpass_url):
    return ask_osm_around_point(lat=coord[0], lng=coord[1], distance = distance, url = url)
