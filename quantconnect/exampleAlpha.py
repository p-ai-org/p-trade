''' this alpha generates a positive insight
based on how early a stock's ticker is in the alphabet.'''

from clr import AddReference
AddReference("QuantConnect.Common")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Algorithm.Framework")

from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Algorithm.Framework import *
from QuantConnect.Algorithm.Framework.Alphas import AlphaModel, Insight, InsightType, InsightDirection

class ExampleAlphaModel(AlphaModel):
    ''' Provides an implementation of AlphaModel that
    returns insight based on the alphabetic value of the security symbols'''

    def __init__(self, **kwargs):
        '''Initializes a new instance of the ConstantAlphaModel class'''
        self.insightsTimeBySymbol = {}
        self.securities = []

    def Update(self, algorithm, changes):
        ''' Creates an insight for each security based on the alphabetical
        value of its symbol
        Returns:
            The new insights generated'''

        algorithm.Debug('update: ' + str(changes))

        insights = []

        for security in self.securities:
            first_letter = str(security.Symbol)[0]
            second_letter = str(security.Symbol)[1]

            # insight parameters based on symbol letters
            direction = InsightDirection.Up if ord(first_letter) > ord('M') else InsightDirection.Down
            magnitude = float(ord(first_letter)) / float(ord('Z'))
            confidence = float(ord(second_letter)) / float(ord('Z'))

            insight = Insight(
                security.Symbol,
                timedelta(minutes=10),
                InsightType.Price,
                direction,
                magnitude,
                confidence,
            )
            #self.EmitInsights(insight)
            insights.append(insight)

        return insights


    def OnSecuritiesChanged(self, algorithm, changes):
        #Event fired each time the we add/remove securities from the data feed
        #Args:
        #    algorithm: The algorithm instance that experienced the change in securities
        #    changes: The security additions and removals from the algorithm

        for added in changes.AddedSecurities:
            algorithm.Debug("to add: " + str(type(added)) + ' ' + str(added))
            self.securities.append(added)

        # this will allow the insight to be re-sent when the security re-joins the universe
        for removed in changes.RemovedSecurities:
            if removed in self.securities:
                self.securities.remove(removed)
            if removed.Symbol in self.insightsTimeBySymbol:
                self.insightsTimeBySymbol.pop(removed.Symbol)

        pass
