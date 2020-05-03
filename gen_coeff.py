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

precision = float(config.get('bit_scaling','precision'))


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
q_cal = np.abs(np.floor(np.log2 ( sos[0,0] )))
    
# scaling factor as facor...
if q > q_cal :
    print("The bit width parameter in the config file is greater as the calculate value and it will be taken.")
elif q < q_cal :
    q = q_cal
    print("The calculate bit width value is greater than from the config file.  !!!")
    print("The calculate bit width value will used. !!!!!!!!!!!!!!!!!!!!")

print("q_cal",q_cal)

bit_width = int ( q ) + precision

title = str(design_of_filter) + " " + str(type_of_filter) + "-filter" + " order:" + str(order) + "  fs:" + str(fs) + " fc1:" + str(f1)
if type_of_filter=='stop' or type_of_filter=='bandstop' or type_of_filter=='bandpass':
    title  = title + " fc2:"+ str(f2)
title = title + " Bit-Width: " + str(bit_width) + " (incl. precision of 2^" + str(precision) + ")"


print( "\n", title)

# scaling factor as facor...
scaling_factor = float(2** bit_width)

print("\n","coefficients without scaling : ")
gain = 1
for biquad in sos:
    gain = gain * sum(biquad[0:3])/sum(biquad[3:6])
    for coeff in biquad:
        print(coeff,",",sep="",end="")
    print("|")
print("Gain: " , gain) 

#scaling the coefficients

sosbin = sos * scaling_factor


# print coefficients
print("\n","coefficients after scaling on bit with", int(bit_width) ," :")
gain = 1
for biquad in sosbin:
    gain = gain * sum(biquad[0:3])/sum(biquad[3:6])
    for coeff in biquad:
        print((coeff),",",sep="",end="")
    print("|")
print("Gain: " , gain) 

sosbinround = np.floor(sos * scaling_factor)

# print coefficients
print("\n","coefficients after scaling and rounding on bit with", int(bit_width) ," :")
gain = 1
for biquad in sosbinround:
    gain = gain * sum(biquad[0:3])/sum(biquad[3:6])
    for coeff in biquad:
        print(int(coeff),",",sep="",end="")
    print("|")
print("Gain: " , gain) 


sosround = sosbinround / float(scaling_factor)

# print coefficients
print("\n","real coefficients after scaling and rounding on bit with", int(bit_width) ," :")
gain = 1
for biquad in sosround:
    gain = gain * sum(biquad[0:3])/sum(biquad[3:6])
    for coeff in biquad:
        print((coeff),",",sep="",end="")
    print("|")
print("Gain: " , gain) 


file_coeff=open("coeff.dat","w")
for biquad in sosbin:
    for coeff in biquad:
        print(int(coeff),",",sep="",end="", file=file_coeff)
    print(bit_width, file=file_coeff)
file_coeff.close()


pl.subplots_adjust(wspace=1,hspace=1)

# plot the frequency response
b,a = signal.sos2tf(sos)
w,h = signal.freqz(b,a, worN=8192)
pl.subplot(311)
#pl.title('Fixed point filtering demo')
pl.title(title)
pl.grid(True, which='both')
pl.xlabel('frequency/Hz')
pl.ylabel('gain/dB')
pl.ylim(-20,3)
pl.axvline(f1, color='green') # cutoff frequency
pl.semilogx(w/np.pi/2*fs, 20 * np.log10(abs(h)))


# plot the impulse respose
pl.subplot(312)
pl.title('Step Response - 1')
#x = np.zeros(400000)
#x[0] = 1
x = np.ones(105000)


################ Hier eigentlich sosround:
#b,a = signal.sos2tf(sosround)
#imp_resp = signal.lfilter(b,a, x)

#imp_resp = signal.sosfilt(sosround, x)
imp_resp = signal.sosfilt(sos, x)

#pl.semilogx(20 * np.log10(abs(imp_resp)))

pl.ylim(-100, 20)
pl.grid(True, which='both')
delta = 2**(-precision)

pl.ylim(-delta,+delta)
#pl.margins(0, delta)
pl.plot(imp_resp-x)



# plot log step response
pl.subplot(313)
pl.ylabel('dB')
pl.xlabel('sample')
pl.title('dB(Step Response -1)')
pl.grid(True, which='both')
pl.plot(20 * np.log10(abs(imp_resp-x)))

pl.show()

print("Ende")