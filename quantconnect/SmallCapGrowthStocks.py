''' quantconnect premade module that selects universe of liquid stocks listed on Nasdaq'''

from Selection.FundamentalUniverseSelectionModel import FundamentalUniverseSelectionModel

class SmallCapGrowthStocks(FundamentalUniverseSelectionModel):

    def __init__(self, filterFineData = True, universeSettings = None, securityInitializer = None):
        '''Initializes a new default instance of the TechnologyUniverseModule'''
        super().__init__(filterFineData, universeSettings, securityInitializer)
        self.numberOfSymbolsCoarse = 1000
        self.numberOfSymbolsFine = 100
        self.dollarVolumeBySymbol = {}
        self.symbols = []
        self.lastMonth = -1

    def SelectCoarse(self, algorithm, coarse):
        '''
        Performs a coarse selection:
        -The stock must have fundamental data
        -The stock must have positive previous-day close price
        -The stock must have positive volume on the previous trading day
        '''
        if algorithm.Time.month == self.lastMonth:
            return self.symbols

        filtered = [x for x in coarse if (x.HasFundamentalData and x.Volume > 0 and x.Price > 0)]
        sortedByDollarVolume = sorted(filtered, key = lambda x: x.DollarVolume, reverse=True)[:self.numberOfSymbolsCoarse]

        self.symbols.clear()
        self.dollarVolumeBySymbol.clear()
        for x in sortedByDollarVolume:
            self.symbols.append(x.Symbol)
            self.dollarVolumeBySymbol[x.Symbol] = x.DollarVolume

        return self.symbols

    def SelectFine(self, algorithm, fine):
        '''
        Performs a fine selection for companies in the Morningstar Banking Sector
        '''
        if algorithm.Time.month == self.lastMonth:
            return self.symbols
        self.lastMonth = algorithm.Time.month

        # Filter stocks
        filteredFine = [x for x in fine if x.AssetClassification.StyleBox == StyleBox.SmallGrowth]

        sortedByDollarVolume = []

        # Sort stocks on dollar volume
        sortedByDollarVolume = sorted(filteredFine, key = lambda x: self.dollarVolumeBySymbol[x.Symbol], reverse=True)

        self.symbols = [x.Symbol for x in sortedByDollarVolume[:self.numberOfSymbolsFine]]

        return self.symbols
