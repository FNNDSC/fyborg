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

    value = self._image[ min( current[0], self._imageDimensions[0] - 1 ), min( current[1], self._imageDimensions[1] - 1 ) , min( current[2], self._imageDimensions[2] - 1 )]

    return value
