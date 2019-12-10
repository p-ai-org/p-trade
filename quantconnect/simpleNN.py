import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD

class SimpleNeuralNetworkAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 1, 20)
        self.SetEndDate(2018, 6, 20)
        
        self.SetCash(100000)
        self.symbols = []
        
        # symbols to track
        self.tickers = ["MMM", "AXP", "AAPL"]
        for ticker in self.tickers:                                 
            equity = self.AddEquity(ticker, Resolution.Daily)
            self.symbols.append(equity.Symbol)
        
        self.lookback = 30 # number of lookback days for historical data

        # train Neural Network every Monday 1 minute after market open
        self.Schedule.On(
            self.DateRules.Every(DayOfWeek.Monday),
            self.TimeRules.AfterMarketOpen("MMM", 1),
            self.NetTrain
        )

        # trade every monday 5 minutes after open
        self.Schedule.On(
            self.DateRules.Every(DayOfWeek.Monday), 
            self.TimeRules.AfterMarketOpen("MMM", 5), 
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

                # add first dense layer with 16 nodes and ReLU activation function
                model.add(Dense(16, activation='relu', input_dim=1))

                # add second dense layer
                model.add(Dense(16, activation='relu'))

                # add final dense layer with one node
                model.add(Dense(1))
                
                # choose loss function as mean-squared error
                # and optimizer as Adam
                model.compile(
                    optimizer='adam',
                    loss='mse'
                )

                # pick an iteration number large enough for convergence 
                num_epochs = 300
                
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
            
            self.buy_prices[symbol] = y_pred_final + np.std(y_data)
            self.sell_prices[symbol] = y_pred_final - np.std(y_data)
        
    def Trade(self):
        ''' 
        Enter or exit positions based on relationship of the open price of the current bar 
        and the prices defined by the neural network model.
        Liquidate if the open price is above the sell price and buy if the open price is below the buy price 
        ''' 
        for holding in self.Portfolio.Values:
            if self.CurrentSlice[holding.Symbol].Open > self.sell_prices[holding.Symbol] and holding.Invested:
                self.Liquidate(holding.Symbol)
            
            if self.CurrentSlice[holding.Symbol].Open < self.buy_prices[holding.Symbol] and not holding.Invested:
                self.SetHoldings(holding.Symbol, 1 / len(self.symbols))