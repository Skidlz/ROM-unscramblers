#BOSS 220 mu-law expander
#table from http://www.threejacks.com/?q=node/176
# edit by Zack Nelson
import struct
filetarget = open("path to original 220 binary",'rb')
fileout = open("output binary",'wb+')

exp_lut = [0,132,396,924,1980,4092,8316,16764] #16bit
#exp_lut = [0,32,64,128,256,512,1024,2048] #12

file = filetarget.read()
filetarget.close()
buf = []
temp = 0
for byte in file:
    ulawbyte = byte
    ulawbyte = ~ulawbyte
    sign = (ulawbyte & 0x80)
    if sign:
        ulawbyte = ~ulawbyte
    exponent = (ulawbyte >> 4) & 0x07
    mantissa = ulawbyte & 0x0F
    #sample = exp_lut[exponent] + (mantissa << exponent)
    sample = exp_lut[exponent] + (mantissa << (exponent + 3));
    if sign != 0:
        sample = -sample
    buf.append(sample)
    
fileout.write(struct.pack('h'*len(buf), *buf))
fileout.close()
