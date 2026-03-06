import board
import busio
import time
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


def init_pot():  
    i2c = busio.I2C(board.SCL, board.SDA)
    return(ADS.ADS1015(i2c))

def pot_read(ads):
    front_right = AnalogIn(ads, ADS.P0)
    front_left = AnalogIn(ads, ADS.P1)
    rear_right = 2 #int(AnalogIn(ads.P2))
    rear_left = 3 #int(AnalogIn(ads.P3))
    return [front_right, front_left, rear_right, rear_left]


if __name__ == '__main__':
    ads = init_pot()

    while True:
        data = pot_read(ads)
        print(f'fr:', data[0].value, 'fl:',data[1].value,'\n')
        # print(f'rr: {data[2]}, rl:{data[3]}\n')
        time.sleep(0.1)