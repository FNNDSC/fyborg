from FyAction import FyAction
from FyMapAction import FyMapAction

class FyFilterCortexAction( FyMapAction ):

  def __init__( self, volume ):
    super( FyFilterCortexAction, self ).__init__( FyAction.NoScalar, volume )

    # some label values
    self.__whiteMatter = [2, 41] # left, right
    self.__corpusCallosum = [251, 255] # left, right
    self.__subCortex = [10, 49, 16, 28, 60, 4, 43]
    self.__fiberResults = {}

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''
    passesWhiteMatter = False
    passesCorpusCallosum = False
    subCortexCounter = 0

    for _current in coords:
      labelValue = super( FyFilterCortexAction, self ).scalarPerCoordinate( uniqueFiberId, _current[0], _current[1], _current[2] )

      if labelValue in self.__whiteMatter:
        passesWhiteMatter = True
      # 2) check if the track passes the corpus callosum
      if labelValue in self.__corpusCallosum:
        passesCorpusCallosum = True
      # 3) check if the track passes a subcortical structure
      if labelValue in self.__subCortex:
        subCortexCounter += 1 # increase the counter

    # store these values
    self.__fiberResults[uniqueFiberId] = [passesWhiteMatter, passesCorpusCallosum, subCortexCounter]

    return FyAction.NoScalar

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):

    return FyAction.NoScalar

  def validate( self, uniqueFiberId ):
    '''
    '''
    results = self.__fiberResults[uniqueFiberId]
    passesWhiteMatter = results[0]
    passesCorpusCallosum = results[1]
    subCortexCounter = results[2]

    return ( passesWhiteMatter and subCortexCounter <= 5 )
