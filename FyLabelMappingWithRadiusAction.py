from FyAction import FyAction
from FyMapAction import FyMapAction
import numpy

class FyLabelMappingWithRadiusAction( FyMapAction ):

  def __init__( self, scalarName, volume, neighbors=0 ):
    super( FyLabelMappingWithRadiusAction, self ).__init__( scalarName, volume )

    self.__startLabels = {}
    self.__endLabels = {}
    self.__neighbors = neighbors

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''
    # image dimensions
    n1, n2, n3 = self.__imageDimensions

    # grab first and last coord
    first = coords[0]
    last = coords[-1]

    labels = []

    for currentCoords in [first, last]:
      # do neighbor search

      # convert to ijk
      ijkCoords = [x / y for x, y in zip( currentCoords, self.__imageSpacing )]
      a, b, c = [max( 1, x ) for x in ijkCoords]
      # create 3d sphere mask (from http://stackoverflow.com/questions/8647024/how-to-apply-a-disc-shaped-mask-to-a-numpy-array)
      x, y, z = numpy.ogrid[-a:n1 - a, -b:n2 - b, -c:n3 - c]
      mask = x * x + y * y + z * z <= r * r # 3d sphere mask
      histogram = numpy.histogram( self.__image[mask] )
      mostFrequentLabel = histogram[1][numpy.argmax( histogram[0] )]
      labels.append( mostFrequentLabel )

    self.__startLabels[uniqueFiberId] = [[first[0], first[1], first[2]], labels[0]]
    self.__endLabels[uniqueFiberId] = [[last[0], last[1], last[2]], labels[1]]

    return FyAction.NoScalar

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    '''
    '''
    # read label values if we have matching coordinates
    startLabel = self.__startLabels[uniqueFiberId]
    endLabel = self.__endLabels[uniqueFiberId]

    if x == startLabel[0][0] and y == startLabel[0][1] and z == startLabel[0][2]:
      # this is the start point, so attach the start label
      return int( startLabel[1] )

    elif x == endLabel[0][0] and y == endLabel[0][1] and z == endLabel[0][2]:
      # this is the end point, so attach the end label
      return int( endLabel[1] )

    return 0 # else wise, return an empty scalar
