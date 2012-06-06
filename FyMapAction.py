from FyAction import FyAction
from _common import FNNDSCFileIO as io

from math import sqrt

def sampleBetween( point1, point2, values ):
    """

    """
    if abs( point2[0] - point1[0] ) > 1 or abs( point2[1] - point1[1] ) > 1 or abs( point2[2] - point1[2] ) > 1:
        middlePoint = [ round(point1[0] + ( point2[0] - point1[0] ) / 2, 6) , round(point1[1] + ( point2[1] - point1[1]) / 2, 6) ,
                    round(point1[2] + ( point2[2] - point1[2] ) / 2, 6) ]

        sampleBetween( point1, middlePoint, values )
        sampleBetween( middlePoint, point2, values )

        values.append( middlePoint )

    # if point2 not already in list, append
    ok2 = True
    ok1 = True
    for toto in values[:]:
        if toto[0] == point2[0] and toto[1] == point2[1] and toto[2] == point2[2]:
            ok2 = False
#    for toto in values[:]:
#        if toto[0] == point1[0] and toto[1] == point1[1] and toto[2] == point1[2]:
#            ok1 = False

    if ok2:
        values.append( point2 )
#    if ok1:
#        values.append( point1 )



class FyMapAction( FyAction ):

  def __init__( self, scalarName, volume ):
    """
    """
    super( FyMapAction, self ).__init__( scalarName )

    # load volume
    self._image = io.readImage( volume )

    self._imageHeader = self._image.header
    self._imageDimensions = self._image.shape[:3]
    self._imageSpacing = self._imageHeader.get_zooms()[:3]

    self._ijkcoordinates = {}

    self._value = []

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    """
    """

    # initiate the list
    self._ijkcoordinates[uniqueFiberId] = []

    for currentCoords in coords:
        # convert to ijk
        ijkCoords = [  a/b for a, b in zip( currentCoords, self._imageSpacing) ]
        self._ijkcoordinates[uniqueFiberId].append( ijkCoords )

    return FyAction.NoScalar

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    """
    """
    current = [ a/b for a, b in zip( [x, y, z], self._imageSpacing )]+
    values = []
    values.append(current)

    value = self._image[ current[0] , current[1] , current[2]]
    self._value.append( round(value, 6) )

    return round(value, 6)

  def validate( self, uniqueFiberId ):
      """
      """


      mean = 0.0;
      lent = 0.0

      for i in range( len( self._value[:] ) - 1 ):
              current = self._ijkcoordinates[uniqueFiberId][i]
              next = self._ijkcoordinates[uniqueFiberId][i+1]
              sub_length = sqrt((next[0]-current[0])*(next[0]-current[0]) + (next[1]-current[1])*(next[1]-current[1]) + (next[2]-current[2])*(next[2]-current[2]))
              mean += ((self._value[i] + self._value[i+1]) / 2 )* sub_length
              lent += sub_length

      mean /= lent

      print 'MEAN VALUE'
      print mean
      print 'length:'
      print lent

      return True
