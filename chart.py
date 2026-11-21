#!/usr/bin/env python3
import argparse
import json
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import serial


def parse_args():
    parser = argparse.ArgumentParser(
        description='Plot INA219 samples streamed as NDJSON over serial.')
    parser.add_argument(
        '-p', '--port',
        default='/dev/ttyUSB0',
        help='Serial port (default: %(default)s)')
    parser.add_argument(
        '-b', '--baud',
        type=int,
        default=115200,
        help='Baud rate (default: %(default)s)')
    parser.add_argument(
        '-o', '--output',
        default='results.jsonl',
        help='NDJSON log file (default: %(default)s)')
    return parser.parse_args()


def main():
    args = parse_args()

    ser = serial.Serial(port=args.port, baudrate=args.baud, timeout=10)
    print('Serial port open:\n', ser, '\n')

    start_time = time.time()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []
    rs = []

    current_avg = 0.0
    current_avg_rem = 0.0
    current_avg_count = 0
    first_reading = True
    peak_current = -1.0
    min_current = 99.0
    min_voltage = 99.0

    with open(args.output, 'w'):
        pass

    def animate(_frame):
        nonlocal current_avg, current_avg_rem, current_avg_count
        nonlocal first_reading, peak_current, min_current, min_voltage

        line = ser.readline()
        try:
            line = line.decode('utf-8')
        except UnicodeDecodeError:
            return

        line = line.strip()
        if not line:
            return

        try:
            sample = json.loads(line)
        except json.JSONDecodeError:
            return

        if 'error' in sample:
            print('Device error:', sample['error'])
            return

        try:
            bus_voltage = float(sample['bus_V'])
            shunt_mV = float(sample['shunt_mV'])
            load_V = float(sample['load_V'])
            current_mA = float(sample['current_mA'])
            power_mW = float(sample['power_mW'])
        except (KeyError, TypeError, ValueError):
            return

        with open(args.output, 'a') as f:
            f.write(json.dumps({
                'bus_V': bus_voltage,
                'shunt_mV': shunt_mV,
                'load_V': load_V,
                'current_mA': current_mA,
                'power_mW': power_mW,
            }) + '\n')

        timestamp = time.time() - start_time

        if current_mA > peak_current:
            peak_current = current_mA

        if current_mA > 0:
            if current_mA < min_current:
                min_current = current_mA
        else:
            print('Got a weird current value:', current_mA)

        if bus_voltage < min_voltage:
            min_voltage = bus_voltage

        current_avg_count += 1
        if first_reading:
            current_avg = current_mA
            current_avg_rem = current_mA
            first_reading = False
        else:
            current_avg_rem += current_mA
            current_avg = current_avg_rem / current_avg_count

        xs.append(timestamp)
        ys.append(current_mA)
        rs.append(power_mW)

        ax.clear()
        ax.plot(xs, ys, label='Current Draw (mA)')
        ax.plot(xs, rs, label='Power (mW)')

        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('ina219 on ' + ser.port)
        plt.xlabel(
            'Time (s)'
            + '\nAverage Current: {} mA'.format(round(current_avg, 2))
            + '\nPeak Current: {} mA'.format(round(peak_current, 2))
            + '\nMin Current: {} mA'.format(round(min_current, 2))
            + '\nBus Voltage: {} V'.format(round(bus_voltage, 2))
            + '\nMin Bus Voltage: {} V'.format(round(min_voltage, 2))
        )
        plt.ylabel('Current (mA)')
        plt.grid(linestyle='-', lw=0.25)
        plt.legend()
        plt.axis([0, None, 0, 20])

    animation.FuncAnimation(fig, animate, interval=100)
    try:
        plt.show()
    finally:
        ser.close()


if __name__ == '__main__':
    main()
