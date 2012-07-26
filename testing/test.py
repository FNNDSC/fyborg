#!/usr/bin/env python
import subprocess, time
import _test_functions as tf
from time import time, gmtime, strftime, sleep

# import the xbuild system
import sys
sys.path.append( './xbuild/' )
from _core import *

TESTS = ['test_mapping', 'test_mapping_2_2_2', 'test_mapping_real', 'test_mapping_neighbors', 'test_mapping_neighbors_real', 'test_mapping_real_outside_vol']

# ENTRYPOINT
if __name__ == "__main__":

  print 'Testing now...'
  print
  sleep( 1 )

  results = []

  for t in TESTS:

    for tool in ['_fyborg.py', '_matlab.py']:

      fullname = t + tool
      command = './' + fullname
      log = ''
      status = 'failed'

      start_time = time()

      process = subprocess.Popen( command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
      for line in process.stdout:

        line = line.strip( '\n' )

        if line.find( 'ALL OK' ) != -1:
          # test ran through
          status = 'passed'

        log += line + '\n'
        print line

      end_time = time()
      execution_time = end_time - start_time

      # we need to also strip the bell and backspace chars from matlab errors
      results.append( [fullname, status, tf.Colors.strip( log.replace( '\a', '' ).replace( '\b', '' ) ) , execution_time, None, None] )

  print
  print
  print 'All done!!'
  print
  print tf.Colors.PURPLE + '================================' + tf.Colors._CLEAR
  print tf.Colors.ORANGE + '         R E S U L T S' + tf.Colors._CLEAR
  print tf.Colors.PURPLE + '================================' + tf.Colors._CLEAR
  for r in results:

    if r[1] == 'passed':
      result = tf.Colors.GREEN + 'PASSED'
    else:
      result = tf.Colors.RED + 'FAILED'

    print tf.Colors.CYAN + 'Test: ' + tf.Colors.PURPLE + r[0] + ' ' + result

  print

  # now we create a dashboard submission file
  cdasher = CDash()
  xmlfile = cdasher.run( ['Testing', results] )

  with open( os.path.join( config.TEMP_PATH, config.SOFTWARE_SHORT + '_Test.xml' ), 'w' ) as f:
    f.write( xmlfile )

  print tf.Colors.PURPLE + 'Uploading to CDash..' + tf.Colors._CLEAR

  # check which submission type
  submissiontype = 'Experimental'
  if len( sys.argv ) > 1 and sys.argv[1] == '-n':
    submissiontype = 'Nightly'

  print Colors.CYAN + 'Loading Testing Report..' + Colors._CLEAR
  testReport = os.path.join( config.TEMP_PATH, config.SOFTWARE_SHORT + '_Test.xml' )

  if os.path.isfile( testReport ):
    # found a build report
    print Colors.ORANGE + 'Found Testing Report!' + Colors._CLEAR

    with open( testReport, 'r' ) as f:
      cdasher.submit( f.read(), submissiontype )

    print Colors.ORANGE + '..Successfully uploaded as ' + Colors.CYAN + submissiontype + Colors.ORANGE + '.' + Colors._CLEAR

  else:
    # not found
    print Colors.ORANGE + 'Not Found!' + Colors._CLEAR
    testReport = None

  if testReport:
    os.unlink( testReport )
