import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import minimize
import math

class Portfolio:
    def __init__(self, name):
        self.name = name
        self.stocks = []
        self.df = pd.DataFrame()
        self.log_ret = pd.DataFrame()
        self.portfolios = pd.DataFrame()
        self.expected_ret = 0
        self.expected_vol = 0
    
    def printstocks(self):
        print(self.stocks)
    
    def addstock(self,s,ds,de):
        '''
        adds the historical stock data to dataframe used in following methods

        s = list[str] or str types of the symbols of desired stocks in portfolio
        ds = start date in string 'YYYY-MM-DD'
        de = start date in string 'YYYY-MM-DD'
        '''
        #print()
        #inp = input('Enter stocks separated by a space: ')
        #s = inp.split()

        #print('stocks:' +  str(s))
        #print('# of stocks: '+ str(len(s)))

        #ds = input('start date (YYYY-MM-DD): ')
        #de = input('end date (YYYY-MM-DD): ')


        dts = datetime.strptime(ds, '%Y-%m-%d')
        dte = datetime.strptime(de, '%Y-%m-%d')
        if type(s) == str:
            if s not in self.stocks:
                self.stocks.append(s)
                self.df[s]=wb.DataReader(s,'yahoo',dts,dte)['Adj Close']
        elif type(s)==list: 
            for i in s:
                if i not in self.stocks:
                    self.stocks.append(i)
                    self.df[i]=wb.DataReader(i,'yahoo',dts,dte)['Adj Close']
        
        self.log_ret = np.log(self.df/self.df.shift(1))

        print("Last 10 Days:")
        print(self.df.tail(10))
        print()

    def delstock(self, s):
        if type(s) == str:
            if s in self.stocks:
                self.stocks.remove(s)
                self.df.drop(s, axis=1, inplace=True)
        elif type(s)==list:
            for i in s:
                if i in self.stocks:
                    self.stocks.remove(i)
                    self.df.drop(s, axis=1, inplace=True)
    
    def monte_port(self):

        np.random.seed(101)

        num_ports = 5000

        self.portfolios = np.zeros((num_ports,len(self.df.columns)))
        ret_arr = np.zeros(num_ports)
        vol_arr = np.zeros(num_ports)
        sharpe_arr = np.zeros(num_ports)

        for ind in range(num_ports):
            weights = np.array(np.random.random(len(self.stocks)))
            weights = weights / np.sum(weights)
            
            self.portfolios[ind,:] = weights

            ret_arr[ind] = np.sum((self.log_ret.mean() * weights) *252)

            vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(self.log_ret.cov() * 252, weights)))

            sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]

        self.portfolios = pd.DataFrame(self.portfolios,columns=self.df.columns)
        self.portfolios['Return'] = ret_arr
        self.portfolios['Volatility'] = vol_arr
        self.portfolios['Sharpe'] = sharpe_arr

    def eff_front(self):

        max_sr_ret = self.portfolios['Return'].iloc[self.portfolios['Sharpe'].argmax()]
        max_sr_vol = self.portfolios['Volatility'].iloc[self.portfolios['Sharpe'].argmax()]

        plt.figure(figsize=(12,8))
        plt.scatter(self.portfolios['Volatility'],self.portfolios['Return'],c=self.portfolios['Sharpe'],cmap='plasma')
        plt.colorbar(label='Sharpe Ratio')
        plt.xlabel('Volatility')
        plt.ylabel('Return')

        # Add red dot for max SR
        return plt.scatter(max_sr_vol,max_sr_ret,c='red',s=50,edgecolors='black')

    def normalplot(self):
        (self.df/self.df.iloc[0]*100).plot(figsize=(15,8))
        plt.legend(bbox_to_anchor=(1.01, 1))
        plt.show()

    
    def invest(self, n, mvol=False, vol=0.5):
        if mvol == True:

            w = {}
            df = self.portfolios
            for i in self.stocks:
                w[i] = df[df['Volatility']<vol].sort_values(['Return'],ascending=False).iloc[0][i]
            
            r = df[df['Volatility']<vol].sort_values(['Return'],ascending=False).head().iloc[0]['Return']
            v = df[df['Volatility']<vol].sort_values(['Return'],ascending=False).head().iloc[0]['Volatility']
            s = df[df['Volatility']<vol].sort_values(['Return'],ascending=False).head().iloc[0]['Sharpe']

            #b = self.beta()
            #pf_b = np.sum(np.dot(b,w))

            for i in w.keys():
                print(i+' ('+str(round(w.get(i),2))+')'+': '+ '$'+ str(round(w.get(i)*n,2)) + ' @ $'+str(round(self.df[i][-1],2))+  ' per share' + \
                    '(#'+str(math.floor((w.get(i)*n)/(self.df[i][-1])))+')')
                print('--')
            print()
            print('r: '+str(r))
            print('v: '+str(v))
            #print('B: '+str(pf_b))
            print('S: '+str(s))
            print()
            print('Expected Return: '+'$'+str(round(n*(1+r),2)))
            print('Range: ' + '$'+str(round(n*(1+(r-v)),2))+ ' - '+ '$'+str(round(n*(1+(r+v)),2)))

            max_sr_ret = self.portfolios['Return'].iloc[self.portfolios['Sharpe'].argmax()]
            max_sr_vol = self.portfolios['Volatility'].iloc[self.portfolios['Sharpe'].argmax()]

            plt.figure(figsize=(12,8))
            plt.scatter(self.portfolios['Volatility'],self.portfolios['Return'],c=self.portfolios['Sharpe'],cmap='plasma')
            plt.colorbar(label='Sharpe Ratio')
            plt.xlabel('Volatility')
            plt.ylabel('Return')

            # Add red dot for max SR
            plt.scatter(max_sr_vol,max_sr_ret,c='red',s=50,edgecolors='black')

            # Add blue dot = chosen pf
            plt.scatter(v,r,c='black',s=50,edgecolors='black')

        
        else:
            w = {}
            df = self.portfolios
            for i in self.stocks:
                w[i]=df[i].iloc[self.portfolios['Sharpe'].argmax()]
            
            r = df['Return'].iloc[self.portfolios['Sharpe'].argmax()]
            v = df['Volatility'].iloc[self.portfolios['Sharpe'].argmax()]
            s = df['Sharpe'].iloc[self.portfolios['Sharpe'].argmax()]

            #b = self.beta()
            #pf_b = np.sum(np.dot(b,w))

            for i in w.keys():
                print(i+' ('+str(round(w.get(i),2))+')'+': '+ '$'+ str(round(w.get(i)*n,2)) + ' @ $'+str(round(self.df[i][-1],2))+  ' per share' + \
                    '(#'+str(math.floor((w.get(i)*n)/(self.df[i][-1])))+')')
                print('--')
            print()
            print('r: '+str(r))
            print('v: '+str(v))
           #print('B: '+str(pf_b))
            print('S: '+str(s))
            print()
            print('Expected Return: '+'$'+str(round(n*(1+r),2)))
            print('Range: ' + '$'+str(round(n*(1+(r-v)),2))+ ' - '+ '$'+str(round(n*(1+(r+v)),2)))

    def optimal_port(self,invest,min_ex,max_ex):
        '''
        Prints the allocation in format:
        Stock (weight): $value @ $shar_price (# of shares)r: expected annual return%

	invest = investment amount in dollars ($USD)
	min_ex = minimum exposure of stock in the portfolio expressed as a percentage
	max_ex = maximum exposure of stock in the portfolio expressed as a percentage

        '''

        
        #invest = int(input('Enter investment amounnt: '))
        #min_ex = float(input('Enter min exposure: '))
        #max_ex = float(input('Enter max exposure: '))

        print()

        s_list = self.stocks

        def get_ret_vol_sr(weights):
            """
            Takes in weights, returns array or return,volatility, sharpe ratio
            """
            weights = np.array(weights)
            ret = np.sum(self.log_ret.mean() * weights) * 252
            vol = np.sqrt(np.dot(weights.T, np.dot(self.log_ret.cov() * 252, weights)))
            sr = ret/vol
            return np.array([ret,vol,sr])

        def neg_sharpe(weights):
            return  get_ret_vol_sr(weights)[2] * -1
        
        def check_sum(weights):
            '''
            Returns 0 if sum of weights is 1.0
            '''
            return np.sum(weights) - 1

        cons = ({'type':'eq','fun': check_sum})
        bounds = []
        init_guess = []
        
        for i in range(len(s_list)):
            init_guess.append(1/len(s_list))
            bounds.append((min_ex,max_ex))

        opt_results = minimize(neg_sharpe,init_guess,method='SLSQP',bounds=bounds,constraints=cons)

        pf_l = 0

        self.port_df = pd.DataFrame()
        self.port_df['Stocks']=s_list
        self.port_df['weights']=opt_results.x

        for i in range(len(s_list)):
            w = round(opt_results.x[i],3)
            if w != 0.0:
                pf_l +=1  
                print(s_list[i] + '('+str(w) + ')' + ': $' + str(w*invest) + ' @ $' + str(round(self.df[s_list[i]][-1],2)) + ' per share' + \
                '(#'+str(math.floor((w*invest)/(self.df[s_list[i]][-1])))+')' + 'r: ' + str(round(self.log_ret[s_list[i]].mean()*252,4)*100)+'%')
                print('---')
            

        (r,v,s) = get_ret_vol_sr(opt_results.x)
        print()
        print('return: ' + str(r))
        print('volatility: ' + str(v))
        print('sharpe: ' + str(s))
        print()

        print('Portfolio length: ' + str(pf_l))

        print()
        print('Expected Return: '+'$'+str(round(invest*(1+r),2)))
        print('Range: ' + '$'+str(round(invest*(1+(r-v)),2))+ ' - '+ '$'+str(round(invest*(1+(r+v)),2)))









    
    