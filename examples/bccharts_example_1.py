# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

import datetime

from mooquant import bar
from mooquant.provider.bitcoincharts import barfeed
from mooquant.tools import resample


def main():
    barFeed = barfeed.CSVTradeFeed()
    barFeed.addBarsFromCSV("data/bitstampUSD.csv", fromDateTime=datetime.datetime(2014, 1, 1))
    resample.resample_to_csv(barFeed, bar.Frequency.MINUTE * 30, "data/30min-bitstampUSD-2.csv")


if __name__ == "__main__":
    main()
