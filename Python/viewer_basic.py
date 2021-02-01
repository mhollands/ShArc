import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scipy.signal
import scipy.stats
import time
import glob

buffer_len = 2000
sampling_rate = 48000000/65336
adc_per_dac = 22;

def connect_to_usb():
	available_devices = []
	print("Looking for usb device...")
	while(len(available_devices) < 1):
		available_devices = glob.glob("/dev/tty.usbmodem*")
	print("Connecting to {0}".format(available_devices[0]))
	s = serial.Serial(available_devices[0])
	return s

s = connect_to_usb()	

data_bytes = []
while(1==1):
	try:
		num_bytes_available = int(np.floor(s.in_waiting/2.0)*2)
		data_bytes.extend(s.read(num_bytes_available))
	except:
		print("Unable to communicate with device...")
		s = connect_to_usb()
		continue
	while(len(data_bytes) > 4):
		b0 = data_bytes.pop(0)
		if(b0 > 4):
			continue
		b1 = data_bytes.pop(0)
		b2 = data_bytes.pop(0)
		b3 = data_bytes.pop(0)
		point = b1 * 256*256 + b2 * 256 + b3 - 2**23;
		if(b0 == 1):
			print("{0}: {1} {2} {3} {4}".format(b0, point, b1, b2, b3))