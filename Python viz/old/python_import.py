import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def data_gen():
    t = data_gen.t
    cnt = 0
    while cnt < 1000:
        cnt+=1
        t += 0.05
        yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)

# def setup_plot():
data_gen.t = 0

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(-1.1, 1.1)
ax.set_xlim(0, 5)
ax.grid()
xdata, ydata = [], []

def run(data):
    # update the data
    t,y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,

def animate():
	ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10,
	    repeat=False)
	plt.show()


ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
def get_data_from_serial():
		pitch_roll=ser.readline()
		print pitch_roll
		# pitch=float(pitch_roll[:str(pitch_roll).find(":")])
		# roll=float(pitch_roll[pitch_roll.find(":")+1:])
		# time.sleep(.10)

def main():
    # setup_plot()
    animate()
	# while True:
		# print serial.Serial('/dev/tty.usbmodem1421', 9600).readline()
		# get_data_from_serial()

if __name__ == '__main__':
	main()
