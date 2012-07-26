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
TEST THE MAPPING
 
 - test the scalar mapping of Fyborg with an artificial volume and an artificial trk file 
   with a fixed spacing 2, 2, 2 
'''

  #
  # show the intro
  t.start_test( desc )

  #
  # define paths
  #
  # temporary storage (always gets overwritten)
  volFile = '/chb/tmp/test123.nii'
  trkFile = '/chb/tmp/test123.trk'
  mappedTrkFile = '/chb/tmp/test123-fyborg.trk'

  #
  # we don't want a random spacing here
  # 
  t.SAMPLE_VOLUME_SPACING_X = 2
  t.SAMPLE_VOLUME_SPACING_Y = 2
  t.SAMPLE_VOLUME_SPACING_Z = 2

  #
  # create an artifical volume
  t.createSampleVolume( volFile )

  #
  # create an artificial trk file
  t.createSampleTrkFile( trkFile )

  #
  # run the mapping
  print
  print t.Colors.PURPLE + 'Map scalars using ' + t.Colors.ORANGE + ' FYBORG' + t.Colors.CYAN + ', the majesty.. ' + t.Colors.PURPLE + ' BE PREPARED!!' + t.Colors._CLEAR
  t.fyborg.fyborg( trkFile, mappedTrkFile, [t.fyborg.FyMapAction( 'test', volFile )], 'debug', 'singlethread' ) # run in test mode with debug enabled and only one thread

  #
  # now validate it!
  print
  print t.Colors.CYAN + 'Testing ' + t.Colors.ORANGE + ' FYBORG' + t.Colors.CYAN + ':' + t.Colors._CLEAR

  # .. now check if the mapping was done correctly
  result = t.validateMapping( volFile, mappedTrkFile )
  if result:
    result = t.Colors.GREEN + 'ALL OK!'
  else:
    result = t.Colors.RED + 'ERRORS!!!!'
  print
  print t.Colors.PURPLE + 'Validation done: ' + result + t.Colors._CLEAR
  print

