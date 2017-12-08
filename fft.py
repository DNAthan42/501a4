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
    pass