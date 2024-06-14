from .distibution import Distibution

class Gaussian(Distibution):
    def __init__(self, mu = 0, sigma = 1 ):
        Distibution.__init__(self, mu, sigma)
        
    def calculate_mean(self):
        """ calculating the mean
        """
        avg = sum(self.data) / len(self.data)
        self.mean = avg
        print(self.mean)
    

    