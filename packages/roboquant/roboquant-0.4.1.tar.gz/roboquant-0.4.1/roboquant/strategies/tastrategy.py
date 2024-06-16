from abc import abstractmethod

from roboquant.event import Bar
from roboquant.strategies.signal import Signal
from roboquant.strategies.buffer import OHLCVBuffer
from roboquant.strategies.signalstrategy import SignalStrategy


class TaStrategy(SignalStrategy):
    """Abstract base class for other strategies that helps to implement trading solutions
    based on technical indicators using bars.

    Subclasses should implement the _create_signal method. This method is only invoked once
    there is at least `size` history for an individual symbol.
    """

    def __init__(self, size: int) -> None:
        super().__init__()
        self._data: dict[str, OHLCVBuffer] = {}
        self.size = size

    def create_signals(self, event):
        signals: list[Signal] = []
        for item in event.items:
            if isinstance(item, Bar):
                symbol = item.symbol
                if symbol not in self._data:
                    self._data[symbol] = OHLCVBuffer(self.size)
                ohlcv = self._data[symbol]
                ohlcv.append(item.ohlcv)
                if ohlcv.is_full():
                    signal = self._create_signal(symbol, ohlcv)
                    if signal is not None:
                        signals.append(signal)
        return signals

    @abstractmethod
    def _create_signal(self, symbol: str, ohlcv: OHLCVBuffer) -> Signal | None:
        """
        Return a signal or None for the provided symbol and ohlcv data.
        """
        ...
