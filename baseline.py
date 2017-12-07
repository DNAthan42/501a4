import sys
import wav_file

####MAIN

#Create a Wave object from the command line argument
waveFile = wav_file.Wave(sys.argv[1])

impulseFile = wav_file.Wave(sys.argv[2])



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
