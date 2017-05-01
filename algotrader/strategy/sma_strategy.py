from algotrader.model.trade_data_pb2 import *
from algotrader.technical.ma import SMA
from algotrader.trading.strategy import Strategy
from algotrader.utils import logger
from algotrader.trading.context import ApplicationContext


class SMAStrategy(Strategy):

    def __init__(self, stg_id: str, state: StrategyState = None):
        super(SMAStrategy, self).__init__(stg_id=stg_id, state=state)
        self.buy_order = None

    def _start(self, app_context: ApplicationContext, **kwargs):
        self.qty = app_context.app_config.get("Strategy", self.state.stg_id, "qty", default=1)
        self.bar = self.app_context.inst_data_mgr.get_series(
            "Bar.%s.Time.86400" % app_context.app_config.get("Application", "instrumentIds")[0])

        self.sma_fast = SMA(self.bar, 'close', 10)
        self.sma_fast.start(app_context)

        self.sma_slow = SMA(self.bar, 'close', 25)
        self.sma_slow.start(app_context)

        super(SMAStrategy, self)._start(app_context, **kwargs)

    def _stop(self):
        super(SMAStrategy, self)._stop()

    def on_bar(self, bar):
        if self.buy_order is None and self.sma_fast.now('value') > self.sma_slow.now('value'):
            self.buy_order = self.market_order(inst_id=bar.inst_id, action=Buy, qty=self.qty)
            logger.info("%s,B,%s,%s,%.2f,%.2f,%.2f" % (
                bar.timestamp, self.buy_order.cl_id, self.buy_order.cl_ord_id, bar.close, self.sma_fast.now('value'),
                self.sma_slow.now('value')))
        elif self.buy_order is not None and self.sma_fast.now('value') < self.sma_slow.now('value'):
            sell_order = self.market_order(inst_id=bar.inst_id, action=Sell, qty=self.qty)
            logger.info("%s,S,%s,%s,%.2f,%.2f,%.2f" % (
                bar.timestamp, sell_order.cl_id, sell_order.cl_ord_id, bar.close, self.sma_fast.now('value'),
                self.sma_slow.now('value')))
            self.buy_order = None
