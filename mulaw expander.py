#DMX-style mu-law expander
#table from http://www.threejacks.com/?q=node/176
# edited by Zack Nelson
import struct, os
from sys import argv

try:
    len(argv[1])
except IndexError:
    print("Input file needed")
    exit(2)

fi = open(argv[1],'rb') #open input
fo = open(os.path.splitext(argv[1])[0]+"_exp.bin", 'wb+') #open output

exp_lut = [0,132,396,924,1980,4092,8316,16764] #16bit
#exp_lut = [0,32,64,128,256,512,1024,2048] #12

file = fi.read()
fi.close()
buf = []
temp = 0
for byte in file:
    ulawbyte = byte
    sign = (ulawbyte & 0x80)
    exponent = (ulawbyte >> 4) & 0x07
    mantissa = ulawbyte & 0x0F
    #sample = exp_lut[exponent] + (mantissa << (exponent))
    sample = exp_lut[exponent] + (mantissa << (exponent+3))
    if sign != 0:
        sample = -sample
    buf.append(sample)
    
fo.write(struct.pack('h'*len(buf), *buf))
fo.close()
