from algotrader.model.trading.analyzer.performance import PerformanceAnalyzer
from algotrader.model.trading.time_series import PandasTimeSeries


class PnlAnalyzer(object):
    Pnl = "Pnl"

    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.state = portfolio.state.pnl
        self.series = PandasTimeSeries(self.portfolio.state.pnl.series)

    def update(self, timestamp: int, current_value: float):
        performance_series = self.portfolio.performance.performance_series

        if self.series.size() >= 2:
            self.state.pnl = performance_series.get_by_idx(-1, PerformanceAnalyzer.TotalEquity) - \
                             self.portfolio.performance_series.get_by_idx(-2, PerformanceAnalyzer.TotalEquity)

            self.series.add(data={self.Pnl: self.state.pnl}, timestamp=timestamp)

    def get_result(self):
        return {self.Pnl: self.state.pnl}

    def get_series(self, keys=None):
        keys = keys if keys else self.Pnl
        return {self.Pnl: self.series.get_series(self.Pnl)}
