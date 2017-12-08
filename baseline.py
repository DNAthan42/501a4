import sys
import wav_file
import ctypes

#if direction >= 0, scales from bytes' size to -1<i<1
#otherwise scales from -1<i<1 to bytes' size
def scale(arr, bits, direction=1):
    #get the maximum value of a signed number that is bytes bytes long
    max = 2 ** (bits - 1)
    # print(max, bits)

    for i in range (0, len(arr)):
        if direction >= 0:
            arr[i] /= max
        else:
            arr[i] = int(arr[i] * max)

def convolve(x, h):
    #load the c ver file
    lib = ctypes.CDLL("liba6.so")
    P = len(x) + len(h) -1
    y = []

    #create output buffer
    for n in range(0, P):
        y.append(0.0)

    #convert x, h, y to float arrays
    c_y = (ctypes.c_float * P)(*y)
    c_x = (ctypes.c_float * len(x))(*x)
    c_h = (ctypes.c_float * len(h))(*h)
    c_P = (ctypes.c_uint(P))

    #call the function in C because python performance is horrible
    lib.convolve(c_x, len(x), c_h, len(h), c_y, c_P)

    #convert y back to python types
    y = [c_y[i] for i in range(0,P)]
    
    return y

def getAbsMax(arr):
    xmin = 0.0
    xmax = 0.0
    for i in arr:
        if i < xmin:
            xmin = i
        elif i > xmax:
            xmax = i
    absxmin = xmin * -1
    if absxmin > xmax:
        xmax = absxmin

    return xmax

def baseline(inName, irName, outName)
    #Create a Wave object from the command line argument
    waveFile = wav_file.Wave(inName)

    impulseFile = wav_file.Wave(irName)

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

    ####MAIN

if (len(sys.argv) != 4):
    sys.stderr.write("Usage: baseline inputfile IRfile outputfile\n")
    sys.stderr.flush()
    sys.exit(0)

baseline(sys.argv[1], sys.argv[2], sys.argv[3])
