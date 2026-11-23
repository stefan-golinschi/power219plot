#!/usr/bin/env python3
"""Minimal Flask dashboard for live INA219 NDJSON samples."""

from __future__ import annotations

import argparse
import json
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any

import serial
from flask import Flask, jsonify, render_template

app = Flask(__name__)


@dataclass
class SampleStore:
    max_points: int = 600
    _samples: deque[dict[str, float]] = field(default_factory=deque)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _start: float = field(default_factory=time.time)
    connected: bool = False
    last_error: str | None = None

    def __post_init__(self) -> None:
        self._samples = deque(maxlen=self.max_points)

    def set_max_points(self, max_points: int) -> None:
        with self._lock:
            self.max_points = max_points
            self._samples = deque(self._samples, maxlen=max_points)

    def clear(self) -> None:
        with self._lock:
            self._samples.clear()
            self._start = time.time()
            self.last_error = None

    def add(self, sample: dict[str, Any]) -> None:
        with self._lock:
            self._samples.append({
                't': time.time() - self._start,
                'bus_V': float(sample['bus_V']),
                'shunt_mV': float(sample['shunt_mV']),
                'load_V': float(sample['load_V']),
                'current_mA': float(sample['current_mA']),
                'power_mW': float(sample['power_mW']),
            })

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            samples = list(self._samples)

        stats: dict[str, Any] = {
            'count': len(samples),
            'avg_current_mA': None,
            'peak_current_mA': None,
            'min_current_mA': None,
            'bus_V': None,
            'min_bus_V': None,
            'power_mW': None,
        }

        if samples:
            currents = [s['current_mA'] for s in samples]
            voltages = [s['bus_V'] for s in samples]
            positive = [c for c in currents if c > 0]
            stats['avg_current_mA'] = sum(currents) / len(currents)
            stats['peak_current_mA'] = max(currents)
            stats['min_current_mA'] = min(positive) if positive else min(currents)
            stats['bus_V'] = samples[-1]['bus_V']
            stats['min_bus_V'] = min(voltages)
            stats['power_mW'] = samples[-1]['power_mW']

        return {
            'connected': self.connected,
            'last_error': self.last_error,
            'samples': samples,
            'stats': stats,
        }


store = SampleStore()


def serial_reader(port: str, baud: int, log_path: str | None) -> None:
    log_file = open(log_path, 'a', encoding='utf-8') if log_path else None
    try:
        while True:
            try:
                ser = serial.Serial(port=port, baudrate=baud, timeout=1)
            except serial.SerialException as exc:
                store.connected = False
                store.last_error = str(exc)
                time.sleep(2)
                continue

            store.connected = True
            store.last_error = None
            try:
                while True:
                    raw = ser.readline()
                    if not raw:
                        continue
                    try:
                        line = raw.decode('utf-8').strip()
                    except UnicodeDecodeError:
                        continue
                    if not line:
                        continue
                    try:
                        payload = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if 'error' in payload:
                        store.last_error = str(payload['error'])
                        continue
                    try:
                        store.add(payload)
                    except (KeyError, TypeError, ValueError):
                        continue
                    if log_file is not None:
                        log_file.write(json.dumps(payload) + '\n')
                        log_file.flush()
            except serial.SerialException as exc:
                store.connected = False
                store.last_error = str(exc)
                time.sleep(1)
            finally:
                if ser.is_open:
                    ser.close()
    finally:
        if log_file is not None:
            log_file.close()


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/api/data')
def api_data():
    return jsonify(store.snapshot())


@app.post('/api/clear')
def api_clear():
    store.clear()
    return jsonify({'ok': True})


def parse_args():
    parser = argparse.ArgumentParser(
        description='Flask dashboard for INA219 NDJSON over serial.')
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
        default=None,
        help='Optional NDJSON log file to append')
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='HTTP bind address (default: %(default)s)')
    parser.add_argument(
        '--http-port',
        type=int,
        default=5000,
        help='HTTP port (default: %(default)s)')
    parser.add_argument(
        '--max-points',
        type=int,
        default=600,
        help='Rolling window size (default: %(default)s)')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    store.set_max_points(args.max_points)

    reader = threading.Thread(
        target=serial_reader,
        args=(args.port, args.baud, args.output),
        daemon=True,
    )
    reader.start()

    print(f'Reading {args.port} @ {args.baud}')
    print(f'Dashboard: http://{args.host}:{args.http_port}/')
    app.run(host=args.host, port=args.http_port, threaded=True, use_reloader=False)


if __name__ == '__main__':
    main()
