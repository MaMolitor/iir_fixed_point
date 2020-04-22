#!/usr/bin/env python3
import numpy as np
import scipy.signal as signal
import pylab as pl

# Calculate the coefficients for a pure fixed point
# integer filter

# sampling rate
fs = 1000

# cutoffs
f1 = 45
#f1 = 100
f2 = 55

# scaling factor in bits
q = 14
# scaling factor as facor...
scaling_factor = 2**q

# let's generate a sequence of 2nd order IIR filters
#sos = signal.iirfilter(6, [f1/fs*2], btype='highpass', ftype='bessel',output='sos')
#sos = signal.butter(6,[f1/fs*2],'highpass', output='sos')
sos = signal.iirfilter(6,[f1/fs*2,f2/fs*2], btype='stop', ftype='butter',output='sos')
#sos = signal.butter(6,[f1/fs*2,f2/fs*2],'stop',output='sos')
#sos = signal.butter(6,[f1/fs*2,f2/fs*2],'stop',output='sos')
#sos = signal.butter(6,[f1/fs*2],'low',output='sos')

sos = np.round(sos * scaling_factor)

# print coefficients
print("coefficients : ")
for biquad in sos:
    for coeff in biquad:
        print(int(coeff),",",sep="",end="")
    print(q)

file_coeff=open("coeff.dat","w")
for biquad in sos:
    for coeff in biquad:
        print(int(coeff),",",sep="",end="", file=file_coeff)
    print(q, file=file_coeff)
file_coeff.close()

pl.title('Fixed point filtering demo');

# plot the frequency response
b,a = signal.sos2tf(sos)
w,h = signal.freqz(b,a)
pl.plot(w/np.pi/2*fs,20*np.log(np.abs(h)))
pl.xlabel('frequency/Hz');
pl.ylabel('gain/dB');
pl.show()
