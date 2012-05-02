from FyLengthAction import FyLengthAction

class FyFilterLengthAction( FyLengthAction ):

  def __init__( self, lowerThreshold, upperThreshold ):
    super( FyFilterLengthAction, self ).__init__()

    self.__lowerThreshold = lowerThreshold
    self.__upperThreshold = upperThreshold
    # buffer for the fiber length
    self.__lengths = {}

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''
    length = super( FyFilterLengthAction, self ).scalarPerFiber( uniqueFiberId, coords, scalars )

    # store the length
    self.__lengths[uniqueFiberId] = length

    return length

  def validate( self, uniqueFiberId ):
    '''
    '''
    length = self.__lengths[uniqueFiberId]
    return ( length > self.__lowerThreshold and length < self.__upperThreshold )
