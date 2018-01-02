#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" calc_alto2.py
+++++++++++++++++
©joaquinstevens
Santiago, Chile.
Octuber 2017.

Notes:
- This script calculates FFT spectra for vibration data exported from SoftdB Alto-6Ch Datalogger.
- The vibration measurement consists of a calibration tone generated by a Rion VE-10 exciter.
- The calculated FFT spectrum is saved to disk in two .TXT files
- SoftdB Alto-6ch datasheet: http://bit.ly/2CsTXPH
- Rion VE-10 datasheet: http://bit.ly/2CrBwM3
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.fftpack

# Read file .txt in work folder.
archivo = 'wave_024_data.txt'
with open(archivo,'r') as archivo:
    data = []                           
    for linea in archivo:               # Read line by file line.
        temp = linea.split()            # Separate elements by line.
        temp = temp[0:]                 # Choose all the separate elements.
        data.append(temp)               # Add items to the list.
    data = np.array(data)               # Convert the list into an arrangement.
    data = data.astype(np.float32)      # Convert "strings" to "float 32" (single).
	# print 'Tamaño:', np.shape(data)
	# print 'Data:', data

# Extracts time array "t".
t = data[:,0]

# Calculate sampling frequency "fs".
fs = math.ceil(1/(t[1])) # proximity to superior integer.

# Sets number of samples "N".
N = [data.shape][0][0]

# Set acquisition time "T".
T = N/float(fs)

# Calculate sampling interval "dt".
dt = T/float(N)

# Calculate frequency resolution "df".
df = 1/T

# Sets vibration components x, y, z.
x = data[:,1]
y = data[:,2]
z = data[:,3]

# Sets display range waveforms.
r = range(int(0.1*fs)) #100ms. 

# Graph waveforms in subplots.
f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
ax1.plot(t[r], x[r], color='r', label=u'Signal X')
ax1.legend(loc="upper right")
ax1.set_xlabel('Time [s]')

ax2.plot(t[r], y[r], color='g', label=u'Signal Y')
ax2.legend(loc="upper right")
ax2.set_xlabel('Time [s]')

ax3.plot(t[r], z[r], color='b', label=u'Signal Z')
ax3.legend(loc="upper right")
ax3.set_xlabel('Time [s]')

# Establishes effective band factor.
Eb = 0.5

# Calculate Fast Fourier Transform (FFT) of Z axis.
yf = scipy.fftpack.fft(z[:N])
Yf = 2.0/N * np.abs(yf[:N//2])
xf = np.linspace(0.0, 1.0/(2.0*dt), N/2)

# Plots FFT spectrum.
f, ax4 = plt.subplots(1, 1, sharey=True)
ax4.plot(xf, Yf, color='b', label=u'FFT='+str(N/2))
ax4.legend(loc="upper right")
ax4.set_xlabel('Frecuencia [Hz]')
ax4.set_ylabel('Amplitud Peak [m/s2]')
ax4.grid(True)
ax4.set_ylim((0,15))

# Prints outputs in console.
print 'Frequency domain calculation' 
print '****************************'
print 'file:', archivo
print 'fmax:', fs/2, 'Hz'
print 'N:', N, 'samples'
print 'FFT:', Eb*N, 'lines'
print 'Eb:', Eb
print 'fs:', fs, 'Hz'
print 'df:', df, 'Hz'
print 'T:', T, 's'
print 'xf:', 'xf_'+str(N/2)+'.txt'
print 'Yf:', 'Yf_'+str(N/2)+'.txt'

# Write frequency array "xf" and FFT data "Yf" on disk.
np.savetxt('xf_'+str(N/2)+'.txt', xf) 
np.savetxt('Yf_'+str(N/2)+'.txt', Yf) 

plt.show()