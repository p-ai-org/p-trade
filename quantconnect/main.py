from CboeVixAlphaModel import CboeVixAlphaModel
from Alphas.RsiAlphaModel import RsiAlphaModel
from Execution.VolumeWeightedAveragePriceExecutionModel import VolumeWeightedAveragePriceExecutionModel
from SmallCapGrowthStocks import SmallCapGrowthStocks
from exampleAlpha import ExampleAlphaModel as ExampleAlpha

class MainAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 8, 17)  # Set Start Date
        #self.SetBenchmark("SPY")

        spy = Symbol.Create("SPY", SecurityType.Equity, Market.USA)
        fb = Symbol.Create("FB", SecurityType.Equity, Market.USA)
        self.SetUniverseSelection(ManualUniverseSelectionModel([spy, fb]))
        self.SetAlpha(ExampleAlpha())

        #self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
        #self.SetExecution(ImmediateExecutionModel())


    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data'''

        if not self.Portfolio.Invested:
            self.SetHoldings("SPY", 1)
