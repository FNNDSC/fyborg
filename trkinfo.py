from _common import FNNDSCConsole as c

def printTrkInfo( header, fileName ):

  dimensions = header['dim']
  spacing = header['voxel_size']
  origin = header['origin']
  numberOfScalars = header['n_scalars']
  scalarNames = header['scalar_name']
  numberOfProperties = header['n_properties']
  propertyNames = header['property_name']
  voxelOrder = header['voxel_order']
  pad1 = header['pad1']
  pad2 = header['pad2']
  imageOrientation = header['image_orientation_patient']
  numberOfTracks = header['n_count']
  version = header['version']

  c.info( 'FILE: ' + fileName )

  c.info( '  TRACKVIS VERSION: ' + str( version ) )
  c.info( '  NUMBER OF TRACKS: ' + str( numberOfTracks ) )

  c.info( '  DIMENSIONS: ' + str( dimensions ) )
  c.info( '  SPACING: ' + str( spacing ) )
  c.info( '  ORIGIN: ' + str( origin ) )

  c.info( '  NUMBER OF SCALARS: ' + str( numberOfScalars ) )
  if numberOfScalars > 0:
    c.info( '    SCALARS: ' + str( scalarNames ) )

  c.info( '  NUMBER OF PROPERTIES: ' + str( numberOfProperties ) )
  if numberOfProperties > 0:
    c.info( '    PROPERTIES: ' + str( propertyNames ) )

  if version == 2:
    # only in trackvis v2
    vox2rasMatrix = header['vox_to_ras']
    c.info( '  VOX2RAS Matrix:' )
    c.info( '    ' + str( vox2rasMatrix[0] ) )
    c.info( '    ' + str( vox2rasMatrix[1] ) )
    c.info( '    ' + str( vox2rasMatrix[2] ) )
    c.info( '    ' + str( vox2rasMatrix[3] ) )

  c.info( '  VOXEL ORDER: ' + str( voxelOrder ) )
