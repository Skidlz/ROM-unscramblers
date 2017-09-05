#626 scrambler
#by Zack Nelson
import struct

import struct, os
from sys import argv

try:
    len(argv[1])
except IndexError:
    print("Input file needed")
    exit(2)
    
filetarget = open(argv[1],'rb') #open input

offset = filetarget.read().find(b'data') + 8 #find end of wav header
filetarget.seek(offset if offset > 8 else 0) #jump after header

fileout = open(os.path.splitext(argv[1])[0]+"1.bin", 'wb+') #open output

#functions

def cym_swap4(cym_adr, trg_buf): #4block(4*8k) scramble
    buf2 = []
    for x in range(cym_adr,cym_adr+(8192*4)):
        adr = x
        hi_bits = (adr >> 13) & 0b11 #13 + 14
        adr <<= 2
        adr &= 0b00000111111111111100 #0x01fff
        adr |= (x & 0b11111000000000000000) | hi_bits
        buf2.append(trg_buf[adr])
    #copy unscrambled cym
    for adr in range(cym_adr,cym_adr+(8192*4)):
        trg_buf[adr] = buf2[adr-cym_adr]

        
def cym_swap2(cym_adr, trg_buf):#2block(2*8k) scramble
    buf2 = []
    for x in range(cym_adr,cym_adr+(8192*2)):
        adr = x
        hi_bits = (adr >> 13) & 1 #13 + 14
        adr <<= 1
        adr &= 0b00000011111111111110 #0x01fff
        adr |= (x & 0b11111000000000000000) | hi_bits
        buf2.append(trg_buf[adr])
    #copy unscrambled ride
    for adr in range(cym_adr,cym_adr+(8192*2)):
        trg_buf[adr] = buf2[adr-cym_adr]

def short_swap(short_adr, trg_buf):
    buf2 = []
    temp_adr = short_adr
    for x in range(3): #3 chunks
        for adr in range(temp_adr,temp_adr+4096):
            buf2.append(trg_buf[adr])
            buf2.append(trg_buf[adr+4096])
            
        temp_adr += 8192 # next block
    #copy unscrambled shorts
    for adr in range(short_adr,short_adr+(8192*3)):
        trg_buf[adr] = buf2[adr-short_adr]

#main

file = filetarget.read()
filetarget.close()
buf = []
temp = 0
adr = 0

for byte in file:   
    buf.append(byte)

crash_adr = pow(2,16)
cym_swap4(crash_adr, buf) #scramble crash

ride_adr = crash_adr+(8192*4)
cym_swap2(ride_adr, buf) #scramble ride

crash2_adr = pow(2,17)+(8192*8)
cym_swap4(crash2_adr, buf) #scramble crash

ride2_adr = crash2_adr+(8192*4)
cym_swap2(ride2_adr, buf) #scramble ride

clap_adr = pow(2,15)
short_swap(clap_adr, buf)

bongo_adr = pow(2,17)+(8192*4)
short_swap(bongo_adr, buf)

buf2 = []
#swap adr pins 6 & 8
for byte in file:   
    adr_swap = adr
    pin_6 = (adr_swap>>6)&1
    pin_8 = (adr_swap>>8)&1
    adr_swap &= ~((1<<8)|(1<<6)) #clear bits
    adr_swap |= (pin_6<<8)|(pin_8<<6) #insert bits
    
    buf2.append(buf[adr_swap])

    adr += 1

fileout.write(struct.pack('B'*len(buf2), *buf2)) #pack Bytes
fileout.close()
