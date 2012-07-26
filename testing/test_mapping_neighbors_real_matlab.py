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
 
 - test the scalar mapping with neighborhood look-up of Matlab 
   with a real Freesurfer segmentation and real fibers
'''

  #
  # show the intro
  t.start_test( desc )

  #
  # define paths
  #
  # temporary storage (always gets overwritten)
  volFile = 'testdata/seg.nii'
  trkFile = 'testdata/streamline_small.trk'
  mappedTrkFile = '/chb/tmp/test111213-kiho.trk'
  radius = t.random.randint( 0, 10 )

  #
  # run the mapping with radius incorporation
  print
  print t.Colors.PURPLE + 'Map scalars using ' + t.Colors.ORANGE + ' MATLAB' + t.Colors._CLEAR
  print t.Colors.PURPLE + 'Using radius ' + t.Colors.CYAN + str( radius ) + t.Colors.PURPLE + ' for the neighborhood look-up!' + t.Colors._CLEAR
  # this stuff overwrites the trk file so we will copy it to a safe place
  t.shutil.copyfile( trkFile, mappedTrkFile )
  t.os.system( './run_matlab_fiber_labelmapping.sh ' + mappedTrkFile + ' ' + volFile + ' ' + str( radius ) )

  #
  # now validate it!
  print
  print t.Colors.CYAN + 'Testing ' + t.Colors.ORANGE + ' MATLAB' + t.Colors.CYAN + ':' + t.Colors._CLEAR

  # .. now check if the mapping was done correctly
  result = t.validateMapping( volFile, mappedTrkFile, radius )
  if result:
    result = t.Colors.GREEN + 'ALL OK!'
  else:
    result = t.Colors.RED + 'ERRORS!!!!'
  print
  print t.Colors.PURPLE + 'Validation done: ' + result + t.Colors._CLEAR
  print

