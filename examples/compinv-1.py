# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

from mooquant import strategy
from mooquant.barfeed import yahoofeed
from mooquant.analyzer import returns, sharpe
from mooquant.utils import stats


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed):
        strategy.BacktestingStrategy.__init__(self, feed, 1000000)

        # We wan't to use adjusted close prices instead of close.
        self.setUseAdjustedValues(True)

        # Place the orders to get them processed on the first bar.
        orders = {
            "aeti": 297810,
            "egan": 81266,
            "glng": 11095,
            "simo": 17293,
        }
        for instrument, quantity in orders.iteritems():
            self.marketOrder(instrument, quantity, onClose=True, allOrNone=True)

    def onBars(self, bars):
        pass

# Load the yahoo feed from CSV files.
feed = yahoofeed.Feed()
feed.addBarsFromCSV("aeti", "data/aeti-2011-yahoofinance.csv")
feed.addBarsFromCSV("egan", "data/egan-2011-yahoofinance.csv")
feed.addBarsFromCSV("glng", "data/glng-2011-yahoofinance.csv")
feed.addBarsFromCSV("simo", "data/simo-2011-yahoofinance.csv")

# Evaluate the strategy with the feed's bars.
strat = MyStrategy(feed)

# Attach returns and sharpe ratio analyzers.
retAnalyzer = returns.Returns()
strat.attachAnalyzer(retAnalyzer)
sharpeRatioAnalyzer = sharpe.SharpeRatio()

strat.attachAnalyzer(sharpeRatioAnalyzer)
strat.run()

# Print the results.
print ("Final portfolio value: $%.2f" % strat.getResult())
print ("Anual return: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
print ("Average daily return: %.2f %%" % (stats.mean(retAnalyzer.getReturns()) * 100))
print ("Std. dev. daily return: %.4f" % (stats.stddev(retAnalyzer.getReturns())))
print ("Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0)))
