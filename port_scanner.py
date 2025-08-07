#!/usr/bin/env python3
"""
Fast TCP Port Scanner
- Concurrencia con ThreadPoolExecutor
- Soporte de rangos y listas de puertos
- Timeout por socket
- Manejo de Ctrl+C para cerrar sockets abiertos
- Intento simple de cabeceras HTTP cuando el puerto responde
"""
from __future__ import annotations

import argparse
import signal
import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, List

open_sockets: List[socket.socket] = []

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fast TCP Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="Objetivo a escanear (IP o hostname)")
    parser.add_argument("-p", "--port", required=True, help="Puertos: 80 | 1-1000 | 22,80,443")
    parser.add_argument("-w", "--workers", type=int, default=50, help="Número de hilos (default: 50)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout por conexión en segundos (default: 1.0)")
    return parser.parse_args()

def handle_sigint(sig, frame):  # type: ignore[override]
    for s in open_sockets:
        try:
            s.close()
        except Exception:
            pass
    sys.exit(1)

signal.signal(signal.SIGINT, handle_sigint)

def create_socket(timeout: float) -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    open_sockets.append(s)
    return s

def try_http_banner(sock: socket.socket) -> List[str]:
    lines: List[str] = []
    try:
        sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        data = sock.recv(1024)
        decoded = data.decode(errors="ignore").split("\n")
        for line in decoded[:5]:
            line = line.strip()
            if line:
                lines.append(line)
    except Exception:
        pass
    return lines

def scan_port(port: int, host: str, timeout: float) -> None:
    s = create_socket(timeout)
    try:
        s.connect((host, port))
        print(f"[OPEN] {port}/tcp")
        banner = try_http_banner(s)
        for line in banner:
            print(f"  {line}")
    except (socket.timeout, ConnectionRefusedError, OSError):
        pass
    finally:
        try:
            s.close()
        except Exception:
            pass

def parse_ports(ports_str: str) -> Iterable[int]:
    if "-" in ports_str:
        start, end = map(int, ports_str.split("-"))
        return range(start, end + 1)
    if "," in ports_str:
        return (int(p.strip()) for p in ports_str.split(",") if p.strip())
    return (int(ports_str),)

def main() -> None:
    args = parse_arguments()
    ports = list(parse_ports(args.port))

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for port in ports:
            executor.submit(scan_port, port, args.target, args.timeout)

if __name__ == "__main__":
    main()
