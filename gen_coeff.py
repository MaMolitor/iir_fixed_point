#!/usr/bin/env python3
import numpy as np
import scipy.signal as signal
import pylab as pl
import configparser

config = configparser.ConfigParser()
config.read('test_config.ini')

# Calculate the coefficients for a pure fixed point
# integer filter

# sampling rate
fs = int(config.get('frequency', 'rate'))

# cutoffs
f1 = int(config.get('frequency', 'cutoff_1'))

f2 = 0;

type_of_filter = config.get('filter', 'type')

wp = np.array([f1/fs*2])
if type_of_filter=='stop' or type_of_filter=='bandstop' or type_of_filter=='bandpass':
        f2 = int(config.get('frequency', 'cutoff_2'))
        wp = np.array([f1/fs*2,f2/fs*2])

design_of_filter = config.get('filter', 'design')


# scaling factor in bits
q = int(config.get('bit_scaling','factor'))

# scaling factor as facor...
scaling_factor = 2**q

# let's generate a sequence of 2nd order IIR filters
sos = signal.iirfilter(6,wp, btype=type_of_filter, ftype=design_of_filter,output='sos')

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
