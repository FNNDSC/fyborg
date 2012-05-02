from FyMapAction import FyMapAction

class FyLabelMappingWithRadiusAction( FyMapAction ):

  def __init__( self, scalarName, volume ):
    super( FyLabelMappingWithRadiusAction, self ).__init__( scalarName, volume )

    self.__startLabels = {}
    self.__endLabels = {}

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''
    # grab first and last coord
    firstCoord = coords[0]
    lastCoord = coords[-1]

    # do neighbor search

    # store the label values
    startLabel = super( FyLabelMappingWithRadiusAction, self ).scalarPerCoordinate( uniqueFiberId, firstCoord[0], firstCoord[1], firstCoord[2] )
    endLabel = super( FyLabelMappingWithRadiusAction, self ).scalarPerCoordinate( uniqueFiberId, lastCoord[0], lastCoord[1], lastCoord[2] )

    self.__startLabels[uniqueFiberId] = [[firstCoord[0], firstCoord[1], firstCoord[2]], startLabel]
    self.__endLabels[uniqueFiberId] = [[lastCoord[0], lastCoord[1], lastCoord[2]], endLabel]

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
