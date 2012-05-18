from FyAction import FyAction
from _common import FNNDSCFileIO as io

class FyMapAction( FyAction ):

  def __init__( self, scalarName, volume ):
    '''
    '''
    super( FyMapAction, self ).__init__( scalarName )

    # load volume
    self._image = io.readImage( volume )
    self._imageHeader = self._image.header
    self._imageDimensions = self._image.shape[:3]
    self._imageSpacing = self._imageHeader.get_zooms()

    self._previous = {}

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    '''
    '''

    # check if we already have a list of previous points for this fiber id
    # if not, create one
    # if yes, attach the current point (append)

    # if we have a previous 

    if not uniqueFiberId in self._previous:
      # we don't have a list
      self._previous[uniqueFiberId] = []

    # check if we have already a previous coordinate
    if len( self._previous[uniqueFiberId] ) > 0:
      # now do spline filtering using last element of the coordinate list and the current one
      lastCoord = self._previous[uniqueFiberId][-1]

    # todo spline creation and lookup scalar values in respect to spacing self._imageSpacing
    # and recalculate the value

    # append the current coordinate
    self._previous[uniqueFiberId].append( [x, y, z] )

    # this will be obsolete
    ijkCoords = [x / y for x, y in zip( [x, y, z], self._imageSpacing )]
    ijkCoords = [max( 1, x ) for x in ijkCoords]
    value = self._image[int( ijkCoords[0] ), int( ijkCoords[1] ), int( ijkCoords[2] )]


    # return the interpolated value
    return value

