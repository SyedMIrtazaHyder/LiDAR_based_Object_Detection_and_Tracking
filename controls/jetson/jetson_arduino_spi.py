import spidev

spi = spidev.SpiDev() # Enabling SPI
spi.max_speed_hz = 14_000_000; # Matching arduino's 14 MHz
spi.open(0, 0) # bus and device (CS), we have 2 spi devices /dev/spi0.0 and /dev/spi0.1, where 0.x stands for bus 0, device x

while(True):
    x = input("Brake? (y/n): ")
    if (x == 'y' or x == 'Y'):
        spi.writebytes(0xFF)
    else if (x == 'n' or x == 'N'):
        spi.writebytes(0x11)
