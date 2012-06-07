import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
a = numpy.genfromtxt('fibmap_fiberlength_cMatrix.csv',delimiter=',')

print a.max()

a /= a.max()/100

print a.max()

imgplot = plt.imshow(a,interpolation='nearest')
imgplot.set_cmap('jet')
cbar = plt.colorbar()
plt.savefig('test.png')


