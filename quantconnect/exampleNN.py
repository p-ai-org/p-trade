# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import clr
clr.AddReference("System")
clr.AddReference("QuantConnect.Algorithm")
clr.AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD

class KerasNeuralNetworkAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2013, 10, 7)  # Set Start Date
        self.SetEndDate(2013, 10, 8) # Set End Date
        
        self.SetCash(100000)  # Set Strategy Cash
        spy = self.AddEquity("SPY", Resolution.Minute)
        self.symbols = [spy.Symbol] # This way can be easily extended to multiply symbols
        
        self.lookback = 30 # day of lookback for historical data

        # train Neural Network every Monday 28 minutes after market open
        self.Schedule.On(
            self.DateRules.Every(DayOfWeek.Monday),
            self.TimeRules.AfterMarketOpen("SPY", 28),
            self.NetTrain
        )

        # trade every monday 30 minutes after open
        self.Schedule.On(
            self.DateRules.Every(DayOfWeek.Monday), 
            self.TimeRules.AfterMarketOpen("SPY", 30), 
            self.Trade
        ) 
        
    def NetTrain(self):
        # Daily historical data is used to train the machine learning model 
        history = self.History(self.symbols, self.lookback + 1, Resolution.Daily)
        
        # dicts that store prices for training
        self.prices_x = {} 
        self.prices_y = {}
        
        # dicts that store prices for sell and buy
        self.sell_prices = {}
        self.buy_prices = {}
        
        for symbol in self.symbols:
            if not history.empty:
                # x: pridictors; y: response
                self.prices_x[symbol] = list(history.loc[symbol.Value]['open'])[:-1]
                self.prices_y[symbol] = list(history.loc[symbol.Value]['open'])[1:]
                
        for symbol in self.symbols:
            if symbol in self.prices_x:
                # convert the original data to np array for fitting the keras NN model
                x_data = np.array(self.prices_x[symbol])
                y_data = np.array(self.prices_y[symbol])
                
                # build a neural network from the 1st layer to the last layer
                model = Sequential()

                # add first dense layer with 10 nodes and ReLU activation function
                model.add(Dense(10, activation='relu', input_dim = 1))

                # add final dense layer with one node
                model.add(Dense(1))

                # optimizer is stochastic gradient descent with learning rate = 0.01
                sgd = SGD(lr = 0.01)
                
                # choose loss function as mean-squared error and set model optimizer
                model.compile(loss='mse', optimizer=sgd)

                # pick an iteration number large enough for convergence 
                num_epochs = 500
                
                # train the model on all the data
                # this is typically not how it is done in practice
                # in practice you want a training dataset and a validation dataset
                model.fit(
                    x_data,
                    y_data,
                    epochs = num_epochs,
                    batch_size = 10,
                )
            
            # get the final predicted price 
            y_pred_final = model.predict(y_data)[0][-1]
            
            # Follow the trend
            self.buy_prices[symbol] = y_pred_final + np.std(y_data)
            self.sell_prices[symbol] = y_pred_final - np.std(y_data)
        
    def Trade(self):
        ''' 
        Enter or exit positions based on relationship of the open price of the current bar 
        and the prices defined by the neural network model.
        Liquidate if the open price is below the sell price and buy if the open price is above the buy price 
        ''' 
        for holding in self.Portfolio.Values:
            if self.CurrentSlice[holding.Symbol].Open < self.sell_prices[holding.Symbol] and holding.Invested:
                self.Liquidate(holding.Symbol)
            
            if self.CurrentSlice[holding.Symbol].Open > self.buy_prices[holding.Symbol] and not holding.Invested:
                self.SetHoldings(holding.Symbol, 1 / len(self.symbols))




