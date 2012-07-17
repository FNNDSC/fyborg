from FyAction import FyAction
from FyMapAction import FyMapAction
import numpy
from _common import FNNDSCConsole as con

class FyLabelMappingWithRadiusAction( FyMapAction ):

  def __init__( self, scalarName, volume, neighbors=0 ):
    super( FyLabelMappingWithRadiusAction, self ).__init__( scalarName, volume )

    self._startLabels = {}
    self._endLabels = {}
    self._neighbors = neighbors

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''
    # image dimensions
    n1, n2, n3 = self._imageDimensions

    # grab first and last coord
    first = coords[0]
    last = coords[-1]

    labels = []

    for currentCoords in [first, last]:
      # do neighbor search

      # convert to ijk
      ijkCoords = [round( x / y ) for x, y in zip( currentCoords, self._imageSpacing )]
      a, b, c = ijkCoords
      # create 3d sphere mask (from http://stackoverflow.com/questions/8647024/how-to-apply-a-disc-shaped-mask-to-a-numpy-array)
      r = self._neighbors
      croppedImage = numpy.asarray( self._image[a - r:a + r + 1, b - r:b + r + 1, c - r:c + r + 1] )
      x, y, z = numpy.ogrid[0:2 * r + 1, 0:2 * r + 1, 0:2 * r + 1]
      mask = ( x - r ) ** 2 + ( y - r ) ** 2 + ( z - r ) ** 2 <= r * r # 3d sphere mask
      # find the most frequent label
      from collections import Counter
      counter = Counter( croppedImage[mask] )
      mostFrequentLabel = counter.most_common( 1 )[0][0]
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

    return 0 # else wise, return an empty scalar
