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
                raise ValueError("Invalid Subchunk1ID: " + self.Subchunk1ID)
            self.Subchunk1Size = struct.unpack('<I', fd.read(4))[0]
            self.AudioFormat, self.NumChannels = struct.unpack('<HH', fd.read(4))
            if self.AudioFormat != 1:
                raise ValueError("Unsupported AudioFormat: " + self.AudioFormat)
            if self.NumChannels != 1:
                raise ValueError("Unsupported NumChannels: " + self.NumChannels)
            self.SampleRate, self.ByteRate = struct.unpack('<II', fd.read(8))
            self.BlockAlign, self.BitsPerSample = struct.unpack('HH', fd.read(4))

    def getData(self):

        #open the file
        with open(self.filename, 'rb') as fd:
            fd.seek(20 + self.Subchunk1Size, 0) #skip over the header
            #double check we're at the data chunk
            id = fd.read(4).decode()
            if id != "data":
                raise ValueError("FD not at start of data chunk. Val: " + id)
            
            #need the data's size
            Subchunk2Size = struct.unpack('<I', fd.read(4))[0]
            if __debug__:
                print("Getting {} samples of {} bytes".format(str(Subchunk2Size/self.BlockAlign), int(self.BitsPerSample/8)))

            #load all the data into the array
            #todo: extend this line for multi channel, h is 2 bytes long
            arr = []
            for i in range(0, Subchunk2Size):
                a = fd.read(self.BlockAlign)
                if not a:
                    print ("i" + str(i))
                    break
                arr.append(struct.unpack('<h', a)[0])

            print("i" + str(i))

        return arr

    def getDataSize(self):
        #open the file
        with open(self.filename, 'rb') as fd:
            fd.seek(20 + self.Subchunk1Size, 0) #skip over the header
            #double check we're at the data chunk
            id = fd.read(4).decode()
            if id != "data":
                raise ValueError("FD not at start of data chunk. Val: " + id)
            
            #need the data's size
            return struct.unpack('<I', fd.read(4))[0]

    def writeFile(self, filename, data):

        #recalculate file size and data chunk size
        Subchunk2Size = len(data) * self.BlockAlign
        self.ChunkSize = 4 + 8 + self.Subchunk1Size + 8 + Subchunk2Size

        with open(filename, 'wb') as fd:
            print(len(self.ChunkID), len(self.Format), len(self.Subchunk1ID), self.Subchunk1Size)
            #copy in the header
            fd.write(self.ChunkID.encode('ascii'))
            fd.write(struct.pack('<I', self.ChunkSize))
            fd.write(self.Format.encode('ascii'))
            fd.write(self.Subchunk1ID.encode('ascii'))
            fd.write(struct.pack('<I', self.Subchunk1Size))
            fd.write(struct.pack('<H', self.AudioFormat))
            fd.write(struct.pack('<H', self.NumChannels))
            fd.write(struct.pack('<I', self.SampleRate))
            fd.write(struct.pack('<I', self.ByteRate))
            fd.write(struct.pack('<H', self.BlockAlign))
            fd.write(struct.pack('<H', self.BitsPerSample))
            fd.write(b"\x00\x00")

            #write the data sub chunk
            fd.write(b"data")
            fd.write(struct.pack('<I', Subchunk2Size))
            
            #dump array to file
            #todo extend for bitspersample != 16
            try:
                for i in range(0, len(data)):
                    fd.write(struct.pack('<h', data[i]))
                print("writei " + str(i))
            except struct.error as e:
                print (i, data[i])
                raise e


####main
# if __debug__:
#     test = Wave(sys.argv[1])
#     #Modified from Meitham's answer at
#     #https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python
#     for a in dir(test):
#         if not a.startswith('__') and not callable(getattr(test,a)):
#             print("{}: {}".format(a, getattr(test, a)))
#     test.writeFile("out.wav", test.getData())
