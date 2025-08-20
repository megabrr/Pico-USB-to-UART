#!/usr/bin/env micropython
from _thread import start_new_thread
from machine import UART, Pin
import time
import select
import sys

# UART Configuration
UART0 = 0
TX_PIN = 0
RX_PIN = 1

# Initialize UART with explicit settings for device communication
uart = UART(UART0, 115200, parity=None, bits=8, stop=1, 
            tx=Pin(TX_PIN, Pin.OUT), rx=Pin(RX_PIN, Pin.IN),
            timeout=0)  # No timeout for immediate response

print("Minimal USB-to-UART Bridge Started", file=sys.stderr)
print("Press F7 to access router BIOS", file=sys.stderr)

# RX thread - UART to USB
def rx_thread():
    print("RX thread started...", file=sys.stderr)
    while True:
        # Read any available data from UART
        if uart.any():
            data = uart.read()
            if data:
                # Forward directly to USB stdout
                sys.stdout.write(data)
                try:
                    sys.stdout.flush()
                except:
                    pass
        # Minimal delay
        time.sleep(0.0001)

# Start RX thread on core1
print("Starting RX thread...", file=sys.stderr)
start_new_thread(rx_thread, ())

# Main thread - USB to UART
print("Starting USB-to-UART forwarding...", file=sys.stderr)
try:
    # Register stdin for polling
    poll = select.poll()
    poll.register(sys.stdin, select.POLLIN)
    
    while True:
        # Check for USB input
        if poll.poll(0):
            try:
                # Read all available input
                data = sys.stdin.read(1024)
                if data:
                    # Forward directly to UART
                    uart.write(data)
            except:
                pass
        
        # Minimal delay for responsiveness
        time.sleep(0.0001)
        
except KeyboardInterrupt:
    print("\nExiting...", file=sys.stderr)