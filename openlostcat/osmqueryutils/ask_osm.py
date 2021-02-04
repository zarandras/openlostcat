"""
ask osm is about to...
"""

import requests
import numpy as np

# overpass_url = "https://overpass.kumi.systems/api/interpreter"
overpass_url = "http://overpass-api.de/api/interpreter"
""" overpass_url 
for other example see the page: 
https://wiki.openstreetmap.org/wiki/Overpass_API
"""

query_teplate =  """
[out:json];
 nwr(around:{distance},{lat},{lng});
out body;
"""

def ask_osm(query, url = overpass_url):
    """

    :param query:
    :param url:
    :return:
    """
    result = requests.get(url, params={'data': query})
    if result.status_code != 200:
        return np.NaN
    else:
        return result.json()


def ask_osm_around_point(lat, lng, distance = 100, url = overpass_url):
    """

    :param lat:
    :param lng:
    :param distance:
    :param url:
    :return:
    """
    return ask_osm(query_teplate.format(distance = distance, lat=lat, lng=lng), url = url)


def ask_osm_around_point_df(df_row, distance = 100, url = overpass_url):
    """for dataframe

    Examaple:
    df.T.apply(ask_osm_around_point_df) or  df.apply(ask_osm_around_point_df, axis = 1)

    :param df_row:
    :param distance:
    :param url:
    :return:
    """
    return ask_osm_around_point(lat=df_row.lat, lng=df_row.lng, distance = distance, url = url)

def ask_osm_around_point_np(coord_row, distance = 100, lat_index = 0, lng_index = 1, url = overpass_url):
    """for np array of coords

    Example:
    np.apply_along_axis(ask_osm_around_point_np, 1, coords)

    :param coord_row:
    :param distance:
    :param lat_index:
    :param lng_index:
    :param url:
    :return:
    """
    return ask_osm_around_point(lat=coord_row[lat_index], lng=coord_row[lng_index], distance = distance, url = url)
