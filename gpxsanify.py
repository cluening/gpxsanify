#!/usr/bin/env python

import xml.etree.ElementTree as elementtree
import math, time

namespace = "http://www.topografix.com/GPX/1/1"
lastlat = 500
lastlon = 500
lasttimestruct = 0

def main():
  inputfile = '/Users/cluening/GPS/GPX/Archive/2014-10-17 09.32.04 Day.gpx'
  inputfile = '/Users/cluening/GPS/bayobench.gpx'
  inputfile = '/Users/cluening/GPS/GPX/Archive/2014-10-03 10.57.04 Day.gpx'
  inputfile = '/Users/cluening/GPS/GPX/Archive/2014-07-19 11.19.34 Day.gpx'
  inputfile = '/Users/cluening/GPS/GPX/Archive/2014-09-17 17.36.06 Day.gpx'

  tree = elementtree.parse(inputfile)

  doelement(tree.getroot())


##
# doelement()
##
def doelement(element):
  global lastlat
  global lastlon
  global lasttimestruct

  if element.tag.endswith("trk"):
    print "New track!"
    lastlat = 500
    lastlon = 500
    lasttimestruct = 0

  if element.tag.endswith("trkpt"):
    #print element.attrib
    #print lastlat

    timeelement = element.find("{%s}time" % namespace)
    timestruct = time.strptime(timeelement.text, "%Y-%m-%dT%H:%M:%SZ")
    lat = float(element.attrib['lat'])
    lon = float(element.attrib['lon'])
 
    if(lastlat < 500 and lastlon < 500):
      #print "Have a comparison!"
      timediff = time.mktime(timestruct) - time.mktime(lasttimestruct)
      distdiff = haversine(lon, lat, lastlon, lastlat)
      #print("Time difference: %f seconds" % timediff)
      #print("Dist difference: %f kilometers" % distdiff)
      #print("Speed: %f km/s" % (distdiff/timediff))

      # Speed of sound: 343 m/s
      if distdiff/timediff > .343:
        print("Absurd speed! %f km/s" % (distdiff/timediff))
      
    lastlat = lat
    lastlon = lon
    lasttimestruct = timestruct

#  timestruct1 = time.strptime(timestamp1, "%Y-%d-%mT%H:%M:%SZ")
#  time.mktime(timestruct2) - time.mktime(timestruct1)

#  print element.tag
#  print element.attrib
#  print element.text

  for child in element:
    doelement(child)

##
##  haversine() function.  Stolen from stacktrace
##
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km 

if __name__ == "__main__":
  main()
