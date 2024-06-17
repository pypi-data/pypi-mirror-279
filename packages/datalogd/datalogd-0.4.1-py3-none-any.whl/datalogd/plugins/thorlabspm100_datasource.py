import asyncio
import logging
from enum import Enum

from datalogd import DataSource

try:
    import pyvisa
    from ThorlabsPM100 import ThorlabsPM100
except (ModuleNotFoundError, ImportError):
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.warning("ThorlabsPM100 and/or visa module not found. Install it with \"pip install pyvisa pyvisa-py pyusb ThorlabsPM100\" or similar. A VISA backend must also be present, use pyvisa-py if the native NI libraries are not installed.")
else:
    # Required modules present, continue loading rest of this module

    class ThorlabsPMDataSource(DataSource):
        """
        Provide data from a Thorlabs laser power meter.

        This uses the VISA protocol over USB. On Linux, read/write permissions to the power meter
        device must be granted. This can be done with a udev rule such as:

        .. code-block:: none
            :caption: ``/etc/udev/rules.d/52-thorlabs-pm.rules``

            # Thorlabs PM100D
            SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="1313", ATTRS{idProduct}=="8078", OWNER="root", GROUP="plugdev", MODE="0664"
            # Thorlabs PM400
            SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="1313", ATTRS{idProduct}=="8075", OWNER="root", GROUP="plugdev", MODE="0664"
            # Thorlabs PM16 Series
            SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="1313", ATTRS{idProduct}=="807c", OWNER="root", GROUP="plugdev", MODE="0664"


        where the ``idVendor`` and ``idProduct`` fields should match that listed from running
        ``lsusb``. The ``plugdev`` group must be created and the user added to it:

        .. code-block:: bash

            groupadd plugdev
            usermod -aG plugdev yourusername

        A reboot will then ensure permissions are set and the user is a part of the group (or use ``udevadm control --reload`` and re-login).
        To check the permissions have been set correctly, get the USB bus and device numbers from the output of ``lsusb``. For example

        .. code-block:: none
            :caption: ``lsusb``
        
            Bus 001 Device 010: ID 1313:8075 ThorLabs PM400 Handheld Optical Power/Energy Meter
        
        the bus ID is 001 and device ID is 010. Then list the device using ``ls -l /dev/bus/usb/[bus ID]/[device ID]``

        .. code-block:: none
            :caption: ``ls /dev/bus/usb/001/010 -l``

            crw-rw-r-- 1 root plugdev 189, 9 Mar 29 13:19 /dev/bus/usb/001/010
        
        The middle "rw" and the "plugdev" indicates read-write permissions enabled to any user in
        the plugdev group. You can check which groups your current user is in using the ``groups``
        command.

        Note that you may also allow read-write access to any user (without having to use/create a
        plugdev group) by changing the lines in the udev rule to ``MODE="0666"`` and removing the
        ``GROUP="plugdev"`` part.

        :param serial_number: Serial number of power meter to use. If ``None``, will use the first device found.
        :param usb_vid: USB vendor ID (0x1313 or 4883 for Thorlabs).
        :param usb_pid: USB product ID (0x8078 for PM100D, 0x8075 for PM400).
        :param interval: How often to poll the sensors, in seconds.
        """
        def __init__(self, sinks=[], serial_number=None, usb_vid="0x1313", usb_pid="0x8078", interval=1.0):
            super().__init__(sinks=sinks)
            self._log = logging.getLogger("ThorlabsPMDataSource")
            self.interval = interval

            self._serial_number = serial_number
            self._usb_vid = usb_vid
            self._usb_pid = usb_pid

            self._inst = None
            self._pm = None
            self._serial_number = None

            self._loop = asyncio.get_event_loop()
            self._connection_task = self._loop.create_task(self._connect_pm()) # python 3.8+: , name="ThorlabsPMDataSource Connector")


        async def _connect_pm(self):
            """
            Coroutine to attempt connection to a Thorlabs power meter.
            """
            self._log.info("Searching for Thorlabs PM device...")
            self._rm = pyvisa.ResourceManager()
            while True:
                if self._rm.visalib.library_path in ("py", "unset"):
                    # Native python VISA library, USB VID and PID in decimal, has extra field
                    # Here, 4883 == vendorID == 0x1313, 32888 == productID == 0x8078
                    try:
                        vid = int(self._usb_vid, 16)
                        pid = int(self._usb_pid, 16)
                    except ValueError as ex:
                        pass
                    device_string = f"USB0::{vid}::{pid}::{self._serial_number if self._serial_number else '?*'}::0::INSTR"
                else:
                    # NI VISA library (probably) in use, USB VID and PID are in hex, also extra field missing
                    device_string = f"USB0::{vid}::{pid}::{self._serial_number if self._serial_number else '?*'}::INSTR"
                self._log.debug(f"Looking for VISA device: {device_string}")
                res = self._rm.list_resources(device_string)
                if len(res) == 0:
                    self._log.debug("Could not find a Thorlabs PM device{}. Check USB device permissions and usb_pid parameter.".format(f" with serial {self._serial_number}" if self._serial_number else ""))
                    self._inst = None
                    self._pm = None
                    self._serial_number = None
                else:
                    try:
                        self._inst = self._rm.open_resource(res[0])
                        self._pm = ThorlabsPM100(self._inst)
                        self._serial_number = self._inst.resource_info.resource_name.split("::")[3]
                        self._log.info(f"Initialised Thorlabs PM device: {self._serial_number}.")
                        # Queue first call of update routine and break out of connect loop
                        self._loop.create_task(self._read_power())
                        break
                    except Exception as ex:
                        self._log.warning("Could not initialise Thorlabs PM device: {}".format(ex))
                # No device, try again in a little while
                await asyncio.sleep(5)
        

        def close(self):
            """
            Close the connection to the power meter.
            """
            if self._rm is not None:
                self._rm.close()


        async def _read_power(self):
            """
            Coroutine to read power and send data to any connected sinks.
            """
            while True:
                try:
                    data = {"type": "power", "source": "ThorlabsPM", "id": self._serial_number, "value": self._pm.read}
                    self.send(data)
                except Exception as ex:
                    self._log.warning("Could not read power from Thorlabs PM device. Will attempt to reconnect.")
                    await asyncio.sleep(2)
                    self._loop.create_task(self._connect_pm()) # python 3.8+: , name="ThorlabsPMDataSource Connector")
                    return
                await asyncio.sleep(self.interval)


    class ThorlabsPM100DataSource(ThorlabsPMDataSource):
        """
        Provide data from a Thorlabs PM100 laser power meter.

        This is a wrapper around
        :class:`~datalogd.plugins.thorlabspm100_datasource.ThorlabsPMDataSource` with the
        appropriate USB PID used as default. See its documentation regarding configuring permissions
        for accessing the USB device.

        :param serial_number: Serial number of power meter to use. If ``None``, will use the first
            device found.
        :param interval: How often to poll the sensors, in seconds.
        """
        def __init__(self, sinks=[], serial_number=None, interval=1.0):
            super().__init__(sinks=sinks, usb_vid="0x1313", usb_pid="0x8078", serial_number=serial_number, interval=interval)


    class ThorlabsPM400DataSource(ThorlabsPMDataSource):
        """
        Provide data from a Thorlabs PM400 laser power meter.

        This is a wrapper around
        :class:`~datalogd.plugins.thorlabspm100_datasource.ThorlabsPMDataSource` with the
        appropriate USB PID used as default. See its documentation regarding configuring permissions
        for accessing the USB device.

        :param serial_number: Serial number of power meter to use. If ``None``, will use the first
            device found.
        :param interval: How often to poll the sensors, in seconds.
        """
        def __init__(self, sinks=[], serial_number=None, interval=1.0):
            super().__init__(sinks=sinks, usb_vid="0x1313", usb_pid="0x8075", serial_number=serial_number, interval=interval)


    class ThorlabsPM16DataSource(ThorlabsPMDataSource):
        """
        Provide data from a Thorlabs PM16 laser power meter.

        This is a wrapper around
        :class:`~datalogd.plugins.thorlabspm100_datasource.ThorlabsPMDataSource` with the
        appropriate USB PID (0x807c) used as default. See its documentation regarding configuring permissions
        for accessing the USB device.

        :param serial_number: Serial number of power meter to use. If ``None``, will use the first
            device found.
        :param interval: How often to poll the sensors, in seconds.
        """
        def __init__(self, sinks=[], serial_number=None, interval=1.0):
            super().__init__(sinks=sinks, usb_vid="0x1313", usb_pid="0x807c", serial_number=serial_number, interval=interval)