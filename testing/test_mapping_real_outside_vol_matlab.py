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
 
 - test the scalar mapping of Matlab using real data (ADC volume + cropped streamline.trk) but where
   some of the tracks are outside of the volume
'''

  #
  # show the intro
  t.start_test( desc )

  #
  # define paths
  #
  # temporary storage (always gets overwritten)
  volFile = 'testdata/dti_fa_outside_vol.nii'
  trkFile = 'testdata/trk_outside_vol.trk'
  mappedTrkFile = '/chb/tmp/test-202122-kiho.trk'

  #
  # run the mapping
  print
  print t.Colors.PURPLE + 'Map scalars using ' + t.Colors.ORANGE + ' MATLAB' + t.Colors._CLEAR
  # this stuff overwrites the trk file so we will copy it to a safe place
  t.shutil.copyfile( trkFile, mappedTrkFile )
  t.os.system( './run_matlab_fiber_mapping.sh ' + mappedTrkFile + ' ' + volFile + ' TEST' )

  #
  # now validate it!
  print
  print t.Colors.CYAN + 'Testing ' + t.Colors.ORANGE + ' MATLAB' + t.Colors.CYAN + ':' + t.Colors._CLEAR

  # .. now check if the mapping was done correctly
  result = t.validateMapping( volFile, mappedTrkFile )
  if result:
    result = t.Colors.GREEN + 'ALL OK!'
  else:
    result = t.Colors.RED + 'ERRORS!!!!'
  print
  print t.Colors.PURPLE + 'Validation done: ' + result + t.Colors._CLEAR
  print
