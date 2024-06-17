from datalogd import DataFilter, listify

class CoolingPowerDataFilter(DataFilter):
    """
    Calculate power absorbed by cooling liquid through a system given flow rate and input and output
    temperatures.

    The calculation requires each receipt of data to contain two temperature entries and one flow
    rate entry. For example:

    .. code-block:: none

        [
            {"type": "temperature", "id": "A_0", "value": 12.34, "units": "C"},
            {"type": "temperature", "id": "A_1", "value": 23.45, "units": "C"},
            {"type": "flow_rate", "id": "A_0", "value": 0.456, "units": "L/min"}
        ]
    
    The IDs used to select the appropriate temperatures and flow rate may be given in the
    initialisation parameters. Temperatures should be in celsius (or kelvin), and flow rate should
    be in litres per minute. By default, the heat capacity and density of water will be used for
    calculations, but alternate values may supplied as a parameters. Heat capacity should be in
    J/kg/K, and density in g/mL.

    If all required data entries are present, a new entry with a ``coolingpower`` type will be
    added, and the data will then look like:

    .. code-block:: none

        [
            {"type": "temperature", "id": "A_0", "value": 12.34, "units": "C"},
            {"type": "temperature", "id": "A_1", "value": 23.45, "units": "C"},
            {"type": "flow_rate", "id": "A_0", "value": 0.456, "units": "L/min"},
            {"type": "coolingpower", "id": "A_0", "value": 353.28, "units": "W"}
        ]
    
    The ID used for the ``coolingpower`` entry may also be specified as an initialisation parameter.
    If the flow rate entry includes a ``"timestamp"`` field, its value will be copied to the
    cooling power entry.

    :param temperature_id_in: ID of temperature data for inlet liquid.
    :param temperature_id_out: ID of temperature data for outlet liquid.
    :param flow_rate_id: ID of liquid flow rate data.
    :param heatcapacity: Heat capacity of cooling liquid, in J/kg/K.
    :param density: Density of cooling liquid, in g/mL.
    :param coolingpower_id: ID to use for the calculated cooling power data.
    """
    def __init__(self, sinks=[], temperature_id_in="A_0", temperature_id_out="A_1", flow_rate_id="A_0", heatcapacity=4184, density=1.0, coolingpower_id="A_0"):
        super().__init__(sinks=[])
        self._t_id_in = temperature_id_in
        self._t_id_out = temperature_id_out
        self._f_id = flow_rate_id
        self._heatcapacity = heatcapacity
        self._density = density
        self._id = coolingpower_id
        # Remember last values of temperatures to use if missing when flow rate data is present
        self._t_in_prev = None
        self._t_out_prev = None
        # Keep a moving window average of n temperatures
        self._t_mwa_n = 5

    def receive(self, data):
        """
        Accept the provided ``data`` and add a ``coolingpower`` entry calculated from flow rate and
        input and output temperatures.

        :param data: Data to calculate cooling power from.
        """
        data = listify(data)
        # Find appropriate t_in, t_out, flow rate among the data
        t_in = t_out = flow_rate = None
        for d in data:
            if isinstance(d, dict) and "type" in d and "id" in d and "value" in d:
                if d["type"] == "temperature":
                    if d["id"] == self._t_id_in:
                        try:
                            self._t_in_prev = ((self._t_mwa_n - 1)*self._t_in_prev + d["value"])/self._t_mwa_n
                        except:
                            self._t_in_prev = d["value"]
                        t_in = self._t_in_prev
                    elif d["id"] == self._t_id_out:
                        try:
                            self._t_out_prev = ((self._t_mwa_n - 1)*self._t_out_prev + d["value"])/self._t_mwa_n
                        except:
                            self._t_out_prev = d["value"]
                        t_out = self._t_out_prev
                elif d["type"] == "flow_rate":
                    if d["id"] == self._f_id:
                        flow_rate = d["value"]
                        # Attempt to copy the timestamp from flow rate if present
                        timestamp = d["timestamp"] if "timestamp" in d else None
            # Stop looking if we have found needed values already
            if not (t_in is None or t_out is None or flow_rate is None):
                break
        # If we have a flow rate, but not temperatures, use last values
        if (not flow_rate is None) and (t_in is None): t_in = self._t_in_prev
        if (not flow_rate is None) and (t_out is None): t_out = self._t_out_prev
        # Calculate cooling power if we have all required values
        if not (t_in is None or t_out is None or flow_rate is None):
            # Assumes density of liquid constant with temperature, probably ok up to about 50℃
            new_data = {
                "type": "coolingpower",
                "id": self._id,
                "value": round(self._heatcapacity*(self._density*flow_rate/60)*(t_out - t_in), 2),
                "units": "W"
            }
            # Add timestamp if we found one attached to the flow rate
            if not timestamp is None:
                new_data["timestamp"] = timestamp
            data.append(new_data)
        self.send(data)
