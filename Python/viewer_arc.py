import numpy as np
from matplotlib import patches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import glob

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
colors = ["green", "red", "blue", "pink", "cyan"]
gains = [-1, -1,-1,-1]
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

# def pixel_reading_to_shift(pixel_readings):

def init():
    return

def update(frame):
	# global pixeldata
	global data_bytes
	global s
	global pixeldata
	global gains
	global arcs
	global curl
	global Lr
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
		if(b0 < num_pixels+1):
			if(b0 > -1):
			# print("{0}: {1}".format(b0, point))	
				pixeldata[b0-0].append(point*gains[b0-0])

	# calculate baselines as the mean of the first 100 points for each pixel
	baselines = [np.mean(pixeldata[i][:100]) for i in range(len(pixeldata))]

	pixel_shifts_adccnt = [pixeldata[i][-1] - baselines[i] for i in range(len(pixeldata))]
	pixel_shifts_ff = 4096 * np.array(pixel_shifts_adccnt)/(2**23)
	pixel_shifts_mm = pixel_shifts_ff*t/dk/width/e0/2

	Ls = Lr + np.pad(pixel_shifts_mm, (1, 0), "constant")
	[dtheta, radius, theta, Cx, Cy, x, y] = calculate_arcs(Lr, Ls, t)
	# print(pixel_shifts_mm, radius, [pixeldata[i][-1] - baselines[i] for i in range(len(pixeldata))])
	print([pixeldata[i][-1] for i in range(len(pixeldata))])
	for i in range(0, len(Cx)):
		update_arc(arcs[i], Cx[i], Cy[i], dtheta[i], theta[i],radius[i])
		
s = connect_to_usb()
data_bytes = []
pixeldata  = [list() for i in range(num_pixels)]
arcs = []
fig, ax = plt.subplots(1,1)

Ls = Lr + np.cumsum(np.ones(len(Lr))*curl)
[dtheta, radius, theta, Cx, Cy, x, y] = calculate_arcs(Lr, Ls, t)
ax.scatter(x,y)
for i in range(0, len(Cx)):
	arc = create_arc(Cx[i], Cy[i], dtheta[i], theta[i],radius[i], colors[i])
	arcs.append(arc)
	ax.add_patch(arc)

ax.set_aspect('equal', 'datalim')

# plt.show()
ani = FuncAnimation(fig, update, init_func=init, interval=1)
plt.ylim([-20, 40])
plt.show(block=True)

s.close()