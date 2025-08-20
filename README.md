# Raspberry Pi Pico USB-to-UART Bridge

A robust, non-blocking USB-to-UART bridge for the Raspberry Pi Pico using MicroPython and uasyncio. This implementation provides efficient data transfer between USB and UART interfaces without blocking or losing data.

## Features

- **Non-blocking**: Both USB-to-UART and UART-to-USB directions run in parallel without freezing
- **No byte loss**: Uses `poll()` for USB and `.any()` for UART to ensure all data is captured
- **Efficient**: Yields to the scheduler with `await asyncio.sleep(0)` to keep the event loop responsive
- **Safe**: Ignores invalid UTF-8 when printing binary data to prevent crashes

## Requirements

- Raspberry Pi Pico
- MicroPython firmware installed on the Pico
- UART device to connect (e.g., ESP32, Arduino, etc.)

## Connection Diagram

```
Raspberry Pi Pico    UART Device
     ______           _________
    |      |         |         |
    | GP0  |-------->| RX      |
    |      |         |         |
    | GP1  |<--------| TX      |
    |      |         |         |
    | GND  |---------| GND     |
    |______|         |_________|
```

## Usage

1. Flash MicroPython to your Pico
2. Save this script as `main.py` on the Pico
3. Connect your UART device:
   - GP0 → RX of device
   - GP1 → TX of device
   - GND → GND
4. Open a terminal (e.g., screen, PuTTY, minicom) to the Pico's USB COM port
5. Data is automatically bridged between USB and UART

## How It Works

The bridge uses two asynchronous tasks:
- `usb_to_uart()`: Reads data from USB and writes it to UART
- `uart_to_usb()`: Reads data from UART and writes it to USB

Both tasks run concurrently using `asyncio.gather()`, ensuring bidirectional communication without blocking. The implementation uses `select.poll()` for efficient USB input detection and `uart.any()` for UART input detection.