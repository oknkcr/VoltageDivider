# Voltage Divider Calculator

This application allows you to perform voltage divider calculation for electronic circuits.

## Features

- Calculations for reference voltage, R1, R2, and output voltage  
- Calculation of resistor values in amplifier circuits  
- Ability to work with standard resistor values  
- Modern, dark-themed interface  
- Scalable interface when resized  

## Installation

### Precompiled Installer

1. Double-click the `DirenBolucu_Setup.exe` file  
2. Follow the installation wizard
3. You must enter a license key "`ABCD-EFGH-IJKL-MNOP-QRST`"
4. You can run the application from the desktop or start menu  

### Build from Source

To build the application from source:

1. Install Python 3.6 or above  
2. Install required dependencies: `pip install pyinstaller`  
3. Directly run from `Calculator.py` source code
   
## Usage

1. Enter R1 and R2 values to calculate the output voltage  
2. Enter R1 and output voltage to calculate R2  
3. Enter R2 and output voltage to calculate R1  
4. Use arrow keys to adjust values in the standard resistor values section  

## Visuals

![](https://github.com/user-attachments/assets/5969db0d-362d-4301-a9a0-a0b56ec60fba)

## Technical Details

The application is developed using Python and Tkinter. The formulas used are:

- `R1 = R2 / (Vout / Vref - 1)`  
- `R2 = R1 * (Vout / Vref - 1)`  
- `Vout = Vref * (1 + R2 / R1)`  

## License
MIT License
	
Copyright © 2025 Okan Kocer. All rights reserved.
	
[LICENSE](LICENSE)

