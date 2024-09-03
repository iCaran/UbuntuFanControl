from subprocess import run as srun, PIPE
from time import sleep
from datetime import timedelta as td, datetime as dt
import logging

## Use step values to activate desired FAN value
STEP1 = 48
STEP2 = 60
STEP3 = 65
STEP4 = 72

SLEEP_TIMER = 1

TICKS = 3
DELTA_TEMP = 3
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
fanControlFile = '/sys/class/thermal/cooling_device0/cur_state'

logging.basicConfig(filename='/home/kookaburra/fan_control.log', level=logging.INFO)

def main():
    print("Running FAN control for RPI5 Ubuntu")
    t0 = dt.now()

    command = f'tee -a {fanControlFile} > /dev/null'
    oldSpeed = 0
    ticks = 0

    speed = 1
    lastTemp = 0

    while True:
        sleep(SLEEP_TIMER) # force 1 second timer, just to reduce polling calls
        t1 = dt.now()
        if(t1 + td(minutes=TICKS) > t0):
            t0 = t1
            
            cels = get_temperature()

            if STEP1 < cels < STEP2:
                speed = 1
            elif STEP2 < cels < STEP3:
                speed = 2
            elif STEP3 < cels < STEP4:
                speed = 3
            elif cels >= STEP4:
                speed = 4

            deltaTempNeg = lastTemp - DELTA_TEMP
            deltaTempPos = lastTemp + DELTA_TEMP

            if oldSpeed != speed and not(deltaTempNeg <= cels <= deltaTempPos):
                print(f'oldSpeed: {oldSpeed} | newSpeed: {speed}')
                print(f'{deltaTempNeg}ºC <= {cels}ºC <= {deltaTempPos}ºC')
                print(f'{"#"*30}\n' +
                      f'Updating fan speed!\t{t0.strftime(DATETIME_FORMAT)}\n' +
                      f'CPU TEMP: {cels}ºC\n' +
                      f'FAN speed will be set to: {speed}\n' +
                      f'{"#"*30}\n')

                _command = f'echo {speed} | sudo {command}'
                callShell(_command, debug=True)
                checkVal = getOutput(f'cat {fanControlFile}')
                print(f'Confirm FAN set to speed: {checkVal}')

                oldSpeed = speed
                lastTemp = cels
                ticks = 0
            
            # Log minor details
            ticks += 1
            if(ticks > TICKS * 3):
                ticks = 0
                print(f'Current Temp is: {cels}ºC\t{t0.strftime(DATETIME_FORMAT)}')
                log_info(f"Current Temp: {cels}ºC, Fan Speed: {speed}")

def get_temperature():
    # Attempt to find the first temperature value
    tempOut = getOutput("sensors | awk '/temp1/ {print $2; exit}'")
    print(f"Raw temperature output: '{tempOut.strip()}'")
    try:
        cels = int(float(tempOut.strip().replace('+', '').replace('°C', '')))
    except Exception as e:
        print(f"Error parsing temperature: {e}")
        cels = 40  # fallback temperature
    return cels

def callShell(cmd, shell=True, debug=False):
    if debug:
        print(f'Calling: [{cmd}]')
    return srun(f'''{cmd}''', stdout=PIPE, shell=shell)

def getOutput(cmd, shell=True):
    stdout = callShell(cmd, shell=shell).stdout
    try:
        stdout = stdout.decode('utf-8')
    except:
        pass
    return stdout

def log_info(message):
    logging.info(message)

## RUN SCRIPT
main()
