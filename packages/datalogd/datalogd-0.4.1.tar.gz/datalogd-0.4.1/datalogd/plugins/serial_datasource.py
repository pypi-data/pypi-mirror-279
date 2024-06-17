import asyncio
import logging
import re
import json

from datalogd import parse_dot_json
from datalogd import DataSource

try:
    import serial, serial.tools.list_ports, serial.threaded, serial_asyncio
except (ModuleNotFoundError, ImportError):
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.warning("Serial modules not found. Install with \"pip install pyserial pyserial-asyncio\" or similar.")
else:
    # Required modules present, continue loading rest of this module

    class SerialDataSource(DataSource):
        """
        Receive data from an Arduino connected via a serial port device.

        .. container:: toggle

            .. container:: header

                See the ``datalog_arduino.ino`` sketch for matching code to run
                on a USB-connected Arduino.

            .. literalinclude:: ../../../arduino/datalog/datalog.ino
                :language: c++
                :caption: ``datalog.ino``

        Other serial-connected devices should work with this class if they conform to the expected
        communications protocol. Message data should be encoded in a JSON format. For example

        .. code-block::

            {"board":"A","timestamp":"1601251","message":"measurement","data":[{"type":"temperature","source":"A","id":"A_TC0","value":"20.25","units":"C"}]}

        which describes a single temperature measurement data point, encapsulated by a message
        header. Note that the values encoded in the ``"value"`` field will be attempted to be
        decoded using the same logic as :data:`~datalogd.parse_dot_json`, so that ``"20.25"`` will
        be interpreted as the equivalent python float, and special values such as ``None`` and
        ``inf`` are supported.

        If the connection to the serial device cannot be established or is interrupted, regular
        reattempts will be performed. Note that this means an exception will not be raised if the
        serial device cannot be found.

        :param port:     Path of serial device to use. A partial name to match
            can also be provided, such as "usb".
        :param board_id: ID label provided by the Arduino data logging board, to
            select a particular device in case multiple boards are connected.
        """

        class SerialHandler(serial.threaded.LineReader):
            """
            A class used as a :mod:`asyncio` :class:`~asyncio.Protocol` to handle
            lines of text received from the serial device.

            :param parent: The parent :class:`~datalogd.plugins.serial_datasource.SerialDataSource` class.
            """
            def __init__(self, parent):
                super().__init__()
                self.parent = parent

            def handle_line(self, line):
                """
                Accept one line of text, parse it to extract data, and pass the
                data on to any connected sinks.

                :param line: Line of text to process.
                """
                try:
                    j = json.loads(line)
                    if j["message"] == "measurement":
                        self.parent.log.debug(f"Received: {j['data']}")
                        # All data is in string form, attempt to convert values to something more appropriate
                        try:
                            for d in j["data"]:
                                if "value" in d.keys():
                                    d["value"] = parse_dot_json(d["value"])
                        except Exception as ex:
                            self.parent.log.warning("Unable to parse serial data.", exc_info=True)
                        self.parent.send(j["data"])
                except Exception as ex:
                    self.parent.log.warning(f"Error interpreting serial data: {ex}\nFailing line was:\n{line}")

            def connection_lost(self, exc):
                self.parent.log.warning("Serial connection lost, will attempt to reconnect.")
                self.parent._connection_task = self.parent.loop.create_task(self.parent._connect_serial_port())


        def __init__(self, sinks=[], port=None, board_id=None, vid=None, pid=None, serial_number=None, location=None):
            super().__init__(sinks=sinks)
            self.log = logging.getLogger("SerialDataSource")
            #: Identifying name, PID, VID etc for the requested serial port
            self._port_identifiers = {
                "serial_port": port,
                "vid": vid,
                "pid": pid,
                "serial_number": serial_number,
                "location": location,
            }
            self.sp = None
            self.board_id = board_id
            # Get reference to event loop and schedule task (but loop probably isn't started yet)
            self.loop = asyncio.get_event_loop()
            self._connection_task = self.loop.create_task(self._connect_serial_port()) # python 3.8+: , name="SerialDataSource Connector")


        async def _connect_serial_port(self):
            """
            Coroutine to attempt to find and connect to device over serial port.
            """
            while True:
                # Loop continuously attempting to connect to correct serial device
                self.sp = None
                # If serial_port not specified, search for a device
                if self._port_identifiers["serial_port"] is None:
                    self.log.debug(f"Searching for serial device with vid={self._port_identifiers['vid']}, pid={self._port_identifiers['pid']}, serial_number={self._port_identifiers['serial_number']}, location={self._port_identifiers['location']}")
                    portlist = find_devices(
                        vid=self._port_identifiers["vid"],
                        pid=self._port_identifiers["pid"],
                        serial_number=self._port_identifiers["serial_number"],
                        location=self._port_identifiers["location"]
                    )
                else:
                    # Make list of available serial ports (matching given port name)
                    portlist = list(serial.tools.list_ports.grep(self._port_identifiers["serial_port"]))
                if len(portlist) == 0:
                    self.log.warning("No serial ports found matching given critera.")

                # Iterate though serial ports looking for requested logging board
                for p in portlist:
                    try:
                        self.sp = serial.Serial(p.device, 115200, timeout=2)
                        # Read and discard potentially partial line
                        self.sp.readline()
                        # Read and attempt json decode of next (complete) line
                        j = json.loads(self.sp.readline().decode("ascii").strip())
                        if j["board"] and j["timestamp"] and j["message"]:
                            # Looks like one of our logging boards
                            if self.board_id is None or j["board"] == str(self.board_id):
                                self.log.info(f"Found board \"{j['board']}\" at {p.device}")
                                break
                            else:
                                self.log.info(f"Found board \"{j['board']}\" at {p.device} (but is not requested board \"{self.board_id}\")")
                                self.sp.close()
                                self.sp = None
                                continue
                    except Exception as ex:
                        # Error opening serial device, or not a logging board
                        self.log.info(f"Error querying board at {p.device} (port error or received invalid data)")
                        try:
                            self.sp.close()
                        except:
                            pass
                        self.sp = None

                # We should now have opened the serial port to requested board...
                if self.sp is None:
                    # ...but failed, so try again in a little while
                    await asyncio.sleep(5.0)
                else:
                    # All seems OK, start the serial reader coroutine and stop connection attempts
                    asyncio.create_task(self._create_reader_coroutine()) # python 3.8+: , name="SerialDataSource Reader")
                    break


        async def _create_reader_coroutine(self):
            """
            Coroutine to create the serial port transport and protocol class instances.
            """
            protocol = self.SerialHandler(parent=self)
            transport = serial_asyncio.SerialTransport(self.loop, protocol, self.sp)
            return (transport, protocol)


        def close(self):
            """
            Close the serial port connection.
            """
            if not self.sp is None:
                try:
                    self.sp.close()
                finally:
                    self.sp = None


