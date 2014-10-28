#!/usr/bin/env python

import xml.etree.ElementTree as elementtree
import math, time, sys, os

namespace = "http://www.topografix.com/GPX/1/1"
lastlat = 500
lastlon = 500
lasttimestruct = None
lasttrkpt = None

def main():
  inputdir = "/Users/cluening/GPS/GPX/Archive"
  outputdir = inputdir + ".sanified"
  inputfile = '/Users/cluening/GPS/bayobench.gpx'
  inputfile = '/Users/cluening/GPS/gpx.etrex/20100713.gpx'
  inputfile = '2014-09-17 17.36.06 Day.gpx'

  try:
    os.mkdir(outputdir)
  except OSError:
    print "Directory already exists"

#  elementtree.register_namespace('', "http://www.topografix.com/GPX/1/0")
  elementtree.register_namespace('', "http://www.topografix.com/GPX/1/1")

#  for inputfile in [inputfile]:
  for inputfile in os.listdir(inputdir):
    if inputfile.endswith(".gpx"):
      print(inputfile)
      tree = elementtree.parse(inputdir + "/" + inputfile)
      doelement(tree.getroot(), None)
      tree.write(outputdir + "/" + inputfile)

##
# doelement()
##
def doelement(element, parent):
  global lastlat
  global lastlon
  global lasttimestruct
  global lasttrkpt

  if element.tag.endswith("trk") or element.tag.endswith("trkseg"):
    lastlat = 500
    lastlon = 500
    lasttimestruct = None
    lasttrkpt = None

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
      # 150 mph = .067 km/s
      if distdiff/timediff > .067:
        print("Absurd speed! %f km/s" % (distdiff/timediff))
        print("%f, %f" % (lat, lon))
        print parent
        parent.remove(lasttrkpt)
        print("Removed")
      
    lastlat = lat
    lastlon = lon
    lasttimestruct = timestruct
    lasttrkpt = element

#  timestruct1 = time.strptime(timestamp1, "%Y-%d-%mT%H:%M:%SZ")
#  time.mktime(timestruct2) - time.mktime(timestruct1)

#  print element.tag
#  print element.attrib
#  print element.text

  for child in element:
    doelement(child, element)

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
