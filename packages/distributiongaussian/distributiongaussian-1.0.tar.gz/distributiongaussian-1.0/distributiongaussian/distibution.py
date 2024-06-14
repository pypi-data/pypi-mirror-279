class Distibution:
    def __init__(self, mu = 0, sigma = 1 ):
        self.mean = mu
        self.stddev = sigma
        self.data = []
            
    def readthefile(self, filename):
        print("Read function")
        data_set = []
        with open(filename) as fl:
            for lines in fl:
                data_set.append(int(lines.strip()))
        self.data = data_set
        
    def show(self):
        print(self.data)    