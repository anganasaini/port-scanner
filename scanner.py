import socket
import argparse
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 3306: "MySQL", 3389: "RDP", 8080: "HTTP-Alt"
}

def grab_banner(sock):
    try:
        sock.settimeout(0.5)
        banner = sock.recv(1024).decode(errors="ignore").strip()
        return banner if banner else None
    except Exception:
        return None

def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target, port))

    if result != 0:
        sock.close()
        return None

    service = COMMON_PORTS.get(port, "Unknown")
    banner = grab_banner(sock)
    sock.close()

    return {"port": port, "service": service, "banner": banner}

def main():
    parser = argparse.ArgumentParser(description="A multi-threaded TCP port scanner.")
    parser.add_argument("--target", default="127.0.0.1", help="IP address or hostname to scan")
    parser.add_argument("--start", type=int, default=1, help="Start of port range")
    parser.add_argument("--end", type=int, default=1024, help="End of port range")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads to use")
    parser.add_argument("--output", help="Optional filename to save results as JSON")
    args = parser.parse_args()

    print(f"Scanning {args.target} ports {args.start}-{args.end} with {args.threads} threads...")
    print(f"Started at {datetime.now().strftime('%H:%M:%S')}\n")

    open_ports = []
    ports_to_scan = range(args.start, args.end + 1)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(scan_port, args.target, port): port for port in ports_to_scan}
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
                banner_info = f" - {result['banner']}" if result['banner'] else ""
                print(f"Port {result['port']}: OPEN ({result['service']}){banner_info}")

    open_ports.sort(key=lambda x: x["port"])

    print(f"\nScan complete at {datetime.now().strftime('%H:%M:%S')}.")
    if open_ports:
        print(f"Found {len(open_ports)} open port(s).")
    else:
        print("No open ports found in this range.")

    if args.output:
        with open(args.output, "w") as f:
            json.dump({
                "target": args.target,
                "scan_range": [args.start, args.end],
                "timestamp": datetime.now().isoformat(),
                "open_ports": open_ports
            }, f, indent=2)
        print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()