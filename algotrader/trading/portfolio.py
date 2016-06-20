from algotrader.event.event_bus import EventBus
from algotrader.event.market_data import MarketDataEventHandler
from algotrader.event.order import OrdAction, OrderEventHandler, ExecutionEventHandler
from algotrader.performance.drawdown import DrawDown
from algotrader.performance.returns import Pnl
from algotrader.utils import logger
from algotrader.utils.time_series import DataSeries


class Position(object):
    def __init__(self, inst_id):
        self.inst_id = inst_id
        self.orders = {}
        self.size = 0
        self.last_price = 0

    def add_order(self, order):
        if order.inst_id != self.inst_id:
            raise RuntimeError("order[%s] inst_id [%s] is not same as inst_id [%s] of position" % (
                order.ord_id, order.inst_id, self.inst_id))

        if order.ord_id in self.orders:
            raise RuntimeError("order[%s] already exist" % order.ord_id)
        self.orders[order.ord_id] = order
        self.size += order.qty if order.action == OrdAction.BUY else -order.qty

    def filled_qty(self):
        qty = 0
        for key, order in self.orders.iteritems():
            qty += order.filled_qty if order.action == OrdAction.BUY else -order.filled_qty
        return qty

    def __repr__(self):
        return "Position(inst_id=%s, orders=%s, size=%s, last_price=%s)" % (
            self.inst_id, self.orders, self.size, self.last_price
        )


class Portfolio(OrderEventHandler, ExecutionEventHandler, MarketDataEventHandler):
    def __init__(self, portfolio_id="test", cash=1000000, analyzers=None):
        self.portfolio_id = portfolio_id
        self.positions = {}
        self.orders = {}

        self.performance_series = DataSeries()

        self.total_equity = 0
        self.cash = cash
        self.stock_value = 0

        self.analyzers = analyzers if analyzers is not None else [Pnl(), DrawDown()]
        for analyzer in self.analyzers:
            analyzer.set_portfolio(self)

    def start(self):
        EventBus.data_subject.subscribe(self.on_next)

    def on_bar(self, bar):
        logger.debug("[%s] %s" % (self.__class__.__name__, bar))
        self.__update_price(bar.timestamp, bar.inst_id, bar.close)

    def on_quote(self, quote):
        logger.debug("[%s] %s" % (self.__class__.__name__, quote))
        self.__update_price(quote.timestamp, quote.inst_id, quote.mid())

    def on_trade(self, trade):
        logger.debug("[%s] %s" % (self.__class__.__name__, trade))
        self.__update_price(trade.timestamp, trade.inst_id, trade.price)

    def on_order(self, order):
        logger.debug("[%s] %s" % (self.__class__.__name__, order))

        if order.ord_id in self.orders:
            raise RuntimeError("order[%s] already exist" % order.ord_id)

        self.orders[order.ord_id] = order
        if order.inst_id not in self.positions:
            self.positions[order.inst_id] = Position(inst_id=order.inst_id)
        self.positions[order.inst_id].add_order(order)

    def on_ord_upd(self, ord_upd):
        logger.debug("[%s] %s" % (self.__class__.__name__, ord_upd))
        order = self.orders[ord_upd.ord_id]
        order.update_status(ord_upd)

    def on_exec_report(self, exec_report):
        logger.debug("[%s] %s" % (self.__class__.__name__, exec_report))
        order = self.orders[exec_report.ord_id]
        order.add_exec_report(exec_report)
        direction = 1 if order.action == OrdAction.BUY else -1
        self.cash -= (direction * exec_report.last_qty * exec_report.last_price + exec_report.commission)
        self.__update_price(exec_report.timestamp, exec_report.inst_id, exec_report.last_price)

    def __update_price(self, time, inst_id, price):
        if inst_id in self.positions:
            position = self.positions[inst_id]
            position.last_price = price
        self.__update_equity(time)
        for analyzer in self.analyzers:
            analyzer.update(time)

    def __update_equity(self, time):
        self.stock_value = 0
        for position in self.positions.itervalues():
            self.stock_value += position.last_price * position.filled_qty()
        self.total_equity = self.stock_value + self.cash

        self.performance_series.add(
            {"timestamp": time, "stock_value": self.stock_value, "cash": self.cash, "total_equity": self.total_equity})

    def get_return(self):
        equity = self.performance_series.get_series("total_equity")
        equity.name = 'equity'
        rets = equity.pct_change().dropna()
        rets.index = rets.index.tz_localize("UTC")
        return rets

    def get_series(self):
        result = self.performance_series.get_series(['stock_value', 'cash', 'total_equity'])

        for analyzer in self.analyzers:
            result.update(analyzer.get_series())
        return result

    def get_result(self):
        result = {
            "TotalEquity": self.total_equity,
            "Cash": self.cash,
            "StockValue": self.stock_value
        }

        for analyzer in self.analyzers:
            result.update(analyzer.get_result())
        return result
