from time import perf_counter
import logging

from datalogd import DataFilter, listify

class SinkTimerDataFilter(DataFilter):
    """
    Time how long each sink takes to receive data and warn if any exceed a given threshold.

    This filter may be used for testing and debugging. If a sink takes longer than a given time to
    process data, report the event using the python logging system. Two levels of reporting are
    enabled, controlled by the ``info`` and ``warning`` parameters. These parameters are the
    threshold times, in seconds.

    :param info: Threshold time to log at the "info" level.
    :param warning: Threshold time to log at the "warning" level.
    """
    def __init__(self, sinks=[], info=0.1, warning=0.5):
        super().__init__(sinks=sinks)
        self._info_t = info
        self._warning_t = warning
        self._log = logging.getLogger("SinkTimer")

    def receive(self, data):
        """
        Accept ``data`` and pass on to connected sinks.

        :param data: Data to process.
        """
        self.send(data)
    
    def send(self, data):
        """
        Send ``data`` to each connected sink, alerting if their processing time exceeds given values.
        """
        for s in self.sinks:
            t_start = perf_counter()
            s.receive(data)
            t = perf_counter() - t_start
            if t >= self._warn_t:
                self._log.warning(f"{s} processed in {t:g} s")
            elif t >= self._info_t:
                self._log.info(f"{s} processed in {t:g} s")


