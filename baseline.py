import sys
import wav_file  

def scale(arr, bytes):
    #get the maximum value of a signed number that is bytes bytes long
    max = 2 ** (8*bytes) - 1

    for i in range (0, len(arr)):
        arr[i] /= max

def convolve(x, h):
    P = len(x) + len(y)
    y = []

    #create output buffer
    for n in range(0, P):
        y.append(0.0)

    #outer loop, process each input value x[n] in turn
    for n in range(0, len(x)):
        #inner loop, process x[n] with each sample of h[n]
        for m in range(0, len(h)):
            y[n+m] += x[n] * h[m]
    
    return y

####MAIN

#Create a Wave object from the command line argument
waveFile = wav_file.Wave(sys.argv[1])

impulseFile = wav_file.Wave(sys.argv[2])

x = waveFile.getData()
h = impulseFile.getData()

scale(x, waveFile.BitsPerSample)
scale(h, impulseFile.BitsPerSample)

if __debug__:
    for i in range(0,len(x)):
        if x[i] > 1.0 or x[i] < -1.0:
            raise ValueError("Post scale value out of range in x")
