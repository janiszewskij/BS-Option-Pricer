
import numpy as np
import scipy.stats as si
import IO_BS_dbo_connect
from statistics import stdev

class get_BS_inputs(IO_BS_dbo_connect.dbo_get_BS_parameters):
    def get_volatility(self):
        return stdev(self.closeprices)

class price_European_Option:
    def __init__(self,S, K, T, r, sigma):
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #sigma: volatility of underlying asset
        self.d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        self.d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        self.call = (S * si.norm.cdf(self.d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(self.d2, 0.0, 1.0))
        self.put = (K * np.exp(-r * T) * si.norm.cdf(-self.d2, 0.0, 1.0) - S * si.norm.cdf(-self.d1, 0.0, 1.0))
        print(self.put)
    def call(self):
        return self.call

    def put(self):
        return self.put

#print(price_European_Option(50, 100, 1, 0.05, 0.25).call)
#d2=get_BS_inputs("WW123456789",CCY="PLN")
#print(d2.get_volatility())
#print(d2.get_interestrate())
#print(d2.get_current_price())