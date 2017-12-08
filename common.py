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