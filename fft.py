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
    normalize(y, x)

    #-1 to scale back up from float to short
    scale(y, waveFile.BitsPerSample, -1)

    waveFile.writeFile(outName, y)

def convolve(x, h):
    #load the c ver file
    lib = ctypes.CDLL("liba6.so")

    #find necessary padding
    biggerArg = max([len(x), len(h)])
    pad = 1
    #double pad until it is larger than the bigger arr
    while pad < biggerArg:
        pad = pad << 1
    dubPad = pad << 1

    print("padding", flush=True, end='')    
    #pad to double size for FFT
    x_pad = []
    h_pad = []
    for i in range(0, dubPad):
        x_pad.append(x[i] if i < len(x) else 0.0)
        h_pad.append(h[i] if i < len(h) else 0.0)

    if len(x_pad) != dubPad or len(h_pad) != dubPad:
        print(" post padding size is not expected val.")
        sys.exit(-1)

    #convert to ctypes for fft
    c_x_pad = (ctypes.c_double * dubPad)(*x_pad)
    c_h_pad = (ctypes.c_double * dubPad)(*h_pad)
    
    print(" -> ffts", flush=True, end='')
    #run fft
    lib.four1(c_x_pad, pad, 1)
    print(" x, ", flush=True, end='')
    lib.four1(c_h_pad, pad, 1)
    print("h", flush=True, end='')

    print(" -> complex mul", flush=True, end='')
    #complex multiplication
    y = []
    for i in range(0, dubPad, 2):
        y.append((c_x_pad[i] * c_h_pad[i]) - (c_x_pad[i+1] * c_h_pad[i+1]))
        y.append((c_x_pad[i] * c_h_pad[i+1]) + (c_x_pad[i+1] * c_h_pad[i]))

    print(" -> ifft", flush=True, end='')
    #convert to ctypes for ifft
    c_y_pad = (ctypes.c_double * dubPad)(*y)

    #run ifft
    lib.four1(c_y_pad, pad, -1)

    print(" -> downscaling y")
    y = [c_y_pad[i] for i in range(0, len(x) + len(h) - 1)]
    for i in range(0, len(y)):
        y[i] /= pad

    #truncate and return
    return y


####MAIN
if len(sys.argv) != 4:
    sys.stderr.write("Usage: fft inputfile, IRfile, outputfile")
    sys.stderr.flush()
    sys.exit(-1)
fft(sys.argv[1], sys.argv[2], sys.argv[3])
