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

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    '''
    '''
    ijkCoords = [x / y for x, y in zip( [x, y, z], self._imageSpacing )]
    ijkCoords = [max( 1, x ) for x in ijkCoords]
    value = self._image[int( ijkCoords[0] ), int( ijkCoords[1] ), int( ijkCoords[2] )]

    return value

