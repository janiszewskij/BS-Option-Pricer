
import pyodbc
import math

class dbo_get_BS_parameters:
    def __init__(self,ISIN="WW123456789",maturity='7D',from_date=None,to_date=None,CCY='USD'):
        self.closeprices=[]
        self.interestrate=None
        self.current_price=None
        self.security_list=[]
        
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-dbname\SQLEXPRESS;'
                      'Database=IO_BS;'
                      'Trusted_Connection=yes;')
        
        cursor = conn.cursor()
        cursor.execute("SELECT PRICE FROM dbo.ClosePrice WHERE ISIN = ? AND CCY = ?" ,[ISIN,CCY])
        
        for row in cursor.fetchall():
            for field in row:
                self.closeprices.append(float(field))
                
        cursor.execute("SELECT Rate FROM dbo.IterestRate WHERE Currency = ? AND Maturity = ?" ,[CCY,maturity])
        for row in cursor.fetchall():
            for field in row:
                self.interestrate=field
                
        cursor.execute("SELECT TOP 1 Price FROM ClosePrice where ISIN = ? ORDER BY Date", [ISIN])
        
        for row in cursor.fetchall():
            for field in row:
                self.current_price=field
                
        cursor.execute("SELECT DISTINCT ISIN from SecurityList ")
        
        for row in cursor.fetchall():
            for field in row:
                self.security_list.append(field)
                
        #cursor.execute("SELECT Rate FROM dbo.IterestRate WHERE Currency = ? AND DateYYYYMMDD = ?" ,[CCY,from_date])
        conn.close() 
        
    def get_closeprices(self):
        return self.closeprices
    
    def get_interestrate(self):
        return self.interestrate
    
    def get_current_price(self):
        return self.current_price
    
    def get_security_list(self):
        return self.security_list
    
    def get_implied_vol(cp, price, s, k, t, rf):
        v = sqrt(2*pi/t)*price/s
        
        for i in range(1, 10):
            d1 = (log(s/k)+(rf+0.5*pow(v,2))*t)/(v*sqrt(t))
            d2 = d1 - v*sqrt(t)
            gamma = norm.pdf(d1)/(s*v*sqrt(t))
            price0 = cp*s*norm.cdf(cp*d1) - cp*k*exp(-rf*t)*norm.cdf(cp*d2)
            v = v - (price0 - price)/gamma
            
            if abs(price0 - price) < 1e-10 :
                break
            return v
    
#d1=dbo_get_BS_parameters("WW123456789",CCY='PLN')
#print(d1.get_closeprices())
