import numpy as np
import matplotlib.pyplot as plt

# Extact haadf image
f1= open("./Sample/00_View000/View000_0000000.img", "r") 
metadata1 = np.fromfile(f1, dtype='u1', count=46913)  # start just after Bits ... ends after 512*512 octets
rawdata1 = np.fromfile(f1, dtype='u1', count=512*512)
f1.close() 

image = rawdata1.reshape(512,512)

# Extract eds hypermap
f2 = open("./Sample/00_View000/View000_0000017.pts", "r") 
metadata2 = np.fromfile(f2, dtype='u1', count=16384)  # guess hypermap start at hex 4000 before it's just metadata
rawdata2 = np.fromfile(f2, dtype='u2')	# unsigned 16 bit little endian decoding
f2.close() 

h = 512
w = 512
e = 2146

hypermap = np.zeros([h,w,e])
for data in rawdata2:
	if (data>=32768) and (data<36864):
		y = int((data-32768)/8-1)
	elif (data>=36864) and (data<40960):
		x = int((data-36864)/8-1)
	elif (data>=45056) and (data<45056+e): #49152 max but memory prob
		z = int(data-45056)
		hypermap[x,y,z] = hypermap[x,y,z]+1

plt.figure()
plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(np.sum(hypermap,2))

plt.figure()
plt.plot(np.sum(hypermap,(0,1)))
