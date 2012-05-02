
class FyAction( object ):

  NoScalar = 'thisIsNothing'

  def __init__( self, scalarName ):
    '''
    '''
    self.__scalarName = scalarName

  def scalarName( self ):
    '''
    '''
    return self.__scalarName

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''
    return FyAction.NoScalar

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    '''
    '''
    return FyAction.NoScalar

  def validate( self, uniqueFiberId ):
    '''
    '''
    return True
