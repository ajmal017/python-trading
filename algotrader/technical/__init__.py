from algotrader import Context
from algotrader.model.model_factory import ModelFactory
from algotrader.trading.data_series import DataSeries
from algotrader.utils.model import get_full_cls_name

class Indicator(DataSeries):
    VALUE = 'value'

    __slots__ = (
        'input_name',
        'input_keys',
        'calculate',
    )

    __transient__ = (
        'app_context',
        'input'
    )

    @staticmethod
    def get_name(indicator_name, input, input_key, *args):
        if not input:
            return '%s' % indicator_name
        parts = [Indicator.get_input_name(input)]
        if input_key:
            parts.extend(DataSeries.convert_to_list(input_key))
        if args:
            parts.extend(args)
        content = ",".join(str(part) for part in parts)
        return '%s(%s)' % (indicator_name, content)

    @staticmethod
    def get_input_name(input):
        if isinstance(input, Indicator):
            return input.name
        if isinstance(input, DataSeries):
            return "'%s'" % input.name
        return "'%s'" % input

    def __init__(self, name, input, input_keys, desc=None, time_series=None):
        if time_series:
            self.input_name = time_series.inputs
            self.input = None
        else:
            if input:
                if isinstance(input, DataSeries):
                    self.input_name = input.name
                    self.input = input
                else:
                    self.input_name = input
                    self.input = None
            else:
                self.input_name = None
            time_series = ModelFactory.build_time_series(series_id=name, series_cls=get_full_cls_name(self), name=name, desc=desc, inputs=self.input_name)

        self.input_keys = self._get_key(input_keys, None)
        self.calculate = True
        super(Indicator, self).__init__(time_series)

    def _start(self, app_context: Context) -> None:
        super(Indicator, self)._start(self.app_context)

        if not hasattr(self, 'input') or not self.input:
            self.input = self.app_context.inst_data_mgr.get_series(self.input_name)

        self.app_context.inst_data_mgr.add_series(self)

        self.update_all()
        self.input.subject.subscribe(self.on_update)

    def _stop(self):
        pass

    def update_all(self):
        data_list = self.input.get_data()
        for data in data_list:
            # if timestamp has been processed, we should skipped the update.....
            if data['timestamp'] not in self.time_list:
                if self.input_keys:
                    filtered_data = {key: data[key] for key in self.input_keys}
                    filtered_data['timestamp'] = data['timestamp']
                    self.on_update(filtered_data)
                else:
                    self.on_update(data)

    def on_update(self, data):
        raise NotImplementedError()
