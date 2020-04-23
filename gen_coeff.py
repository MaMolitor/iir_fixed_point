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

# scaling factor in bits
q = int(config.get('bit_scaling','factor'))

# let's generate a sequence of 2nd order IIR filters
sos = signal.iirfilter(order,wp, btype=type_of_filter, ftype=design_of_filter,output='sos')
#Calculating of the bit width
bit_width = int ( np.abs(np.floor(np.log2 ( sos[0,0] ))))
# scaling factor as facor...
if q > bit_width :
    bit_with = q
    print("The bit width parameter in the config file is greater as the calculate and it will be taken.")
elif q < bit_width :
    print("The calculate bit width is greater than from the config file.  .!!!")
    print("It will take calculate !!!!!!!!!!!!!!!!!!!!")


print ("\n",design_of_filter, type_of_filter, "filter" , "order:", order, " fs:", fs, "fc1:", f1 ,end=" ")
if type_of_filter=='stop' or type_of_filter=='bandstop' or type_of_filter=='bandpass':
    print ("fc2:", f2 , end=" ")
print("Bit-Width:",  bit_width )
# scaling factor as facor...
scaling_factor = 2** bit_width

#print ( np.log2 ( sos[0,0] ))
print("\n","coefficients without scaling : ")
for biquad in sos:
    for coeff in biquad:
        print(coeff,",",sep="",end="")
    print("|")
#scaling the coefficients
sos = np.floor(sos * scaling_factor)

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
    print(bit_width, file=file_coeff)
file_coeff.close()

# plot the frequency response
b,a = signal.sos2tf(sos)
w,h = signal.freqz(b,a)
pl.subplot(311)
pl.title('Fixed point filtering demo')
pl.semilogx(w/np.pi/2*fs, 20 * np.log10(abs(h)))
pl.grid(True, which='both')
pl.xlabel('frequency/Hz')
pl.ylabel('gain/dB')


# plot the impulse respose
pl.subplot(312)
pl.title('IMPULSE')
x = np.zeros(4000)
x[0] = 1
imp_resp = signal.lfilter(b,a, x)
#pl.semilogx(20 * np.log10(abs(imp_resp)))
pl.plot(imp_resp)
#pl.ylim(-100, 20)
pl.grid(True, which='both')


pl.subplot(313)
pl.title('LOG IMPULSE')
#pl.semilogx(20 * np.log10(abs(imp_resp)))
pl.plot(20 * np.log10(abs(imp_resp)))
pl.grid(True, which='both')

pl.show()
