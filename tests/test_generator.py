from posters.generator import MapGen
import pyproj
import math


def test__latLonToPixels():
    (px,py) = MapGen._latLonToPixels(1,1,1)
    assert (px,py) == ()





P = pyproj.Proj(proj='utm', zone=31, ellps='WGS84', preserve_units=True)
G = pyproj.Geod(ellps='WGS84')

def LatLon_To_XY(Lat,Lon):
    return P(Lat,Lon)  

print(MapGen._latLonToPixels(10,10,1))
print(LatLon_To_XY(10,10))