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
from nibabel.nifti1 import Nifti1Header, Nifti1Image, save
from _common.nibabelPATCHES.trackvis import empty_header as eH
import numpy

import random

# the fabulous common lib
from _common import FNNDSCFileIO as io


# ..and fyborg, the majesty, himself
import fyborg
import arraypad as ap

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
SAMPLE_VOLUME_SPACING_X = random.sample( [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 2.0], 1 )[0]
SAMPLE_VOLUME_SPACING_Y = random.sample( [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 2.0], 1 )[0]
SAMPLE_VOLUME_SPACING_Z = random.sample( [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 2.0], 1 )[0]

# fiber configuration:
# from 1 to 10 fibers, randomly chosen
NUMBER_OF_FIBERS = random.randint( 1, 10 )


def createSampleVolume( outputfile ):
  '''
  Create a sample volume which has a different value for each voxel.
  
  Then, save the volume.
  '''

  print Colors.PURPLE + 'Creating a sample volume (d:' + Colors.CYAN + str( SAMPLE_VOLUME_DIMENSION_X ) + ',' + str( SAMPLE_VOLUME_DIMENSION_Y ) + ',' + str( SAMPLE_VOLUME_DIMENSION_Z ) + Colors.PURPLE + ' s:' + Colors.CYAN + str( SAMPLE_VOLUME_SPACING_X ) + ',' + str( SAMPLE_VOLUME_SPACING_Y ) + ',' + str( SAMPLE_VOLUME_SPACING_Z ) + '): ' + Colors.ORANGE + outputfile + Colors.PURPLE + '..' + Colors._CLEAR

  testArr = numpy.zeros( ( SAMPLE_VOLUME_DIMENSION_X, SAMPLE_VOLUME_DIMENSION_Y, SAMPLE_VOLUME_DIMENSION_Z ) )

  r = 0
  for i in range( testArr.shape[0] ):
    for j in range( testArr.shape[1] ):
      for k in range( testArr.shape[2] ):
        r += 1
        testArr[i, j, k] = r

  img = Nifti1Image( testArr, None )
  hdr = img.get_header()
  hdr.set_zooms( [SAMPLE_VOLUME_SPACING_X, SAMPLE_VOLUME_SPACING_Y, SAMPLE_VOLUME_SPACING_Z] );
  hdr.set_xyzt_units( 1.0, 1.0 )

  save( img, outputfile )

  return testArr


def createSampleVolumeWithSelectedLabels( outputfile, values ):
  '''
  Create a sample volume which has a randomly chosen value from the values list.
  
  Then, save the volume.
  '''

  print Colors.PURPLE + 'Creating a sample volume (d:' + Colors.CYAN + str( SAMPLE_VOLUME_DIMENSION_X ) + ',' + str( SAMPLE_VOLUME_DIMENSION_Y ) + ',' + str( SAMPLE_VOLUME_DIMENSION_Z ) + Colors.PURPLE + ' s:' + Colors.CYAN + str( SAMPLE_VOLUME_SPACING_X ) + ',' + str( SAMPLE_VOLUME_SPACING_Y ) + ',' + str( SAMPLE_VOLUME_SPACING_Z ) + '): ' + Colors.ORANGE + outputfile + Colors.PURPLE + '..' + Colors._CLEAR

  testArr = numpy.zeros( ( SAMPLE_VOLUME_DIMENSION_X, SAMPLE_VOLUME_DIMENSION_Y, SAMPLE_VOLUME_DIMENSION_Z ) )

  for i in range( testArr.shape[0] ):
    for j in range( testArr.shape[1] ):
      for k in range( testArr.shape[2] ):
        testArr[i, j, k] = random.sample( values, 1 )[0]

  img = Nifti1Image( testArr, None )
  hdr = img.get_header()
  hdr.set_zooms( [SAMPLE_VOLUME_SPACING_X, SAMPLE_VOLUME_SPACING_Y, SAMPLE_VOLUME_SPACING_Z] );
  hdr.set_xyzt_units( 1.0, 1.0 )

  save( img, outputfile )

  return testArr




def createSampleTrkFile( outputfile ):
  '''
  Create a sample track file which contains fibers with random points.
  
  The fiber coordinates match the sample volume from above.
  '''
  fibers = []

  numberOfFibers = NUMBER_OF_FIBERS

  print Colors.PURPLE + 'Creating a sample trkFile (' + Colors.CYAN + str( numberOfFibers ) + ' fibers' + Colors.PURPLE + '): ' + Colors.ORANGE + outputfile + Colors.PURPLE + '..' + Colors._CLEAR

  for f in range( numberOfFibers ):

    # from 3 to 10 points, randomly chosen
    numberOfPoints = random.randint( 3, 10 )

    # the point array reserves 3 components for each point (x,y,z)
    points = numpy.empty( shape=( numberOfPoints, 3 ), dtype=numpy.float32 )

    for p in range( numberOfPoints ):

      # create random points with coordinates in the range 0..9 to match the sample volume's dimensions
      points[p] = [random.randint( 0, int( SAMPLE_VOLUME_DIMENSION_X * SAMPLE_VOLUME_SPACING_X ) - 1 ),
                   random.randint( 0, int( SAMPLE_VOLUME_DIMENSION_Y * SAMPLE_VOLUME_SPACING_Y ) - 1 ),
                   random.randint( 0, int( SAMPLE_VOLUME_DIMENSION_Z * SAMPLE_VOLUME_SPACING_Z ) - 1 )]

    # create an appropriate header
    header = eH()
    header['voxel_size'] = ( SAMPLE_VOLUME_SPACING_X, SAMPLE_VOLUME_SPACING_Y, SAMPLE_VOLUME_SPACING_Z )
    header['dim'] = ( SAMPLE_VOLUME_DIMENSION_X, SAMPLE_VOLUME_DIMENSION_Y, SAMPLE_VOLUME_DIMENSION_Z )

    # store the trk file
    fibers.append( ( points, None, None ) )
    io.saveTrk( outputfile, fibers, header, None, True )

  return numberOfFibers


