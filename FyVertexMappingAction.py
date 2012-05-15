from FyAction import FyAction
from FyMapAction import FyMapAction
import numpy
from _common import FNNDSCConsole as con
from _common import pysurfer_io as sio

class FyVertexMappingAction( FyMapAction ):

  def __init__( self, scalarName, volume, leftMesh, rightMesh ):
    super( FyVertexMappingAction, self ).__init__( scalarName, volume )

    self._leftMesh = sio.read_geometry( leftMesh )
    self._rightMesh = sio.read_geometry( rightMesh )
    self._leftVerticesRAS = []
    self._rightVerticesRAS = []
    self._startVertices = {}
    self._endVertices = {}

    # transform the coords for the right and left hemisphere
    qForm = self._imageHeader.get_qform()
    qFormM = numpy.matrix( qForm ) # as matrix
    # extend the vertex coordinates with an element
    leftVertices = numpy.column_stack( ( self._leftMesh[0], numpy.ones( len( self._leftMesh[0] ) ) ) )
    rightVertices = numpy.column_stack( ( self._rightMesh[0], numpy.ones( len( self._rightMesh[0] ) ) ) )

    for l in leftVertices:
      self._leftVerticesRAS.extend( numpy.dot( qFormM.I, l ) )
    for r in rightVertices:
      self._rightVerticesRAS.extend( numpy.dot( qFormM.I, r ) )

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    '''
    '''
    # image dimensions
    n1, n2, n3 = self._imageDimensions

    # grab first and last coord
    first = coords[0]
    last = coords[-1]

    vertexIndices = []

    for currentCoords in [first, last]:

      minVertexIndexLeft = None
      minDistanceLeft = float( 'inf' )
      minVertexIndexRight = None
      minDistanceRight = float( 'inf' )

      # check which surface point is the closest
      # .. for the left hemisphere
      for index, l in enumerate( self._leftVerticesRAS ):
        distance = numpy.linalg.norm( coords - l )
        if distance < minDistanceLeft:
          # .. grab its' vertex index
          minVertexIndexLeft = index

      # .. and for the right hemisphere
      for index, l in enumerate( self._rightVerticesRAS ):
        distance = numpy.linalg.norm( coords - l )
        if distance < minDistanceRight:
          # .. grab its' vertex index
          minVertexIndexRight = index

      # and store it (either left or right, whichever is closer)
      if minDistanceRight < minDistanceLeft:
        vertexIndices.append( minVertexIndexRight )
      else:
        vertexIndices.append( minVertexIndexLeft )

    # now we have two vertex indicies, first the one of the start point, then the one of the end point
    self._startVertices[uniqueFiberId] = [[first[0], first[1], first[2]], vertexIndices[0]]
    self._endVertices[uniqueFiberId] = [[last[0], last[1], last[2]], vertexIndices[1]]

    return FyAction.NoScalar

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    '''
    '''
    # read label values if we have matching coordinates
    startVertex = self._startVertices[uniqueFiberId]
    endVertex = self._endVertices[uniqueFiberId]

    if x == startVertex[0][0] and y == startVertex[0][1] and z == startVertex[0][2]:
      # this is the start point, so attach the start vertex
      return int( startVertex[1] )

    elif x == endVertex[0][0] and y == endVertex[0][1] and z == endVertex[0][2]:
      # this is the end point, so attach the end vertex
      return int( endVertex[1] )

    return -1 # else wise, return an empty scalar
