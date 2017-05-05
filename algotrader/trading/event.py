import abc

from rx import Observer
from rx.subjects import Subject

from algotrader import Startable
from algotrader.model.market_data_pb2 import Bar, Quote, Trade, MarketDepth
from algotrader.model.model_helper import ModelHelper
from algotrader.model.trade_data_pb2 import NewOrderRequest, OrderCancelRequest, OrderReplaceRequest, OrderStatusUpdate, \
    ExecutionReport, AccountUpdate, PortfolioUpdate
from algotrader.utils.logging import logger


class EventBus(object):
    def __init__(self):
        self.data_subject = Subject()
        self.order_subject = Subject()
        self.execution_subject = Subject()
        self.portfolio_subject = Subject()
        self.account_subject = Subject()


class EventHandler(Observer):
    __metaclass__ = abc.ABCMeta

    def on_next(self, event) -> None:
        if isinstance(event, (Bar, Quote, Trade, MarketDepth)):
            self.on_market_data_event(event)

        elif isinstance(event, (NewOrderRequest, OrderCancelRequest, OrderReplaceRequest)):
            self.on_order_event(event)

        elif isinstance(event, (OrderStatusUpdate, ExecutionReport)):
            self.on_execution_event(event)

        elif isinstance(event, (AccountUpdate)):
            self.on_account_event(event)

        elif isinstance(event, (PortfolioUpdate)):
            self.on_portfolio_event(event)

        else:
            raise AttributeError()

    def on_error(self, err):
        logger.debug("[%s] Error: %s" % (self.__class__.__name__, err))

    def on_completed(self):
        logger.debug("[%s] Completed" % self.__class__.__name__)

    def _start(self, app_context):
        pass

    def _stop(self):
        pass

    def on_market_data_event(self, event) -> None:
        pass

    def on_order_event(self, event) -> None:
        pass

    def on_execution_event(self, event) -> None:
        pass

    def on_account_event(self, event) -> None:
        pass

    def on_portfolio_event(self, event) -> None:
        pass


class MarketDataEventHandler(EventHandler):
    __metaclass__ = abc.ABCMeta

    def on_market_data_event(self, event) -> None:
        if isinstance(event, Bar):
            self.on_bar(event)
        elif isinstance(event, Quote):
            self.on_quote(event)
        elif isinstance(event, Trade):
            self.on_trade(event)
        elif isinstance(event, MarketDepth):
            self.on_market_depth(event)
        else:
            raise AttributeError()

    def on_bar(self, bar: Bar) -> None:
        logger.debug("[%s] %s" % (self.__class__.__name__, bar))

    def on_quote(self, quote: Quote) -> None:
        logger.debug("[%s] %s" % (self.__class__.__name__, quote))

    def on_trade(self, trade: Trade) -> None:
        logger.debug("[%s] %s" % (self.__class__.__name__, trade))

    def on_market_depth(self, market_depth: MarketDepth) -> None:
        logger.debug("[%s] %s" % (self.__class__.__name__, market_depth))


class OrderEventHandler(EventHandler):
    __metaclass__ = abc.ABCMeta

    def on_order_event(self, event) -> None:
        if isinstance(event, NewOrderRequest):
            self.on_new_ord_req(event)
        elif isinstance(event, OrderCancelRequest):
            self.on_ord_cancel_req(event)
        elif isinstance(event, OrderReplaceRequest):
            self.on_ord_replace_req(event)
        else:
            raise AttributeError()

    # Sync interface, return Order
    def send_order(self, new_ord_req: NewOrderRequest) -> None:
        raise NotImplementedError()

    # Sync interface, return Order
    def cancel_order(self, ord_cancel_req: OrderCancelRequest) -> None:
        raise NotImplementedError()

    # Sync interface, return Order
    def replace_order(self, ord_replace_req: OrderReplaceRequest) -> None:
        raise NotImplementedError()

    # Async interface
    def on_new_ord_req(self, new_ord_req: NewOrderRequest) -> None:
        logger.debug("[%s] %s" % (self.__class__.__name__, new_ord_req))
        self.send_order(new_ord_req)

    # Async interface
    def on_ord_replace_req(self, ord_replace_req: OrderReplaceRequest) -> None:
        logger.debug("[%s] %s" % (self.__class__.__name__, ord_replace_req))
        self.replace_order(ord_replace_req)

    # Async interface
    def on_ord_cancel_req(self, ord_cancel_req: OrderCancelRequest) -> None:
        logger.debug("[%s] %s" % (self.__class__.__name__, ord_cancel_req))
        self.cancel_order(ord_cancel_req)


