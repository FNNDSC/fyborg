from FyAction import FyAction
import numpy

class FyLengthAction( FyAction ):

  def __init__( self ):
    '''
    '''
    super( FyLengthAction, self ).__init__( 'length' )
    self._length = 0

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

    self._length += length
    return length

  def validate( self, uniqueFiberId ):
      """
      """
      print 'calculated length'
      print self._length

      return True