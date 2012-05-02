from FyAction import FyAction
from _common import FNNDSCFileIO as io

class FyMapAction( FyAction ):

  def __init__( self, scalarName, volume ):
    '''
    '''
    super( FyMapAction, self ).__init__( scalarName )

    # load volume
    self.__image = io.readImage( volume )
    self.__imageHeader = self.__image.header
    self.__imageDimensions = self.__image.shape[:3]
    self.__imageSpacing = self.__imageHeader.get_zooms()

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    '''
    '''
    ijkCoords = [x / y for x, y in zip( [x, y, z], self.__imageSpacing )]
    ijkCoords = [max( 1, x ) for x in ijkCoords]
    value = self.__image[int( ijkCoords[0] ), int( ijkCoords[1] ), int( ijkCoords[2] )]

    return value

