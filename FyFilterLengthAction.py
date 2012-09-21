from FyAction import FyAction

class FyFilterLengthAction( FyAction ):

  def __init__( self, scalarIndex, lowerThreshold, upperThreshold ):
    super( FyFilterLengthAction, self ).__init__( FyAction.NoScalar )

    self.__scalarIndex = scalarIndex
    self.__lowerThreshold = lowerThreshold
    self.__upperThreshold = upperThreshold
    # buffer for the fiber length
    self.__lengths = {}

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''
    firstPointScalars = scalars[0]

    length = firstPointScalars[self.__scalarIndex]

    # store the length
    self.__lengths[uniqueFiberId] = length

    return FyAction.NoScalar

  def validate( self, uniqueFiberId ):
    '''
    '''
    length = self.__lengths[uniqueFiberId]
    return ( length > self.__lowerThreshold and length < self.__upperThreshold )
