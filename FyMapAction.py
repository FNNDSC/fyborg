from FyAction import FyAction
from _common import FNNDSCFileIO as io

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

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    """
    """

    # initiate the list
    self._ijkcoordinates[uniqueFiberId] = []

    for currentCoords in coords:
        # convert to ijk
        ijkCoords = [  a / b for a, b in zip( currentCoords, self._imageSpacing ) ]
        self._ijkcoordinates[uniqueFiberId].append( ijkCoords )

    return FyAction.NoScalar

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    """
    """
    current = [ a / b for a, b in zip( [x, y, z], self._imageSpacing )]
    values = []
    values.append( current )

    value = self._image[ current[0] , current[1] , current[2]]

    return round( value, 6 )
