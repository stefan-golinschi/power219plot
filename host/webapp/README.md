# webapp

Minimal Flask dashboard for live INA219 samples (NDJSON over serial).

Shows a rolling current/power chart plus average, peak, min, bus voltage, and power.

## Setup (venv)

```bash
cd host/webapp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Flash the firmware first, then:

```bash
python app.py
python app.py -p /dev/ttyUSB1
python app.py -p /dev/ttyUSB0 -o results.jsonl --http-port 8080
```

Open http://127.0.0.1:5000/

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-p`, `--port` | `/dev/ttyUSB0` | Serial device |
| `-b`, `--baud` | `115200` | Baud rate |
| `-o`, `--output` | _(none)_ | Optional NDJSON log to append |
| `--host` | `127.0.0.1` | HTTP bind address |
| `--http-port` | `5000` | HTTP port |
| `--max-points` | `600` | Rolling window size |

Do not run this and `python-chart` against the same serial port at the same time.
