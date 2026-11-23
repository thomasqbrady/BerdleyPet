#!/usr/bin/env python3
"""
Time server for Arduino Leonardo.
Listens for "TIME?" requests and responds with the current hour (0-23).

Usage:
    python time_server.py [port]

    port: Serial port (default: auto-detect Leonardo)

Examples:
    python time_server.py
    python time_server.py /dev/cu.usbmodem2101
    python time_server.py COM3
"""

import sys
import time
from datetime import datetime

import serial
import serial.tools.list_ports


def find_leonardo_port():
    """Auto-detect Arduino Leonardo port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Leonardo typically shows up with these identifiers
        if "usbmodem" in port.device.lower() or "arduino" in port.description.lower():
            return port.device
    return None


def main():
    # Determine port
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = find_leonardo_port()
        if not port:
            print("Could not auto-detect Arduino Leonardo.")
            print(
                "Please specify port as argument: python time_server.py /dev/cu.usbmodem2101"
            )
            sys.exit(1)

    print(f"Connecting to {port}...")

    try:
        ser = serial.Serial(port, 9600, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening port: {e}")
        sys.exit(1)

    print(f"Connected. Listening for TIME? requests...")
    print("Press Ctrl+C to exit.\n")

    try:
        while True:
            if ser.in_waiting:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if line == "TIME?":
                    current_hour = datetime.now().hour
                    response = f"{current_hour}\n"
                    ser.write(response.encode())
                    print(
                        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sent hour: {current_hour}"
                    )
                elif line:
                    print(
                        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received: {line}"
                    )
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        ser.close()


if __name__ == "__main__":
    main()
