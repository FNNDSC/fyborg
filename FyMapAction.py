from FyAction import FyAction
from _common import FNNDSCFileIO as io

def sampleBetween( point1, point2, values ):
    """

    """

    print 'sampleBetween'
    print point1
    print point2

    middlePoint = [int( point1[0] + ( point2[0] - point1[0] ) / 2 ), int( point1[1] + ( point2[1] - point1[1] ) / 2 ),
                   int( point1[2] + ( point2[2] - point1[2] ) / 2 )]

    threshold = 1
    if abs( middlePoint[0] - point1[0] ) > threshold or abs( middlePoint[1] - point1[1] ) > threshold or abs( middlePoint[2] - point1[2] ) > threshold:
        sampleBetween( point1, middlePoint, values )

    if abs( middlePoint[0] - point2[0] ) > threshold or abs( middlePoint[1] - point2[1] ) > threshold or abs( middlePoint[2] - point2[2] ) > threshold:
        sampleBetween( middlePoint, point2, values )

    values.append( middlePoint )

class FyMapAction( FyAction ):

  def __init__( self, scalarName, volume ):
    """
    """
    super( FyMapAction, self ).__init__( scalarName )

    # load volume
    self._image = io.readImage( volume )
    self._imageHeader = self._image.header
    self._imageDimensions = self._image.shape[:3]
    self._imageSpacing = self._imageHeader.get_zooms()

    self._ijkcoordinates = {}

    self._value = []

#    self._previous = {}

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    """
    """

    # initiate the list
    self._ijkcoordinates[uniqueFiberId] = []

    for currentCoords in coords:
        # convert to ijk
        ijkCoords = [ int( a / b ) for a, b in zip( currentCoords, self._imageSpacing ) ]
        self._ijkcoordinates[uniqueFiberId].append( ijkCoords )


    print self._ijkcoordinates[uniqueFiberId]

    return FyAction.NoScalar

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    """
    """

    current = [int( a / b ) for a, b in zip( [x, y, z], self._imageSpacing )]

    i = 0
    # find the index of the coordinate in the list
    for i in range( len( self._ijkcoordinates[uniqueFiberId] ) ):
        if self._ijkcoordinates[uniqueFiberId][i][0] == current[0] and self._ijkcoordinates[uniqueFiberId][i][1] == current[1] and self._ijkcoordinates[uniqueFiberId][i][2] == current[2]:
            break
    index = i

    prevIndex = max( index - 1, 0 )
    nextIndex = min( index + 1, len( self._ijkcoordinates ) - 1 )

    lower = self._ijkcoordinates[uniqueFiberId][prevIndex]
    upper = self._ijkcoordinates[uniqueFiberId][nextIndex]

    values = []
    # list points
    sampleBetween( lower, current, values )
    sampleBetween( current, upper, values )

    print 'values:'
    print values

    # average points
    value = 0
    for element in values[:]:
        value += self._image[int( element[0] ), int( element[1] ), int( element[2] )]

    value /= len( values )

    print 'value: '
    print value
    print '==============='
    # return the interpolated value
    self._value.append( value )

    return value

  def validate( self, uniqueFiberId ):
      """
      """
      value = 0

      for element in self._value[:]:
        value += element

      value /= len( self._value )


      print 'MEAN VALUE'
      print value

      return True
#
#  void GetVoxels( short* n1, short* n2, vector<short>& indices_out )
#
#      {
#
#      size_t k;
#
#      size_t n_out = indices_out.size()/3;
#
#      for (k = 0; k < n_out; k++)
#
#          {
#
#          if (n1[0] == indices_out[k*3] && n1[1] == indices_out[k*3+1] && n1[2] == indices_out[k*3+2])
#
#              {
#
#              break;
#
#              }
#
#          }
#
#      if ( k >= n_out )
#
#          {
#
#          for ( int i = 0; i < 3; i++ )
#
#              indices_out.push_back( n1[i] );
#
#          }
#
#
#
#      if ( abs( n1[0]-n2[0]) > 1 || abs( n1[1]-n2[1]) > 1 || abs( n1[2]-n2[2]) > 1 )
#
#          {
#
#          short m[3];
#
#          for ( int i = 0; i < 3; i++ )
#
#              m[i] = (n1[i] + n2[i] ) /2;
#
#
#
#          GetVoxels( n1, m, indices_out );
#
#          GetVoxels( m, n2, indices_out );
#
#          }
#
#      else
#
#          {
#
#          if ( n1[0] != n2[0] || n1[1] != n2[1] || n1[2] != n2[2] )
#
#              {
#
#              for ( int i = 0; i < 3; i++ )
#
#                  indices_out.push_back( n2[i] );
#
#              }
#
#          }
#
#      }
