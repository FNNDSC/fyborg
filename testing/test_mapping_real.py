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
from _common.nibabelPATCHES.trackvis import empty_header as eH
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

  # incorporate spacing
  spacing = volume.header.get_zooms()[:3]

  # .. and loop through them
  for t in tracks:

    points = t[0] # the points of this fiber track
    scalars = t[1] # the mapped scalars

    for i, p in enumerate( points ):

      current_point = [ int( a / b ) for a, b in zip( [p[0], p[1], p[2]], spacing )]

      real_scalar = volume[current_point[0], current_point[1], current_point[2]]

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

      print Colors.PURPLE + 'Probing RAS:' + Colors.CYAN + str( p ) + Colors.PURPLE + ' IJK:' + Colors.CYAN + str( current_point ) + Colors.PURPLE + ' for scalar.. SHOULD BE: ' + Colors.CYAN + str( real_scalar ) + Colors.PURPLE + ' WAS: ' + Colors.CYAN + str( mapped_scalar ) + Colors.PURPLE + ' ... ' + str( compare ) + Colors._CLEAR


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
# 2. Testcase
#   - test the scalar mapping on real data
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
volFile = 'testdata/dti_adc.nii'
trkFile = 'testdata/streamline_small_2_2_2.trk'
mappedTrkFile = '/chb/tmp/test456-fyborg.trk'
kihosTrkFile = '/chb/tmp/test456-kiho.trk'

# load the volume
volume = io.readImage( volFile )
imageHeader = volume.header
imageDimensions = volume.shape[:3]
imageSpacing = imageHeader.get_zooms()[:3]

print Colors.PURPLE + 'Using volume (' + Colors.CYAN + str( imageDimensions[0] ) + ',' + str( imageDimensions[1] ) + ',' + str( imageDimensions[2] ) + Colors.PURPLE + '): ' + Colors.ORANGE + volFile + Colors.PURPLE + '..' + Colors._CLEAR

# load the trk file
s = io.loadTrk( trkFile )
tracks = s[0]
origHeader = s[1]
numberOfFibers = origHeader['n_count']

print Colors.PURPLE + 'Using trkFile (' + Colors.CYAN + str( numberOfFibers ) + ' fibers' + Colors.PURPLE + '): ' + Colors.ORANGE + trkFile + Colors.PURPLE + '..' + Colors._CLEAR


# map the scalars with FYBORG, the majesty
print
print Colors.PURPLE + 'Map the scalars with ' + Colors.ORANGE + ' FYBORG' + Colors.CYAN + ', the majesty.. ' + Colors.PURPLE + ' BE PREPARED!!' + Colors._CLEAR
fyborg.fyborg( trkFile, mappedTrkFile, [fyborg.FyMapAction( 'adc', volFile )] ) # run in test mode

# matlab
print
print Colors.PURPLE + 'Map the scalars with ' + Colors.ORANGE + ' Kihos FIBER_M MATLAB PACKAGE..' + Colors._CLEAR
# this stuff overwrites the trk file so we will copy it to a safe place
shutil.copyfile( trkFile, kihosTrkFile )
os.system( './test_real.sh' )

print
print Colors.YELLOW + ' _    _____    __    ________  ___  ______________  _   __'
print Colors.YELLOW + '| |  / /   |  / /   /  _/ __ \/   |/_  __/  _/ __ \/ | / /'
print Colors.YELLOW + '| | / / /| | / /    / // / / / /| | / /  / // / / /  |/ /'
print Colors.YELLOW + '| |/ / ___ |/ /____/ // /_/ / ___ |/ / _/ // /_/ / /|  /'
print Colors.YELLOW + '|___/_/  |_/_____/___/_____/_/  |_/_/ /___/\____/_/ |_/'
print

print Colors.CYAN + 'Testing ' + Colors.ORANGE + ' FYBORG' + Colors.CYAN + ':' + Colors._CLEAR

# .. now check if the mapping was done correctly
result_fyborg = validateMapping( volume, mappedTrkFile )

print Colors.CYAN + 'Testing ' + Colors.ORANGE + ' MATLAB' + Colors.CYAN + ':' + Colors._CLEAR

# .. now check if the mapping was done correctly
result_kiho = validateMapping( volume, kihosTrkFile )

if result_fyborg:
  result_fyborg = Colors.GREEN + 'ALL OK!'
else:
  result_fyborg = Colors.RED + 'ERRORS!!!!'
print
print Colors.PURPLE + 'Fyborg Validation done: ' + result_fyborg + Colors._CLEAR

if result_kiho:
  result_kiho = Colors.GREEN + 'ALL OK!'
else:
  result_kiho = Colors.RED + 'ERRORS!!!!'
print Colors.PURPLE + 'Matlab Validation done: ' + result_kiho + Colors._CLEAR
print

