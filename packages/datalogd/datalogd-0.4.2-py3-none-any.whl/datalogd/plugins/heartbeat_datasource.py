import asyncio
import logging

from datalogd import DataSource

class HeartbeatDataSource(DataSource):
    """
    Generate a regular heartbeat message for failsafe or keep-alive type purposes.

    A basic message will be generated at regular intervals (default 1.0 second), controlled by the
    ``interval`` parameter. By default an integer counter will be appended to the message as the
    ``value`` field. The initial value for the counter can be set using the ``counter`` paramter, or
    set ``counter=False`` to disable.

    The message can be set with the ``message`` parameter. To use the counter functionality, the
    message should be of a dictionary type.

    :param interval: Time interval between heartbeat messages, in seconds.
    :param counter: Append an integer counter to the message data.
    :param message: Message to use as the heartbeat data.
    """
    def __init__(self, sinks=[], interval=1.0, counter=True, message={"type": "config", "id": "heartbeat"}):
        super().__init__(sinks=sinks)
        self._log = logging.getLogger("HeartbeatDataSource")
        self.interval = float(interval)
        try:
            self.counter = int(counter)
        except:
            self.counter = int(bool(counter))
        if self.counter and not isinstance(message, dict):
            self._log.warning("Heartbeat counter only works with dictionary type messages.")
            self.counter = 0
        self.message = message
        # Queue first call of update routine
        self._loop = asyncio.get_event_loop()
        self._loop.call_soon(self.generate_heartbeat)

    def generate_heartbeat(self):
        """
        Generate the heartbeat message and send to any connected sinks.
        """
        if isinstance(self.message, dict):
            data = self.message.copy()
        else:
            data = self.message
        # If non-zero counter, use as value in message and increment it
        if self.counter:
            data.update({"value": self.counter})
            self.counter += 1
        self.send([data])
        # Schedule next update
        self._loop.call_later(self.interval, self.generate_heartbeat)
