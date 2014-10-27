#!/usr/bin/env python

import xml.etree.ElementTree as elementtree

lastlat = 500
lastlon = 500

def main():
  inputfile = '/Users/cluening/GPS/GPX/Archive/2014-10-17 09.32.04 Day.gpx'
  inputfile = '/Users/cluening/GPS/bayobench.gpx'

  tree = elementtree.parse(inputfile)

  doelement(tree.getroot())



def doelement(element):
  global lastlat
  global lastlon

  if element.tag.endswith("trk"):
    print "Foo!"
    lastlat = 500
    lastlon = 500

  if element.tag.endswith("trkpt"):
    print element.attrib
    print lastlat
    if(lastlat < 500 and lastlon < 500):
      print "Have a comparison!"
    lastlat = float(element.attrib['lat'])
    lastlon = float(element.attrib['lon'])

#  print element.tag
#  print element.attrib
#  print element.text

  for child in element:
    doelement(child)

if __name__ == "__main__":
  main()
