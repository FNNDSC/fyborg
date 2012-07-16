# we need to be able to import stuff from one above since this guy lives inside the fyborg repo
import sys
sys.path.append( '../../' )
sys.path.append( '../' )
import shutil
import os
import types

# imaging libs
from nipy.core.image import image
from nipy.io.api import load_image, save_image
import numpy

import random

# the fabulous common lib
from _common import FNNDSCFileIO as io

# ..and fyborg, the majesty, himself
import fyborg

# .. and some colors
from _colors import Colors


# 
#   ___         __                        
# .'  _|.--.--.|  |--..-----..----..-----.
# |   _||  |  ||  _  ||  _  ||   _||  _  |
# |__|  |___  ||_____||_____||__|  |___  |
#       |_____|                    |_____|
#
# THE ULTIMATE SCALAR MAPPING FRAMEWORK FOR TRACKVIS (.TRK) FILES
#
#         -= T E S T I N G =-
#

# dimensions for the sample volume, randomly selected between 10 and 100
SAMPLE_VOLUME_DIMENSION_X = random.randint( 10, 100 )
SAMPLE_VOLUME_DIMENSION_Y = random.randint( 10, 100 )
SAMPLE_VOLUME_DIMENSION_Z = random.randint( 10, 100 )


def createSampleVolume( outputfile ):
  '''
  Create a sample volume 10x10x10 which has a different value for each voxel.
  
  Then, save the volume.
  '''

  testArr = numpy.zeros( ( SAMPLE_VOLUME_DIMENSION_X, SAMPLE_VOLUME_DIMENSION_Y, SAMPLE_VOLUME_DIMENSION_Z ) )

  r = 0
  for i in range( testArr.shape[0] ):
    for j in range( testArr.shape[1] ):
      for k in range( testArr.shape[2] ):
        r += 1
        testArr[i, j, k] = r

  img = image.fromarray( testArr, 'ijk', 'xyz' )

  save_image( img, outputfile )

  return testArr


def createSampleTrkFile( outputfile ):
  '''
  Create a sample track file which contains fibers with random points.
  
  The fiber coordinates match the sample volume from above.
  '''
  fibers = []

  # from 1 to 10 fibers, randomly chosen
  numberOfFibers = random.randint( 1, 10 )

  for f in range( numberOfFibers ):

    # from 3 to 10 points, randomly chosen
    numberOfPoints = random.randint( 3, 10 )

    # the point array reserves 3 components for each point (x,y,z)
    points = numpy.empty( shape=( numberOfPoints, 3 ), dtype=numpy.float32 )

    for p in range( numberOfPoints ):

      # create random points with coordinates in the range 0..9 to match the sample volume's dimensions
      points[p] = [random.randint( 0, SAMPLE_VOLUME_DIMENSION_X - 1 ),
                   random.randint( 0, SAMPLE_VOLUME_DIMENSION_Y - 1 ),
                   random.randint( 0, SAMPLE_VOLUME_DIMENSION_Z - 1 )]

    # store the trk file
    fibers.append( ( points, None, None ) )
    io.saveTrk( outputfile, fibers, None, None, True )

  return numberOfFibers


def validateMapping( volume, trkfile ):
  '''
  Check if a trk file has correctly mapped scalar values from a volume.
  
  Returns TRUE if everything is fine, FALSE if there were errors.
  '''
  # load the mapped trk file
  s = io.loadTrk( trkfile )

  # grab the tracks
  tracks = s[0]

  # any errors?
  any_errors = False

  # .. and loop through them
  for t in tracks:

    points = t[0] # the points of this fiber track
    scalars = t[1] # the mapped scalars

    for i, p in enumerate( points ):

      current_point = p[0], p[1], p[2]
      real_scalar = volume[current_point]

      if type( scalars ) is types.NoneType:
        mapped_scalar = -1
      else:
        mapped_scalar = scalars[i][0]

      # now check if the mapped scalar from the trk file matches the real scalar
      compare = ( mapped_scalar == real_scalar )
      if compare:
        compare = Colors.GREEN + 'OK'
      else:
        compare = Colors.RED + 'WRONG!!!'
        any_errors = True

      print Colors.PURPLE + 'Probing ' + Colors.CYAN + str( current_point ) + Colors.PURPLE + ' for scalar.. SHOULD BE: ' + Colors.CYAN + str( real_scalar ) + Colors.PURPLE + ' WAS: ' + Colors.CYAN + str( mapped_scalar ) + Colors.PURPLE + ' ... ' + str( compare ) + Colors._CLEAR


  # return TRUE if everything went fine and FALSE if there were errors
  return not any_errors


