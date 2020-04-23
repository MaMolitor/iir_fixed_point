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
fs = float(config.get('frequency', 'rate'))

# cutoffs
f1 = float(config.get('frequency', 'cutoff_1'))

f2 = 0;

type_of_filter = config.get('filter', 'type')

wp = np.array([f1/fs*2])
if type_of_filter=='stop' or type_of_filter=='bandstop' or type_of_filter=='bandpass':
        f2 = float(config.get('frequency', 'cutoff_2'))
        wp = np.array([f1/fs*2,f2/fs*2])

design_of_filter = config.get('filter', 'design')

order = int(config.get('filter','order'))

# let's generate a sequence of 2nd order IIR filters
sos = signal.iirfilter(order,wp, btype=type_of_filter, ftype=design_of_filter,output='sos')
#Calculating of the bit width
bit_width = np.abs(np.round(np.log2 ( sos[0,0] )))
# scaling factor as facor...
scaling_factor = 2** np.abs(bit_width)

print ("\n",design_of_filter, type_of_filter, "filter" , "order:", order, " fs:", fs, "fc1:", f1 ,end=" ")
if type_of_filter=='stop' or type_of_filter=='bandstop' or type_of_filter=='bandpass':
    print ("fc2:", f2 , end=" ")
print("Bit-Width:",  bit_width )
# scaling factor as facor...
q = int(bit_width)
#print ( np.log2 ( sos[0,0] ))
print("\n","coefficients without scaling : ")
for biquad in sos:
    for coeff in biquad:
        print(coeff,",",sep="",end="")
    print("|")
#scaling the coefficients
sos = np.round(sos * scaling_factor)

# print coefficients
print("\n","coefficients after scaling on bit with", int(bit_width) ," :")
for biquad in sos:
    for coeff in biquad:
        print(int(coeff),",",sep="",end="")
    print("|")

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
# pl.plot(w/np.pi/2*fs,20*np.log(np.abs(h)))
pl.semilogx(w/np.pi/2*fs, 20 * np.log10(abs(h)))
pl.xlabel('frequency/Hz');
pl.ylabel('gain/dB');
pl.show()
