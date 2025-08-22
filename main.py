#!/usr/bin/env micropython
import uasyncio as asyncio
import select
from machine import UART, Pin
import sys

# UART Configuration
UART0 = 0
TX_PIN = 0
RX_PIN = 1
BAUD_RATE = 115200

# Initialize UART with explicit settings for device communication
uart = UART(UART0, BAUD_RATE, parity=None, bits=8, stop=1, 
            tx=Pin(TX_PIN, Pin.OUT), rx=Pin(RX_PIN, Pin.IN),
            timeout=0)  # No timeout for immediate response

# Set up poll for stdin
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

print("USB-to-UART Bridge Started")

async def usb_to_uart():
    """Forward data from USB to UART"""
    print("USB-to-UART task started...")
    try:
        while True:
            # Check if data is available on USB using poll
            if poll.poll(0):  # Non-blocking check
                data = sys.stdin.read(1024)
                if data:
                    # Forward to UART
                    uart.write(data)
            # Yield control to event loop
            await asyncio.sleep_ms(1)
    except Exception as e:
        print(f"USB-to-UART error: {e}")

async def uart_to_usb():
    """Forward data from UART to USB"""
    print("UART-to-USB task started...")
    try:
        while True:
            # Check if data is available on UART
            if uart.any():
                data = uart.read()
                if data:
                    # Forward to USB
                    sys.stdout.write(data)
                    try:
                        sys.stdout.flush()
                    except:
                        pass
            # Yield control to event loop
            await asyncio.sleep_ms(1)
    except Exception as e:
        print(f"UART-to-USB error: {e}")

async def main():
    """Main function to run both tasks concurrently"""
    print("Starting USB-to-UART bridge...")
    # Run both tasks concurrently
    await asyncio.gather(
        usb_to_uart(),
        uart_to_usb()
    )

# Run the main async function
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    # Clean up
    uart.deinit()