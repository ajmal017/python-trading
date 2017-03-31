from algotrader.trading.analyzer import Analyzer
from algotrader.trading.data_series import DataSeries


class PerformanceAnalyzer(Analyzer):
    Performance = "Performance"
    StockValue = "stock_value"
    Cash = "cash"
    TotalEquity = "total_equity"

    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.state = self.portfolio.state
        self.performance = self.portfolio.state.performance
        self.series = DataSeries(self.performance.series)

    def update(self, timestamp: int, total_equity: float):
        self.performance.total_equity = total_equity
        self.series.add(
            data={self.StockValue: self.state.stock_value,
                  self.Cash: self.state.cash,
                  self.TotalEquity: total_equity},
            timestamp=timestamp)

    def get_result(self):
        return {self.StockValue: self.state.stock_value,
                self.Cash: self.state.cash,
                self.TotalEquity: self.performance.total_equity}

    def get_series(self, keys=None):
        keys = keys if keys else [self.StockValue, self.Cash, self.TotalEquity]
        return self.series.get_series(keys)


    def now(self, key):
        return self.series.now(key)