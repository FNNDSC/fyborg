#!/usr/bin/env python
import _test_functions as t

# 
#   ___         __                        
# .'  _|.--.--.|  |--..-----..----..-----.
# |   _||  |  ||  _  ||  _  ||   _||  _  |
# |__|  |___  ||_____||_____||__|  |___  |
#       |_____|                    |_____|
#
# THE ULTIMATE SCALAR MAPPING FRAMEWORK FOR TRACKVIS (.TRK) FILES
#
#         -= T E S T I N G =-
#


# ENTRYPOINT
if __name__ == "__main__":

  # .. the test case description
  desc = '''
TEST THE NEIGHBORHOOD MAPPING
 
 - test the scalar mapping with neighborhood look-up of Fyborg 
   with an artificial volume and an artificial trk file 
'''

  #
  # show the intro
  t.start_test( desc )

  #
  # define paths
  #
  # temporary storage (always gets overwritten)
  volFile = '/chb/tmp/test789.nii'
  trkFile = '/chb/tmp/test789.trk'
  mappedTrkFile = '/chb/tmp/test789-fyborg.trk'
  radius = t.random.randint( 0, 10 )

  #
  # create an artifical volume with duplicate values to test the label look-up
  t.createSampleVolumeWithSelectedLabels( volFile, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] )

  #
  # modify the volume and add some duplicate values for the label look-up

  #
  # create an artificial trk file
  t.createSampleTrkFile( trkFile )

  #
  # run the mapping with radius incorporation
  print
  print t.Colors.PURPLE + 'Map scalars using ' + t.Colors.ORANGE + ' FYBORG' + t.Colors.CYAN + ', the majesty.. ' + t.Colors.PURPLE + ' BE PREPARED!!' + t.Colors._CLEAR
  print t.Colors.PURPLE + 'Using radius ' + t.Colors.CYAN + str( radius ) + t.Colors.PURPLE + ' for the neighborhood look-up!' + t.Colors._CLEAR
  t.fyborg.fyborg( trkFile, mappedTrkFile, [t.fyborg.FyRadiusMapAction( 'test', volFile, radius )], 'debug', 'singlethread' ) # run in test mode with debug enabled and only one thread

  #
  # now validate it!
  print
  print t.Colors.CYAN + 'Testing ' + t.Colors.ORANGE + ' FYBORG' + t.Colors.CYAN + ':' + t.Colors._CLEAR

  # .. now check if the mapping was done correctly
  result = t.validateMapping( volFile, mappedTrkFile, radius )
  if result:
    result = t.Colors.GREEN + 'ALL OK!'
  else:
    result = t.Colors.RED + 'ERRORS!!!!'
  print
  print t.Colors.PURPLE + 'Validation done: ' + result + t.Colors._CLEAR
  print

