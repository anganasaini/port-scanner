# Simple Port Scanner

A multi-threaded TCP port scanner written in Python, built as a learning project to understand networking and cybersecurity fundamentals.

## What it does

This tool checks a range of ports on a target machine and reports which are "open" (accepting connections). For open ports, it identifies the likely service (e.g. HTTP, SSH) and attempts to grab a banner — a message the service sends back, which can reveal more about what's running. It's a simplified version of tools like `nmap`.

## ⚠️ Legal / ethical note

Only scan machines you own or have explicit permission to scan. Scanning devices without authorization is illegal in many countries.

## How to use it

python scanner.py --target 127.0.0.1 --start 1 --end 1024

**Options:**
- `--target` – IP address or hostname to scan (default: `127.0.0.1`, your own computer)
- `--start` – first port to check (default: `1`)
- `--end` – last port to check (default: `1024`)
- `--threads` – number of threads used to scan in parallel (default: `100`)
- `--output` – optional filename to save results as JSON (e.g. `--output results.json`)

## Example output

Scanning 127.0.0.1 ports 1-1024 with 100 threads...
Started at 14:32:01

Port 80: OPEN (HTTP)

Scan complete at 14:32:03.
Found 1 open port(s).

## How it works

The scanner uses a thread pool to check many ports in parallel via TCP connection attempts (`socket`). If a port responds, it looks up the likely service from a table of common ports, then tries to read a banner the service sends back. Results can optionally be exported to a structured JSON file for later review.

## Future improvements

- UDP port scanning (currently TCP only)
- More accurate service fingerprinting
- Progress bar for large scans
- Command-line colored output

## Built with

- Python 3
- `socket`, `argparse`, `concurrent.futures`, `json` (all built-in Python libraries)
