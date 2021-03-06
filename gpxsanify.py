#!/usr/bin/env python

import xml.etree.ElementTree as elementtree
import math, time, sys, os
import argparse

# Command line options to include:
# - absurd speed (default to speed of sound)
# - iterate until no more changes

args = None
debuglevel = 1
namespaces = ["http://www.topografix.com/GPX/1/0",
              "http://www.topografix.com/GPX/1/1"]
lastlat = 500
lastlon = 500
lasttimestruct = None
lasttrkpt = None
filechanged = True  # Set to true to ensure at least one pass through doelement()

def main():
  global args
  global filechanged
  #inputdir = "/Users/cluening/GPS/GPX/Archive"
  #outputdir = inputdir + ".sanified"
  #inputfile = '/Users/cluening/GPS/bayobench.gpx'
  #inputfile = '/Users/cluening/GPS/gpx.etrex/20100713.gpx'
  #inputfile = '2014-09-17 17.36.06 Day.gpx'

  # Set up the option parser
  parser = argparse.ArgumentParser(description='Sanify those GPX files!')
  parser.add_argument('--inputfile', dest='inputfile', action='store', 
                      help="Single GPX file to sanify")
  parser.add_argument('--outputfile', dest='outputfile', action='store', 
                      help="Output file for single file sanification")
  parser.add_argument('--inputdir', dest='inputdir', action='store', 
                      help="Input directory to search for GPX files")
  parser.add_argument('--outputdir', dest='outputdir', action='store', 
                      help="Output directory for sanified GPX files")
  parser.add_argument('--debuglevel', dest='debuglevel', action='store',
                      help="Debug level", default=0)
  args = parser.parse_args()

  # Verify the option input
  if args.inputfile == None and args.inputdir == None:
    error("Need an input file or input directory", 1)
  if args.inputfile != None and args.inputdir != None:
    error("Can't do both a single file and a directory at the same time", 1)
  if args.inputfile != None and args.outputfile == None:
    error("Need to specify an output file with an input file", 1)
  if args.inputdir != None and args.outputdir == None:
    error("Need to specify an output directory with an input directory", 1)

  if args.inputdir == None:
    args.inputdir = ""

  if args.outputdir != None:
    try:
      os.mkdir(args.outputdir)
    except OSError:
      warn("Directory already exists")
  else:
    # We didn't get an output directory, so we must be doing a single
    # file with a full path
    outputdir = ""


  if args.inputfile != None:
    inputfiles = [args.inputfile]
  else:
    try:
      inputfiles = os.listdir(args.inputdir)
    except OSError as detail:
      error("Error opening %s: %s" % (args.inputdir, detail), 1)

  for inputfile in inputfiles:
    if inputfile.endswith(".gpx"):
      debug(inputfile)
      filechanged = True
      try:
        tree = elementtree.parse(os.path.join(args.inputdir, inputfile))
      except elementtree.ParseError as detail:
        warn("Bad file: %s: %s" % (inputfile, detail))
        continue
#      tree.write(sys.stdout)

      for namespace in namespaces:
        elementtree.register_namespace('', namespace)
        trkpts = tree.getroot().findall("{%s}trk" % namespace)
        if len(trkpts) > 0:
          debug("Good namespace: %s" % namespace)
          break
      else:
        warn("Couldn't find any valid namespaces in %s" % (inputfile))
        continue

      while filechanged != False:
        filechanged = False
        doelement(tree.getroot(), None, namespace)

      if args.outputfile != None:
        tree.write(args.outputfile)
      else:
        tree.write(os.path.join(args.outputdir, inputfile))

##
## doelement()
##
def doelement(element, parent, namespace):
  global lastlat
  global lastlon
  global lasttimestruct
  global lasttrkpt
  global filechanged

  if element.tag.endswith("trk") or element.tag.endswith("trkseg"):
    lastlat = 500
    lastlon = 500
    lasttimestruct = None
    lasttrkpt = None

  if element.tag.endswith("trkpt"):
    #print(element.attrib)
    #print(lastlat)

    timeelement = element.find("{%s}time" % namespace)
    timestruct = time.strptime(timeelement.text, "%Y-%m-%dT%H:%M:%SZ")
    lat = float(element.attrib['lat'])
    lon = float(element.attrib['lon'])
 
    if(lastlat < 500 and lastlon < 500):
      #print("Have a comparison!")
      timediff = time.mktime(timestruct) - time.mktime(lasttimestruct)
      distdiff = haversine(lon, lat, lastlon, lastlat)
      #print("Time difference: %f seconds" % timediff)
      #print("Dist difference: %f kilometers" % distdiff)

      debug("Speed: %f km/s" % (distdiff/timediff))

      # Speed of sound: 343 m/s
      # 150 mph = .067 km/s
      if distdiff/timediff > .067:
        debug("Absurd speed! %f km/s" % (distdiff/timediff))
        debug("%f, %f" % (lat, lon))
        parent.remove(lasttrkpt)
        filechanged = True
      
    lastlat = lat
    lastlon = lon
    lasttimestruct = timestruct
    lasttrkpt = element

  for child in element:
    doelement(child, element, namespace)

##
## debug()
## 
def debug(message):
  if args.debuglevel > 0:
    sys.stderr.write(message + "\n")

##
## warn()
##
def warn(message):
  sys.stderr.write(message + "\n")

##
## error()
##
def error(message, exitcode):
  sys.stderr.write(message + "\n")
  sys.exit(exitcode)

##
##  haversine() function.  Stolen from stackoverflow
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
