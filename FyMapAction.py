from FyAction import FyAction
from _common import FNNDSCFileIO as io

from math import sqrt
import numpy

def sampleBetween( point1, point2, values ):
    """

    """
    if abs( point2[0] - point1[0] ) > 1 or abs( point2[1] - point1[1] ) > 1 or abs( point2[2] - point1[2] ) > 1:
        middlePoint = [ round(point1[0] + ( point2[0] - point1[0] ) / 2, 6) , round(point1[1] + ( point2[1] - point1[1]) / 2, 6) ,
                    round(point1[2] + ( point2[2] - point1[2] ) / 2, 6) ]

        sampleBetween( point1, middlePoint, values )
        sampleBetween( middlePoint, point2, values )

        values.append( middlePoint )

    # if point2 not already in list, append
    ok2 = True
    ok1 = True
    for toto in values[:]:
        if toto[0] == point2[0] and toto[1] == point2[1] and toto[2] == point2[2]:
            ok2 = False
#    for toto in values[:]:
#        if toto[0] == point1[0] and toto[1] == point1[1] and toto[2] == point1[2]:
#            ok1 = False

    if ok2:
        values.append( point2 )
#    if ok1:
#        values.append( point1 )



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

    self._weigth = []

#    self._previous = {}

  def scalarPerFiber( self, uniqueFiberId, coords, scalars ):
    """
    """

    # initiate the list
    self._ijkcoordinates[uniqueFiberId] = []

    for currentCoords in coords:
        # convert to ijk
        ijkCoords = [  round(a / b, 6) for a, b in zip( currentCoords, self._imageSpacing) ]
        self._ijkcoordinates[uniqueFiberId].append( ijkCoords )


    print self._ijkcoordinates[uniqueFiberId]

    return FyAction.NoScalar

  def scalarPerCoordinate( self, uniqueFiberId, x, y, z ):
    """
    """

    current = [ round(a / b, 6)  for a, b in zip( [x, y, z], self._imageSpacing )]

    i = 0
    # find the index of the coordinate in the list
    for i in range( len( self._ijkcoordinates[uniqueFiberId] ) ):
        if self._ijkcoordinates[uniqueFiberId][i][0] == current[0] and self._ijkcoordinates[uniqueFiberId][i][1] == current[1] and self._ijkcoordinates[uniqueFiberId][i][2] == current[2]:
            break

    # convert to integers
    index = i

    prevIndex = max( index - 1, 0 )
    nextIndex = min( index + 1, len( self._ijkcoordinates[uniqueFiberId] ) - 1 )

    lower = self._ijkcoordinates[uniqueFiberId][prevIndex]
    upper = self._ijkcoordinates[uniqueFiberId][nextIndex]
#    lower = [0, 0, 0];
#    upper = [0, 0, 0];
#
#    if(index>prevIndex):
#        lower[0] = round(self._ijkcoordinates[uniqueFiberId][prevIndex][0]+ (self._ijkcoordinates[uniqueFiberId][index][0] - self._ijkcoordinates[uniqueFiberId][prevIndex][0])/2, 6)
#        lower[1] = round(self._ijkcoordinates[uniqueFiberId][prevIndex][1]+ (self._ijkcoordinates[uniqueFiberId][index][1] - self._ijkcoordinates[uniqueFiberId][prevIndex][1])/2, 6)
#        lower[2] = round(self._ijkcoordinates[uniqueFiberId][prevIndex][2]+ (self._ijkcoordinates[uniqueFiberId][index][2] - self._ijkcoordinates[uniqueFiberId][prevIndex][2])/2, 6)
#    else:
#        lower = self._ijkcoordinates[uniqueFiberId][index]
#
#    if(index<nextIndex):
#        upper[0] = round(self._ijkcoordinates[uniqueFiberId][index][0]+ (self._ijkcoordinates[uniqueFiberId][nextIndex][0] - self._ijkcoordinates[uniqueFiberId][index][0])/2, 6)
#        upper[1] = round(self._ijkcoordinates[uniqueFiberId][index][1]+ (self._ijkcoordinates[uniqueFiberId][nextIndex][1] - self._ijkcoordinates[uniqueFiberId][index][1])/2, 6)
#        upper[2] = round(self._ijkcoordinates[uniqueFiberId][index][2]+ (self._ijkcoordinates[uniqueFiberId][nextIndex][2] - self._ijkcoordinates[uniqueFiberId][index][2])/2, 6)
#    else:
#        upper = self._ijkcoordinates[uniqueFiberId][index]

    values = []

    # list points
    print current
    values.append(current)
    values.append(upper)
