import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import glob

num_pixels = 4

gains = [-1,1,-1,1]

def connect_to_usb():
	available_devices = []
	print("Looking for usb device...")
	while(len(available_devices) < 1):
		available_devices = glob.glob("/dev/tty.usbmodem*")
	print("Connecting to {0}".format(available_devices[0]))
	s = serial.Serial(available_devices[0])	
	return s

def init():
    return

def update(frame):
	global pixeldata
	global lines
	global data_bytes
	global s
	global gains

	try:
		num_bytes_available = int(np.floor(s.in_waiting/2.0)*2)
		if(num_bytes_available < 1):
			return
		data_bytes.extend(s.read(num_bytes_available))
	except:
		print("Unable to communicate with device...")
		s = connect_to_usb()
		return

	while(len(data_bytes) > 4):
		b0 = data_bytes.pop(0)
		if(b0 > 4):
			continue
		b1 = data_bytes.pop(0)
		b2 = data_bytes.pop(0)
		b3 = data_bytes.pop(0)
		point = b1 * 256*256 + b2 * 256 + b3 - 2**23;
		if(b0 < num_pixels):
			print("{0}: {1}".format(b0, point))	
			pixeldata[b0].append(point*gains[b0])

	for i in range(num_pixels):
		pixeldata[i] = pixeldata[i][-200:]
		lines[i].set_data(range(len(pixeldata[i])), pixeldata[i])
	ax.set_xlim(0, len(pixeldata[0]))
	ax.set_ylim(np.min(np.min(pixeldata)), np.max(np.max(pixeldata)))

s = connect_to_usb()

fig, ax = plt.subplots(1,1)
data_bytes = []
pixeldata = [list() for i in range(num_pixels)]
lines = []

for i in range(num_pixels):
	ln, = ax.plot([], [])
	lines.append(ln)

ax.legend([i for i in range(num_pixels)], loc="upper left")
ani = FuncAnimation(fig, update, init_func=init)
plt.show(block=True)