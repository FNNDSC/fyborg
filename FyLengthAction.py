from FyAction import FyAction
import numpy

class FyLengthAction( FyAction ):

  def __init__( self ):
    '''
    '''
    super( FyLengthAction, self ).__init__( 'length' )

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''
    length = 0
    _last = None
    for _current in coords:
      if _last != None:
        # we have the previous point
        length += numpy.sqrt( numpy.sum( ( _current - _last ) ** 2 ) )

      _last = _current

    return length
