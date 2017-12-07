import sys
import struct

class Wave():

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

        self.filename = filename

        #open file for reading bytes
        with open(filename, 'rb') as fd:
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

    def getData(self):

        #open the file
        with open(self.filename, 'rb') as fd:
            print(fd.seek(20 + self.Subchunk1Size, 0)) #skip over the header
            #double check we're at the data chunk
            id = fd.read(4).decode()
            if id != "data":
                raise ValueError("FD not at start of data chunk. Val: " + id)
            
            #need the data's size
            Subchunk2Size = struct.unpack('<I', fd.read(4))[0]
            if __debug__:
                print("Getting {} samples of {} bytes".format(str(Subchunk2Size/self.BlockAlign), int(self.BitsPerSample/8)))

            #load all the data into the array
            arr = []
            for i in range(0, Subchunk2Size, self.BlockAlign):
                arr.append(fd.read(self.BlockAlign))

        return arr

####main
if __debug__:
    test = Wave(sys.argv[1])
    #Modified from Meitham's answer at
    #https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python
    for a in dir(test):
        if not a.startswith('__') and not callable(getattr(test,a)):
            print("{}: {}".format(a, getattr(test, a)))
    print(len(test.getData()))
