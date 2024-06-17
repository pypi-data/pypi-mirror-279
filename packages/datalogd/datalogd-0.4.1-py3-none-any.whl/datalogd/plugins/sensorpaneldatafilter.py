import os
import sys
import logging
import time
from datetime import datetime
from multiprocessing import Process, Queue
import inspect
import asyncio

from datalogd import DataFilter, listify

try:
    from PySide6 import QtCore, QtWidgets, QtGui
    from PySide6.QtUiTools import QUiLoader, loadUiType
    from PySide6.QtCore import Property, QTimer
    from PySide6.QtGui import QGuiApplication, QPalette, QColor
    from PySide6 import QtDesigner
except (ModuleNotFoundError, ImportError):
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.warning("PySide6 module not found. Install it with \"pip install pyside6\" or similar.")
else:
    # Required modules present, continue loading rest of this module
    
    # Add current location to python path so loadUiType can find resources_rc.py
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # Build the tooltip text for SensorWidgets
    def build_sensorwidget_tooltip(data):
        returnstring = ""
        if "sensor_identifier" in data:
            returnstring += f"<h3>{data['sensor_identifier']}</h3>"
        return returnstring + format_data(data, html=True)

    # Return a semi-nice string representation of a dictionary/list/etc
    def format_data(x, html=False, newline=False):
        returnstring = ""
        keytag_open = "<b>" if html else ""
        keytag_close = "</b>" if html else ""
        lineend = "<br>" if html else "\n"
        indent = "&nbsp;&nbsp;" if html else "  "
        if type(x) == dict:
            if newline:
                returnstring += lineend
            else:
                newline = True
            for k, v in sorted(x.items()):
                returnstring += f"{keytag_open}{k}{keytag_close} : {format_data(v, html=html, newline=newline).replace(lineend, lineend + indent)}{lineend}"
            returnstring = returnstring.rpartition(lineend)[0]
        elif type(x) == list:
            for v in x:
                returnstring += f"{format_data(v, html=html, newline=newline)}, "
            returnstring = returnstring[:-2]
        elif type(x) == time.struct_time:
            returnstring += f"{time.strftime('%a, %d %b %Y %H:%M:%S (%Z %z)', x)}"
        else:
            returnstring += f"{x}"
        return returnstring


    class SensorPanelDataFilter(DataFilter):
        """
        A panel of SensorWidgets to display sensor data.
        """
        def __init__(self, sinks=[], **kwargs):
            super().__init__(sinks=sinks)
            #: A Queue for placing data to be sent to the SensorDataPanel process.
            self.panel_input_queue = Queue()
            #: A Queue for the SensorDataPanel process to place data on.
            self.panel_output_queue = Queue()
            # Update kwargs with queues to pass on to the SensorPanel process
            kwargs.update({"data_input_queue": self.panel_input_queue, "data_output_queue": self.panel_output_queue})
            # Get reference to event loop and schedule queue checking task (note loop probably hasn't started yet)
            self._loop = asyncio.get_event_loop()
            self._queue_check_task = self._loop.create_task(self._check_queue()) # python 3.8+: , name="SensorPanelDataFilter data queue check")
            #: Process to run the SensorDataPanel QApplication.
            self.app_process = Process(target=self._exec_qt_app, kwargs=kwargs, name="SensorDataPanel")
            self.app_process.start()
        
        def close(self):
            """
            Signal the Qt application to close when the system is shutting down.
            """
            self.app_process.terminate()
            self.app_process.join()
        
        def receive(self, data):
            """
            Accept the provided ``data`` and pass it to the SensorPanel to display.
            """
            if self.app_process.is_alive():
                data = listify(data)
                self.panel_input_queue.put(data)

        async def _check_queue(self):
            while True:
                while not self.panel_output_queue.empty():
                    try:
                        data = listify(self.panel_output_queue.get(timeout=0.05))
                    except Queue.Empty:
                        break
                    if not data:
                        break
                    self.send(data)
                await asyncio.sleep(0.02)

        def _exec_qt_app(self, **kwargs):
            app = QtWidgets.QApplication()
            # Register the custom SensorWidgets with Qt Designer so they can be loaded by other UIs.
            # Find subclasses of SensorWidgetBase and register them with Qt Designer
            m = sys.modules[__name__]
            for sw_name, sw_class in inspect.getmembers(m, inspect.isclass):
                if issubclass(sw_class, m.SensorWidgetBase) and not sw_class == m.SensorWidgetBase:
                    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
                        sw_class,
                        tool_tip=sw_class.TOOL_TIP,
                        xml=sw_class.XML
                        )
            # Try to change tooltip colour away from unreadable grey-on-yellow
            # (modifying inactive palette colour didn't seem to work)
            app.setStyleSheet("QToolTip { background: #202020; color: white }")
            self.panelwindow = SensorPanel(**kwargs)
            self.panelwindow.show()
            app.exec()


    class SensorWidgetBase():
        """
        Base class for all SensorPanel widgets describing basic functionality.
        """
        def __init__(self, parent=None):
            self._id = ""
            super().__init__()

        @Property(str)
        def identifier(self):
            return self._id
        
        @identifier.setter
        def identifier(self, id=""):
            self._id = id

        def update_data(self, data={}):
            pass


    #: File name for SensorWidget UI file.
    _sensorwidget_ui_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensorwidget.ui")

    class SensorWidget(*loadUiType(_sensorwidget_ui_filename), SensorWidgetBase):

        TOOL_TIP = "A widget to display sensor data"
        XML = "<ui language='c++'><widget class='SensorWidget' name='sensorWidget'></widget></ui>"

        RED = QColor("#c01c28")
        RED_LIGHT = QColor("#f66151")
        YELLOW = QColor("#e5a50a")
        YELLOW_LIGHT = QColor("#f9f06b")
        ORANGE = QColor("#e66100")
        ORANGE_LIGHT = QColor("#ffbe6f")
        GREEN = QColor("#26a269")
        GREEN_LIGHT = QColor("#8ff0a4")
        GREY = QColor("#241f31")
        GREY_LIGHT = QColor("#77767b")
        BLACK = QColor("#000000")

        def __init__(self, parent=None):
            super().__init__(parent=parent)
            #self._log = logging.getLogger(__name__)
            self._name = ""
            self._icon = ""
            self.setupUi(self)
            self.identifier = ""
            self.name = ""
            # Timer to check for missing updates if an update interval is given
            self._interval_timer = QTimer(self)
            self._interval_timer.setSingleShot(True)
            self._interval_timer.timeout.connect(self._interval_exceeded)
            # Flag to indicate whether missing updates are treated as critical
            self._interval_critical = False
            # Flag to indicate whether out of range values are treated as critical
            self._range_critical = False
            self.update_data()
        
        @Property(str)
        def name(self):
            return self._name
        
        @name.setter
        def name(self, name=""):
            self._name = name
            if not name:
                name = self._id
            self.nameQLabel.setText(name)
        
        @Property(str)
        def identifier(self):
            return self._id
        
        @identifier.setter
        def identifier(self, id=""):
            if not id:
                id = self.objectName()
            self._id = id
            if not self._name:
                self.nameQLabel.setText(id)

        @Property(str)
        def icon(self):
            return self._icon
        
        @icon.setter
        def icon(self, icon=""):
            pm = QtGui.QPixmap(f":icons/{icon}")
            if icon and not pm :
                pm = QtGui.QPixmap(f":icons/default")
            self.iconQLabel.setPixmap(pm)
            self._icon = icon

        def update_data(self, data={}):
            # Format value and units
            try:
                units = f" {data['units']}" if "units" in data else ""
                if ("type" in data) and units == " C":
                    # Substitute degree celsius for capital C
                    units = " ℃"
                value = data['value']
                if isinstance(value, float):
                    if value != value:  # == NaN
                        raise ValueError
                    value = f"{value:g}"
                self.valueQLabel.setText(f"{value}{units}")
                self.statusQLabel.setPixmap(QtGui.QPixmap())
                palette = QGuiApplication.palette()
                self.statusQLabel.setPalette(palette)
            except (KeyError, ValueError):
                self.valueQLabel.setText("--")
                self.statusQLabel.setPixmap(QtGui.QPixmap(f":icons/watchdogfault"))
                palette = QGuiApplication.palette()
                palette.setColor(QPalette.Window, SensorWidget.RED if self._range_critical else SensorWidget.ORANGE)
                self.statusQLabel.setPalette(palette)
            
            # Format allowed range
            try:
                low, high = data['range']
                if low == high:
                    # If range isn't actually a range, don't bother filling in values
                    raise ValueError
                if isinstance(low, float):
                    low = f"{low:g}"
                if isinstance(high, float):
                    high = f"{high:g}"
                self.minQLabel.setText(f"{low}")
                self.maxQLabel.setText(f"{high}")
            except (KeyError, ValueError):
                self.minQLabel.setText("")
                self.maxQLabel.setText("")
            
            # Format nominal range
            try:
                low, high = data['nominal']
                if isinstance(low, float):
                    low = f"{low:g}"
                if isinstance(high, float):
                    high = f"{high:g}"
                self.nomQLabel.setText(f"[{low}, {high}]")
            except KeyError:
                self.nomQLabel.setText("")

            # Set indicator (progress) bar as fraction (0-1000) of allowed range
            try:
                value = data['value']
                try:
                    low, high = data['range']
                except KeyError:
                    low, high = data['nominal']
                perthou = max(0, min(1000, int(1000.0*(value - low)/(high - low))))
                self.progressBar.setValue(perthou)
            except (KeyError, ValueError):
                #self._log.exception("Error setting indicator bar.")
                self.progressBar.setValue(1000)
            
            # Set indicator (progress) bar colour depending on value in ranges
            palette = QGuiApplication.palette()
            # Use black text on coloured progress bars
            palette.setColor(QPalette.Text, SensorWidget.BLACK)
            palette.setColor(QPalette.HighlightedText, SensorWidget.BLACK)
            try:
                value = data['value']
                if (value != value) or value in (None, "NaN", "nan", "NAN"):
                    raise ValueError
                try:
                    limit_low, limit_high = data['range']
                except KeyError:
                    limit_low, limit_high = (None, None)
                try:
                    nominal_low, nominal_high = data['nominal']
                except KeyError:
                    nominal_low, nominal_high = (None, None)
                if (not limit_low is None and value < limit_low):
                    # Below low limit, red
                    palette.setColor(QPalette.Base, SensorWidget.RED_LIGHT)
                    palette.setColor(QPalette.Highlight, SensorWidget.RED)
                    self.progressBar.setTextVisible(True)
                    self.progressBar.setFormat("LOW")
                elif (not limit_high is None and value > limit_high):
                    # Above allowed limit
                    if "critical_range" in data and data["critical_range"]:
                        # Out of range is marked critical, red
                        palette.setColor(QPalette.Base, SensorWidget.RED_LIGHT)
                        palette.setColor(QPalette.Highlight, SensorWidget.RED)
                    else:
                        # Out of range, but not marked as critical, orange
                        palette.setColor(QPalette.Base, SensorWidget.ORANGE_LIGHT)
                        palette.setColor(QPalette.Highlight, SensorWidget.ORANGE)
                    self.progressBar.setTextVisible(True)
                    self.progressBar.setFormat("HIGH")
                elif (not nominal_low is None and value < nominal_low):
                    # Below nominal range, yellow
                    palette.setColor(QPalette.Base, SensorWidget.YELLOW_LIGHT)
                    palette.setColor(QPalette.Highlight, SensorWidget.YELLOW)
                    self.progressBar.setTextVisible(True)
                    self.progressBar.setFormat("LOW")
                elif (not nominal_high is None and value > nominal_high):
                    # Above nominal range, yellow
                    palette.setColor(QPalette.Base, SensorWidget.YELLOW_LIGHT)
                    palette.setColor(QPalette.Highlight, SensorWidget.YELLOW)
                    self.progressBar.setTextVisible(True)
                    self.progressBar.setFormat("HIGH")
                else:
                    # Within nominal range, green
                    palette.setColor(QPalette.Base, SensorWidget.GREEN_LIGHT)
                    palette.setColor(QPalette.Highlight, SensorWidget.GREEN)
                    self.progressBar.setTextVisible(False)
            except (KeyError, TypeError, ValueError):
                # Couldn't compare value, grey/black
                palette.setColor(QPalette.Base, SensorWidget.GREY_LIGHT)
                palette.setColor(QPalette.Highlight, SensorWidget.GREY)
                self.progressBar.setTextVisible(True)
                self.progressBar.setFormat("INVALID")
            self.progressBar.setPalette(palette)
            
            # Update icon based on sensor type
            if "type" in data:
                self.icon = data['type']
            else:
                self.icon = "default"

            # Update name
            if "sensor_name" in data:
                self.name = data['sensor_name']

            # Update tooltip
            if data:
                self.setToolTip(build_sensorwidget_tooltip(data))
            else:
                self.setToolTip("No sensor data!")
            
            # Remember if range or updates are marked as critical
            if "critical_range" in data:
                self._range_critical = bool(data["critical_range"])
            else:
                self._range_critical = False
            if "critical_interval" in data:
                self._interval_critical = bool(data["critical_interval"])
            else:
                self._interval_critical = False
            
            # An update was received, stop any running interval timer
            self._interval_timer.stop()
            # If an update interval specified, start the interval timer
            try:
                if "interval" in data:
                    # Give an extra 25% margin of error on interval time (in milliseconds)
                    self._interval_timer.start(1250*int(data["interval"]))
            except (ValueError, TypeError):
                pass


        def _interval_exceeded(self):
            """
            Timer set for update interval has expired, which means sensor data is delay and may indicate a failed sensor.
            """
            # Null out value so outdated values don't get mistaken for current
            self.valueQLabel.setText("--")
            # Set indicator (progress) bar colour, black text on grey progress bar
            palette = QGuiApplication.palette()
            palette.setColor(QPalette.Text, SensorWidget.BLACK)
            palette.setColor(QPalette.HighlightedText, SensorWidget.BLACK)
            palette.setColor(QPalette.Base, SensorWidget.GREY_LIGHT)
            palette.setColor(QPalette.Highlight, SensorWidget.GREY)
            self.progressBar.setPalette(palette)
            self.progressBar.setTextVisible(True)
            self.progressBar.setFormat("MISSING")
            self.progressBar.setValue(0)
            # Set icon and colour
            self.statusQLabel.setPixmap(QtGui.QPixmap(f":icons/watchdogfault"))
            palette = QGuiApplication.palette()
            palette.setColor(QPalette.Window, SensorWidget.RED if self._interval_critical else SensorWidget.ORANGE)
            self.statusQLabel.setPalette(palette)

    #: File name for Watchdog Widget UI file.
    _watchdogwidget_ui_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "watchdogwidget.ui")

    class WatchdogWidget(*loadUiType(_watchdogwidget_ui_filename), SensorWidgetBase):

        TOOL_TIP = "A widget to display sensor watchdog status and history"
        XML = "<ui language='c++'><widget class='WatchdogWidget' name='watchdogWidget'></widget></ui>"

        def __init__(self, parent=None):
            super().__init__(parent)
            self._name = ""
            self._previous_state = ""
            self.setupUi(self)
            self.textbox.setPlainText("")
            self.identifier = "WATCHDOG"
            self.name = "Watchdog"
            self.update_data()
        
        @Property(str)
        def name(self):
            return self._name
        
        @name.setter
        def name(self, name=""):
            self._name = name
            if not name:
                name = self._id
            self.setTitle(name)
        
        @Property(str)
        def identifier(self):
            return self._id

        @identifier.setter
        def identifier(self, id=""):
            if not id:
                id = self.objectName()
            self._id = id
            if not self._name:
                self.setTitle(id)

        def update_data(self, data={}):
            try:
                state = data["value"]
                if state == "FAULT" and "faults" in data:
                    # Construct string listing fault(s) for each sensor
                    sensorfaults = []
                    for sensor, faults in data["faults"].items():
                        sensorfaults.append(f"{sensor} {', '.join(faults)}")
                    faultlist = "; ".join(sensorfaults)
                    state = f"{state}: {faultlist}"
                if state != self._previous_state:
                    self._previous_state = state
                    self.textbox.appendPlainText(datetime.now().strftime(f"%H:%M.%S: {state}"))
                    if state[:5] == "FAULT":
                        self.icon.setPixmap(QtGui.QPixmap(f":icons/fault"))
                    else:
                        self.icon.setPixmap(QtGui.QPixmap(f":icons/ok"))
            except KeyError:
                pass


    #: File name for Log Widget UI file.
    _logwidget_ui_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logwidget.ui")

    class LogWidget(*loadUiType(_logwidget_ui_filename), SensorWidgetBase):

        TOOL_TIP = "A widget to display raw sensor data in text form"
        XML = "<ui language='c++'><widget class='LogWidget' name='logWidget'></widget></ui>"

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.clear()
            self.identifier = "LOG"
            self.clearPushButton.clicked.connect(self.clear)

        def update_data(self, data={}):
            data = data.copy()
            try:
                timestamp = data.pop("timestamp").strftime("%H:%M.%S")
            except (KeyError, AttributeError) as ex:
                timestamp = datetime.now().strftime("%H:%M.%S")
            self.logTextEdit.appendPlainText(f"{timestamp}: {data}")

        def clear(self):
            self.logTextEdit.setPlainText("")


    #: Default filename for SensorPanel UI file.
    _sensorpanel_ui_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensorpaneldatafilter_demo.ui")
    
    class SensorPanel(QtWidgets.QWidget):
        def __init__(self, parent=None, data_input_queue=None, data_output_queue=None, uifile=_sensorpanel_ui_filename, **kwargs):
            super().__init__(parent=parent)
            #: Sink data sent from subwidgets through our own send() method
            self.sink = self
            #: Queue object for receiving data through.
            self.data_input_queue = data_input_queue
            #: Queue object for sending data through.
            self.data_output_queue = data_output_queue
            # Build the UI for the (real) sensor panel
            loader = QUiLoader(parent=self)
            loader.addPluginPath(os.path.dirname(os.path.abspath(__file__)))
            #print(f"QUiLoader pluginPaths is {loader.pluginPaths()}")
            #print(f"UI file is {uifile}")
            #: The loaded UI panel widget which is placed inside this SensorPanel.
            self.panel = loader.load(uifile)
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(self.panel)
            self.setLayout(layout)

            # Configure a QTimer to periodically check for data on the Queue
            if not self.data_input_queue is None:
                #: QTimer to periodically check for data on the Queue.
                self.timer = QtCore.QTimer()
                self.timer.timeout.connect(self._update_panel)
                self.timer.start(15)

        def send(self, data):
            """
            Receive data from subwidgets and place onto our output queue for SensorPanelDataFilter to handle.
            """
            data = listify(data)
            self.data_output_queue.put(data)

        def update_sensorwidget_mapping(self):
            """
            Rebuild the map of sensor indentifiers to SensorWidget objects.

            This should be run any time a SensorWidget is dynamically added or removed from the panel.
            """
            # Build a map of identifiers to SensorWidgets (searching all sub-container widgets)
            def _find_sensorwidgets(widget):
                """
                Recursively find SensorWidgets within any child widgets.
                """
                sw = {}
                for child in widget.children():
                    if isinstance(child, SensorWidgetBase):
                        # Widget is capable of accepting data and should have an identifier property
                        if not child.identifier in sw:
                            # No widget for this identifier yet, create list of widgets
                            sw[child.identifier] = []
                        # Append widget to the list of widgets for this identifier
                        sw[child.identifier].append(child)
                    else:
                        # Widget could be a container, recursively search inside for other sensor widgets
                        for k, v in _find_sensorwidgets(child).items():
                            if k in sw:
                                # Add widgets to existing list
                                sw[k].extend(v)
                            else:
                                sw[k] = v
                return sw
            
            self._sensor_widgets = _find_sensorwidgets(self.panel)


        def showEvent(self, event):
            # Update the sensorwidget mapping on show, since children don't exist yet during __init__()
            self.update_sensorwidget_mapping()
            return super().showEvent(event)


        def closeEvent(self, event):
            # Don't close window, wait for parent to terminate our process instead
            event.ignore()
            self.showMinimized()


        def _update_panel(self):
            while not self.data_input_queue.empty():
                try:
                    data = listify(self.data_input_queue.get(timeout=0.05))
                except Queue.Empty:
                    return
                if not data:
                    return
                
                # Loop through data, assign send values to widgets matching identifier
                for d in data:
                    # Send all data to any LogWidgets
                    if "LOG" in self._sensor_widgets:
                        for lw in self._sensor_widgets["LOG"]:
                            lw.update_data(d)
                    # Try to find matching SensorWidgets matching this sensor identifier
                    try:
                        for sw in self._sensor_widgets[d["sensor_identifier"]]:
                            sw.update_data(d)
                    except KeyError:
                        # A SensorWidget with for this sensor identifier doesn't exist in the panel
                        pass