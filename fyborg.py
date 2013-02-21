import sys
import os
import time
import tempfile
import multiprocessing
from multiprocessing import Process
import numpy

from FyAction import FyAction
import _common
from _common import FNNDSCConsole as c
from _common import FNNDSCFileIO as io
from _common import FNNDSCUtil as u
from trkinfo import *

# 
#   ___         __                        
# .'  _|.--.--.|  |--..-----..----..-----.
# |   _||  |  ||  _  ||  _  ||   _||  _  |
# |__|  |___  ||_____||_____||__|  |___  |
#       |_____|                    |_____|
#
# THE ULTIMATE SCALAR MAPPING FRAMEWORK FOR TRACKVIS (.TRK) FILES
#
#
#
# (c) 2012 FNNDSC, Children's Hospital Boston 
#
#


def fyborg( trkFile, outputTrkFile, actions, *args ):

  if not actions:
    c.error( "We gotta do something.." )
    return

  showDebug = 'debug' in args

  singleThread = 'singlethread' in args

  c.debug( "trkFile:" + str( trkFile ), showDebug )
  c.debug( "outputTrkFile:" + str( outputTrkFile ), showDebug )
  c.debug( "args:" + str( args ), showDebug )



  # load trk file
  s = io.loadTrk( trkFile )
  tracks = s[0]
  origHeader = s[1]
  tracksHeader = numpy.copy( s[1] )
  numberOfScalars = origHeader['n_scalars']
  scalars = origHeader['scalar_name'].tolist()
  numberOfTracks = origHeader['n_count']

  # show some file informations
  printTrkInfo( tracksHeader, trkFile )

  # grab the scalarNames
  scalarNames = []
  for a in actions:
    if a.scalarName() != FyAction.NoScalar:
      scalarNames.append( a.scalarName() )

  # increase the number of scalars
  tracksHeader['n_scalars'] += len( scalarNames )

  # .. attach the new scalar names
  for i in range( len( scalarNames ) ):
    tracksHeader['scalar_name'][numberOfScalars + i] = scalarNames[i]

  #
  # THREADED COMPONENT
  #
  if singleThread:
    numberOfThreads = 1
  else:
    numberOfThreads = multiprocessing.cpu_count()
  c.info( 'Splitting master into ' + str( numberOfThreads ) + ' pieces..' )
  splittedOutputTracks = u.split_list( tracks[:], numberOfThreads )

  # list of threads
  t = [None] * numberOfThreads

  # list of alive flags
  a = [None] * numberOfThreads

  # list of tempFiles
  f = [None] * numberOfThreads

  for n in xrange( numberOfThreads ):
    # configure actions
    __actions = []
    for act in actions:
      __actions.append( act )

    # mark thread as alive
    a[n] = True
    # fire the thread and give it a filename based on the number
    tmpFile = tempfile.mkstemp( '.trk', 'fyborg' )[1]
    f[n] = tmpFile
    t[n] = Process( target=fyborgLooper_, args=( splittedOutputTracks[n][:], tracksHeader, tmpFile, __actions, showDebug, n + 1 ) )
    c.info( "Starting Thread-" + str( n + 1 ) + "..." )
    t[n].start()

  allDone = False

  while not allDone:

    time.sleep( 1 )

    for n in xrange( numberOfThreads ):

      a[n] = t[n].is_alive()

    if not any( a ):
      # if no thread is alive
      allDone = True

  #
  # END OF THREADED COMPONENT
  #
  c.info( "All Threads done!" )

  #
  # Merging stage
  #
  c.info( "Merging tracks.." )

  outputTracks = []
  # now read all the created tempFiles and merge'em to one
  for tmpFileNo in xrange( 0, len( f ) ):
    tTracks = io.loadTrk( f[tmpFileNo] )

    # add them
    outputTracks.extend( tTracks[0] )

  c.info( "Merging done!" )

  io.saveTrk( outputTrkFile, outputTracks, tracksHeader, None, True )

  c.info( "All done!" )







def fyborgLooper_( tracks, tracksHeader, outputTrkFile, actions, showDebug, threadNumber ):

  import numpy

  numberOfTracks = len( tracks )

  # the buffer for the new tracks
  newTracks = []

  # now loop through the tracks
  for tCounter, t in enumerate( tracks ):

    # some debug stats
    c.debug( 'Thread-' + str( threadNumber ) + ': Processing ' + str( tCounter + 1 ) + '/' + str( numberOfTracks ), showDebug )

    # generate a unique ID for this track
    uniqueId = str( threadNumber ) + str( tCounter )

    tCoordinates = t[0]
    tScalars = t[1]

    # buffer for fiberScalars
    _fiberScalars = {}

    # first round: mapping per fiber
    # .. execute each action and buffer return value (scalar)
    for a in actions:
      value = a.scalarPerFiber( uniqueId, tCoordinates, tScalars )
      _fiberScalars[a.scalarName()] = value

    #
    # Coordinate Loop
    #
    # buffer for coordinate scalars)    
    scalars = []

    # second round: mapping per coordinate
    for cCounter, coords in enumerate( tCoordinates ):

      _coordScalars = {}
      _mergedScalars = [] # this is the actual buffer for ordered fiber and coord scalars merged together

      # .. execute each action and buffer return value (scalar)
      for a in actions:
        value = a.scalarPerCoordinate( uniqueId, coords[0], coords[1], coords[2] ) # pass x,y,z
        _coordScalars[a.scalarName()] = value

      # now merge the old scalars and the fiber and coord scalars
      # this preserves the ordering of the configured actions
      if tScalars != None:
        _mergedScalars.extend( tScalars[cCounter] )

      for a in actions:
        value = _fiberScalars[a.scalarName()]
        if value != FyAction.NoScalar:
          _mergedScalars.append( value )
        else:
          # no fiber scalar, check if there is a coord scalar
          value = _coordScalars[a.scalarName()]
          if value != FyAction.NoScalar:
            _mergedScalars.append( value )

      # attach scalars
      scalars.append( _mergedScalars )

    # validate the fibers using the action's validate methods
    validator = []
    for a in actions:
      validator.append( a.validate( uniqueId ) )

    if all( validator ):
      # this is a valid fiber
      # .. add the new track with the coordinates, the new scalar array and the properties
      newScalars = numpy.asarray( scalars )
      newTracks.append( ( t[0], newScalars, t[2] ) )

  # save everything
  io.saveTrk( outputTrkFile, newTracks, tracksHeader, None, True )




