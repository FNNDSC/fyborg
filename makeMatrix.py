from _common import FNNDSCFileIO as io
from _common import FNNDSCConsole as c

import sys
import os
import numpy
import scipy.io as sio

def makeMatrix( inputs, outputs, no_cortex ):
  '''
  Make 1/ADC, ADC, FA, FiberNumber, FiberLength, E1, E2, E3 connectivity matrices.
  '''

  s = io.loadTrk( outputs['fibers_final'] )
  tracks = s[0]
  header = s[1]

  scalarNames = header['scalar_name'].tolist()
  matrix = {}

  # check if the segmentation is mapped
  try:
    scalarNames.index( 'segmentation' )
  except:
    c.error( Colors.RED )

  for s in scalarNames:

    if not s:
      continue

    print s

  return



  for i in inputs:

    if i == 'fibers' or i == 'segmentation' or i == 'T1' or i == 'b0':
      # we do not map these
      continue

  #for tCounter, t in enumerate( tracks ):





  try:
    labelIndex = scalarNames.index( 'segmentation' )
    adcIndex = scalarNames.index( 'adc' )
    faIndex = scalarNames.index( 'fa' )
    e1Index = scalarNames.index( 'e1' )
    e2Index = scalarNames.index( 'e2' )
    e3Index = scalarNames.index( 'e3' )
    lengthIndex = scalarNames.index( 'length' )
  except:
    c.error( 'Not all scalars were found: aparc_aseg_endlabel, adc, fa, length, e1, e2, e3' )
    sys.exit( 2 )

  m_fn = numpy.zeros( [68, 68] )
  m_fa = numpy.zeros( [68, 68] )
  m_adc = numpy.zeros( [68, 68] )
  m_adcinv = numpy.zeros( [68, 68] )
  m_len = numpy.zeros( [68, 68] )
  m_e1 = numpy.zeros( [68, 68] )
  m_e2 = numpy.zeros( [68, 68] )
  m_e3 = numpy.zeros( [68, 68] )

  fslabel_vol = [2012, 2019, 2032, 2014, 2020, 2018, 2027, 2028, 2003, 2024, 2017, 2026, 2002, 2023, 2010, 2022, 2031, 2029, 2008, 2025, 2005, 2021, 2011, 2013, 2007, 2016, 2006, 2033, 2009, 2015, 2001, 2030, 2034, 2035, 1012, 1019, 1032, 1014, 1020, 1018, 1027, 1028, 1003, 1024, 1017, 1026, 1002, 1023, 1010, 1022, 1031, 1029, 1008, 1025, 1005, 1021, 1011, 1013, 1007, 1016, 1006, 1033, 1009, 1015, 1001, 1030, 1034, 1035]

  for tCounter, t in enumerate( tracks ):

    tCoordinates = t[0]
    tScalars = t[1]

    fa = numpy.mean( tScalars[:, faIndex] )
    adc = numpy.mean( tScalars[:, adcIndex] )
    e1 = numpy.mean( tScalars[:, e1Index] )
    e2 = numpy.mean( tScalars[:, e2Index] )
    e3 = numpy.mean( tScalars[:, e3Index] )
    len = tScalars[0, lengthIndex]

    firstLabel = tScalars[0, labelIndex]
    lastLabel = tScalars[-1, labelIndex]

    try:
      fIndex = fslabel_vol.index( firstLabel )
      lIndex = fslabel_vol.index( lastLabel )
    except:
      continue

    print 'found', firstLabel, lastLabel

    m_fn[fIndex, lIndex] += 1
    m_fa[fIndex, lIndex] += fa
    m_adc[fIndex, lIndex] += adc
    m_e1[fIndex, lIndex] += e1
    m_e2[fIndex, lIndex] += e2
    m_e3[fIndex, lIndex] += e3
    m_adcinv[fIndex, lIndex] += 1 / adc
    m_len[fIndex, lIndex] += len


  # symmetrize matrices
  m_fn = m_fn + m_fn.T - numpy.diag( m_fn.diagonal() )
  m_fa = m_fa + m_fa.T - numpy.diag( m_fa.diagonal() )
  m_adc = m_adc + m_adc.T - numpy.diag( m_adc.diagonal() )
  m_e1 = m_e1 + m_e1.T - numpy.diag( m_e1.diagonal() )
  m_e2 = m_e2 + m_e2.T - numpy.diag( m_e2.diagonal() )
  m_e3 = m_e3 + m_e3.T - numpy.diag( m_e3.diagonal() )
  m_adcinv = m_adcinv + m_adcinv.T - numpy.diag( m_adcinv.diagonal() )
  m_len = m_len + m_len.T - numpy.diag( m_len.diagonal() )

  # normalize matrices
  m_fa[:] /= m_fn[:]
  m_adc[:] /= m_fn[:]
  m_e1[:] /= m_fn[:]
  m_e2[:] /= m_fn[:]
  m_e3[:] /= m_fn[:]
  m_adcinv[:] /= m_fn[:]
  m_len[:] /= m_fn[:]
  m_fa = numpy.nan_to_num( m_fa )
  m_e1 = numpy.nan_to_num( m_e1 )
  m_e2 = numpy.nan_to_num( m_e2 )
  m_e3 = numpy.nan_to_num( m_e3 )
  m_adc = numpy.nan_to_num( m_adc )
  m_adcinv = numpy.nan_to_num( m_adcinv )
  m_len = numpy.nan_to_num( m_len )

  # save as .mat and .csv
  sio.savemat( outputDirectory + "fibmap_all_cMatrix.mat", {'m_fiberNumber':m_fn, 'm_fa':m_fa, 'm_adc':m_adc, 'm_adcInverse':m_adcinv, 'm_fiberLength':m_len, 'm_e1':m_e1, 'm_e2':m_e2, 'm_e3':m_e3} )

  numpy.savetxt( outputDirectory + "fibmap_fibernumber_cMatrix.csv", m_fn, delimiter="," )
  numpy.savetxt( outputDirectory + "fibmap_fa_cMatrix.csv", m_fa, delimiter="," )
  numpy.savetxt( outputDirectory + "fibmap_e1_cMatrix.csv", m_e1, delimiter="," )
  numpy.savetxt( outputDirectory + "fibmap_e2_cMatrix.csv", m_e2, delimiter="," )
  numpy.savetxt( outputDirectory + "fibmap_e3_cMatrix.csv", m_e3, delimiter="," )
  numpy.savetxt( outputDirectory + "fibmap_adc_cMatrix.csv", m_adc, delimiter="," )
  numpy.savetxt( outputDirectory + "fibmap_adcinv_cMatrix.csv", m_adcinv, delimiter="," )
  numpy.savetxt( outputDirectory + "fibmap_fiberlength_cMatrix.csv", m_len, delimiter="," )

  c.info( 'Connectivity matrices generated and stored.' )

