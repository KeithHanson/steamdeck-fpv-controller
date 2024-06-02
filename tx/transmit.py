import micropython
import select
import sys
from sx1262 import SX1262
import time

"""
From: http://community.heltec.cn/t/heltec-lora-32-v3-with-micropython/14023
screen io:
scl pin is 18
sda pin is 17
and the “reset” pin that needs to stay high to write to the screen is pin 21

radio io:
chip is SX1262
uPy lib for chip: https://github.com/git512/micropySX126X 61
chip pins
SS (CS)= 8
SCK (CLK)= 9
MOSI = 10
MISO = 11
RST = 12
BUSY = 13
DIO (also irq) = 14

the onboard led is gpio pin 35
"""

sx = SX1262(spi_bus=1, clk=9, mosi=10, miso=11, cs=8, irq=14, rst=12, gpio=13)

def tx_callback(events):
    if events & SX1262.TX_DONE:
        print('TX done.')
    else:
        print(events)

def begin_lora():
    sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True) 

    sx.setBlockingCallback(False, tx_callback)

begin_lora()

def main():
    should_loop = True
    while should_loop:

      while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:        

        line = sys.stdin.readline().strip()

        print("Got line " + line)

        try:
            sx.send(line.encode())
        except:
            print("Failed. Trying to begin lora again.")
            begin_lora()
            print("begin_lora() complete")

        if line == "quit":
            should_loop = False
            break
