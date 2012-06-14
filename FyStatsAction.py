from FyAction import FyAction
import numpy

class FyStatsAction( FyAction ):

  def __init__( self, outputFile ):
    '''
    '''
    super( FyStatsAction, self ).__init__( FyAction.NoScalar )

    self.__outputFile = outputFile

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''

    buffer = [len( scalars )]

    for _current in scalars:



    return FyAction.NoScalar

