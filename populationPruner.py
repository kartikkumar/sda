'''
Copyright (c) 2014, K. Kumar (me@kartikkumar.com)
All rights reserved.
'''

###################################################################################################
# Set up input deck
###################################################################################################

# Set path to TLE catalog file.
tleCatalogFilePath          = "141202_3le_test_catalog.txt"

# Set number of lines per entry in TLE catalog (2 or 3).
tleEntryNumberOfLines       = 3

# Set path to output directory.
outputPath                  = "."

# Set minimum and maximum inclinations [deg].
inclinationMinimum          =
inclinationMaximum          =

# Set minimum and maximum semi-major axes [km].
altitudeMinimum             =
altitudeMaximum             =

# Set minimum and maximum eccentricities [-].
eccentricityMinimum         =
eccentricityMaximum         =

# Set output file name.
outputFileName              = "test_catalog.txt"

###################################################################################################

'''

                        DO NOT EDIT PARAMETERS BEYOND THIS POINT!!!

'''

###################################################################################################
# Set up modules and packages
###################################################################################################

import numpy as np

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from sgp4.propagation import getgravconst

from twoBodyMethods import convertSemiMajorAxisToMeanMotion

###################################################################################################

###################################################################################################
# Read and store TLE catalog
###################################################################################################

# Read in catalog and store lines in list.
fileHandle = open(tleCatalogFilePath)
catalogLines = fileHandle.readlines()
fileHandle.close()

# Strip newline and return carriage characters.
for i in xrange(len(catalogLines)):
    catalogLines[i] = catalogLines[i].strip('\r\n')

# Parse TLE entries and store debris objects.
debrisObjects = []
for tleEntry in xrange(0, len(catalogLines), tleEntryNumberOfLines):
    debrisObjects.append(twoline2rv(catalogLines[tleEntry+1], catalogLines[tleEntry+2], wgs72))

###################################################################################################

###################################################################################################
# Compute pruned list and write to file.
###################################################################################################

# Convert altitude bounds [km] to mean motion [rad/min].
meanMotionMaximum = convertSemiMajorAxisToMeanMotion( \
    altitudeMinimum + getgravconst('wgs72')[2], getgravconst('wgs72')[1]) * 60.0
meanMotionMinimum = convertSemiMajorAxisToMeanMotion( \
    altitudeMaximum + getgravconst('wgs72')[2], getgravconst('wgs72')[1]) * 60.0

# Create pruned list based on bounds specified by user.
prunedList = [(objectIndex) for objectIndex, debrisObject in enumerate(debrisObjects) \
                if (debrisObject.inclo > np.deg2rad(inclinationMinimum)) \
                    & (debrisObject.inclo < np.deg2rad(inclinationMaximum)) \
                    & (debrisObject.no > meanMotionMinimum) \
                    & (debrisObject.no < meanMotionMaximum) \
                    & (debrisObject.ecco > eccentricityMinimum) \
                    & (debrisObject.ecco < eccentricityMaximum)]

# Write pruned catalog in bounded list to text file.
outputFile = open(outputFileName, 'w')

for debrisObjectIndex in prunedList:
    outputFile.write(catalogLines[tleEntryNumberOfLines*debrisObjectIndex])
    outputFile.write('\n')
    outputFile.write(catalogLines[tleEntryNumberOfLines*debrisObjectIndex+1])
    outputFile.write('\n')
    if tleEntryNumberOfLines == 3:
        outputFile.write(catalogLines[tleEntryNumberOfLines*debrisObjectIndex+2])
        outputFile.write('\n')

outputFile.close()

###################################################################################################