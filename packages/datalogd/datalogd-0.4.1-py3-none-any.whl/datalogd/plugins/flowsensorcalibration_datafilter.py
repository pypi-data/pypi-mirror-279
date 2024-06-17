from  math import exp

from datalogd import DataFilter, listify

class FlowSensorCalibrationDataFilter(DataFilter):
    r"""
    Use a pulse counter's counts per second to compute a liquid flow rate in litres per minute using
    an experimentally determined calibration function.

    A flow sensor has a spinning turbine and outputs pulses due to the flow rate of the liquid.
    However, the pulse rate will not be directly proportional to the flow rate (each pulse does not
    correspond to a fixed volume of liquid). A calibration curve can be constructed by measuring the
    number of pulses emitted over time for a given volume of liquid at a range of different flow
    rates. A plot of counts per litre versus counts per minute displays the characteristics of the
    sensor. Fitting the points to a curve of the form :math:`f(x) = a(1-\exp(-k(x-x_0)^b))` will
    provide the required calibration parameters.
    
    The default parameters (``a=5975, k=0.173734, x0=0, b=0.284333``) convert from counts per second
    to litres per minute for the YF-S401 flow sensor, and may be compatible with models from the
    same family such as YF-S402 and YF-S402B. A similar, smaller sensor common in automatic coffee
    machines, model number FM-HL3012C, was found to have parameters of ``a=1950, k=0.0965882, x0=0,
    b=0.721649``.

    The original ``count_rate`` entry in the data will be preserved, with the calculated
    ``flow_rate`` being appended as a new data entry.

    :param counter_rate_id: ID field to match to the data.
    :param a: Parameter :math:`a` in calibration function.
    :param k: Parameter :math:`k` in calibration function.
    :param x0: Parameter :math:`x_0` in calibration function.
    :param b: Parameter :math:`b` in calibration function.
    :param units: New units for the data.
    """
    def __init__(self, sinks=[], counter_rate_id="A_0", a=5975, k=0.173734, x0=0, b=0.284333):
        super().__init__(sinks=[])
        self._counter_rate_id = counter_rate_id
        self._a = a
        self._k = k
        self._x0 = x0
        self._b = b


    def receive(self, data):
        """
        Accept the provided ``data`` and compute a flow rate using the calibration function.

        :param data: Data to calculate flow rate from.
        """
        data = listify(data)
        # Find appropriate count rate among the data
        for d in data:
            try:
                if d["type"] == "counter_rate" and d["id"] == self._counter_rate_id:
                    # Get count rate, convert to counts per minute
                    cpm = 60.0*d["value"]
                    d_new = d.copy()
                    d_new["type"] = "flow_rate"
                    d_new["units"] = "L/min"
                    # Apply calibration function (for non-zero flow rates)
                    if cpm <= self._x0:
                        d_new["value"] = 0.0
                    else:
                        d_new["value"] = cpm/(self._a*(1 - exp(-self._k*(cpm - self._x0)**self._b)))
                    data.append(d_new)
            except KeyError:
                # That didn't work, not the data we're looking for
                continue
        self.send(data)
