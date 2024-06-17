import asyncio
import logging
from ctypes import c_int8, c_int16, c_int32, c_float, byref
from datetime import datetime, timezone, timedelta

from datalogd import DataSource

try:
    from picosdk.usbtc08 import usbtc08 as tc08
except (ModuleNotFoundError, ImportError):
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.warning("picosdk module not found. Install it with \"pip install picosdk\" or similar.")
else:
    class PicoTC08DataSource(DataSource):
        """
        Obtain readings from a Pico Technologies TC-08 USB data logging device.

        The drivers and libraries (such as libusbtc08.so on Linux, usbtc08.dll on Windows) from
        PicoTech must be installed into a system library directory, and the ``picosdk`` python
        wrappers package must be on the system (with ``pip install picosdk`` or similar).

        On Linux, read/write permissions to the USB device must be granted. This can be done with a
        udev rule such as:

        .. code-block:: none
            :caption: ``/etc/udev/rules.d/51-picotc08.rules``

            # PicoTech TC-08
            SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="0ce9, ATTRS{idProduct}=="1000", OWNER="root", GROUP="usbusers", MODE="0664"

        where the ``idVendor`` and ``idProduct`` fields should match that listed from running
        ``lsusb``. The ``usbusers`` group must be created and the user added to it:

        .. code-block:: bash

            groupadd usbusers
            usermod -aG usbusers yourusername
        
        A reboot will then ensure permissions are set and the user is a part of the group (or use ``udevadm control --reload`` and re-login).
        To check the permissions have been set correctly, get the USB bus and device numbers from the output of ``lsusb``. For example

        .. code-block:: none
            :caption: ``lsusb``
        
            Bus 001 Device 009: ID 0ce9:1000 Pico Technology 
        
        the bus ID is 001 and device ID is 009. Then list the device using ``ls -l /dev/bus/usb/[bus ID]/[device ID]``

        .. code-block:: none
            :caption: ``ls /dev/bus/usb/001/009 -l``

            crw-rw-r-- 1 root usbusers 189, 9 Mar 29 13:19 /dev/bus/usb/001/009
        
        The middle "rw" and the "usbusers" indicates read-write permissions enabled to any user in
        the usbusers group. You can check which groups your current user is in using the ``groups``
        command.

        Note that you may also allow read-write access to any user (without having to make a
        usbusers group) by changing the lines in the udev rule to ``MODE="0666"`` and removing the
        ``GROUP="usbusers"`` part.

        The ``interval`` parameter determines how often data will be obtained from the sensors, in
        seconds. The minimum interval time is about 0.2 s for a single probe and 0.9 s for all
        eight.

        The ``mains_rejection`` parameter filters out either 50 Hz or 60 Hz interference from mains
        power. The frequency is selected as either ``"50Hz"`` or ``"60Hz"``.

        The ``probes`` parameter is a list of probe to initialise. Each element is itself a list of
        the form ``[number, label, type, units]``, where probe numbers are unique integers from 1 to
        8 corresponding to an input channel on the device. Probe labels can be any valid string.
        Valid probe thermocouple types are ``"B"``, ``"E"``, ``"J"``, ``"K"``, ``"N"``, ``"R"``,
        ``"S"``, ``"T"``, or ``"X"``, where ``"X""`` indicates a raw voltage reading. Units are one
        of Celsius, Fahrenheit, Kelvin, Rankine specified as ``"C"``, ``"F"``, ``"K"`` or ``"R"``.
        For the ``"X"`` probe type, readings will always be returned in millivolts.

        If the device cannot be found or initialised, or the device is unplugged during operation,
        regular reattempts will be performed. Note that this means that an exception will not be
        raised if the device cannot be found.

        :param interval: Time interval between readings, in seconds.
        :param mains_rejection: Mains power filter frequency.
        :param probes: List of probes and configuration parameters.
        """
        def __init__(self, sinks=[], interval=1.0, mains_rejection="50Hz", probes=[
                [1, "Channel_1", "K", "C"],
                [2, "Channel_2", "K", "C"],
                [3, "Channel_3", "K", "C"],
                [4, "Channel_4", "K", "C"],
                [5, "Channel_5", "K", "C"],
                [6, "Channel_6", "K", "C"],
                [7, "Channel_7", "K", "C"],
                [8, "Channel_8", "K", "C"],
            ]):
            super().__init__(sinks=sinks)
            self._log = logging.getLogger("PicoTC08")
            # Store requested device settings to use during later initialisation
            self._req_interval = interval
            self._req_mains_rejection = mains_rejection
            self._req_probes = probes
            # Handle to opened device (means no device opened)
            self._handle = 0
            # Dictionary describing configured probes
            self._probes = {}
            # Configured sampling time interval, in seconds
            self._interval = self._req_interval
            # Get reference to event loop and schedule task (note loop probably hasn't started yet)
            self._loop = asyncio.get_event_loop()
            self._connection_task = self._loop.create_task(self._connect_tc08())  # For python 3.8+: , name="PicoTC08DataSource Connector")
            self._acquisition_task = None


        async def _connect_tc08(self):
            """
            Coroutine to attempt to find and connect to device over serial port.
            """
            # If a device handle is present, attempt to close the device first before reconnecting
            if self._handle > 0: tc08.usb_tc08_close_unit(self._handle)
            # Loop continuously attempting to connect to the device
            self._log.info("Searching for PicoTech TC-08 device.")
            while True:
                self._log.debug("Attempting to open TC-08 device.")
                self._handle = tc08.usb_tc08_open_unit()
                if self._handle > 0:
                    self._log.debug("TC-08 device found.")
                    # A unit was opened successfully
                    # Set mains power frequency rejection
                    tc08.usb_tc08_set_mains(self._handle, 1 if self._req_mains_rejection == "60Hz" else 0)
                    # Configure each specified channel, add configured probes to dictionary by channel
                    self._probes = {}
                    for i, probe in enumerate(self._req_probes):
                        try:
                            probe_n = int(probe[0])
                            probe_label = str(probe[1])
                            probe_type = str(probe[2])[0]
                            probe_units = str(probe[3])[0]
                            status = tc08.usb_tc08_set_channel(self._handle, probe_n, ord(probe_type))
                            if status == 1:
                                self._probes[probe_n] = {"type": probe_type, "label": probe_label, "units": probe_units}
                                self._log.info(f"Configured TC-08 channel {probe_n} as type {probe_type}.")
                            else:
                                self._log.error(f"Error configuring TC-08 channel {probe_n} as type {probe_type}.")
                        except Exception as ex:
                            self._log.exception("Error configuring TC-08 channel using probe configuration \"{probe}\"")
                    # Should check that at least one probe was configured...
                    if len(self._probes) <= 0:
                        # No probes configured successfully (configuration file error?), abort connection attempt
                        self._log.error("No TC-08 channels were successfully configured, aborting connection.")
                        tc08.usb_tc08_close_unit(self._handle)
                        self._handle = 0
                        return False
                    # Get minimum possible sampling interval, in ms
                    interval = max(int(1000*self._req_interval), tc08.usb_tc08_get_minimum_interval_ms(self._handle))
                    # Start the device
                    self._log.debug("Starting TC-08 device.")
                    interval = tc08.usb_tc08_run(self._handle, interval)
                    if interval == 0:
                        # Something went wrong starting the device, but retry later
                        self._log.warning("Error starting PicoTech TC-08 device, will retry.")
                        tc08.usb_tc08_close_unit(self._handle)
                        self._handle = 0
                    else:
                        self._log.debug("Starting TC-08 acquisition.")
                        # Everything seems OK, start the acquisition coroutine
                        self._interval = interval/1000
                        # Record local time of acquisition start
                        self._time_start = datetime.now(timezone.utc).astimezone()
                        self._acquistion_task = self._loop.create_task(self._acquire_data())  # For python 3.8+: , name="PicoTC08DataSource Acquisition")
                        return True
                # No unit found, device busy, error opening device etc. Wait a bit before retrying
                self._log.debug("No TC-08 units found or configured successfully, will retry.")
                try:
                    await asyncio.sleep(5.0)
                except asyncio.CancelledError:
                    return True


        async def _acquire_data(self):
            """
            Coroutine to acquire data from the TC-08 streaming buffer.
            """
            while True:
                data = []
                for probe_n, probe in self._probes.items():
                    temps = (c_float * 128)()
                    times = (c_int32 * 128)()
                    overflow = c_int16()
                    count = tc08.usb_tc08_get_temp(
                        self._handle,
                        byref(temps),
                        byref(times),
                        128,
                        byref(overflow),
                        probe_n,
                        "CFKR".index(probe["units"]) if probe["units"] in "CFKR" else 0,
                        1)
                    if count < 0:
                        self._log.warning("Error acquiring data from Pico TC-08, will retry connection.")
                        # Closing sometimes seems to trigger a segfailt in the PicoTech library...
                        #tc08.usb_tc08_close_unit(self._handle)
                        self._handle = 0
                        self._connection_task = self._loop.create_task(self._connect_tc08())  # For python 3.8+: , name="PicoTC08DataSource Connector")
                        return False
                    # Loop through each record
                    for i in range(count):
                        data.append({
                            "timestamp" : (self._time_start + timedelta(milliseconds=times[i])).isoformat(),
                            "type" : "analog" if probe["type"] == "X" else "temperature",
                            "source" : "TC-08",
                            "id" : probe_n,
                            "label" : probe["label"],
                            "probe" : probe["type"],
                            "units" : "mV" if probe["type"] == "X" else probe["units"],
                            "value": temps[i]})
                self.send(data)
                # Reschedule next update
                try:
                    await asyncio.sleep(self._interval)
                except asyncio.CancelledError:
                    return True


        def close(self):
            """
            Close the connection to the Pico TC-08 device.
            """
            if (not self._connection_task is None):
                self._connection_task.cancel()
            if (not self._acquisition_task is None):
                self._acquisition_task.cancel()
            if self._handle:
                self._log.info("Closing PicoTech TC-08.")
                # Note, occasional segfault in PicoTech library when closing...
                tc08.usb_tc08_close_unit(self._handle)
                self._handle = 0

