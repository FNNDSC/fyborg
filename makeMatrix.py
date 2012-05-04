from _common import FNNDSCFileIO as io
from _common import FNNDSCConsole as c

import sys
import os
import numpy
import scipy.io as sio

def makeMatrix( trkFile1, outputDirectory ):
  '''
  Make 1/ADC, ADC, FA, FiberNumber, FiberLength connectivity matrices.
  '''

  outputDirectory += os.sep

  s = io.loadTrk( trkFile1 )
  tracks = s[0]
  header = s[1]

  scalarNames = header['scalar_name'].tolist()

  try:
    labelIndex = scalarNames.index( 'aparc_aseg_endlabel' )
    adcIndex = scalarNames.index( 'adc' )
    faIndex = scalarNames.index( 'fa' )
    lengthIndex = scalarNames.index( 'length' )
  except:
    c.error( 'Not all scalars were found: aparc_aseg_endlabel, adc, fa, length' )
    sys.exit( 2 )

  m_fn = numpy.zeros( [68, 68] )
  m_fa = numpy.zeros( [68, 68] )
  m_adc = numpy.zeros( [68, 68] )
  m_adcinv = numpy.zeros( [68, 68] )
  m_len = numpy.zeros( [68, 68] )

  fslabel_vol = [2012, 2019, 2032, 2014, 2020, 2018, 2027, 2028, 2003, 2024, 2017, 2026, 2002, 2023, 2010, 2022, 2031, 2029, 2008, 2025, 2005, 2021, 2011, 2013, 2007, 2016, 2006, 2033, 2009, 2015, 2001, 2030, 2034, 2035, 1012, 1019, 1032, 1014, 1020, 1018, 1027, 1028, 1003, 1024, 1017, 1026, 1002, 1023, 1010, 1022, 1031, 1029, 1008, 1025, 1005, 1021, 1011, 1013, 1007, 1016, 1006, 1033, 1009, 1015, 1001, 1030, 1034, 1035]

  for tCounter, t in enumerate( tracks ):

    tCoordinates = t[0]
    tScalars = t[1]

    fa = numpy.mean( tScalars[:, faIndex] )
    adc = numpy.mean( tScalars[:, adcIndex] )
    len = tScalars[0, lengthIndex]

    firstLabel = tScalars[0, labelIndex]
    lastLabel = tScalars[-1, labelIndex]

    try:
      fIndex = fslabel_vol.index( firstLabel )
      lIndex = fslabel_vol.index( lastLabel )
    except:
      continue

    m_fn[fIndex, lIndex] += 1
    m_fa[fIndex, lIndex] += fa
    m_adc[fIndex, lIndex] += adc
    m_adcinv[fIndex, lIndex] += 1 / adc
    m_len[fIndex, lIndex] += len


  # symmetrize matrices
  m_fn = m_fn + m_fn.T - numpy.diag( m_fn.diagonal() )
  m_fa = m_fa + m_fa.T - numpy.diag( m_fa.diagonal() )
  m_adc = m_adc + m_adc.T - numpy.diag( m_adc.diagonal() )
  m_adcinv = m_adcinv + m_adcinv.T - numpy.diag( m_adcinv.diagonal() )
  m_len = m_len + m_len.T - numpy.diag( m_len.diagonal() )

  # normalize matrices
  m_fa[:] /= m_fn[:]
  m_adc[:] /= m_fn[:]
  m_adcinv[:] /= m_fn[:]
  m_len[:] /= m_len[:]
  m_fa = numpy.nan_to_num( m_fa )
  m_adc = numpy.nan_to_num( m_adc )
  m_adcinv = numpy.nan_to_num( m_adcinv )
  m_len = numpy.nan_to_num( m_len )

  # save as .mat and .csv
  sio.savemat( outputDirectory + "fibmap_all_cMatrix.mat", {'m_fiberNumber':m_fn, 'm_fa':m_fa, 'm_adc':m_adc, 'm_adcInverse':m_adcinv, 'm_fiberLength':m_len} )

  numpy.savetxt( outputDirectory + "fibmap_fibernumber_cMatrix.csv", m_fn, delimiter="," )
  numpy.savetxt( outputDirectory + "fibmap_fa_cMatrix.csv", m_fa, delimiter="," )
  numpy.savetxt( outputDirectory + "fibmap_adc_cMatrix.csv", m_adc, delimiter="," )
  numpy.savetxt( outputDirectory + "fibmap_adcinv_cMatrix.csv", m_adcinv, delimiter="," )
  numpy.savetxt( outputDirectory + "fibmap_fiberlength_cMatrix.csv", m_len, delimiter="," )

  c.info( 'Connectivity matrices generated and stored.' )
