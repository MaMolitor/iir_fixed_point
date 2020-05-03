#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 10:20:43 2020

@author: molitor
"""

#!python

from numpy import cos, sin, pi, arange
import numpy as np
import pylab as pl
import configparser

config = configparser.ConfigParser()
config.read('test_config.ini')
#------------------------------------------------
# Create a signal for demonstration.
#------------------------------------------------

sample_rate = int(config.get('frequency', 'rate'))
nsamples = sample_rate * 10
scaling_factor = 2**12
t = arange(nsamples) / sample_rate
#x = cos(2*pi*50*t) + 0.2*sin(2*pi*2.5*t+0.1) + 0.2*sin(2*pi*15.3*t) + 0.1*sin(2*pi*16.7*t + 0.1) + 0.1*sin(2*pi*23.45*t+.8)
#x = cos(2*pi*50*t)  + 0.2*sin(2*pi*60*t+0.1)
#x = cos(2*pi*50*t)  + sin(2*pi*200*t)
x = (cos(2*pi*50*t) + 0.2*(sin(2*pi*1*t)))
# + sin(2*pi*60*t)
print(scaling_factor)
x = (x * scaling_factor);
x = np.floor(x)

file=open("unfiltered.dat","w")
s = 1;
for d in x:
   i = int(d)
   file.write(str(s) + " " + str(i) + "\n")
   s = s + 1
file.close()

pl.title('Fixed point filtering demo');
# unfiltered
pl.subplot(211);
pl.plot(x);
pl.xlabel('samples');
pl.ylabel('unfiltered/raw ADC units');
pl.show()
