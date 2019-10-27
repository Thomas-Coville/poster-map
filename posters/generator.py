# ########################################################################
#                       DISCLAIMER
# I am not the inventor of this algorithm, I merely refactored it to fit 
# in a class as a learning project to ramp up on Python.
# the original implementation can be found here: https://github.com/kuboris/high-def-gmap-export
#
# ########################################################################

# Based on older script by Hayden Eskriett
# and https://gis.stackexchange.com/questions/46729/corner-coordinates-of-google-static-map-tile
# Updated 2/2018 to use newer api
### GoogleMapDownloader.py 
### Based on by Hayden Eskriett [http://eskriett.com]
### A script which when given a longitude, latitude and zoom level downloads a
### high resolution google map

import urllib.request
from PIL import Image
import os
import math

from dynaconf import settings

class MapGen(object):

    #Google uses this tile size
    #based on https://gis.stackexchange.com/questions/46729/corner-coordinates-of-google-static-map-tile
    _tileSize = 256
    _initialResolution = 2 * math.pi * 6378137 / _tileSize
    _originShift = 2 * math.pi * 6378137 / 2.0

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude   
        self.zoom = 14            
        self.scale=1
        self.size_tile_x = 512
        self.size_tile_y=512
        self.map_tile_width=18
        self.map_tile_height=14
        self.format_image='png'
        self.maptype='roadmap'
        self.style = 'element:labels.icon%7Cvisibility:off&style=element:labels.text%7Cvisibility:off&style=element:labels.text.fill%7Ccolor:0x000000%7Csaturation:36%7Clightness:40%7Cvisibility:off&style=element:labels.text.stroke%7Ccolor:0x000000%7Clightness:16%7Cvisibility:off&style=feature:administrative%7Celement:geometry.fill%7Ccolor:0x000000%7Clightness:20&style=feature:administrative%7Celement:geometry.stroke%7Ccolor:0x000000%7Clightness:15%7Cweight:1&style=feature:landscape%7Celement:geometry%7Ccolor:0x000000%7Clightness:20&style=feature:poi%7Celement:geometry%7Ccolor:0xeec844%7Clightness:20&style=feature:poi.park%7Cvisibility:off&style=feature:road%7Celement:geometry.fill%7Ccolor:0xf9f9f9%7Cvisibility:on&style=feature:road.arterial%7Celement:geometry%7Ccolor:0x000000%7Clightness:18&style=feature:road.arterial%7Celement:geometry.fill%7Ccolor:0xeec844&style=feature:road.highway%7Celement:geometry.fill%7Ccolor:0xeec844%7Clightness:15%7Cvisibility:on&style=feature:road.highway%7Celement:geometry.stroke%7Ccolor:0x000000%7Clightness:30&style=feature:road.local%7Celement:geometry%7Ccolor:0x000000%7Clightness:16&style=feature:road.local%7Celement:geometry.fill%7Ccolor:0xfffcfc&style=feature:transit%7Celement:geometry%7Ccolor:0x000000%7Clightness:19&style=feature:water%7Celement:geometry%7Ccolor:0xffffff%7Clightness:17'
        self.apikey=settings['GOOGLE_STATIC_MAPS_API_KEY']

    @staticmethod
    def _latLonToPixels(lat, lon, zoom):
        "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"
        mx = lon * MapGen._originShift / 180.0
        my = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)
        my = my * MapGen._originShift / 180.0
        res =MapGen._initialResolution / (2**zoom)
        
        px = (mx + MapGen._originShift) / res
        py = (my + MapGen._originShift) / res
        return px, py
    
    @staticmethod
    def _pixelsToLat( px, py, zoom):
        "Converts pixel coordinates in given zoom level of pyramid to EPSG:900913"
        res = MapGen._initialResolution / (2**zoom)
        mx = px * res - MapGen._originShift
        my = py * res - MapGen._originShift
        lon = (mx / MapGen._originShift) * 180.0
        lat = (my / MapGen._originShift) * 180.0
        lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
        return lat, lon


    def execute(self, id):            
        self.tileSize_width=self.size_tile_x*self.scale
        self.tileSize_height=self.size_tile_y*self.scale
        width_final=self.map_tile_width*self.tileSize_width
        ##Special usecase add another line of tiles at the end for better world map editing
        #width_final=map_tile_width*(self.tileSize_width+1)
        height_final=self.map_tile_height*(self.tileSize_height-50*self.scale)
        map_img = Image.new('RGB', (width_final,height_final))
        #Get coordinates of starting pixels
        pixel_x, pixel_y = self._latLonToPixels(self.latitude, self.longitude,self.zoom)
        for x in range(0, self.map_tile_width):
            for y in range(0, self.map_tile_height) :
                #Get coordinnates for next center of the map
                #Removes 50pix for footer
                final_lat,final_long=self._pixelsToLat(pixel_x+self.size_tile_x*x,pixel_y+((self.size_tile_y-50)*y),self.zoom)
                #print(final_lat,final_long)
                url = 'https://maps.googleapis.com/maps/api/staticmap?key='+self.apikey+'&scale='+str(self.scale)+'&center='+str(final_lat)+','+str(final_long)+'&zoom='+str(self.zoom)+'&format='+ self.format_image+'&maptype='+self.maptype+'&style='+self.style+'&size='+str(self.size_tile_x)+'x'+str(self.size_tile_y)
                print(url)
                current_tile = str(x)+'-'+str(y)
                urllib.request.urlretrieve(url, current_tile)            
                im = Image.open(current_tile)
                # Removes bottom of the image
                im = im.crop((0, 0, self.tileSize_width, self.tileSize_height-(50*self.scale)))
                #If you want to download all tiles manually 
                #im.save("high_resolution_image"+f'{x:02}'+"-"+f'{y:02}'+".png")
                #files.download("high_resolution_image"+f'{x:02}'+"-"+f'{y:02}'+".png")
                map_img.paste(im, (x*self.tileSize_width, (self.map_tile_height-1-y)*(self.tileSize_height-50*self.scale)))
                ### Special usecase -  add another line of tiles at the end for better world map editing
                #if x==1:
                #       print('pasting_side')
                #       map_img.paste(im, ((x-1+map_tile_width)*self.tileSize_width, (map_tile_height-1-y)*(self.tileSize_height-50*scale)))
            
                os.remove(current_tile)
        map_img.save(f"{id}.png")    