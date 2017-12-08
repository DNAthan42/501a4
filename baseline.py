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
    # print("created y")
    c_x = (ctypes.c_float * len(x))(*x)
    c_h = (ctypes.c_float * len(h))(*h)
    c_P = (ctypes.c_uint(P))

    # print(c_y[len(x) + 10000])

    # print("converted x, h")
    # print(len(c_y))

    lib.convolve(c_x, len(x), c_h, len(h), c_y, c_P)

    # print(c_y[len(x) + 10000])
    #convert y back to python types
    y = [c_y[i] for i in range(0,P)]

    # print(len(y))
    # print(y[len(x) + 10000])
    
    return y

####MAIN

#Create a Wave object from the command line argument
waveFile = wav_file.Wave(sys.argv[1])

impulseFile = wav_file.Wave(sys.argv[2])

x = waveFile.getData()
h = impulseFile.getData()

scale(x, waveFile.BitsPerSample)
scale(h, impulseFile.BitsPerSample)

print("len(x)", len(x))
print("len(h)", len(h))
y = convolve(x, h)
print("len(x)", len(x))
print("len(h)", len(h))
print("len(y)", len(y))
# print(y[10000 + 10000])
#normalize y
#get furthest out of range
ymin = 0.0
ymax = 0.0
for i in y:
    if i < ymin:
        ymin = i
    elif i > ymax:
        ymax = i
absymin = ymin * -1
if absymin > ymax:
    ymax = absymin

print("ymax", ymax)

#get max of original
xmin = 0.0
xmax = 0.0
for i in x:
    if i < xmin:
        xmin = i
    elif i > xmax:
        xmax = i
absxmin = xmin * -1
if absxmin > xmax:
    xmax = absxmin

print("xmax", xmax)

#scale y according to greatest out of range
mult = xmax/ymax
print("mult", mult)
for i in range(0, len(y)):
    y[i] *= mult

scale(y, waveFile.BitsPerSample, -1)
# print(y[20000])

ymin = 0.0
ymax = 0.0
for i in y:
    if i < ymin:
        ymin = i
    elif i > ymax:
        ymax = i
absymin = ymin * -1
if absymin > ymax:
    ymax = absymin

print("ymax", ymax)

waveFile.writeFile("convOut.wav", y)

# if __debug__:
#     print("startDebug")
#     for i in range(0,len(x)):
#         if x[i] > 1.0 or x[i] < -1.0:
#             raise ValueError("Post scale value out of range in x")
#     print("endDebug")
