from FyAction import FyAction
from FyMapAction import FyMapAction
import numpy
import arraypad as ap
from _common import FNNDSCConsole as con

class FyRadiusMapAction( FyMapAction ):

  def __init__( self, scalarName, volume, neighbors=0 ):
    super( FyRadiusMapAction, self ).__init__( scalarName, volume )

    self._startLabels = {}
    self._endLabels = {}
    self._neighbors = neighbors
    self._paddedImage = ap.pad( self._image, neighbors, 'constant', constant_values=( 0 ) )

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''
    # image dimensions
    n1, n2, n3 = self._imageDimensions

    # grab first and last coord
    first = coords[0]
    last = coords[-1]

    labels = []

    image_size = self._imageDimensions

    for currentCoords in [first, last]:
      # do neighbor search

      # convert to ijk
      ijkCoords = [int( x / y ) for x, y in zip( currentCoords, self._imageSpacing )]
      a, b, c = ijkCoords
      # create 3d sphere mask (from http://stackoverflow.com/questions/8647024/how-to-apply-a-disc-shaped-mask-to-a-numpy-array)
      r = self._neighbors

      # if the radius is 0, just map the regular value
      if r == 0:
        labels.append( self._image[a, b, c] )
        continue

      # pad the image with zeros (which are later ignored) to always get a nice sphere around the original point
      image = self._paddedImage

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
      mostFrequentLabel = self._image[a, b, c]

      if len( masked_container ) != 0:
        counter = Counter( masked_container )
        all_labels = counter.most_common()
        best_match_label = counter.most_common( 1 )

        original_pos = [i for i, v in enumerate( all_labels ) if v[0] == mostFrequentLabel]

        if not original_pos or all_labels[original_pos[0]][1] != best_match_label[0][1]:
          # the original label appears less often as the new best_match_label
          # in this case, we use the new best matched label _or_ the original label is 0.0
          mostFrequentLabel = best_match_label[0][0]
          # we don't need an else here since the original label is already set

      # this will be the best matched label in the neighborhood or the original label because we
      # prefer the original label if it counts as much as the best matched label
      labels.append( mostFrequentLabel )

    self._startLabels[uniqueFiberId] = [[first[0], first[1], first[2]], labels[0]]
    self._endLabels[uniqueFiberId] = [[last[0], last[1], last[2]], labels[1]]

    return FyAction.NoScalar

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    '''
    '''
    # read label values if we have matching coordinates
    startLabel = self._startLabels[uniqueFiberId]
    endLabel = self._endLabels[uniqueFiberId]

    if x == startLabel[0][0] and y == startLabel[0][1] and z == startLabel[0][2]:
      # this is the start point, so attach the start label
      return int( startLabel[1] )

    elif x == endLabel[0][0] and y == endLabel[0][1] and z == endLabel[0][2]:
      # this is the end point, so attach the end label
      return int( endLabel[1] )

    # else wise, return the scalar value without neighborhood lookaround
    return super( FyRadiusMapAction, self ).scalarPerCoordinate( uniqueFiberId, x, y, z )
