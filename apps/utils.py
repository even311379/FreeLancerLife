import pandas as pd
import os
import re
from scipy.spatial import ConvexHull
import numpy as np
from math import radians, cos, sin, asin, sqrt
import json


reflon = 120.982024
reflat = 23.973875

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    '''
    For my purpose, I modify the formula such that negative distance
    would exist.
    '''
    if dlon < 0 or dlat <0:
        c = -c
    km = 6367 * c
    return km

def PolyArea2D(pts):
    lines = np.hstack([pts,np.roll(pts,-1,axis=0)])
    area = 0.5*abs(sum(x1*y2-x2*y1 for x1,y1,x2,y2 in lines))
    return area

def EOO_calculator(data):
    """
    Calculator EOO by projecting GPS data to real distance system (km), 
    and the put in ConvexHull and PolyArea2D function.  
    
    The main bias is the projecting process. Since the 'haversine' 
    function is used to calculate great circle distance between 2 points,
    I have to set a "reference point" for such calculation. So far, I don't 
    have a very solid idea to set a correct "reference point".
    
    I've tried some different ways to set this reference points, and pick one
    with least divergence compared to the result from "http://geocat.kew.org/editor".
    
    There is still some bias range from 1~150 km^2.
    """
    data = data[['Longitude','Latitude']]
    X = [haversine(data.min()[0],(i[1]+data.min()[1])*0.5,i[0],(i[1]+data.min()[1])*0.5) for i in np.array(data)]
    Y = [haversine((i[0]+data.min()[0])*0.5,data.min()[1],(i[0]+data.min()[0])*0.5,i[1]) for i in np.array(data)]
#    X = [haversine(reflon,(reflat+i[1])*.5,i[0],(reflat+i[1])*.5) for i in np.array(data)]
#    Y = [haversine((reflon+i[0])*.5,reflat,(reflon+i[0])*.5,i[1]) for i in np.array(data)]
    points = np.column_stack([X,Y])      
    hull = ConvexHull(points)
    hull_points = [[i,j] for i, j in zip(data.iloc[hull.vertices,0],data.iloc[hull.vertices,1])]
        
    return hull_points, PolyArea2D(points[hull.vertices,:])

def create_geojson(point_list,fish_name):
    print('create my.json')
    base_text = '{"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"type": "Polygon","coordinates": ['

    base_text += str(point_list)
    base_text += "]}}]}"

    with open(os.getcwd()+'/media/documents/{}.json'.format(fish_name), 'w') as f:
        f.write(base_text)

def parse_my_geoj(geoj_filename):
    with open(geoj_filename) as jfile:
        j = json.load(jfile)
    
    name = [j['features'][i]['properties']['name'] for i in range(len(j['features']))]
    coords = [j['features'][i]['geometry']['coordinates'] for i in range(len(j['features']))]
    # since it's so small scale, I can ignore the projection issue to calculate centroid?
    # cents = [(np.array(p[0])[:,0].mean(),np.array(p[0])[:,1].mean()) for p in coords]
    clats = [np.array(p[0])[:,1].mean() for p in coords]
    clons = [np.array(p[0])[:,0].mean() for p in coords]
    return [name, clats, clons]