def validateMapping( volumefile, trkfile, radius=0, map_intermediate=True ):
  '''
  Check if a trk file has correctly mapped scalar values from a volume file.
  
  If radius is > 0 take it into account by looking for the most common value in a sphere
  around the original point. This only happens on start and end points so.
  
  If map_intermediate is active, also the points between end points are validated but never
  using the radius.
  
  Returns TRUE if everything is fine, FALSE if there were errors.
  '''
  # load the mapped trk file
  s = io.loadTrk( trkfile )

  volume = io.readImage( volumefile )
  imageHeader = volume.header
  image_size = volume.shape[:3]

  # grab the tracks
  tracks = s[0]

  # pad the image with zeros
  image = ap.pad( volume, radius, 'constant', constant_values=( 0 ) )

  # any errors?
  any_errors = False

  # incorporate spacing
  spacing = imageHeader.get_zooms()[:3]

  # .. and loop through them
  for t in tracks:

    points = t[0] # the points of this fiber track
    scalars = t[1] # the mapped scalars

    for index, p in enumerate( points ):

      current_point = [ int( a / b ) for a, b in zip( [p[0], p[1], p[2]], spacing )]

      #print 'ORIG', volume[current_point[0], current_point[1], current_point[2]]

      is_first_point = ( index == 0 )
      is_last_point = ( index == len( points ) - 1 )

      # if this is 
      if not map_intermediate and not is_first_point and not is_last_point:
        real_scalar = 0.0
      else:

        # here we check for the neighborhood if radius > 0
        if radius > 0 and ( is_first_point or is_last_point ):

          # neighborhood search!
          r = radius
          a, b, c = current_point

          # crop the image according to the neighborhood look-up
          # since we zero-padded the image, we don't need boundary checks here
          min_x = a - r
          max_x = a + r + 1
          min_y = b - r
          max_y = b + r + 1
          min_z = c - r
          max_z = c + r + 1
          cropped_image = numpy.asarray( image[min_x + r:max_x + r, min_y + r:max_y + r, min_z + r:max_z + r] )


          # create a sphere mask
          x, y, z = numpy.ogrid[0:2 * r + 1, 0:2 * r + 1, 0:2 * r + 1]
          mask = ( x - r ) ** 2 + ( y - r ) ** 2 + ( z - r ) ** 2 <= r * r # 3d sphere mask

          # apply the mask
          masked_container = cropped_image[mask]

          # throw away all zeros (0)
          masked_container = masked_container[numpy.nonzero( masked_container )]

          # find the most frequent label in the masked container
          from collections import Counter

          # by default, we use the original one
          mostFrequentLabel = volume[a, b, c]

          if len( masked_container ) != 0:
            counter = Counter( masked_container )
            all_labels = counter.most_common()
            best_match_label = counter.most_common( 1 )

            original_pos = [i for i, v in enumerate( all_labels ) if v[0] == mostFrequentLabel]

            if not original_pos or all_labels[original_pos[0]][1] != best_match_label[0][1]:
              # the original label appears less often as the new best_match_label
              # in this case, we use the new best matched label
              mostFrequentLabel = best_match_label[0][0]
              # we don't need an else here since the original label is already set

          real_scalar = mostFrequentLabel

        else:

          # simple mapping without radius incorporation and make sure we are inside the volume
          real_scalar = volume[min( current_point[0], image_size[0] - 1 ), min( current_point[1], image_size[1] - 1 ) , min( current_point[2], image_size[2] - 1 )]

      if type( scalars ) is types.NoneType:
        mapped_scalar = -1
      else:
        mapped_scalar = scalars[index][0]

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


def start_test( desc ):

  print Colors.CYAN
  print "   ___         __"
  print " .'  _|.--.--.|  |--..-----..----..-----."
  print " |   _||  |  ||  _  ||  _  ||   _||  _  |"
  print " |__|  |___  ||_____||_____||__|  |___  |"
  print "       |_____|                    |_____|"
  print
  print Colors.ORANGE + "               -= T E S T I N G =-"
  print Colors._CLEAR
  print desc
  print