class ExecutionEventHandler(EventHandler):
    __metaclass__ = abc.ABCMeta

    def on_execution_event(self, event) -> None:
        if isinstance(event, OrderStatusUpdate):
            self.on_ord_upd(event)
        elif isinstance(event, ExecutionReport):
            self.on_exec_report(event)
        else:
            raise AttributeError()

    def on_ord_upd(self, ord_upd: OrderStatusUpdate) -> None:
        logger.debug("[%s] %s" % (self.__class__.__name__, ord_upd))

    def on_exec_report(self, exec_report: ExecutionReport) -> None:
        logger.debug("[%s] %s" % (self.__class__.__name__, exec_report))


class AccountEventHandler(EventHandler):
    __metaclass__ = abc.ABCMeta

    def on_account_event(self, event) -> None:
        if isinstance(event, AccountUpdate):
            self.on_acc_upd(event)
        else:
            raise AttributeError()

    def on_acc_upd(self, acc_upd: AccountUpdate) -> None:
        logger.debug("[%s] %s" % (self.__class__.__name__, acc_upd))


class PortfolioEventHandler(EventHandler):
    __metaclass__ = abc.ABCMeta

    def on_portfolio_event(self, event) -> None:
        if isinstance(event, PortfolioUpdate):
            self.on_portf_upd(event)
        else:
            raise AttributeError()

    def on_portf_upd(self, portf_upd: PortfolioUpdate) -> None:
        logger.debug("[%s] %s" % (self.__class__.__name__, portf_upd))


class EventLogger(ExecutionEventHandler, MarketDataEventHandler, OrderEventHandler, PortfolioEventHandler,
                  AccountEventHandler, Startable):
    def __init__(self):
        from collections import Counter
        self.count = Counter()
        self.last_item = {}

    def _start(self, app_context):
        self.data_subject = app_context.event_bus.data_subject
        self.execution_subject = app_context.event_bus.execution_subject
        self.data_subject.subscribe(self.on_market_data_event)
        self.execution_subject.subscribe(self.on_execution_event)

    def log(self, item) -> None:
        logger.info(ModelHelper.model_to_str(item))
        self.count[type(item)] += 1
        self.last_item[type(item)] = item

    def on_bar(self, bar: Bar) -> None:
        self.log(bar)

    def on_quote(self, quote: Quote) -> None:
        self.log(quote)

    def on_trade(self, trade: Trade) -> None:
        self.log(trade)

    def on_market_depth(self, market_depth: MarketDepth) -> None:
        self.log(market_depth)

    def on_new_ord_req(self, new_ord_req: NewOrderRequest) -> None:
        self.log(new_ord_req)

    def on_ord_replace_req(self, ord_replace_req: OrderReplaceRequest) -> None:
        self.log(ord_replace_req)

    def on_ord_cancel_req(self, ord_cancel_req: OrderCancelRequest) -> None:
        self.log(ord_cancel_req)

    def on_ord_upd(self, ord_upd: OrderStatusUpdate) -> None:
        self.log(ord_upd)

    def on_exec_report(self, exec_report: ExecutionReport) -> None:
        self.log(exec_report)

    def on_acc_upd(self, acc_upd: AccountUpdate) -> None:
        self.log(acc_upd)

    def on_portf_upd(self, portf_upd: PortfolioUpdate) -> None:
        self.log(portf_upd)
