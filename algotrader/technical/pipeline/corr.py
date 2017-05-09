import numpy as np

from algotrader.technical.pipeline import PipeLine
from typing import Dict


class Corr(PipeLine):
    _slots__ = (
    )

    def __init__(self, inputs, input_key='close', length=30, desc="Correlation"):
        super(Corr, self).__init__(PipeLine.get_name(Corr.__name__, input),
                                   input, input_key, length, desc)
        super(Corr, self).update_all()

    def _process_update(self, source: str, timestamp: int, data: Dict[str, float]):
        result = {}
        if self.inputs[0].size() > self.length:
            if self.all_filled():
                result[PipeLine.VALUE] = self.df.corr()
            else:
                result[PipeLine.VALUE] = self._default_output()
        else:
            result[PipeLine.VALUE] = self._default_output()
        self.add(timestamp=timestamp, data=result)

    def _default_output(self):
        na_array = np.empty(shape=self.shape())
        na_array[:] = np.nan
        return na_array

    def shape(self):
        return np.array([self.numPipes, self.numPipes])
