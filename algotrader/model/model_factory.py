from typing import Dict, List, Union, Callable

from algotrader.model.market_data_pb2 import *
from algotrader.model.model_helper import ModelHelper
from algotrader.model.ref_data_pb2 import *
from algotrader.model.time_series_pb2 import *
from algotrader.model.trade_data_pb2 import *


class ModelFactory(object):
    # ref data
    @staticmethod
    def new_instrument(symbol: str, type: Instrument.InstType, primary_exch_id: str, ccy_id: str,
                       name: str = None, exch_ids: List[str] = None, sector: str = None, industry: str = None,
                       margin: float = None, tick_size: float = None,
                       alt_symbols: Dict[str, str] = None, alt_ids: Dict[str, str] = None,
                       alt_sectors: Dict[str, str] = None, alt_industries: Dict[str, str] = None,
                       underlying_type: Underlying.UnderlyingType = None,
                       underlying_ids: List[str] = None,
                       underlying_weights: List[float] = None,
                       option_type: Instrument.OptionType = None,
                       option_style: Instrument.OptionStyle = None, strike: float = None,
                       exp_date: int = None,
                       multiplier: float = None) -> Instrument:
        inst = Instrument()
        inst.inst_id = symbol + '@' + primary_exch_id
        inst.symbol = symbol
        if isinstance(type, int):
            inst.type = type
        else:
            inst.type = Instrument.InstType.DESCRIPTOR.values_by_name[type].number
        inst.primary_exch_id = primary_exch_id
        inst.ccy_id = ccy_id

        if name:
            inst.name = name

        ModelHelper.add_to_list(inst.exch_ids, exch_ids)

        if sector:
            inst.sector = sector

        if industry:
            inst.industry = industry

        if margin:
            inst.margin = margin

        if tick_size:
            inst.tick_size = tick_size

        ModelHelper.add_to_dict(inst.alt_symbols, alt_symbols)
        ModelHelper.add_to_dict(inst.alt_ids, alt_ids)
        ModelHelper.add_to_dict(inst.alt_sectors, alt_sectors)
        ModelHelper.add_to_dict(inst.alt_industries, alt_industries)

        if underlying_type and underlying_ids:
            ModelFactory.new_underlying(inst, underlying_type, underlying_ids, underlying_weights)

            if option_type:
                inst.option_type = option_type
            if option_style:
                inst.option_style = option_style
            if strike:
                inst.strike = strike
            if exp_date:
                inst.exp_date = exp_date
            if multiplier:
                inst.multiplier = multiplier

        return inst

    @staticmethod
    def new_underlying(inst: Instrument, type: Underlying.UnderlyingType, assets: List[str],
                       weights: List[float] = None) -> Underlying:
        underlying = inst.underlying
        underlying.type = type

        if weights:
            for asset_id, weight in zip(assets, weights):
                ModelFactory.add_asset(underlying=underlying, asset_id=asset_id, weight=weight)
        else:
            for asset_id in assets:
                ModelFactory.add_asset(underlying=underlying, asset_id=asset_id)

        return underlying

    @staticmethod
    def add_asset(underlying: Underlying, asset_id: str, weight: float = None) -> Underlying.Asset:
        asset = underlying.assets.add()
        asset.inst_id = asset_id
        if weight is not None:
            asset.weight = weight
        return asset

    @staticmethod
    def new_exchange(exch_id: str, name: str, country_id: str = None, trading_hours_id: str = None,
                     holidays_id: str = None,
                     alt_ids: Dict[str, str] = None) -> Exchange:
        exchange = Exchange()
        exchange.exch_id = exch_id
        if name:
            exchange.name = name
        if country_id:
            exchange.country_id = country_id
        if trading_hours_id:
            exchange.trading_hours_id = trading_hours_id
        if holidays_id:
            exchange.holidays_id = holidays_id
        ModelHelper.add_to_dict(exchange.alt_ids, alt_ids)
        return exchange

    @staticmethod
    def new_currency(ccy_id: str, name: str) -> Currency:
        currency = Currency()
        currency.ccy_id = ccy_id
        if name:
            currency.name = name
        return currency

    @staticmethod
    def new_country(country_id: str, name: str, holidays_id: str = None) -> Country:
        country = Country()
        country.country_id = country_id
        country.name = name
        country.holidays_id = holidays_id
        return country

    @staticmethod
    def new_holiday_series(holidays_id) -> HolidaySeries:
        holiday_series = HolidaySeries()
        holiday_series.holidays_id = holidays_id
        return holiday_series

    @staticmethod
    def add_holiday(holiday_series: HolidaySeries, trading_date: int, type: HolidaySeries.Holiday.Type, start_date: int,
                    end_date: int,
                    start_time: int = None,
                    end_time: int = None,
                    desc: str = None) -> HolidaySeries.Holiday:
        holiday = holiday_series.holidays.add()
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

    @staticmethod
    def new_trading_hours(trading_hours_id: str, timezone_id: str) -> TradingHours:
        trading_hour = TradingHours()
        trading_hour.trading_hours_id = trading_hours_id
        trading_hour.timezone_id = timezone_id
        return trading_hour

    @staticmethod
    def add_trading_session(trading_hour: TradingHours, start_weekdate: int, start_time: int, end_weekdate: int,
                            end_time: int,
                            eod: bool) -> TradingHours.Session:
        session = trading_hour.sessions.add()
        session.start_weekdate = start_weekdate
        session.start_time = start_time
        session.end_weekdate = end_weekdate
        session.end_time = end_time
        session.eod = eod
        return session

    @staticmethod
    def new_timezone(timezone_id: str) -> TimeZone:
        timezone = TimeZone()
        timezone.timezone_id = timezone_id
        return timezone

    @staticmethod
    def new_time_series(series_id: str, name: str = '', desc: str = '',
                        inputs: Union[str, List[str]] = None, keys: Union[str, List[str]] = None,
                        default_output_key: str = 'value', missing_value_replace: float = 0.0, start_time: int = 0,
                        end_time: int = 0) -> TimeSeries:
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

        return time_series

    @staticmethod
    def add_time_series_item(time_series: TimeSeries, timestamp: int, data: Dict[str, float]) -> TimeSeries.Item:
        item = time_series.items.add()
        ModelFactory.update_time_series_time(item, timestamp=timestamp, data=data)
        return item

    @staticmethod
    def update_time_series_time(item: TimeSeries.Item, timestamp: int = None,
                                data: Dict[str, float] = None) -> TimeSeries.Item:
        item.timestamp = timestamp
        ModelHelper.add_to_dict(item.data, data)
        return item

    @staticmethod
    def new_bar(inst_id: str, type: Bar.Type = None, size: int = None, provider_id: str = None, timestamp: int = None,
                open: float = None, high: float = None, low: float = None, close: float = None, vol: float = None, adj_close: float = None,
                open_interest: float = None,
                utc_time: int = None, begin_time: int = None) -> Bar:
        bar = Bar()
        bar.inst_id = inst_id
        if type:
            bar.type = type
        if size:
            bar.size = size
        if provider_id:
            bar.provider_id = provider_id
        if timestamp:
            bar.timestamp = timestamp
        if open:
            bar.open = open
        if high:
            bar.high = high
        if low:
            bar.low = low
        if close:
            bar.close = close
        if vol:
            bar.vol = vol
        if adj_close:
            bar.adj_close = adj_close
        if open_interest:
            bar.open_interest = open_interest
        if utc_time:
            bar.utc_time = utc_time
        if begin_time:
            bar.begin_time = begin_time

        return bar

    @staticmethod
    def new_quote(inst_id: str, provider_id: str = None, timestamp: float = None, bid: float = None, bid_size: float = None, ask: float = None,
                  ask_size: float = None, utc_time: int = None) -> Quote:
        quote = Quote()
        quote.inst_id = inst_id
        if provider_id:
            quote.provider_id = provider_id
        if timestamp:
            quote.timestamp = timestamp
        if utc_time:
            quote.utc_time = utc_time
        if bid:
            quote.bid = bid
        if bid_size:
            quote.bid_size = bid_size
        if ask:
            quote.ask = ask
        if ask_size:
            quote.ask_size = ask_size

        return quote

    @staticmethod
    def new_trade(inst_id: str, provider_id: str = None, timestamp: int = None, price: float = None, size: float = None,
                  utc_time: int = None) -> Trade:
        trade = Trade()
        trade.inst_id = inst_id
        if provider_id:
            trade.provider_id = provider_id
        if timestamp:
            trade.timestamp = timestamp
        if price:
            trade.price = price
        if size:
            trade.size = size
        if utc_time:
            trade.utc_time = utc_time

        return trade

    @staticmethod
    def new_market_depth(inst_id: str, provider_id: str = None, timestamp: int = None, md_provider: str = None, position: int = None,
                         operation: MarketDepth.Operation = None, side: MarketDepth.Side = None, price: float = None, size: float = None,
                         utc_time: int = None) -> MarketDepth:
        md = MarketDepth()
        md.inst_id = inst_id
        if provider_id:
            md.provider_id = provider_id
        if timestamp:
            md.timestamp = timestamp
        if md_provider:
            md.md_provider = md_provider
        if position:
            md.position = position
        if operation:
            md.operation = operation
        if side:
            md.side = side
        if price:
            md.price = price
        if size:
            md.size = size
        if utc_time:
            md.utc_time = utc_time
        return md

    @staticmethod
    def new_new_order_request(timestamp: int, cl_id: str, cl_ord_id: str, portf_id: str, broker_id: str,
                              inst_id: str,
                              action: OrderAction, type: OrderType, qty: float, limit_price: float,
                              stop_price: float = 0.0,
                              tif: TIF = DAY, oca_tag: str = None,
                              params: Dict[str, str] = None) -> NewOrderRequest:
        req = NewOrderRequest()

        req.timestamp = timestamp
        req.cl_id = cl_id
        req.cl_ord_id = cl_ord_id
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

    @staticmethod
    def new_order_replace_request(timestamp: int, cl_id: str, cl_ord_id: str, cl_orig_req_id: str,
                                  type: OrderType, qty: float,
                                  limit_price: float, stop_price: float = None,
                                  tif: TIF = DAY, oca_tag: str = None,
                                  params: Dict[str, str] = None) -> OrderReplaceRequest:
        req = OrderReplaceRequest()

        req.timestamp = timestamp
        req.cl_id = cl_id
        req.cl_ord_id = cl_ord_id
        req.cl_orig_req_id = cl_orig_req_id
        req.type = type
        req.qty = qty
        req.limit_price = limit_price
        req.stop_price = stop_price
        req.tif = tif
        req.oca_tag = oca_tag
        ModelHelper.add_to_dict(req.params, params)

        return req

    @staticmethod
    def new_order_cancel_request(timestamp: int, cl_id: str, cl_ord_id: str, cl_orig_req_id: str,
                                 params: Dict[str, str] = None) -> OrderCancelRequest:
        req = OrderCancelRequest()
        req.timestamp = timestamp
        req.cl_id = cl_id
        req.cl_ord_id = cl_ord_id
        req.cl_orig_req_id = cl_orig_req_id
        ModelHelper.add_to_dict(req.params, params)

        return req

    @staticmethod
    def new_order_status_update(timestamp: int, broker_id: str, broker_event_id: str, broker_ord_id: str,
                                cl_id: str,
                                cl_ord_id: str, inst_id: str, filled_qty: float, avg_price: float,
                                status: OrderStatus) -> OrderStatusUpdate:
        event = OrderStatusUpdate()
        event.timestamp = timestamp
        event.broker_id = broker_id
        event.broker_event_id = broker_event_id
        event.broker_ord_id = broker_ord_id
        event.cl_id = cl_id
        event.cl_ord_id = cl_ord_id
        event.inst_id = inst_id
        event.filled_qty = filled_qty
        event.avg_price = avg_price
        event.status = status

        return event

    @staticmethod
    def new_execution_report(timestamp: int, broker_id: str, broker_event_id: str = None, broker_ord_id: str = None,
                             cl_id: str = None,
                             cl_ord_id: str = None, inst_id: str = None, last_qty: float = None, last_price: float = None, commission: float = None,
                             filled_qty: float = None, avg_price: float = None,
                             status: OrderStatus = None) -> ExecutionReport:
        event = ExecutionReport()
        event.timestamp = timestamp
        event.broker_id = broker_id
        if broker_event_id:
            event.broker_event_id = broker_event_id
        if broker_ord_id:
            event.broker_ord_id = broker_ord_id
        if cl_id:
            event.cl_id = cl_id
        if cl_ord_id:
            event.cl_ord_id = cl_ord_id
        if inst_id:
            event.inst_id = inst_id
        if last_qty:
            event.last_qty = last_qty
        if last_price:
            event.last_price = last_price
        if commission:
            event.commission = commission
        if filled_qty:
            event.filled_qty = filled_qty
        if avg_price:
            event.avg_price = avg_price
        if status:
            event.status = status

        return event

    @staticmethod
    def new_account_update(timestamp: int, broker_id: str, broker_event_id: str, account_name) -> AccountUpdate:
        event = AccountUpdate()

        event.timestamp = timestamp
        event.broker_id = broker_id
        event.broker_event_id = broker_event_id
        event.account_name = account_name

        return event

    @staticmethod
    def update_account_value(value: AccountValue, key: str, ccy_values: Dict[str, float]) -> AccountValue:
        value.key = key
        ModelHelper.add_to_dict(value.ccy_values, ccy_values)
        return value

    @staticmethod
    def new_portfolio_update(timestamp: int, broker_id: str, broker_event_id: str, portf_id: str, inst_id: str,
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

    @staticmethod
    def new_account_state(acct_id: str) -> AccountState:
        account = AccountState()
        account.acct_id = acct_id
        return account

    @staticmethod
    def new_portfolio_state(portf_id: str, cash: float, stock_value: float = None) -> PortfolioState:
        portfolio = PortfolioState()
        portfolio.portf_id = portf_id
        portfolio.cash = cash
        if stock_value:
            portfolio.stock_value = stock_value
        ModelFactory.new_portfolio_performance(portfolio=portfolio)
        ModelFactory.new_portfolio_pnl(portfolio=portfolio)
        ModelFactory.new_portfolio_drawdown(portfolio=portfolio)
        return portfolio

    @staticmethod
    def new_portfolio_performance(portfolio: PortfolioState, total_equity: float = 0) -> Performance:
        performance = portfolio.performance
        performance.total_equity = total_equity
        performance.series.series_id = portfolio.portf_id + "@performance"
        return performance

    @staticmethod
    def new_portfolio_pnl(portfolio: PortfolioState, last_pnl: float = 0) -> Pnl:
        pnl = portfolio.pnl
        pnl.last_pnl = last_pnl
        pnl.series.series_id = portfolio.portf_id + "@pnl"
        return pnl

    @staticmethod
    def new_portfolio_drawdown(portfolio: PortfolioState, last_drawdown: float = 0, last_drawdown_pct: float = 0,
                               high_equity: float = 0,
                               low_equity: float = 0,
                               current_run_up: float = 0, current_drawdown: float = 0) -> DrawDown:
        dd = portfolio.drawdown
        dd.last_drawdown = last_drawdown
        dd.last_drawdown_pct = last_drawdown_pct
        dd.high_equity = high_equity
        dd.low_equity = low_equity
        dd.current_run_up = current_run_up
        dd.current_drawdown = current_drawdown
        dd.series.series_id = portfolio.portf_id + "@drawdown"

        return dd

    @staticmethod
    def update_config(config: Config, config_id: str = None, config_values: Dict[str, str] = None) -> Config:
        if config_id:
            config.config_id = config_id
        if config_values:
            ModelHelper.add_to_dict(config.values, config_values)
        return config

    @staticmethod
    def new_strategy_state(stg_id: str, config_values: Dict[str, str] = None) -> StrategyState:
        stg = StrategyState()
        stg.stg_id = stg_id
        stg.config.config_id = stg_id
        ModelFactory.update_config(stg.config, None, config_values)
        return stg

    @staticmethod
    def new_order_state(cl_id: str, cl_ord_id: str, portf_id: str, broker_id: str, inst_id: str,
                        creation_timestamp: int, action: OrderAction, type: OrderType, qty: float, limit_price: float,
                        stop_price: float = None, tif: TIF = DAY, oca_tag: str = None, params: Dict[str, str] = None,
                        broker_ord_id: str = None, update_timestamp: int = None, status: OrderStatus = None,
                        filled_qty: float = 0, avg_price: float = 0, last_qty: float = 0, last_price: float = 0,
                        stop_limit_ready: bool = False, trailing_stop_exec_price: float = None) -> OrderState:
        order = OrderState()
        order.cl_id = cl_id
        order.cl_ord_id = cl_ord_id
        order.portf_id = portf_id
        order.broker_id = broker_id
        if broker_ord_id:
            order.broker_ord_id = broker_ord_id
        order.inst_id = inst_id

        if creation_timestamp:
            order.creation_timestamp = creation_timestamp
        if update_timestamp:
            order.update_timestamp = update_timestamp
        if action:
            order.action = action
        if type:
            order.type = type
        if qty:
            order.qty = qty
        if limit_price:
            order.limit_price = limit_price
        if stop_price:
            order.stop_price = stop_price
        if tif:
            order.tif = tif
        if oca_tag:
            order.oca_tag = oca_tag
        ModelHelper.add_to_dict(order.params, params)

        if status:
            order.status = status
        if filled_qty:
            order.filled_qty = filled_qty
        if avg_price:
            order.avg_price = avg_price
        if last_qty:
            order.last_qty = last_qty
        if last_price:
            order.last_price = last_price
        if stop_limit_ready:
            order.stop_limit_ready = stop_limit_ready
        if trailing_stop_exec_price:
            order.trailing_stop_exec_price = trailing_stop_exec_price

        return order

    @staticmethod
    def new_order_state_from_nos(req: NewOrderRequest) -> OrderState:
        return ModelFactory.new_order_state(
            cl_id=req.cl_id,
            cl_ord_id=req.cl_ord_id,
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

    @staticmethod
    def add_position(attribute: Callable, inst_id: str, ordered_qty: float = 0, filled_qty: float = 0,
                     last_price: float = 0) -> Position:
        position = attribute.positions[inst_id]

        position.inst_id = inst_id
        position.ordered_qty = ordered_qty
        position.filled_qty = filled_qty
        position.last_price = last_price
        return position

    @staticmethod
    def add_order_position(position: Position, cl_id: str, cl_ord_id: str, ordered_qty: float = 0,
                           filled_qty: float = 0) -> OrderPosition:
        id = ModelFactory.new_cl_ord_id(cl_id, cl_ord_id)
        pos = position.orders[id]
        pos.cl_id = cl_id
        pos.cl_ord_id = cl_ord_id
        pos.ordered_qty = ordered_qty
        pos.filled_qty = filled_qty
        return pos

    @staticmethod
    def new_cl_ord_id(cl_id: str, ord_id: str) -> str:
        return "%s@%s" % (cl_id, ord_id)

    @staticmethod
    def new_inst_id(symbol: str, exch_id: str) -> str:
        return "%s@%s" % (symbol, exch_id)

    @staticmethod
    def new_sequence(id: str, seq: int) -> Sequence:
        sequence = Sequence()
        sequence.id = id
        sequence.seq = seq
        return sequence
