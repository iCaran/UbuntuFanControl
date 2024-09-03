# Fan Control Scripts

This repository contains scripts to manage fan speeds on both a Raspberry Pi (meaning ARM devices) and a PC (meaning x86 devices) running Ubuntu. These scripts allow for automatic adjustment of fan speeds based on the system's temperature to prevent overheating and optimize performance.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Raspberry Pi](#raspberry-pi)
  - [PC](#PC)
- [Customization](#customization)
  - [Temperature Thresholds](#temperature-thresholds)
  - [Max Fan Speed](#max-fan-speed)
- [Contributing](#contributing)
- [License](#license)

## Overview

The scripts are designed to run in the background and automatically adjust fan speeds based on temperature readings. They can be set to start on boot using systemd services.

### Raspberry Pi 
## or other ARM devices
The Raspberry Pi script reads temperature data using the `sensors` command and adjusts the fan speed accordingly. The script is configured to handle up to four speed levels based on the current temperature.

### PC
## x86 devices
This script manages the fan speeds on any PC running Ubuntu. It also reads the temperature data using the `sensors` command and adjusts the fan speed accordingly. The script works with the built-in cooling device, which has three states.

## Features
- Automatic fan speed adjustment based on temperature.
- Background operation as a systemd service.
- Configurable to start automatically on boot.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/iCaran/UbuntuFanControl.git
   cd fan-control
   ```

2. **Install Required Packages**
   For both the Raspberry Pi and Ubuntu laptop:
   ```bash
   sudo apt-get install lm-sensors
   ```

3. **Set Up the Systemd Service**
   Copy the relevant `.service` file to `/etc/systemd/system/` and enable it:
   ```bash
   sudo cp fancontrol-rpi.service /etc/systemd/system/fancontrol.service
   sudo systemctl enable fancontrol.service
   ```

## Usage

### Raspberry Pi
1. **Run the Script Manually**
   ```bash
   python3 /path/to/fan.py
   ```

2. **Start the Systemd Service**
   ```bash
   sudo systemctl start fancontrol.service
   ```

### PC
1. **Run the Script Manually**
   ```bash
   python3 /path/to/fan.py
   ```

2. **Start the Systemd Service**
   ```bash
   sudo systemctl start fancontrol.service
   ```

## Customization

### Temperature Thresholds

You may want to customize the temperature thresholds and fan speeds based on your specific needs or hardware configuration. 

1. **Edit the Thresholds in the Code:**
   Open the script in a text editor and locate the temperature threshold section. For example:
   ```python
   if temp < 50:
       fan_speed = 0
   elif temp < 60:
       fan_speed = 1
   elif temp < 70:
       fan_speed = 2
   else:
       fan_speed = 3
   ```
   Modify these values to your desired temperature thresholds.

2. **Save and Restart:**
   After editing, save the file and restart the script or systemd service to apply the changes.

### Max Fan Speed

To check the maximum fan speed that can be set:

1. **Check Max Fan Speed:**
   Run the following command to see the maximum fan state:
   ```bash
   cat /sys/class/thermal/cooling_device0/max_state
   ```
   This will return a number, such as `3`, indicating the highest fan speed level your device supports.

2. **Edit the Fan Speed Levels:**
   Adjust the fan speed levels in the script accordingly. For example:
   ```python
   echo 3 | sudo tee /sys/class/thermal/cooling_device0/cur_state
   ```
   If your maximum fan speed is `3`, ensure that the highest value in your script does not exceed this number.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue if you have suggestions for improvements or new features.

## License

This project is licensed under the Unlicense, which means it is free and unencumbered software released into the public domain. You can copy, modify, distribute, or use it in any way you like.

For more information, see the [LICENSE](LICENSE) file.

---

This README now includes a section on customizing the script to fit different systems or user needs and reflects the Unlicense license. Replace `<your-username>` with your actual GitHub username before uploading.
