import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

# initialize serial port
ser = serial.Serial()
ser.port = '/dev/ttyUSB1'  # Arduino serial port
ser.baudrate = 115200

ser.timeout = 10  # specify timeout when using readline()
ser.open()
if ser.is_open == True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n")  # print serial parameters

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []  # store trials here (n)
ys = []  # store relative frequency here
rs = []  # for theoretical probability

current_avg = 0
current_avg_rem = 0
current_avg_count = 0

first_reading = True

peak_current = -1
min_current = 99

min_voltage = 99

csv_file = "results.csv"

with open(csv_file, 'a') as f:
    f.truncate(0)

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    # Aquire and parse data from serial port
    line = ser.readline()  # ascii

    line = line.decode('utf-8')


    with open(csv_file, 'a') as f:
        f.write(line)

    line_as_list = line.split(',')

    if (line_as_list[0] == 'timestamp'):
        print("CSV Header detected, pass this.")
        return

    timestamp = float(line_as_list[0])
    current_mA = float(line_as_list[4])
    power_mW = float(line_as_list[5])
    bus_voltage = float(line_as_list[1])

    global first_reading
    global current_avg
    global peak_current
    global min_current
    global min_voltage
    global current_avg_rem
    global current_avg_count

    if current_mA > peak_current:
        peak_current = current_mA

    if current_mA > 0:
        if current_mA < min_current:
            min_current = current_mA
    else:
        print("Got a weird current value: ", current_mA)

    if bus_voltage < min_voltage:
        min_voltage = bus_voltage

    current_avg_count = current_avg_count + 1

    if first_reading:
        current_avg = current_mA
        current_avg_rem = current_mA

        first_reading = False
    else:
        current_avg_rem = current_avg_rem + current_mA
        current_avg = current_avg_rem / current_avg_count

    # Add x and y to lists
    xs.append(timestamp / 1000)
    ys.append(current_mA)
    rs.append(power_mW)

    # Limit x and y lists to 20 items
    # xs = xs[-20:]
    # ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, label="Current Draw (mA)")
    ax.plot(xs, rs, label="Power (mW)")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('ina219 on ' + ser.port)
    plt.xlabel('Time (s)' +
               '\nAverage Current: {} mA'.format(round(current_avg, 2)) +
               '\nPeak Current: {} mA'.format(round(peak_current, 2)) +
               '\nMin Current: {} mA'.format(round(min_current, 2)) +
               '\nBus Voltage: {} V'.format(round(bus_voltage, 2)) +
               '\nMin Bus Voltage: {} V'.format(round(min_voltage, 2))
               )
    plt.ylabel('Current (mA)')
    plt.grid(linestyle='-', lw=0.25)
    plt.legend()

    plt.axis([
        0, None, # x axis boundaries
        0, None # y axis boundaries
    ])  # Use for 100 trial demo


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100)
plt.show()
