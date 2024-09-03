import os
import time
import logging

# Setup logging
logging.basicConfig(filename='/home/kuka/fan_control.log', level=logging.INFO)

def get_temperature():
    # Get the temperature from the sensors command for the desired core
    temp_str = os.popen("sensors | grep 'Package id 0' | awk '{print $4}' | sed 's/+//' | sed 's/°C//'").read().strip()
    return int(float(temp_str))

def set_fan_speed(speed):
    # Set the fan speed
    os.system(f"echo {speed} | sudo tee /sys/class/thermal/cooling_device0/cur_state > /dev/null")
    logging.info(f"Fan Speed Set to: {speed}")
    print(f"Fan Speed Set to: {speed}")  # Print to terminal

def main():
    print("Running FAN control for Ubuntu laptop")
    max_temp = 75  # Temperature threshold for max fan speed
    min_temp = 55  # Temperature threshold for minimum fan speed
    
    while True:
        temp = get_temperature()
        print(f"Current Temp: {temp}ºC")  # Print to terminal
        
        if temp >= max_temp:
            new_speed = 3  # Max fan speed
        elif temp <= min_temp:
            new_speed = 0  # Min fan speed (off)
        else:
            new_speed = 1 + (temp - min_temp) // ((max_temp - min_temp) / 3)  # Intermediate speeds

        set_fan_speed(int(new_speed))
        logging.info(f"Current Temp: {temp}ºC, Fan Speed: {new_speed}")
        time.sleep(5)  # Adjust the sleep time as needed

if __name__ == "__main__":
    main()
