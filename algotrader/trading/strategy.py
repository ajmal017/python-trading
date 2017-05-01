from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from algotrader import Startable
from builtins import *
from typing import Dict

from algotrader.config.app import BacktestingConfig
from algotrader.event.event_bus import EventBus
from algotrader.event.event_handler import MarketDataEventHandler, ExecutionEventHandler
from algotrader.model.market_data_pb2 import *
from algotrader.model.trade_data_pb2 import *
from algotrader.provider.subscription import SubscriptionKey, HistDataSubscriptionKey, MarketDataSubscriber
from algotrader.trading.position import HasPositions
from algotrader.model.model_factory import ModelFactory

class Strategy(HasPositions, ExecutionEventHandler, MarketDataSubscriber):
    def __init__(self, stg_id: str, state: StrategyState = None):
        self.state = state if state else ModelFactory.build_strategy_state(stg_id=stg_id)
        super().__init__(self.state)

    def __get_next_req_id(self):
        id = self.state.next_ord_id if self.state.next_ord_id else 1
        self.state.next_ord_id = id + 1
        return id

    def get_stg_config_value(self, key, default_value=None):
        if self.state.config and self.state.config.values:
            return self.state.config.values.get(key, default_value)
        return default_value

    def _start(self, app_context, **kwargs):
        self.app_context.stg_mgr.add(self)
        self.model_factory = self.app_context.model_factory
        self.app_config = self.app_context.app_config
        self.ord_reqs ={}

        # TODO
        self.config = None

        self.ref_data_mgr = self.app_context.ref_data_mgr
        self.portfolio = self.app_context.portf_mgr.get(self.app_config.portfolio_id)
        self.feed = self.app_context.provider_mgr.get(self.app_config.feed_id) if self.app_config else None
        self.broker = self.app_context.provider_mgr.get(self.app_config.broker_id)

        self.instruments = self.ref_data_mgr.get_insts_by_ids(self.app_context.app_config.instrument_ids)
        self.clock = self.app_context.clock
        self.event_subscription = EventBus.data_subject.subscribe(self.on_next)

        for order_req in self.app_context.order_mgr.get_strategy_order_reqs(self.id()):
            self.ord_reqs[order_req.cl_ord_id] = order_req

        if self.portfolio:
            self.portfolio.start(app_context)

        if self.broker:
            self.broker.start(app_context)

        if self.feed:
            self.feed.start(app_context)

        if isinstance(self.app_config, BacktestingConfig):
            self.subscript_market_data(self.feed, self.instruments, self.app_config.subscription_types,
                                       self.app_config.from_date, self.app_config.to_date)
        else:
            self.subscript_market_data(self.feed, self.instruments, self.app_config.subscription_types)

    def _stop(self):
        if self.event_subscription:
            self.event_subscription.dispose()

    def _subscribe_market_data(self, feed, instruments, subscription_types):
        for instrument in instruments:
            for subscription_type in subscription_types:
                if isinstance(self.app_config, BacktestingConfig):

                    sub_key = HistDataSubscriptionKey(inst_id=instrument.inst_id,
                                                      provider_id=self.app_config.feed_id,
                                                      subscription_type=subscription_type,
                                                      from_date=self.app_config.from_date,
                                                      to_date=self.app_config.to_date)

                else:
                    sub_key = SubscriptionKey(inst_id=instrument.inst_id,
                                              provider_id=self.app_config.feed_id,
                                              subscription_type=subscription_type)
                self.feed.subscribe_mktdata(sub_key)

    def id(self):
        return self.state.stg_id

    def on_bar(self, bar: Bar):
        super().on_bar(bar)

    def on_quote(self, quote: Quote):
        super().on_quote(quote)

    def on_trade(self, trade: Trade):
        super().on_trade(trade)

    def on_market_depth(self, market_depth: MarketDepth):
        super().on_market_depth(market_depth)

    def on_ord_upd(self, ord_upd: OrderStatusUpdate):
        if ord_upd.cl_id == self.state.stg_id:
            super().on_ord_upd(ord_upd)

    def on_exec_report(self, exec_report: ExecutionReport):
        if exec_report.cl_id == self.state.stg_id:
            super().on_exec_report(exec_report)
            ord_req = self.ord_reqs[exec_report.cl_ord_id]
            direction = 1 if ord_req.action == Buy else -1
            if exec_report.last_qty > 0:
                self.add_position(exec_report.inst_id, exec_report.cl_id, exec_report.cl_ord_id,
                                  direction * exec_report.last_qty)
                self.update_price(exec_report.timestamp, exec_report.inst_id, exec_report.last_price)

    def market_order(self, inst_id, action, qty, tif=DAY, oca_tag=None, params=None):
        return self.new_order(inst_id=inst_id, action=action, type=Market, qty=qty, limit_price=0.0, tif=tif,
                              oca_tag=oca_tag, params=params)

    def limit_order(self, inst_id, action, qty, price, tif=DAY, oca_tag=None, params=None):
        return self.new_order(inst_id=inst_id, action=action, type=Limit, qty=qty, limit_price=price, tif=tif,
                              oca_tag=oca_tag, params=params)

    def stop_order(self):
        # TODO
        pass

    def stop_limit_order(self):
        # TODO
        pass

    def close_position(self, inst_id: str):
        # TODO
        pass

    def close_all_positions(self):
        # TODO
        pass

    def new_order(self,
                  inst_id: str, action: OrderAction, type: OrderType,
                  qty: float, limit_price: float = 0,
                  stop_price: float = 0, tif: TIF = DAY, oca_tag: str = None,
                  params: Dict[str, str] = None) -> NewOrderRequest:

        req = self.model_factory.build_new_order_request(timestamp=self.clock.now(),
                                                         cl_id=self.state.stg_id,
                                                         cl_ord_id=self.__get_next_req_id(),
                                                         portf_id=self.portfolio.state.portf_id,
                                                         broker_id=self.app_config.broker_id,
                                                         inst_id=inst_id,
                                                         action=action,
                                                         type=type,
                                                         qty=qty,
                                                         limit_price=limit_price,
                                                         stop_price=stop_price,
                                                         tif=tif,
                                                         oca_tag=oca_tag,
                                                         params=params)
        self.ord_reqs[req.cl_ord_id] = req
        self.add_order(inst_id=req.inst_id, cl_id=req.cl_id, cl_ord_id=req.cl_ord_id, ordered_qty=req.qty)
        self.portfolio.send_order(req)
        return req

    def cancel_order(self, cl_orig_req_id: str, params: Dict[str, str] = None) -> OrderCancelRequest:
        req = self.model_factory.build_order_cancel_request(timestamp=self.clock.now(),
                                                            cl_id=self.state.stg_id, cl_ord_id=self.__get_next_req_id(),
                                                            cl_orig_req_id=cl_orig_req_id, params=params)
        self.ord_reqs[req.cl_ord_id] = req
        self.portfolio.cancel_order(req)
        return req

    def replace_order(self, cl_orig_req_id: str, type: OrderType = None, qty: float = None, limit_price: float = None,
                      stop_price: float = None, tif: TIF = None, oca_tag: str = None,
                      params: Dict[str, str] = None) -> OrderReplaceRequest:
        req = self.model_factory.build_order_replace_request(timestamp=self.clock.now(),
                                                             cl_id=self.state.stg_id, cl_ord_id=self.__get_next_req_id(),
                                                             cl_orig_req_id=cl_orig_req_id, type=type, qty=qty,
                                                             limit_price=limit_price,
                                                             stop_price=stop_price, tif=tif,
                                                             oca_tag=oca_tag,
                                                             params=params)
        self.ord_reqs[req.cl_ord_id] = req
        self.portfolio.replace_order(req)
        return req

    def get_portfolio(self):
        return self.portfolio

    def portf_id(self) -> str:
        if not self.state:
            return None
        return self.state.portf_id
