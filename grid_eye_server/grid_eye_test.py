__author__ = 'tmkasun'
from libs.grideye import GridEye


def main():
    sensor = GridEye(0x68)
    print(sensor.thermistor_value)
    print(sensor.frame_rate)

if __name__ == '__main__':
    main()