def matlab():
  '''
  Starts matlab.
  '''
  from pymatbridge import Matlab
  mlab = Matlab( matlab='/chb/arch/Linux64/packages/matlab/R2012a/bin/matlab' )

  return mlab

#
# TEST THE MAPPING
# 
# 1. Testcase
#   - test the scalar mapping
#
# 2. Testcase
#   - test the neighborhood look-up mapping
#

print Colors.CYAN
print "   ___         __"
print " .'  _|.--.--.|  |--..-----..----..-----."
print " |   _||  |  ||  _  ||  _  ||   _||  _  |"
print " |__|  |___  ||_____||_____||__|  |___  |"
print "       |_____|                    |_____|"
print
print Colors.ORANGE + "               -= T E S T I N G =-"
print Colors._CLEAR

# temporary storage (always gets overwritten)
volFile = '/chb/tmp/test123.nii'
trkFile = '/chb/tmp/test123.trk'
mappedTrkFile = '/chb/tmp/test123-fyborg.trk'
kihosTrkFile = '/chb/tmp/test123-kiho.trk'

# create a sample volume
print Colors.PURPLE + 'Creating a sample volume (' + Colors.CYAN + str( SAMPLE_VOLUME_DIMENSION_X ) + ',' + str( SAMPLE_VOLUME_DIMENSION_Y ) + ',' + str( SAMPLE_VOLUME_DIMENSION_Z ) + Colors.PURPLE + '): ' + Colors.ORANGE + volFile + Colors.PURPLE + '..' + Colors._CLEAR
volume = createSampleVolume( '/chb/tmp/test123.nii' )
# create a sample trk file
numberOfFibers = createSampleTrkFile( trkFile )
print Colors.PURPLE + 'Creating a sample trkFile (' + Colors.CYAN + str( numberOfFibers ) + ' fibers' + Colors.PURPLE + '): ' + Colors.ORANGE + trkFile + Colors.PURPLE + '..' + Colors._CLEAR


# map the scalars with FYBORG, the majesty
print
print Colors.PURPLE + 'Map the scalars with ' + Colors.ORANGE + ' FYBORG' + Colors.CYAN + ', the majesty.. ' + Colors.PURPLE + ' BE PREPARED!!' + Colors._CLEAR
fyborg.fyborg( trkFile, mappedTrkFile, [fyborg.FyMapAction( 'test', volFile )], 'debug', 'singlethread' ) # run in test mode with debug enabled and only one thread

# matlab
print
print Colors.PURPLE + 'Map the scalars with ' + Colors.ORANGE + ' Kihos FIBER_M MATLAB PACKAGE..' + Colors._CLEAR
# this stuff overwrites the trk file so we will copy it to a safe place
shutil.copyfile( trkFile, kihosTrkFile )
os.system( './test.sh' )

print
print Colors.YELLOW + ' _    _____    __    ________  ___  ______________  _   __'
print Colors.YELLOW + '| |  / /   |  / /   /  _/ __ \/   |/_  __/  _/ __ \/ | / /'
print Colors.YELLOW + '| | / / /| | / /    / // / / / /| | / /  / // / / /  |/ /'
print Colors.YELLOW + '| |/ / ___ |/ /____/ // /_/ / ___ |/ / _/ // /_/ / /|  /'
print Colors.YELLOW + '|___/_/  |_/_____/___/_____/_/  |_/_/ /___/\____/_/ |_/'
print

print Colors.CYAN + 'Testing ' + Colors.ORANGE + ' FYBORG' + Colors.CYAN + ':' + Colors._CLEAR

# .. now check if the mapping was done correctly
result = validateMapping( volume, mappedTrkFile )
if result:
  result = Colors.GREEN + 'ALL OK!'
else:
  result = Colors.RED + 'ERRORS!!!!'
print
print Colors.PURPLE + 'Validation done: ' + result + Colors._CLEAR
print


print Colors.CYAN + 'Testing ' + Colors.ORANGE + ' MATLAB' + Colors.CYAN + ':' + Colors._CLEAR

# .. now check if the mapping was done correctly
result = validateMapping( volume, kihosTrkFile )
if result:
  result = Colors.GREEN + 'ALL OK!'
else:
  result = Colors.RED + 'ERRORS!!!!'
print
print Colors.PURPLE + 'Validation done: ' + result + Colors._CLEAR
print

