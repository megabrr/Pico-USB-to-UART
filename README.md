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
2. Save this script as `main_new.py` on the Pico
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

## Troubleshooting

If you're experiencing issues with the USB-to-UART bridge, try these solutions:

### 1. Connection Issues

- **Check wiring**: Ensure all connections are secure and correct:
  - GP0 (Pico) → RX (UART device)
  - GP1 (Pico) → TX (UART device)
  - GND (Pico) → GND (UART device)
- **Verify power supply**: Ensure your UART device is properly powered
- **Check for short circuits**: Make sure no pins are accidentally touching

### 2. USB Serial Communication Issues

- **Device not recognized**:
  - Check if the Pico appears as a USB serial device in your OS
  - On Linux: `ls /dev/ttyACM*`
  - On macOS: `ls /dev/tty.usbmodem*`
  - On Windows: Check Device Manager for COM ports
- **Driver issues**: Ensure you have the correct drivers installed for the Pico

### 3. Screen Session Issues

- **Incorrect baud rate**: Make sure your terminal is set to 115200 baud:
  ```bash
  screen /dev/ttyACM0 115200
  ```
- **Permissions**: On Linux, you might need to add your user to the dialout group:
  ```bash
  sudo usermod -a -G dialout $USER
  ```
- **Port in use**: Make sure no other program is using the serial port

### 4. Data Not Flowing

- **Check UART device**: Ensure your UART device is sending data
- **Verify baud rate match**: Both the bridge and your UART device must use the same baud rate (115200)
- **Test loopback**: Connect GP0 to GP1 on the Pico to test if data echoes back

### 5. Code Issues

- **Firmware**: Ensure you're using a recent version of MicroPython for the Pico
- **File name**: Make sure the script is saved as `main_new.py` on the Pico
- **Reset device**: Try unplugging and replugging the Pico

### 6. Debugging

- **Add debug prints**: Uncomment print statements in the code to see what's happening
- **Check Pico output**: Connect to the Pico's serial console to see debug messages:
  ```bash
  screen /dev/ttyACM0 115200
  ```
  You should see "USB-to-UART bridge started" when the script runs correctly.
Both tasks run concurrently using `asyncio.gather()`, ensuring bidirectional communication without blocking. The implementation uses `select.poll()` for efficient USB input detection (checking if data is available before reading) and `uart.any()` for UART input detection.