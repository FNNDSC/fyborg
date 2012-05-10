from _common import FNNDSCFileIO as io
from _common import FNNDSCConsole as c

import numpy

def clearScalars( trkFile1, outputFile ):
  '''
  Copy scalars from trkFile1 to trkFile2
  '''

  s = io.loadTrk( trkFile1 )
  tracks = s[0]
  origHeader = s[1]
  tracksHeader = numpy.copy( s[1] )

  newTracks = []

  for tCounter, t in enumerate( tracks ):

    tCoordinates = t[0]
    tScalars = t[1]
    tProperties = t[2]

    # clear scalars
    newTracks.append( ( tCoordinates, None, tProperties ) )

  # write trkFile2 with update scalars
  io.saveTrk( outputFile, newTracks, tracksHeader, None, True )

  c.info( 'Cleared scalars from ' + trkFile1 + ' and saved as ' + outputFile )

