
import logging

try:
    import numpy as np
except (ModuleNotFoundError, ImportError):
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.warning("numpy module not found. Install it with \"pip install numpy\" or similar.")
else:
    # OK, continue loading rest of module
    import re
    
    from datalogd import DataFilter, listify

    class PolynomialFunctionDataFilter(DataFilter):
        r"""
        Select data based on key--value pairs, then apply a polynomial function to a value.

        Any data which matches all of the ``match_keyvals`` key--value pairs will be processed. The
        format of the ``match_keyvals`` parameter is a list in the form ``[[key, value], [key2,
        value2]...]``. For example, ``match_keyvals=[["type", "temperature"], ["id", "123"]]`` will
        process any data which has a ``"type"`` field of ``"temperature"`` and an ``"id"`` field of
        ``"123"``. A ``value`` of the python special ``NotImplemented`` will match any value for the
        given key. In the case that values are strings, they will be matched as regular expressions, for
        example ``".*"`` will match any string.

        Once a data item is matched, a value will be selected to apply the polynomial function to,
        selected by the ``value`` parameter. By default this is the value stored under the ``"value"`` key.

        The polynomial function is defined by a set of coefficients, given by the ``coeffs`` parameter.
        This is an array of :math:`n` coefficients, :math:`c_n`, which forms the function
        :math:`x^\prime = \sum_n c_n x^{(n-1)} \equiv c_0 + c_1x + c_2x^2 \ldots c_nx^n`. For example,
        ``coeffs=[1.23, 1.0]`` would add 1.23 to a value, while ``coeffs=[0, 10]`` would multiply a
        value by 10. Specifying additional coefficients include quadratic, cubic terms etc.

        Rounding may be applied to the result by supplying the number of decimal places in the
        ``rounding`` parameter. Rounding behaviour is determined by the numpy ``around()`` function.
        Negative numbers specify positions to the left of the decimal point.

        The value of the data entry's ``"units"`` field can be modified or created using the ``units``
        parameter. For example, ``units="V"`` might be used to indicate that an analogue measurement in
        arbitrary units now equates to voltage, determined by the polynomial function calibration curve.

        :param match_keyvals: Key--value pairs to match to data items.
        :param value: Key from data item containing the value to modify.
        :param coeffs: Coefficients of the polynomial function to apply.
        :param rounding: Number of decimal places to round the result.
        :param units: New value of units field for the modified data item.
        """
        def __init__(self, sinks=[], match_keyvals=[["type", ".*"], ["id", ".*"]], value="value", coeffs=[0.0, 1.0], rounding=None, units=None):
            super().__init__(sinks=sinks)
            self._keyvals = match_keyvals
            self._value = value
            self._coeffs = coeffs
            self._rounding = rounding
            self._units = units


        def receive(self, data):
            """
            Accept the provided ``data``, select based on key/value pairs, apply function, and pass
            onto connected sinks.

            The selection is based upon the parameters provided to the constructor of this
            :class:`~datalogd.plugins.polynomialfunction_datafilter.PolynomialFunctionDataFilter`.

            :param data: Data to correct.
            """
            data = listify(data)
            for d in data:
                try:
                    # Look for matches to all key/value pairs
                    match = True
                    for kv_k, kv_v in self._keyvals:
                        # Try looking for this key in this data entry
                        v = d[kv_k]
                        # This key exists, check its value
                        if kv_v == v or ((type(kv_v) == type(v) == str) and re.fullmatch(kv_v, v)) or kv_v is NotImplemented:
                            # Value matches, keep checking any remaining keyval pairs
                            continue
                        else:
                            # Value doesn't match, can stop checking now
                            match = False
                            break
                    if match:
                        # Retrieve specified value to correct
                        x = d[self._value]
                        # Allow correcting numpy arrays
                        if isinstance(x, np.ndarray):
                            y = np.zeros_like(x)
                        else:
                            y = 0
                        # Apply polynomial function
                        for n, c in enumerate(self._coeffs):
                            y += c*x**n
                        # Apply rounding if requested
                        if self._rounding is not None:
                            y = np.round(y, int(self._rounding))
                        d[self._value] = y
                        # Change or add new units to the data if given
                        if self._units is not None:
                            d["units"] = self._units
                except (IndexError, KeyError, ValueError):
                    # An exception means we couldn't match this data entry, or find specified value
                    pass
            self.send(data)


