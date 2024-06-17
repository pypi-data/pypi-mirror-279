import logging
from datetime import datetime, timezone

from datalogd import DataSink, listify

try:
    from influxdb_client import InfluxDBClient
    #from influxdb_client.client.write_api import SYNCHRONOUS
except (ModuleNotFoundError, ImportError):
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.warning("influxdb_client module not found. Install it with \"pip install influxdb_client\" or similar.")
else:
    # Required modules present, continue loading rest of this module

    class InfluxDB2DataSink(DataSink):
        """
        Connection to a InfluxDB 2.x (or 1.8+) database for storing time-series data.

        Note that this doesn't actually run the InfluxDB database service, but simply connects to an
        existing InfluxDB database via a network (or localhost) connection. See the `getting started
        <https://docs.influxdata.com/influxdb/v2.4/get-started/>`__ documentation for details on
        configuring a new database server.

        The ``url`` parameter should be a string specifying the protocol, server ip or name, and
        port. For example, ``url="http://localhost:8086"``.

        The authentication ``token`` parameter needs to be specified to allow commits to the
        database. See the `token <https://docs.influxdata.com/influxdb/v2.4/security/tokens/>`__
        documentation to see how to create and obtain tokens.

        Parameters for ``org``, ``bucket`` must correspond to a valid organisation and bucket
        created in the database for which the authentication token is valid. See the documentation
        for `organisations <https://docs.influxdata.com/influxdb/v2.4/organizations/>`__ and
        `buckets <https://docs.influxdata.com/influxdb/v2.4/organizations/buckets/>`__ for details.

        The ``measurement`` parameter specifies the data point measurement (or "table") the data
        will be entered into, and does not need to already exist. See the documentation on `data
        elements
        <https://docs.influxdata.com/influxdb/v2.4/reference/key-concepts/data-elements/#measurement>`__
        for details.

        A ``run_id`` parameter may be passed which will be added as a tag to the data points. It may
        be used to identify data obtained from this particular run of the data logging session. If
        no value is provided, a value will be generated from a YYYYMMDD-HHMMSS formatted time stamp.

        The data point field key will be attempted to be determined automatically from the incoming
        data dictionaries. If the data dictionary contains a ``name`` or ``label`` key, then its
        value will be used as the database point field key. Alternatively, a field key will be
        generated from the values of ``type`` and ``id`` if present. Finally, a default field key of
        ``data`` will be used. To instead specify the data entry which should provide the field key,
        specify it as the ``field_key`` parameter. If the field is specified by a parameter or taken
        from a name or label, then those will not also be included in the entry's database keys.
        However, if the field name is automatically built from type and id values, these will still
        be part of the entries keys.

        Similarly, the data point field value will use the value from the incoming data dictionary's
        ``value`` field if present. To instead specify the data entry which should provide the field
        value, specify it as the ``field_value`` parameter. The value won't also appear in the
        database entry's keys.

        :param url: Protocol, host name or IP address, and port number of InfluxDB server.
        :param token: API token used to authenticate with the InfluxDB server.
        :param org: Name of InfluxDB organisation in which to store data.
        :param bucket: Name of InfluxDB bucket in which to store data.
        :param measurement: Name for the InfluxDB measurement session.
        :param run_id: A tag to identify commits from this run.
        :param field_key: A field from the incoming data used to determine the data point field key.
        :param field_value: A field from the incoming data used to determine the data point field value.
        """
        def __init__(self, url="http://localhost:8086", token="", org="default", bucket="default", measurement="measurement", run_id=None, field_key=None, field_value=None):
            self.log = logging.getLogger("InfluxDB2DataSink")
            try:
                self.client = InfluxDBClient(url, token=token, org=org)
            except Exception as ex:
                self.log.exception("Unable to make connection to InfluxDB database.")
            self.write_api = self.client.write_api()
            self.org = org
            self.bucket = bucket
            self.measurement = measurement
            if run_id is None:
                self.run_id = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d-%H%M%S")
            else:
                self.run_id = run_id
            self.field_key = field_key
            self.field_value = field_value

        def receive(self, data):
            """
            Commit data to the InfluxDB database.

            Multiple items of data can be submitted at once if ``data`` is a
            list. A typical format of ``data`` would be::

                [
                    {'type': 'temperature', 'id': '0', 'value': 22.35},
                    {'type': 'humidity', 'id': '0', 'value': 55.0},
                    {'type': 'temperature', 'id': '1', 'value': 25.80},
                ]

            In the above case (assuming the ``field_key`` and ``field_value`` parameters were not
            supplied when initialising the plugin), the InfluxDB data point field would be generated
            as ``<type>_<id> = <value>``, and only the global ``run_id`` parameter would be entered
            into the data point keys.

            If a ``name`` or ``label`` field is present, then it will instead be used as the
            InfluxDB data point field key. For example::

                [
                    {'name': 'Temperature', 'type': 'temperature', 'id': '0', 'value': 22.35},
                    {'name': 'Humidity', 'type': 'humidity', 'id': '0', 'value': 55.0},
                ]
            
            In this case, the InfluxDB data point field would be generated as ``<name> = <value>``,
            and the remaining fields (``type`` and ``id``) would be added as data point field keys,
            along with the ``run_id``.


            A timestamp for the commit will be generated using the current system clock if a
            "timestamp" field does not already exist.

            :param data: Data to commit to the database.
            """
            if data is None or data == []: return
            if not self.client.ping():
                self.log.debug("No database connection, data won't be stored.")
                return
            data = listify(data)

            # Loop through each element in data list
            for d in data:
                if type(d) == dict:
                    # Don't modify the original dict data
                    d = d.copy()

                # Start building the structure to enter into database
                datapoint = {
                    "measurement": self.measurement,
                    "tags": {"run_id": self.run_id},
                    "fields": {},
                }

                # Attempt to determine a suitable field name
                if self.field_key is not None and self.field_key in d.keys():
                    # If database field key was specified, use it
                    k = str(d[self.field_key])
                elif "name" in d.keys():
                    # Format as <name> = <value>
                    k = str(d["name"])
                elif "label" in d.keys():
                    # Format as <label> = <value>
                    k = str(d["label"])
                elif "type" in d.keys():
                    # Format as <type>_<id> = <value> (but keep type, id as tags)
                    k = str(d["type"]) + ("_" + str(d["id"])) if "id" in d.keys() else ""
                else:
                    k = "data"
                # Attempt to determine the correct field value
                if self.field_value is not None and self.field_value in d.keys():
                    # If database field value was specified, use it
                    v = str(d[self.field_value])
                elif "value" in d.keys():
                    v = d["value"]
                else:
                    v = None
                # Add the field to the data point
                datapoint["fields"][k] = v

                # Use the provided timestamp if available, else create one
                if "timestamp" in d.keys():
                    timestamp = d.pop("timestamp")
                    if type(timestamp) == datetime:
                        datapoint["time"] = timestamp.isoformat()
                    else:
                        datapoint["time"] = timestamp
                else:
                    datapoint["time"] =  datetime.now(timezone.utc).astimezone().isoformat()
                
                # Add any entries which weren't used in the field to the tags
                datapoint["tags"].update(d)
                
                # Send data point out to database
                try:
                    self.log.debug(f"Committing: {datapoint}")
                    self.write_api.write(self.bucket, self.org, datapoint)
                except Exception as ex:
                    self.log.warning("Unable to commit data to InfluxDB database.")

        def close(self):
            """
            Close the connection to the database.
            """
            try:
                self.write_api.close()
            except:
                pass
            try:
                self.client.close()
            except:
                pass
