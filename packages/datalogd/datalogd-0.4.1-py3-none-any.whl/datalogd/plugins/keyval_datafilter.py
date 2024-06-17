import re

from datalogd import DataFilter, listify

class KeyValDataFilter(DataFilter):
    """
    Select or reject data based on key--value pairs.

    Received data items will be inspected to see whether they contain the given keys, and that their
    values match the given values. The key-value pairs are supplied as a list in the form ``[[key,
    value], [key2, value2]...]``. All key-value pairs must be matched. A value of the python
    special value of ``NotImplemented`` will match any value. If both ``value`` and ``data[key]`` are
    strings, matching will be performed using regular expressions (in which case ``".*"`` will match
    all strings). If the ``select`` flag is ``True``, only matching data will be passed on to the
    connected sinks, if it is ``False``, only non-matching data (or data that does not contain the
    given ``key``) will be passed on.

    If only a single key-value pair needs to be matched, they may alternatively be passed as the
    ``key`` and ``val`` parameters. This is mainly intended for backwards compatibility.

    :param select: Pass only matching data, or only non-matching data.
    :param keyvals: List of dictionary key-value pairs to match in incoming data.
    """
    def __init__(self, sinks=[], select=True, keyvals=None, key="type", val=None):
        super().__init__(sinks=sinks)
        self._select = bool(select)
        self._keyvals = keyvals
        if self._keyvals is None:
            self._keyvals = [[key, val]]


    def receive(self, data):
        """
        Accept the provided ``data``, and select or reject items before passing
        on to any connected sinks.

        The selection is based upon the parameters provided to the constructor
        of this :class:`~datalogd.plugins.keyval_datafilter.KeyValDataFilter`.

        :param data: Data to filter.
        """
        data = listify(data)
        data_accept = []
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
            except (IndexError, KeyError, ValueError):
                # An exception means we couldn't match this data entry
                match = False
            if (match and self._select) or (not match and not self._select):
                data_accept.append(d)
        self.send(data_accept)