#    if( index > prevIndex):
#        sampleBetween( lower, current, values )
#    if( index < nextIndex):
#        sampleBetween( current, upper, values )
#    sampleBetween( lower, current, values )
#    sampleBetween( current, upper, values )
##
##    if len(values) == 0:
##        values.append(current)
#
#    print 'values:'
#    print values
#    print(prevIndex, index, nextIndex)
    # average points
#
#    values.append(current)
    value = 0.0
#    pos = 0
    for element in values[:]:
        self._ijkcoordinates[uniqueFiberId][0]
        value += self._image[int( element[0] ), int( element[1] ), int( element[2] )]
        print self._image[int( element[0] ), int( element[1] ), int( element[2] )]

    value /= len( values )

#    #
#    self._value.append( round(value, 6) )
#    #
##    l1 = numpy.sqrt( numpy.sum( ( current - lower ) ** 2 ) )
##    l2 = numpy.sqrt( numpy.sum( ( upper - current ) ** 2 ) )
#    current = [ round(a * b, 6)  for a, b in zip( current, self._imageSpacing )]
#    lower = [ round(a * b, 6)  for a, b in zip( lower, self._imageSpacing )]
#    upper = [ round(a * b, 6)  for a, b in zip( upper, self._imageSpacing )]
#    l1= sqrt((current[0]-lower[0])*(current[0]-lower[0]) + (current[1]-lower[1])*(current[1]-lower[1]) + (current[2]-lower[2])*(current[2]-lower[2]))
#    l2= sqrt((upper[0]-current[0])*(upper[0]-current[0]) + (upper[1]-current[1])*(upper[1]-current[1]) + (upper[2]-current[2])*(current[2]-current[2]))
#    length = l1 +l2
#    self._weigth.append(length)

    print 'value: '
    print round(value, 6)
    self._value.append( round(value, 6) )
#    print 'length: '
#    print length
    print '==============='

    # return the interpolated value
    return round(value, 6)

  def validate( self, uniqueFiberId ):
      """
      """
#      value = 0.0
#      weighttotal = 0
#      count = 0
#
##      for element in self._value[:]:
##          for elements in element:
##              value += self._image[int( elements[0] ), int( elements[1] ), int( elements[2] )]
##              count = count + 1
##
##      value /= count
#
#      for w in self._weigth[:]:
#          weighttotal += w
#
#      for element in self._value[:]:
#          value += element
##          value += element*self._weigth[count]/weighttotal
##          count += 1
#
#      value /= len(self._value)

      mean = 0.0;
      lent = 0.0

      for i in range( len( self._value[:] ) - 1 ):
          current = self._ijkcoordinates[uniqueFiberId][i]
          next = self._ijkcoordinates[uniqueFiberId][i+1]
          sub_length = sqrt((next[0]-current[0])*(next[0]-current[0]) + (next[1]-current[1])*(next[1]-current[1]) + (next[2]-current[2])*(next[2]-current[2]))
          mean += ((self._value[i] + self._value[i+1]) / 2 )* sub_length
          lent += sub_length

      mean /= lent


      print 'MEAN VALUE'
      print mean
      print 'length:'
      print lent

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
