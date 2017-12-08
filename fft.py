import sys
import wav_file
import ctypes
from common import *

def fft(inName, irName, outName):
    #Load wave file information from the arguments
    waveFile = wav_file.Wave(inName)
    impulseFile = wav_file.Wave(irName)

    #Pull the data arrays from the files
    x = waveFile.getData()
    h = impulseFile.getData()

    scale(x, waveFile.BitsPerSample)
    scale(h, impulseFile.BitsPerSample)

    y = convolve(x, h)

    #normalize y
    #get furthest out of range
    ymax = getAbsMax(y)
    print("ymax", ymax)

    #get max of original
    xmax = getAbsMax(x)
    print("xmax", xmax)

    #scale y according to greatest out of range
    mult = xmax/ymax
    print("mult", mult)
    for i in range(0, len(y)):
        y[i] *= mult

    #-1 to scale back up from float to short
    scale(y, waveFile.BitsPerSample, -1)

    ymax = getAbsMax(y)
    print("ymax", ymax)

    waveFile.writeFile(outName, y)

def convolve(x, h):
    #load the c ver file
    lib = ctypes.CDLL("liba6.so")

    #find necessary padding
    biggerArg = max([len(x), len(h)])
    pad = 1
    #double pad until it is larger than the bigger arr
    while pad < biggerArg:
        pad << 1
    
    #pad to double size for FFT
    x_pad = []
    h_pad = []
    i = 0
    while i < 2*pad:
        x_pad[i] = x[i] if i < len(x) else 0.0
        h_pad[i] = h[i] if i < len(h) else 0.0

    #convert to ctypes for fft
    c_x_pad = (ctypes.c_double * 2 * pad)(*x)
    c_h_pad = (ctypes.c_double * 2 * pad)(*h)
    
    #run fft
    lib.four1(c_x_pad, pad, 1)
    lib.four1(c_h_pad, pad, 1)

    #complex multiplication
    y = []
    for i in range(0, 2*pad, 2):
        y[i] = (c_x_pad[i] * c_h_pad[i]) - (c_x_pad[i+1] * c_h_pad[i+1])
        y[i+1] = (c_x_pad[i+1] * c_h_pad[i+1]) + (c_x_pad[i] * c_h_pad[i])

    #convert to ctypes for ifft
    c_y_pad = (ctypes.c_double * 2 * pad)(*y)

    #run ifft
    lib.four1(c_y_pad, pad, -1)

    #truncate and return
    return c_y_pad[:len(x) + len(h) - 1]


####MAIN
if len(sys.argv) != 4:
    sys.stderr.write("Usage: fft inputfile, IRfile, outputfile")
    sys.stderr.flush()
    sys.exit(-1)
fft(sys.argv[1], sys.argv[2], sys.argv[3])
