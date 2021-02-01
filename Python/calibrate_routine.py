import numpy as np
from matplotlib import patches
import matplotlib.pyplot as plt
import serial
import glob
import matplotlib as mpl

mpl.style.use("seaborn-pastel")

Lr = np.array([0, 6.25, 18.75, 31.25, 43.75])
# Lr = np.array([0, 18.75, 31.25, 43.75])
# Lr = np.array([0, 31.25, 43.75])
# Lr = np.array([0, 43.75])
num_pixels = len(Lr)-1
dk = 3.2
e0 = 8.8541878128 #fF/mm
t = 0.1016 * 5
width = 7
curl = 1e-12;
# gains = [-1, 1,-1,-1]

def connect_to_usb():
	available_devices = []
	print("Looking for usb device...")
	while(len(available_devices) < 1):
		available_devices = glob.glob("/dev/tty.usbmodem*")
	print("Connecting to {0}".format(available_devices[0]))
	s = serial.Serial(available_devices[0])	
	return s

def calculate_dtheta_and_radius(Lr, Ls, t):
	dLr = np.diff(Lr) # Eq 1
	dLs = np.diff(Ls) # Eq 2
	r = t * dLr / (dLr - dLs) # Eq 6
	dtheta = (dLr - dLs)/t # Eq 7
	return dtheta, r

def create_arc(Cx, Cy, dtheta, theta, radius, colour):
	# Calculate starting and ending angle
	if(radius >= 0):
		starting_angle = (theta - np.pi/2)
		ending_angle = starting_angle+dtheta

	if(radius < 0):
		ending_angle = (theta + np.pi/2)
		starting_angle = ending_angle+dtheta
		radius *= -1

	return patches.Arc((Cx,Cy), radius*2, radius*2, angle=0.0, theta1=starting_angle*180/np.pi, theta2=(ending_angle)*180/np.pi, color=colour, linewidth=5)

def update_arc(arc, Cx, Cy, dtheta, theta, radius):
	# Calculate starting and ending angle
	if(radius >= 0):
		starting_angle = (theta - np.pi/2)
		ending_angle = starting_angle+dtheta

	if(radius < 0):
		ending_angle = (theta + np.pi/2)
		starting_angle = ending_angle+dtheta
		radius *= -1
	arc.width = radius*2
	arc.height = radius*2
	arc.center = (Cx, Cy)
	arc.angle = 0
	arc.theta1 = starting_angle*180/np.pi
	arc.theta2 = (ending_angle)*180/np.pi

def calculate_arcs(Lr, Ls, t):
	dtheta, radius = calculate_dtheta_and_radius(Lr, Ls, t)
	theta = np.cumsum(np.pad(dtheta, (1, 0), "constant")) # Integrate dtheta to get theta (Theta[0] = 0)

	# Equations 8 and 9
	x = np.zeros(len(Lr))
	y = np.zeros(len(Lr))
	for i in range(0, len(x) - 1):
		x[i+1] = x[i] + radius[i] * (np.sin(theta[i+1]) - np.sin(theta[i]))
		y[i+1] = y[i] + radius[i] * (np.cos(theta[i]) - np.cos(theta[i+1]))

	Cx = x[:-1] - radius * np.sin(theta[:-1]) # Eq 12
	Cy = y[:-1] + radius * np.cos(theta[:-1]) # Eq 13
	return [dtheta, radius, theta, Cx, Cy, x, y]

def collect_frames(nframes):
	global data_bytes
	global s
	frames  = [list() for i in range(num_pixels)]

	num_bytes_available = s.in_waiting
	while(num_bytes_available > 0):
		print(num_bytes_available)
		s.read(num_bytes_available)
		num_bytes_available = s.in_waiting

	s.reset_input_buffer()

	while(sum([len(x) < nframes for x in frames]) > 0):
		print(len(frames[0]))
		try:
			num_bytes_available = int(np.floor(s.in_waiting/2.0)*2)
			if(num_bytes_available < 1):
				continue
			data_bytes.extend(s.read(num_bytes_available))
		except:
			print("Unable to communicate with device...")
			s = connect_to_usb()

		while(len(data_bytes) > 4):
			b0 = data_bytes.pop(0)
			if(b0 > 4):
				continue
			b1 = data_bytes.pop(0)
			b2 = data_bytes.pop(0)
			b3 = data_bytes.pop(0)
			point = b1 * 256*256 + b2 * 256 + b3 - 2**23;
			if(b0 < num_pixels+1):
				frames[b0].append(point)
	return frames	
		
s = connect_to_usb()
data_bytes = []

dLr = np.diff(Lr)
calibration_radii = [np.inf, 80+3, 40+3]
expected_shift_mm = t * (np.tile(dLr,(3,1)).transpose()/calibration_radii).transpose()
adc_counts = []

for calibration_radius in calibration_radii:
	input("Apply curvature of {0}mm".format(calibration_radius))
	frames = collect_frames(10)
	adc_counts.append([np.mean(frames[i]) for i in range(len(frames))])
s.close()

adc_counts = np.array(adc_counts).transpose()
expected_shift_mm = expected_shift_mm.transpose()
for i in range(num_pixels):
	a,b = np.polyfit(adc_counts[i], expected_shift_mm[i],1)
	plt.scatter(adc_counts[i], expected_shift_mm[i])
	plt.plot([adc_counts[i].min(), adc_counts[i].max()], [adc_counts[i].min()*a+b, adc_counts[i].max()*a+b])

plt.xlabel("ADC Counts")
plt.ylabel("Expected shift /mm")
plt.show()