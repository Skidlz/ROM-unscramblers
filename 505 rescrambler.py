#505 scrambler
#Zack Nelson
import struct

filetarget = open("505_unscrambled.bin",'rb')
fileout = open("505_rescrambled.bin",'wb+')

#functions

def cym_swap4(cym_adr, trg_buf): #4block(4*8k) scramble
    buf2 = []
    for x in range(cym_adr,cym_adr+(8192*4)):
        adr = x
        hi_bits = (~adr >> 13) & 0b11 #13 + 14
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
        hi_bits = (~adr >> 13) & 1 #13 + 14
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
    chunks = 4
    for x in range(chunks): #3 chunks
        for adr in range(temp_adr,temp_adr+4096):
            buf2.append(trg_buf[adr])
            buf2.append(trg_buf[adr+4096])
            
        temp_adr += 8192 # next block
    #copy unscrambled shorts
    for adr in range(short_adr,short_adr+(8192*chunks)):
        trg_buf[adr] = buf2[adr-short_adr]

#main

file = filetarget.read()
filetarget.close()
buf = []
temp = 0
adr = 0

for byte in file:   
    buf.append(byte)

crash_adr = 0x10000
cym_swap4(crash_adr, buf) #scramble crash

ride_adr = 0x18000
cym_swap2(ride_adr, buf) #scramble ride

clap_adr = 0x8000
short_swap(clap_adr, buf)

buf2 = []
#swap adr pins 6 & 8
for byte in file:   
    adr_swap = adr ^ 1
    buf2.append(buf[adr_swap])
    adr += 1

fileout.write(struct.pack('B'*len(buf2), *buf2)) #pack Bytes
fileout.close()
