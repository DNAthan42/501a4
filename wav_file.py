import sys

class header():

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

    def __init__(filename):
        
