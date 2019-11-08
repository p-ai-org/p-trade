# can uncomment these when running in qc
#from CboeVixAlphaModel import CboeVixAlphaModel
#from Alphas.RsiAlphaModel import RsiAlphaModel
#from Execution.VolumeWeightedAveragePriceExecutionModel import VolumeWeightedAveragePriceExecutionModel
#from SmallCapGrowthStocks import SmallCapGrowthStocks

class ModulatedResistanceRegulators(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 4, 17)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.AddEquity("SPY", Resolution.Hour)

        #self.AddAlpha(CboeVixAlphaModel(self))
        #self.AddAlpha(RsiAlphaModel(60, Resolution.Minute))
        #self.SetExecution(VolumeWeightedAveragePriceExecutionModel())
        #self.SetPortfolioConstruction(InsightWeightingPortfolioConstructionModel())
        #self.SetRiskManagement(MaximumDrawdownPercentPortfolio(0.03))
        #self.SetUniverseSelection(SmallCapGrowthStocks())

    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data'''

        if not self.Portfolio.Invested:
            self.SetHoldings("SPY", 1)
