import sys
import wav_file
import ctypes

####MAIN
if len(sys.argv) != 4:
    sys.stderr.write("Usage: fft inputfile, IRfile, outputfile")
    sys.stderr.flush()
    sys.exit(-1)
fft(sys.argv[1], sys.argv[2], sys.argv[3])

def fft(inFile, irFile, outFile):
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
    #find necessary padding
    minPad = 2* len(x)
    pad = 1
    #double pad until it is larger than minpad
    while pad < minPad:
        pad << 1
    
    #create and fill the output buffer
    y = []
    for i in range(0, pad):
        y.append(0.0)

    #convert to ctypes
    c_y = (ctypes.c_double * pad)(*y)
    
