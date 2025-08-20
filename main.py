import uasyncio as asyncio
import machine
import sys
import select

# UART Configuration
# UART0 on GP0 (TX) and GP1 (RX) at 115200 baud
uart = machine.UART(0, baudrate=115200)

async def usb_to_uart():
    """Forward data from USB to UART."""
    poll = select.poll()
    poll.register(sys.stdin, select.POLLIN)

    while True:
        if poll.poll(0):  # Check if USB has incoming data
            data = sys.stdin.read(1)
            if data:
                uart.write(data)
        await asyncio.sleep(0)  # Yield to other tasks

async def uart_to_usb():
    """Forward data from UART to USB."""
    while True:
        if uart.any():
            data = uart.read()
            if data:
                try:
                    sys.stdout.write(data.decode(errors="ignore"))
                except UnicodeError:
                    pass
        await asyncio.sleep(0)  # Yield to other tasks

async def main():
    print("USB-to-UART bridge started")
    print("TX=GP0, RX=GP1, Baud=115200")
    await asyncio.gather(usb_to_uart(), uart_to_usb())

# Run event loop
asyncio.run(main())
