from _common import FNNDSCFileIO as io
from _common import FNNDSCConsole as c

import numpy

def copyScalars( trkFile1, trkFile2, outputFile ):
  '''
  Copy scalars from trkFile1 to trkFile2
  '''

  s = io.loadTrk( trkFile1 )
  s2 = io.loadTrk( trkFile2 )
  tracks = s[0]
  tracks2 = s2[0]
  origHeader = s[1]
  origHeader2 = s2[1]
  tracksHeader = numpy.copy( s[1] )
  tracksHeader2 = numpy.copy( s2[1] )

  #if tracksHeader['n_count'] != tracksHeader2['n_count']:
  #  c.error( 'The track counts do not match!' )
  #  sys.exit( 2 )

  # now copy
  tracksHeader2['n_scalars'] = tracksHeader['n_scalars']
  tracksHeader2['scalar_name'] = tracksHeader['scalar_name']

  newTracks2 = []

  for tCounter, t in enumerate( tracks ):

    tCoordinates = t[0]
    tScalars = t[1]

    # copy scalars over
    #tracks2[tCounter][1] = numpy.copy( tScalars )
    newTracks2.append( ( tracks2[tCounter][0], tScalars[:], tracks2[tCounter][2] ) )

  # write trkFile2 with update scalars
  io.saveTrk( outputFile, newTracks2, tracksHeader2, None, True )

  c.info( 'Copied Scalars from ' + trkFile1 + ' to ' + trkFile2 + ' and saved as ' + outputFile )

