import sys
import wav_file
import ctypes

#if direction >= 0, scales from bytes' size to -1<i<1
#otherwise scales from -1<i<1 to bytes' size
def scale(arr, bytes, direction=1):
    #get the maximum value of a signed number that is bytes bytes long
    max = 2 ** (8*bytes) - 1
    if direction < 0:
        max = 1/max

    for i in range (0, len(arr)):
        arr[i] /= max


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
    print("created y")
    c_x = (ctypes.c_float * len(x))(*x)
    c_h = (ctypes.c_float * len(h))(*h)
    c_P = (ctypes.c_uint(P))

    print("converted x, h")

    lib.convolve(c_x, len(x), c_h, len(h), c_y, c_P)

    #convert y back to python types
    y = [c_y[i] for i in range(0,P)]
    
    return y

####MAIN

#Create a Wave object from the command line argument
waveFile = wav_file.Wave(sys.argv[1])

impulseFile = wav_file.Wave(sys.argv[2])

x = waveFile.getData()
h = impulseFile.getData()

scale(x, waveFile.BitsPerSample)
scale(h, impulseFile.BitsPerSample)

y = convolve(x, h)

waveFile.writeFile("convOut.wav", scale(y, waveFile.BitsPerSample))

if __debug__:
    print("startDebug")
    for i in range(0,len(x)):
        if x[i] > 1.0 or x[i] < -1.0:
            raise ValueError("Post scale value out of range in x")
    print("endDebug")
