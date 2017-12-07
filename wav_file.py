import sys
import struct

class Header():

    def __init__(self):
        self.ChunkID = ""
        self.ChunkSize = 0
        self.Format = ""
        self.Subchunk1ID = ""
        self.Subchunk1Size = 0
        self.AudioFormat = 0
        self.NumChannels = 0
        self.SampleRate = 0
        self.ByteRate = 0
        self.BlockAlign = 0
        self.BitsPerSample = 0

    def __init__(self, filename):
        #open file for reading bytes
        fd = open(filename, 'rb')

        self.ChunkID = fd.read(4).decode()
        if self.ChunkID != "RIFF":
            raise ValueError("Unsupported ChunkID")
        self.ChunkSize = struct.unpack('<I', fd.read(4))[0]
        self.Format = fd.read(4).decode()
        if self.Format != "WAVE":
            raise ValueError("Unsupported Format")
        self.Subchunk1ID = fd.read(4).decode()
        if self.Subchunk1ID != "fmt ":
            raise ValueError("Invalid Subchunk1ID: " + Subchunk1ID)
        self.Subchunk1Size = struct.unpack('<I', fd.read(4))[0]
        self.AudioFormat, self.NumChannels = struct.unpack('<HH', fd.read(4))
        if self.AudioFormat != 1:
            raise ValueError("Unsupported AudioFormat: " + AudioFormat)
        if self.NumChannels != 1:
            raise ValueError("Unsupported NumChannels: " + NumChannels)
        self.SampleRate, self.ByteRate = struct.unpack('<II', fd.read(8))
        self.BlockAlign, self.BitsPerSample = struct.unpack('HH', fd.read(4))

####main
if __debug__:
    test = Header(sys.argv[1])
    #Modified from Meitham's answer at
    #https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python
    for a in dir(test):
        if not a.startswith('__') and not callable(getattr(test,a)):
            print("{}: {}".format(a, getattr(test, a)))

