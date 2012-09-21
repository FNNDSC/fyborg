from FyAction import FyAction
from FyMapAction import FyMapAction

class FyFilterCortexAction( FyAction ):

  def __init__( self, scalarIndex ):
    super( FyFilterCortexAction, self ).__init__( FyAction.NoScalar )

    self.__scalarIndex = scalarIndex

    # some label values
    self.__whiteMatter = [2, 41] # left, right
    self.__corpusCallosum = [251, 255] # left, right
    self.__subCortex = [10, 49, 16, 28, 60, 4, 43]
    self.__leftCortex = range( 1000, 1036 )
    self.__rightCortex = range( 2000, 2036 )
    self.__fiberResults = {}

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''
    passesWhiteMatter = False
    passesCorpusCallosum = False
    subCortexCounter = 0
    sameHemisphere = False

    for _current in scalars:

      # grab the label value
      labelValue = int( _current[self.__scalarIndex] )

      # 1) check if the track passes the white matter
      if labelValue in self.__whiteMatter:
        passesWhiteMatter = True
      # 2) check if the track passes the corpus callosum
      if labelValue in self.__corpusCallosum:
        passesCorpusCallosum = True
      # 3) count how often the track passes a subcortical structure
      if labelValue in self.__subCortex:
        subCortexCounter += 1 # increase the counter

    # now just check the endpoints
    start_label = scalars[0][self.__scalarIndex]
    end_label = scalars[-1][self.__scalarIndex]

    # by using these, check if the track starts and ends in the same hemisphere
    # this only counts for cortex structures
    start_left = start_label in self.__leftCortex
    start_right = start_label in self.__rightCortex
    end_left = end_label in self.__leftCortex
    end_right = end_label in self.__rightCortex

    sameHemisphere = ( start_left and end_left ) or ( start_right and end_right )

    # store these values
    self.__fiberResults[uniqueFiberId] = [passesWhiteMatter, passesCorpusCallosum, subCortexCounter, sameHemisphere]

    return FyAction.NoScalar

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):

    return FyAction.NoScalar

  def validate( self, uniqueFiberId ):
    '''
    '''
    results = self.__fiberResults[uniqueFiberId]
    passesWhiteMatter = results[0] # TRUE/FALSE if white matter passed
    passesCorpusCallosum = results[1] # TRUE/FALSE if corpus callosum passed
    subCortexCounter = results[2] # number of sub cortical structures passed
    sameHemisphere = results[3] # TRUE/FALSE if track starts and ends in the same hemisphere

    #
    # we now apply the following conditions to state that this fiber is valid
    #
    # 1. the track has to pass the white matter
    # 2. the track shall only pass sub-cortical structures 5 times
    # 3. the track shall not pass the corpus callosum and end in the same hemisphere

    if passesCorpusCallosum and sameHemisphere:
      # directly jump out
      return False

    return ( passesWhiteMatter and subCortexCounter <= 5 )


"""
Cortex structures


1000    ctx-lh-unknown                      25  5   25  0
1001    ctx-lh-bankssts                     25  100 40  0
1002    ctx-lh-caudalanteriorcingulate      125 100 160 0
1003    ctx-lh-caudalmiddlefrontal          100 25  0   0
1004    ctx-lh-corpuscallosum               120 70  50  0
1005    ctx-lh-cuneus                       220 20  100 0
1006    ctx-lh-entorhinal                   220 20  10  0
1007    ctx-lh-fusiform                     180 220 140 0
1008    ctx-lh-inferiorparietal             220 60  220 0
1009    ctx-lh-inferiortemporal             180 40  120 0
1010    ctx-lh-isthmuscingulate             140 20  140 0
1011    ctx-lh-lateraloccipital             20  30  140 0
1012    ctx-lh-lateralorbitofrontal         35  75  50  0
1013    ctx-lh-lingual                      225 140 140 0
1014    ctx-lh-medialorbitofrontal          200 35  75  0
1015    ctx-lh-middletemporal               160 100 50  0
1016    ctx-lh-parahippocampal              20  220 60  0
1017    ctx-lh-paracentral                  60  220 60  0
1018    ctx-lh-parsopercularis              220 180 140 0
1019    ctx-lh-parsorbitalis                20  100 50  0
1020    ctx-lh-parstriangularis             220 60  20  0
1021    ctx-lh-pericalcarine                120 100 60  0
1022    ctx-lh-postcentral                  220 20  20  0
1023    ctx-lh-posteriorcingulate           220 180 220 0
1024    ctx-lh-precentral                   60  20  220 0
1025    ctx-lh-precuneus                    160 140 180 0
1026    ctx-lh-rostralanteriorcingulate     80  20  140 0
1027    ctx-lh-rostralmiddlefrontal         75  50  125 0
1028    ctx-lh-superiorfrontal              20  220 160 0
1029    ctx-lh-superiorparietal             20  180 140 0
1030    ctx-lh-superiortemporal             140 220 220 0
1031    ctx-lh-supramarginal                80  160 20  0
1032    ctx-lh-frontalpole                  100 0   100 0
1033    ctx-lh-temporalpole                 70  70  70  0
1034    ctx-lh-transversetemporal           150 150 200 0
1035    ctx-lh-insula                       255 192 32  0

2000    ctx-rh-unknown                      25  5   25  0
2001    ctx-rh-bankssts                     25  100 40  0
2002    ctx-rh-caudalanteriorcingulate      125 100 160 0
2003    ctx-rh-caudalmiddlefrontal          100 25  0   0
2004    ctx-rh-corpuscallosum               120 70  50  0
2005    ctx-rh-cuneus                       220 20  100 0
2006    ctx-rh-entorhinal                   220 20  10  0
2007    ctx-rh-fusiform                     180 220 140 0
2008    ctx-rh-inferiorparietal             220 60  220 0
2009    ctx-rh-inferiortemporal             180 40  120 0
2010    ctx-rh-isthmuscingulate             140 20  140 0
2011    ctx-rh-lateraloccipital             20  30  140 0
2012    ctx-rh-lateralorbitofrontal         35  75  50  0
2013    ctx-rh-lingual                      225 140 140 0
2014    ctx-rh-medialorbitofrontal          200 35  75  0
2015    ctx-rh-middletemporal               160 100 50  0
2016    ctx-rh-parahippocampal              20  220 60  0
2017    ctx-rh-paracentral                  60  220 60  0
2018    ctx-rh-parsopercularis              220 180 140 0
2019    ctx-rh-parsorbitalis                20  100 50  0
2020    ctx-rh-parstriangularis             220 60  20  0
2021    ctx-rh-pericalcarine                120 100 60  0
2022    ctx-rh-postcentral                  220 20  20  0
2023    ctx-rh-posteriorcingulate           220 180 220 0
2024    ctx-rh-precentral                   60  20  220 0
2025    ctx-rh-precuneus                    160 140 180 0
2026    ctx-rh-rostralanteriorcingulate     80  20  140 0
2027    ctx-rh-rostralmiddlefrontal         75  50  125 0
2028    ctx-rh-superiorfrontal              20  220 160 0
2029    ctx-rh-superiorparietal             20  180 140 0
2030    ctx-rh-superiortemporal             140 220 220 0
2031    ctx-rh-supramarginal                80  160 20  0
2032    ctx-rh-frontalpole                  100 0   100 0
2033    ctx-rh-temporalpole                 70  70  70  0
2034    ctx-rh-transversetemporal           150 150 200 0
2035    ctx-rh-insula                       255 192 32  0

"""
