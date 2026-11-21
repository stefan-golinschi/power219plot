# python-chart

Live plotter for INA219 samples streamed from the Arduino as NDJSON over serial.

## Setup (venv)

```bash
cd host/python-chart
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows: `.venv\Scripts\activate`

## Run

Flash the firmware first, then:

```bash
python chart.py
python chart.py -p /dev/ttyUSB1
python chart.py --port /dev/ttyUSB0 --baud 115200 -o results.jsonl
```

Press Ctrl-C to stop. Samples are appended to `results.jsonl` (NDJSON).

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-p`, `--port` | `/dev/ttyUSB0` | Serial device |
| `-b`, `--baud` | `115200` | Baud rate |
| `-o`, `--output` | `results.jsonl` | Log file |

You may need dialout/uucp group membership to open the serial port on Linux.
