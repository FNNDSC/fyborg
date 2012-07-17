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

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    """
    """
    current = [ int( a / b ) for a, b in zip( [x, y, z], self._imageSpacing )]

    value = self._image[ current[0] , current[1] , current[2]]

    return value
