#505 unscrambler
#Zack Nelson
import struct

filetarget = open("path to original 505 binary",'rb')
fileout = open("output binary",'wb+')

#functions
def cym_swap4(cym_adr, trg_buf): #4block(4*8k) unscramble
    buf2 = []
    for x in range(cym_adr,cym_adr+(8192*4)):
        lo_bits = ~x & 0b11 #bits 0 + 1
        adr = x >> 2
        adr &= 0b00000001111111111111 #0x01fff
        adr |= (x & 0b11111000000000000000)|(lo_bits << 13)
        buf2.append(buf[adr])
    #copy unscrambled cym
    adr = 0
    for x in range(cym_adr,cym_adr+(8192*4)):
        trg_buf[x] = buf2[adr]
        adr += 1
        
def cym_swap2(cym_adr, trg_buf):#2block(2*8k) unscramble
    buf2 = []
    for x in range(cym_adr,cym_adr+(8192*2)):
        lo_bits = ~x & 1 #bit 0
        adr = x >> 1
        adr &= 0b00000001111111111111 #0x01fff
        adr |= (x & 0b11111100000000000000)|(lo_bits << 13)
        buf2.append(buf[adr])
    #copy unscrambled ride
    adr = 0
    for x in range(cym_adr,cym_adr+(8192*2)):
        buf[x] = buf2[adr]
        adr += 1

def short_swap(short_adr, buf):
    buf2 = []
    temp_adr = short_adr
    chunks = 4
    for x in range(chunks): #4 chunks
        for x in range(2): #odds/evens
            for adr in range(temp_adr,temp_adr+8192,2):
                buf2.append(buf[adr])
            temp_adr +=1 #evens
        temp_adr += 8192 - 2# next block
    #copy unscrambled shorts
    adr = 0
    for x in range(short_adr,short_adr+(8192*chunks)):
        buf[x] = buf2[adr]
        adr += 1

#main

file = filetarget.read()
filetarget.close()
buf = []
temp = 0
adr = 0

#invert lsb
for byte in file:   
    adr_swap = adr ^ 1 #invert lsb
    buf.append(file[adr_swap])
    adr += 1

crash_adr = 0x10000
cym_swap4(crash_adr, buf) #unscramble crash

ride_adr = 0x18000
cym_swap2(ride_adr, buf) #unscramble ride

short_swap(0x8000, buf) #unscramble bass, snare, clap, rim

fileout.write(struct.pack('B'*len(buf), *buf)) #pack Bytes
fileout.close()