def find_device(vid=None, pid=None, manufacturer=None, product=None, serial_number=None, location=None):
    """
    Search attached serial ports for a specific device.

    The first device found matching the criteria will be returned. Because there is no consistent
    way to identify serial devices, various parameters are available. The default is to return the
    first found serial port device. A more specific device can be selected using a unique
    combination of the parameters.

    The USB vendor (``vid``) and product (``pid``) IDs are exact matches to the numerical values,
    for example ``vid=0x2e8a`` or ``vid=0x000a``. The remaining parameters are strings specifying a
    regular expression match to the corresponding field. For example ``serial_number="83"`` would
    match devices with serial numbers starting with 83, while ``serial_number=".*83$"`` would match
    devices ending in 83. A value of ``None`` means that the parameter should not be considered,
    however an empty string value (``""``) is subtly different, requiring the field to be present,
    but then matching any value.

    Be aware that different operating systems may return different data for the various fields,
    which can complicate matching.

    To get a list of serial ports and the relevant data fields see the :data:`list_devices` method.

    :param vid: Numerical USB vendor ID to match.
    :param pid: Numerical USB product ID to match.
    :param manufacturer: Regular expression to match to a device manufacturer string.
    :param product: Regular expression to match to a device product string.
    :param serial_number: Regular expression to match to a device serial number.
    :param location: Regular expression to match to a device physical location (eg. USB port).
    :returns: First :class:`~serial.tools.list_ports.ListPortInfo` device which matches given criteria.
    """
    for p in serial.tools.list_ports.comports():
        if (vid is not None) and not vid == p.vid: continue
        if (pid is not None) and not pid == p.pid: continue
        if (manufacturer is not None) and ((p.manufacturer is None) or not re.match(manufacturer, p.manufacturer)): continue
        if (product is not None) and ((p.product is None) or not re.match(product, p.product)): continue
        if (serial_number is not None) and ((p.serial_number is None) or not re.match(serial_number, p.serial_number)): continue
        if (location is not None) and ((p.location is None) or not re.match(location, p.location)): continue
        return p


def find_devices(vid=None, pid=None, manufacturer=None, product=None, serial_number=None, location=None):
    """
    Search attached serial ports for specific devices.

    Similar to :data:`~find_device` exce[pt returns a list of all matching devices. A list is returned
    even in a single device matches. An empty list is returned if no devices match.

    :param vid: Numerical USB vendor ID to match.
    :param pid: Numerical USB product ID to match.
    :param manufacturer: Regular expression to match to a device manufacturer string.
    :param product: Regular expression to match to a device product string.
    :param serial_number: Regular expression to match to a device serial number.
    :param location: Regular expression to match to a device physical location (eg. USB port).
    :returns: List of :class:`~serial.tools.list_ports.ListPortInfo` devices which match given criteria.
    """
    port_list = []
    for p in serial.tools.list_ports.comports():
        if (vid is not None) and not vid == p.vid: continue
        if (pid is not None) and not pid == p.pid: continue
        if (manufacturer is not None) and ((p.manufacturer is None) or not re.match(manufacturer, p.manufacturer)): continue
        if (product is not None) and ((p.product is None) or not re.match(product, p.product)): continue
        if (serial_number is not None) and ((p.serial_number is None) or not re.match(serial_number, p.serial_number)): continue
        if (location is not None) and ((p.location is None) or not re.match(location, p.location)): continue
        port_list.append(p)
    return port_list


def list_devices():
    """
    Return a string listing all detected serial devices and any associated identifying properties.

    The manufacturer, product, vendor ID (vid), product ID (pid), serial number, and physical device
    location are provided. These can be used as parameters to :meth:`find_device` or the constructor
    of a :class:`~serial_datasource.SerialDataSource` class to identify and select a specific serial device.

    :returns: String listing all serial devices and their details.
    """
    result = ""
    for p in serial.tools.list_ports.comports():
        try:
            vid = f"{p.vid:#06x}"
            pid = f"{p.pid:#06x}"
        except:
            vid = p.vid
            pid = p.pid
        result += f"device={p.device}, manufacturer={p.manufacturer}, product={p.product}, vid={vid}, pid={pid}, serial_number={p.serial_number}, location={p.location}\n"
    return result.strip("\n")