from unittest import TestCase

from algotrader.trading.context import ApplicationContext
from algotrader.utils.data_series_utils import parse_series, get_or_create_indicator


class IndicatorTest(TestCase):
    def setUp(self):
        self.app_context = ApplicationContext()

    def test_reuse(self):
        close = self.app_context.inst_data_mgr.get_series("bar")
        close.start(self.app_context)

        sma1 = get_or_create_indicator(self.app_context.inst_data_mgr, "SMA", 'bar', 'close', 3)
        sma1.start(self.app_context)

        sma2 = get_or_create_indicator(self.app_context.inst_data_mgr, "SMA", 'bar', 'close', 3)
        sma2.start(self.app_context)

        sma3 = get_or_create_indicator(self.app_context.inst_data_mgr, "SMA", 'bar', 'close', 10)
        sma3.start(self.app_context)

        self.assertEquals(sma1, sma2)
        self.assertNotEquals(sma2, sma3)
        self.assertNotEquals(sma1, sma3)

        sma4 = self.utils.get_or_create_indicator(self.app_context.inst_data_mgr, "SMA", "SMA('bar',close,3)", 10)
        sma4.start(self.app_context)

        self.assertEquals(sma4.input, sma2)

    def test_parse(self):
        bar = parse_series(self.app_context.inst_data_mgr, "bar")
        bar.start(self.app_context)

        sma1 = parse_series(self.app_context.inst_data_mgr, "SMA('bar',close,3)")
        sma1.start(self.app_context)

        sma2 = parse_series(self.app_context.inst_data_mgr, "SMA(SMA('bar',close,3),value,10)")
        sma2.start(self.app_context)

        rsi = parse_series(self.app_context.inst_data_mgr, "RSI(SMA(SMA('bar',close,3),value,10),value,14, 9)")
        rsi.start(self.app_context)

        self.assertEquals(sma1.input, bar)
        self.assertEquals(3, sma1.length)

        self.assertEquals(sma2.input, sma1)
        self.assertEquals(10, sma2.length)

        self.assertEquals(rsi.input, sma2)
        self.assertEquals(14, rsi.length)

    def test_fail_parse(self):
        with self.assertRaises(AssertionError):
            parse_series(self.app_context.inst_data_mgr, "SMA('Bar.Close',3")

        with self.assertRaises(AssertionError):
            parse_series(self.app_context.inst_data_mgr, "RSI(SMA(SMA('Bar.Close',3,10),14)")
