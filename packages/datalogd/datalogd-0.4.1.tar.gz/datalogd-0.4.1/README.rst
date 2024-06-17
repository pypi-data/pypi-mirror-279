datalogd - A Data Logging Daemon
================================

datalogd is a data logging daemon service which uses a source/filter/sink plugin architecture to
allow extensive customisation and maximum flexibility. There are no strict specifications or
requirements for data types, but typical examples would be readings from environmental sensors such
as temperature, humidity, voltage or the like.

The user guide and API documentation can be read online at `Read the Docs
<https://datalogd.readthedocs.io/>`_. Source code is available on `GitLab
<https://gitlab.com/ptapping/datalogd>`_.

Custom data sources, filters, or sinks can be created simply by extending an existing
``DataSource``, ``DataFilter``, or ``DataSink`` python class and placing it in a plugin directory.

Data sources, filters, and sinks can be arbitrarily connected together with a connection digraph
described using the `DOT graph description language
<https://en.wikipedia.org/wiki/DOT_(graph_description_language)>`_.

Provided data source plugins include:
  * ``LibSensorsDataSource`` - (Linux) computer motherboard sensors for temperature, fan speed,
    voltage etc.
  * ``SerialDataSource`` - generic data received through a serial port device. Arduino code for
    acquiring and sending data through its USB serial connection is also included.
  * ``RandomWalkDataSource`` - testing or demonstration data source using a random walk algorithm.
  * ``ThorlabsPMDataSource`` - laser or light power measurement using the Thorlabs PM100 or PM400
    power meter.
  * ``PicoTC08DataSource`` - thermocouple or other sensor measurements using the Pico Technologies
    TC-08 USB data logger.

Provided data sink plugins include:
  * ``PrintDataSink`` - print to standard out or standard error streams.
  * ``FileDataSink`` - write to a file.
  * ``LoggingDataSink`` - simple output to console using python logging system.
  * ``InfluxDB2DataSink`` - InfluxDB 2.x database system specialising in time-series data.
  * ``MatplotlibDataSink`` - create a plot of data using matplotlib.
  * ``PyqtgraphDataSink`` - plot incoming data in realtime in a pyqtgraph window.

Provided data filter plugins include:
  * ``SocketDataFilter`` - bridge a connection over a network socket.
  * ``KeyValDataFilter`` - selecting or discarding data entries based on key-value pairs.
  * ``TimeStampDataFilter`` - adding timestamps to data.
  * ``AggregatorDataFilter`` - aggregating multiple data readings into a fixed-size buffer.
  * ``CSVDataFilter`` - format data as a table of comma separated values.
  * ``PolynomialFunctionDataFilter`` - apply a polynomial function to a value.
  * ``FlowSensorCalibrationDataFilter`` - convert a pulse rate into liquid flow rate.
  * ``CoolingPowerDataFilter`` - calculate power dissipation into a liquid using temperatures and
    flow rate.

See the Data Logging Recipes section in the documentation for examples of how to link various data
sources, filters, and sinks to make something useful.