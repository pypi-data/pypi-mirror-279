import sys
import re
import json
import logging
from datetime import datetime, timezone, timedelta
import asyncio
import math
import copy

from datalogd import DataFilter, listify

try:
    import numpy as np
except (ModuleNotFoundError, ImportError):
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.warning("numpy module available, so won't be available in sensor \"eval\" expressions. Install it with \"pip install numpy\" or similar.")

class SensorIdentifierDataFilter(DataFilter):
    
    #: Message for when a sensor has never sent any data.
    NOT_PRESENT = "not present"
    #: Message for when a sensor has previously sent data, but hasn't updated within the expected timeframe.
    NO_UPDATES = "no updates since {}"
    #: Message for when a sensor value has exceeded it's expected range.
    OUT_OF_RANGE = "out of range"

    #: Dictionary of built-in variables and functions available in eval expressions.
    _BUILTINS = {k: v for k, v in globals()["__builtins__"].items() if k in [
        "abs", "all", "any", "ascii", "bin", "chr", "divmod", "format", "hash", "hex", "len",
        "max", "min", "oct", "ord", "pow", "repr", "round", "sorted", "sum", "False", "True",
        "None", "bool", "bytearray", "bytes", "complex", "dict", "enumerate", "filter", "float",
        "int", "list", "map", "range", "reversed", "str", "tuple", "type", "zip"]}

    """
    Assign identifiers and additional properties to sensor data based off matching rules.
    """
    def __init__(self, sinks=[], rules="sensoridentifier_rules.json"):
        super().__init__(sinks=sinks)
        self._log = logging.getLogger(__name__)
        
        if rules[-5:] in (".JSON" ".json"):
            # If rules string looks like a filename, attempt to load JSON from file
            try:
                with open(rules) as f:
                    self._rules = json.load(f)
            except Exception as ex:
                self._log.error(f"Couldn't load matching rules from file: {rules}, {ex}")
                self._rules = []
        elif type(rules) == str:
            # Attempt to interpret string as raw JSON
            try:
                self._rules = json.loads(rules)
            except Exception as ex:
                self._log.error(f"Couldn't interpret matching rules string as JSON (note JSON files must end with a \".json\" extension):\n{rules}\n{ex}")
                self._rules = []
        elif type(rules) == list:
            # Assume correct data structure passed in
            self._rules = rules
        else:
            self._rules = rules
    
        # Do some basic sanity checking on rules here
        # E.g. ensure sensor_identifier and other essentials defined
        for i, r in enumerate(self._rules.copy()):
            if not "selector" in r:
                self._log.warning(f"Rule set {i} does not contain a \"selector\" entry thus won't match any data, dropping rule.")
                self._rules.remove(r)
            if (not "update" in r) and (not "eval" in r):
                self._log.warning(f"Rule set {i} does not contain an \"update\" or \"eval\" entry thus won't modify data, dropping rule.")
                self._rules.remove(r)
            if not "sensor_identifier" in r["update"]:
                self._log.warning(f"Rule set {i} \"update\" entry does not contain the mandatory \"sensor_identifier\" entry, dropping rule.")
                self._rules.remove(r)

        # Dictionary of faults currently detected
        # Keys are sensor identifier, values list of strings describing fault(s)
        self._faults = {}

        # Determine interval needed to check sensor update age
        self._watchdog_interval = float("inf")
        for r in self._rules:
            try:
                if not r["critical"]["interval"]:
                    # Loss/late updates not critical, don't need to check this against this rule
                    continue
                try:
                    interval = timedelta(seconds=r["update"]["interval"])
                except:
                    self._log.warning(f"Rule for {r['update']['sensor_identifier']} states update interval is critical, but no interval is defined.")
                    continue
                interval = float(r["update"]["interval"])
                if 0.0 < interval < self._watchdog_interval:
                    self._watchdog_interval = interval
            except KeyError:
                pass
        # Get reference to event loop and schedule task (note loop probably hasn't started yet)
        self._loop = asyncio.get_event_loop()
        if self._watchdog_interval < float("inf"):
            self._watchdog_task = self._loop.create_task(self._watchdog_update())  # For python 3.8+: , name="SensorIdentifier Watchdog")
        else:
            self._watchdog_task = None


    async def _watchdog_update(self):
        """
        Check sensor rules and send OK/Fault messages to connected sinks if update ages exceeded.
        """
        while True:
            now = datetime.now(timezone.utc).astimezone()
            for r in self._rules:
                try:
                    identifier = r['update']['sensor_identifier']
                    if not r["critical"]["interval"]:
                        # Loss/late updates not critical, don't need to check this against this rule
                        continue
                    interval = timedelta(seconds=r["update"]["interval"])
                    # Interval exists, check against timestamp (or fail if no timestamp yet)
                    if (not "timestamp" in r):
                        # No timestamp, sensor has never sent any data
                        description = SensorIdentifierDataFilter.NOT_PRESENT
                    elif (now > r["timestamp"] + 1.1*interval):
                        # Update hasn't been seen within given interval
                        description = SensorIdentifierDataFilter.NO_UPDATES.format(r['timestamp'].isoformat())
                    else:
                        description = ""
                    if description:
                        # A fault was detected
                        if not identifier in self._faults:
                            # Create list of faults for this sensor
                            self._faults[identifier] = []
                        if not description in self._faults[identifier]:
                            # Add description of faults to list if not already present
                            self._faults[identifier].append(description)
                    else:
                        # OK, updated within specified interval
                        if identifier in self._faults:
                            if SensorIdentifierDataFilter.OUT_OF_RANGE in self._faults[identifier]:
                                # Range error still valid, leave it in the list
                                self._faults[identifier] = [SensorIdentifierDataFilter.OUT_OF_RANGE]
                            else:
                                # Clear this sensor from faults
                                self._faults.pop(identifier)
                except KeyError:
                    pass
            # Send watchdog message indicating OK/Fault
            self._send_watchdog()
            # Wait before continuing the loop
            await asyncio.sleep(self._watchdog_interval)
    

    def _send_watchdog(self):
        """
        Send a watchdog type message with current fault conditions, if any.
        """
        message = {
                "type": "watchdog",
                "sensor_identifier": "WATCHDOG",
                "sensor_name": "Watchdog",
                "value": "OK",
                "range": ["OK", "OK"],
                "critical_range": True,
            }
        if self._faults:
            message.update({
                "value": "FAULT",
                "faults": self._faults.copy()
            })
        self.send(message)


    def receive(self, data):
        """
        Accept the provided ``data``, and assign identifier and additional properties based on the
        matching rules.

        :param data: Data to filter.
        """
        data = copy.deepcopy(listify(data))
        # Timestamp to use for this set of data
        timestamp = datetime.now(timezone.utc).astimezone()
        # Flag to indicate fault conditions have changed
        updated_faults = False
        for d in data:
            # Look through rules for matching criteria
            for r in self._rules:
                # Start by assuming rules match this data item
                match = True
                try:
                    for s_k, s_v in r["selector"]:
                        # Try looking for this key in this data entry
                        v = d[s_k]
                        # This key exists, check its value
                        if s_v == v or ((type(s_v) == type(v) == str) and re.fullmatch(s_v, v)) or s_v is NotImplemented:
                            # Value matches this rule so far, keep checking any remaining selection criteria
                            continue
                        else:
                            # Value doesn't match this rule, can stop checking now
                            match = False
                            break
                except (IndexError, KeyError, ValueError) as ex:
                    # An exception means we couldn't match this data entry to this rule
                    match = False
                # Finished checking this data item, act if it matched selection criteria
                if match:
                    # This data entry matched the selection criteria for this rule
                    # Perform requested updates to data fields to add/change data fields
                    d.update(r["update"])
                    # Add critical conditions if they exist
                    try:
                        d["critical_range"] = r["critical"]["range"]
                    except:
                        pass
                    try:
                        d["critical_interval"] = r["critical"]["interval"]
                    except:
                        pass
                    d["timestamp"] = timestamp
                    # Keep timestamp in rules dictionary for our records (to check on update ages)
                    r["timestamp"] = timestamp

                    # Perform function evaluations to calculate new values, apply calibration curves etc
                    if "eval" in r and isinstance(r["eval"], dict):
                        for k, expr in r["eval"].items():
                            try:
                                #self._log.debug(f"Evaluating {k} = {expr}")
                                # Construct a slightly safe environment in which to run eval expressions
                                eval_globals = {"math": math, "__builtins__": SensorIdentifierDataFilter._BUILTINS}
                                # Add numpy functionality if numpy module has been loaded
                                if "numpy" in sys.modules:
                                    eval_globals["np"] = np
                                d[k] = eval(expr, eval_globals, d)
                            except Exception as ex:
                                self._log.warning(f"Error during eval of \"{k} = {expr}\": {ex}")

                    # Update fault list (clear presence/update interval, check valid range)
                    try:
                        identifier = r['update']['sensor_identifier']
                        # Update occurred, clear presence/interval faults if they exist
                        if identifier in self._faults and SensorIdentifierDataFilter.NOT_PRESENT in self._faults[identifier]:
                                self._faults[identifier].remove(SensorIdentifierDataFilter.NOT_PRESENT)
                                updated_faults = True
                        if identifier in self._faults and SensorIdentifierDataFilter.NO_UPDATES in self._faults[identifier]:
                                self._faults[identifier].remove(SensorIdentifierDataFilter.NO_UPDATES)
                                updated_faults = True
                        # Check valid range if range is marked as critical
                        if r["critical"]["range"]:
                            value = d["value"]
                            if ((value < r["update"]["range"][0]) or
                                (value > r["update"]["range"][1]) or
                                (value != value) or value in (None, "NaN", "nan", "NAN")):
                                # Value out of range or is NaN
                                if not identifier in self._faults:
                                    # Create list of faults for this sensor
                                    self._faults[identifier] = []
                                if not SensorIdentifierDataFilter.OUT_OF_RANGE in self._faults[identifier]:
                                    # Add out of range description to faults list if not already present
                                    self._faults[identifier].append(SensorIdentifierDataFilter.OUT_OF_RANGE)
                                    updated_faults = True
                            else:
                                # Value in range, clear any previous out-of-range error
                                if identifier in self._faults and SensorIdentifierDataFilter.OUT_OF_RANGE in self._faults[identifier]:
                                    self._faults[identifier].remove(SensorIdentifierDataFilter.OUT_OF_RANGE)
                                    updated_faults = True
                        # Clear sensor from fault list if no faults remaining
                        if identifier in self._faults and not self._faults[identifier]:
                            self._faults.pop(identifier)
                    except (KeyError, TypeError) as ex:
                        pass
        
        # Send watchdog message indicating faults if new out-of-range sensors discovered
        if updated_faults:
            self._send_watchdog()
        # Send updated data onto connected sinks
        self.send(data)
                