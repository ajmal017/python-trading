from typing import Dict, List, Union

from algotrader.model.market_data_pb2 import *
from algotrader.model.model_helper import ModelHelper
from algotrader.model.ref_data_pb2 import *
from algotrader.model.time_series_pb2 import *
from algotrader.model.trade_data_pb2 import *


class ModelFactory(object):
    # ref data
    def build_instrument(self, symbol: str, type: Instrument.InstType, primary_exch_id: str, ccy_id: str,
                         name: str = None, exch_ids: List[str] = None, sector: str = None, industry: str = None,
                         margin: float = None, tick_size: float = None,
                         underlying: Underlying = None, derivative: DrivativeTraits = None,
                         alt_symbols: Dict[str, str] = None, alt_ids: Dict[str, str] = None,
                         alt_sectors: Dict[str, str] = None, alt_industries: Dict[str, str] = None) -> Instrument:
        inst = Instrument()
        # inst.inst_id = 10
        inst.inst_id = symbol + '@' + primary_exch_id
        inst.symbol = symbol
        inst.name = name
        inst.type = type
        inst.primary_exch_id = primary_exch_id
        ModelHelper.add_to_list(inst.exch_ids, exch_ids)
        inst.ccy_id = ccy_id

        inst.sector = sector
        inst.industry = industry
        inst.margin = margin
        inst.tick_size = tick_size
        if underlying:
            inst.underlying.CopyFrom(underlying)
        if derivative:
            inst.derivative.CopyFrom(derivative)
        ModelHelper.add_to_dict(inst.alt_symbols, alt_symbols)
        ModelHelper.add_to_dict(inst.alt_ids, alt_ids)
        ModelHelper.add_to_dict(inst.alt_sectors, alt_sectors)
        ModelHelper.add_to_dict(inst.alt_industries, alt_industries)

        return inst

    def build_derivative_traits(self, option_type: DrivativeTraits.OptionType = None,
                                option_style: DrivativeTraits.OptionStyle = None, strike: float = None,
                                exp_date: int = None,
                                multiplier: float = None) -> DrivativeTraits:
        deriv = DrivativeTraits()
        deriv.option_type = option_type
        deriv.option_style = option_style
        deriv.strike = strike
        deriv.exp_date = exp_date
        deriv.multiplier = multiplier

        return deriv

    def build_underlying(self, type: Instrument.InstType, assets: List[Underlying.Asset]) -> Underlying:
        underlying = Underlying()
        underlying.type = type
        ModelHelper.add_to_list(underlying.assets, assets)

        return underlying

    def build_asset(self, inst_id: str, weight: float) -> Underlying.Asset:
        asset = Underlying.Asset()
        asset.inst_id = inst_id
        asset.weight = weight

        return asset

    def build_exchange(self, exch_id: str, name: str, country_id: str = None, trading_hours_id: str = None,
                       holidays_id: str = None,
                       alt_ids: Dict[str, str] = None) -> Exchange:
        exchange = Exchange()
        exchange.exch_id = exch_id
        exchange.name = name
        exchange.country_id = country_id
        exchange.trading_hours_id = trading_hours_id
        exchange.holidays_id = holidays_id
        ModelHelper.add_to_dict(exchange.alt_ids, alt_ids)
        return exchange

    def build_currency(self, ccy_id: str, name: str) -> Currency:
        currency = Currency()
        currency.ccy_id = ccy_id
        currency.name = name
        return currency

    def build_country(self, country_id: str, name: str, holidays_id: str = None) -> Country:
        country = Country()
        country.country_id = country_id
        country.name = name
        country.holidays_id = holidays_id
        return country

    def build_holiday_series(self, holidays_id, holidays) -> HolidaySeries:
        holiday_series = HolidaySeries()
        holiday_series.holidays_id = holidays_id
        ModelHelper.add_to_list(holiday_series.holidays, holidays)
        return holiday_series

    def build_holiday(self, trading_date: int, type: HolidaySeries.Holiday.Type, start_date: int, end_date: int,
                      start_time: int = None,
                      end_time: int = None,
                      desc: str = None) -> HolidaySeries.Holiday:
        holiday = HolidaySeries.Holiday()
        holiday.trading_date = trading_date
        holiday.type = type
        holiday.start_date = start_date
        holiday.end_date = end_date

        if start_time:
            holiday.start_time = start_time
        if end_time:
            holiday.end_time = end_time

        if desc:
            holiday.desc = desc
        return holiday

    def build_trading_hours(self, trading_hours_id: str, timezone_id: str,
                            sessions: List[TradingHours.Session]) -> TradingHours:
        trading_hour = TradingHours()
        trading_hour.trading_hours_id = trading_hours_id
        trading_hour.timezone_id = timezone_id
        ModelHelper.add_to_list_value(trading_hour.sessions, sessions)
        return trading_hour

    def build_trading_session(self, start_weekdate: int, start_time: int, end_weekdate: int, end_time: int,
                              eod: bool) -> TradingHours.Session:
        session = TradingHours.Session()
        session.start_weekdate = start_weekdate
        session.start_time = start_time
        session.end_weekdate = end_weekdate
        session.end_time = end_time
        session.eod = eod

        return session

    def build_timezone(self, timezone_id: str) -> TimeZone:
        timezone = TimeZone()
        timezone.timezone_id = timezone_id
        return timezone

    # time series
    def build_time_series_item(self, timestamp: int, data: Dict[str, float]) -> TimeSeries.Item:
        item = TimeSeries.Item()
        item.timestamp = timestamp
        ModelHelper.add_to_dict(item.data, data)

        return item

    def build_time_series(self, series_id: str, name: str = '', desc: str = '',
                          inputs: Union[str, List[str]] = None, keys: Union[str, List[str]] = None,
                          default_output_key: str = 'value', missing_value_replace: float = 0.0, start_time: int = 0,
                          end_time: int = 0, items: List[TimeSeries.Item] = None) -> TimeSeries:
        time_series = TimeSeries()
        time_series.series_id = series_id
        time_series.name = name
        time_series.desc = desc
        ModelHelper.add_to_list(time_series.inputs, inputs)
        ModelHelper.add_to_list(time_series.keys, keys)
        time_series.default_output_key = default_output_key
        time_series.missing_value_replace = missing_value_replace
        time_series.start_time = start_time
        time_series.end_time = end_time
        ModelHelper.add_to_list(time_series.items, items)

        return time_series

    # Market data
    def build_bar(self, inst_id: str, type: Bar.Type, size: int, provider_id: str, timestamp: int,
                  open: float, high: float, low: float, close: float, vol: float, adj_close: float = None,
                  open_interest: float = None,
                  utc_time: int = None, begin_time: int = None) -> Bar:
        bar = Bar()
        bar.inst_id = inst_id
        bar.type = type
        bar.size = size
        bar.provider_id = provider_id
        bar.timestamp = timestamp
        bar.open = open
        bar.high = high
        bar.low = low
        bar.close = close
        bar.vol = vol
        bar.adj_close = adj_close
        bar.open_interest = open_interest
        bar.utc_time = utc_time
        bar.begin_time = begin_time

        return bar

    def build_quote(self, inst_id: str, provider_id: str, timestamp: float, bid: float, bid_size: float, ask: float,
                    ask_size: float, utc_time: int = None) -> Quote:
        quote = Quote()
        quote.inst_id = inst_id
        quote.provider_id = provider_id
        quote.timestamp = timestamp
        quote.utc_time = utc_time
        quote.bid = bid
        quote.bid_size = bid_size
        quote.ask = ask
        quote.ask_size = ask_size

        return quote

    def build_trade(self, inst_id: str, provider_id: str, timestamp: int, price: float, size: float,
                    utc_time: int = None) -> Trade:
        trade = Trade()
        trade.inst_id = inst_id
        trade.provider_id = provider_id
        trade.timestamp = timestamp
        trade.price = price
        trade.size = size
        trade.utc_time = utc_time

        return trade

    def build_market_depth(self, inst_id: str, provider_id: str, timestamp: int, md_provider: str, position: int,
                           operation: MarketDepth.Operation, side: MarketDepth.Side, price: float, size: float,
                           utc_time: int = None) -> MarketDepth:
        md = MarketDepth()
        md.inst_id = inst_id
        md.provider_id = provider_id
        md.timestamp = timestamp
        md.md_provider = md_provider
        md.position = position
        md.operation = operation
        md.side = side
        md.price = price
        md.size = size
        md.utc_time = utc_time
        return md

    # trade data
    def build_new_order_request(self, timestamp: int, cl_id: str, cl_req_id: str, portf_id: str, broker_id: str,
                                inst_id: str,
                                action: OrderAction, type: OrderType, qty: float, limit_price: float,
                                stop_price: float = 0.0,
                                tif: TIF = DAY, oca_tag: str = None,
                                params: Dict[str, str] = None) -> NewOrderRequest:
        req = NewOrderRequest()

        req.timestamp = timestamp
        req.cl_id = cl_id
        req.cl_req_id = cl_req_id
        req.portf_id = portf_id
        req.broker_id = broker_id
        req.inst_id = inst_id
        req.action = action
        req.type = type
        req.qty = qty
        req.limit_price = limit_price
        req.stop_price = stop_price
        req.tif = tif
        if oca_tag:
            req.oca_tag = oca_tag
        ModelHelper.add_to_dict(req.params, params)

        return req

    def build_order_replace_request(self, timestamp: int, cl_id: str, cl_req_id: str, cl_orig_req_id: str,
                                    type: OrderType, qty: float,
                                    limit_price: float, stop_price: float = None,
                                    tif: TIF = DAY, oca_tag: str = None,
                                    params: Dict[str, str] = None) -> OrderReplaceRequest:
        req = OrderReplaceRequest()

        req.timestamp = timestamp
        req.cl_id = cl_id
        req.cl_req_id = cl_req_id
        req.cl_orig_req_id = cl_orig_req_id
        req.type = type
        req.qty = qty
        req.limit_price = limit_price
        req.stop_price = stop_price
        req.tif = tif
        req.oca_tag = oca_tag
        ModelHelper.add_to_dict(req.params, params)

        return req

    def build_order_cancel_request(self, timestamp: int, cl_id: str, cl_req_id: str, cl_orig_req_id: str,
                                   params: Dict[str, str] = None) -> OrderCancelRequest:
        req = OrderCancelRequest()
        req.timestamp = timestamp
        req.cl_id = cl_id
        req.cl_req_id = cl_req_id
        req.cl_orig_req_id = cl_orig_req_id
        ModelHelper.add_to_dict(req.params, params)

        return req

    def build_order_status_update(self, timestamp: int, broker_id: str, broker_event_id: str, broker_ord_id: str,
                                  cl_id: str,
                                  cl_req_id: str, inst_id: str, filled_qty: float, avg_price: float,
                                  status: OrderStatus) -> OrderStatusUpdate:
        event = OrderStatusUpdate()
        event.timestamp = timestamp
        event.broker_id = broker_id
        event.broker_event_id = broker_event_id
        event.broker_ord_id = broker_ord_id
        event.cl_id = cl_id
        event.cl_req_id = cl_req_id
        event.inst_id = inst_id
        event.filled_qty = filled_qty
        event.avg_price = avg_price
        event.status = status

        return event

    def build_execution_report(self, timestamp: int, broker_id: str, broker_event_id: str, broker_ord_id: str,
                               broker_er_id: str,
                               cl_id: str,
                               cl_req_id: str, inst_id: str, last_qty: float, last_price: float, commission: float,
                               filled_qty: float, avg_price: float,
                               status: OrderStatus) -> ExecutionReport:
        event = ExecutionReport()
        event.timestamp = timestamp
        event.broker_id = broker_id
        event.broker_event_id = broker_event_id
        event.broker_ord_id = broker_ord_id
        event.broker_er_id = broker_er_id
        event.cl_id = cl_id
        event.cl_req_id = cl_req_id
        event.inst_id = inst_id
        event.last_price = last_price
        event.last_price = last_price
        event.commission = commission
        event.filled_qty = filled_qty
        event.avg_price = avg_price
        event.status = status

        return event

    def build_account_value(self, key: str, ccy_values: Dict[str, float]) -> AccountValue:
        value = AccountValue()
        value.key = key
        ModelHelper.add_to_dict(value.ccy_values, ccy_values)
        return value

    def build_account_update(self, timestamp: int, broker_id: str, broker_event_id: str, account_name,
                             values: AccountValue) -> AccountUpdate:
        event = AccountUpdate()

        event.timestamp = timestamp
        event.broker_id = broker_id
        event.broker_event_id = broker_event_id
        event.account_name = account_name
        ModelHelper.add_to_dict_value(event.values, values)

        return event

    def build_portfolio_update(self, timestamp: int, broker_id: str, broker_event_id: str, portf_id: str, inst_id: str,
                               position: float, mkt_price: float, mkt_value: float, avg_cost: float,
                               unrealized_pnl: float, realized_pnl: float) -> PortfolioUpdate:
        event = PortfolioUpdate()

        event.timestamp = timestamp
        event.broker_id = broker_id
        event.broker_event_id = broker_event_id
        event.portf_id = portf_id
        event.inst_id = inst_id
        event.position = position
        event.mkt_price = mkt_price
        event.mkt_value = mkt_value
        event.avg_cost = avg_cost
        event.unrealized_pnl = unrealized_pnl
        event.realized_pnl = realized_pnl

        return event

    def build_account_state(self, acct_id: str, values: Dict[str, AccountValue] = None,
                            positions: Dict[str, Position] = None) -> AccountState:
        account = AccountState()

        account.acct_id = acct_id
        ModelHelper.add_to_dict_value(account.values, values)
        ModelHelper.add_to_dict_value(account.positions, positions)

        return account

    def build_portfolio_state(self, portf_id: str, cash: float, positions: Dict[str, Position] = None,
                              performance: Performance = None,
                              pnl: Pnl = None, drawdown: DrawDown = None) -> PortfolioState:
        portfolio = PortfolioState()
        portfolio.portf_id = portf_id
        portfolio.cash = cash
        ModelHelper.add_to_dict_value(portfolio.positions, positions)
        portfolio.performance.CopyFrom(performance if performance else Performance())
        portfolio.pnl.CopyFrom(pnl if pnl else Pnl())
        portfolio.drawdown.CopyFrom(drawdown if drawdown else DrawDown())

        return portfolio

    def build_performance(self, total_equity: float, stock_value: float,
                          performance_series: TimeSeries = None) -> Performance:
        performance = Performance()
        performance.total_equity = total_equity
        performance.stock_value = stock_value
        performance.series.CopyFrom(performance_series if performance_series else TimeSeries())
        return performance

    def build_pnl(self, last_pnl: float, pnl_series: TimeSeries = None) -> Pnl:
        pnl = Pnl()
        pnl.last_pnl = last_pnl
        pnl.series.CopyFrom(pnl_series if pnl_series else TimeSeries())
        return pnl

    def build_drawdown(self, last_drawdown: float, last_drawdown_pct: float, high_equity: float, low_equity: float,
                       current_run_up: float, current_drawdown: float, drawdown_series: TimeSeries = None) -> DrawDown:
        dd = DrawDown()
        dd.last_drawdown = last_drawdown
        dd.last_drawdown_pct = last_drawdown_pct
        dd.high_equity = high_equity
        dd.low_equity = low_equity
        dd.current_run_up = current_run_up
        dd.current_drawdown = current_drawdown
        dd.series.CopyFrom(drawdown_series if drawdown_series else TimeSeries())

        return dd

    def build_config(self, config_id: str, values: Dict[str, str]) -> Config:
        config = Config()

        config.config_id = config_id
        ModelHelper.add_to_dict(config.values, values)
        return config

    def build_strategy_state(self, stg_id: str, config: Config, positions: Dict[str, Position] = None) -> StrategyState:
        stg = StrategyState()
        stg.stg_id = stg_id
        stg.config.CopyFrom(config if config else Config())
        ModelHelper.add_to_dict_value(stg.positions, positions)
        return stg

    def build_order_state(self, cl_id: str, cl_req_id: str, portf_id: str, broker_id: str, inst_id: str,
                          creation_timestamp: int, action: OrderAction, type: OrderType, qty: float, limit_price: float,
                          stop_price: float = None, tif: TIF = DAY, oca_tag: str = None, params: Dict[str, str] = None,
                          broker_ord_id: str = None, update_timestamp: int = None, status: OrderStatus = None,
                          filled_qty: float = 0, avg_price: float = 0, last_qty: float = 0, last_price: float = 0,
                          stop_limit_ready: bool = False, trailing_stop_exec_price: float = None) -> OrderState:
        order = OrderState()
        order.cl_id = cl_id
        order.cl_req_id = cl_req_id
        order.portf_id = portf_id
        order.broker_id = broker_id
        order.broker_ord_id = broker_ord_id
        order.inst_id = inst_id

        order.creation_timestamp = creation_timestamp
        order.update_timestamp = update_timestamp

        order.action = action
        order.type = type
        order.qty = qty
        order.limit_price = limit_price
        order.stop_price = stop_price
        order.tif = tif
        order.oca_tag = oca_tag
        ModelHelper.add_to_dict(order.params, params)

        order.status = status
        order.filled_qty = filled_qty
        order.avg_price = avg_price
        order.last_qty = last_qty
        order.last_price = last_price
        order.stop_limit_ready = stop_limit_ready
        order.trailing_stop_exec_price = trailing_stop_exec_price

        return order

    def build_order_state_from_nos(self, req: NewOrderRequest):
        return self.build_order_state(
            cl_id=req.cl_id,
            cl_req_id=req.cl_req_id,
            portf_id=req.portf_id,
            broker_id=req.broker_id,
            inst_id=req.inst_id,
            creation_timestamp=req.timestamp,
            action=req.action,
            type=req.type,
            qty=req.qty,
            limit_price=req.limit_price,
            stop_price=req.stop_price,
            tif=req.tif,
            oca_tag=req.oca_tag,
            params=req.params
        )

    def build_position(self, inst_id: str, ordered_qty: float = 0, filled_qty: float = 0, last_price: float = 0,
                       orders: Dict[str, OrderPosition] = None) -> Position:
        position = Position()

        position.inst_id = inst_id
        position.ordered_qty = ordered_qty
        position.filled_qty = filled_qty
        position.last_price = last_price
        ModelHelper.add_to_dict_value(position.orders, orders)
        return position

    def build_order_position(self, cl_id: str, cl_req_id: str, ordered_qty: float = 0,
                             filled_qty: float = 0) -> OrderPosition:
        pos = OrderPosition()
        ord_id = pos.ord_id
        ord_id.cl_id = cl_id
        ord_id.cl_req_id = cl_req_id
        pos.ordered_qty = ordered_qty
        pos.filled_qty = filled_qty
        return pos

    def build_cl_ord_id(self, cl_id: str, ord_id: str) -> str:
        return "%s@%s" % (cl_id, ord_id)

    def build_inst_id(self, symbol: str, exch_id: str) -> str:
        return "%s@%s" % (symbol, exch_id)

    def build_sequence(self, id: str, seq: int) -> Sequence:
        sequence = Sequence()
        sequence.id = id
        sequence.seq = seq
        return sequence