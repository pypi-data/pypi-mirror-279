import asyncio
import logging
import json

from datalogd import DataFilter

class SocketDataFilter(DataFilter):
    r"""
    Send and receive data over a network socket.

    The SocketDataFilter bridges data over a network socket. The other end of the connection may be
    another SocketDataFilter, but can be any application that uses the correct message encoding and
    structure. The connected sockets don't have to be on remote computers, and may be used to
    perform inter-process communications within a single machine.

    The SocketDataFilter can also act as either a socket server, or a client. Connections must
    involve at least one server and one client. Servers will listen on their given port and accept
    multiple client connections. Clients will only make a single connection to the given server
    address and port. If a connection can't be established or is lost, it will be retried
    indefinitely.

    Incoming network data will be forwarded on to all of the SocketDataFilter's
    :class:`~datalogd.DataSink`\ s, and input from any connected :class:`~datalogd.DataSource`\ s will be
    sent on to any network connections. Note that this behaviour is more like a "bridge" than a
    "filter".

    The network communications protocol is quite basic, but allows some degree of customisation. The
    defaults are to convert the incoming python data from :class:`~datalogd.DataSource`\ s to a JSON
    structure, and encode the resulting string into a byte stream using UTF-8. Network connections
    are kept open, and messages are separated by an end-of-transmission (EOT, 0x17) byte.

    The ``role`` parameter selects whether the SocketDataFilter acts as a socket server, or socket
    client. In server mode (default), a server is started bound to the given ``host`` name or
    address and ``port`` number. The server will accept multiple connections, and data will be sent
    and received from any/all connected clients. If ``role="client"``, then the SocketDataFilter
    will attempt to connect to a server given by the ``host`` address and ``port`` number.

    The ``host`` address can be any name or IP address. To only allow connections to/from the local
    machine, use loopback address of ``host="127.0.0.1"`` (default). To allow a server to bind to
    any network interface, use ``host=""``.

    The ``port`` can be any unused port number, typically a high number between 1024 and 65535.

    The ``buffer_size`` should be set to the maximum expected size of a data message packet. The
    default is 1 MiB.

    For string (or JSON structured) data, the ``message_encoding`` determines how it will be
    converted to or from a byte stream. The default of ``"utf8"`` is typically fine.

    By default, network connections will be kept open, with data message packets separated by a
    delimiter end-of-transmission (EOT, 0x17) byte. This may be changed to a different byte sequence
    using the ``message_delimiter`` parameter. Setting ``message_delimiter=None`` will mean than the
    end of a message packet is expected to be followed by the client closing the network connection.
    Further messages can be sent if the network socket connection is re-established.

    To transmit data through the network, it needs to be converted to a stream of bytes. The
    ``structure_type`` parameter determines how arbitrary python data should be converted to a
    structure which can be converted to a byte stream. The default is ``structure_type="json"``
    which will attempt to convert data to or from a JSON object.

    :param role: Act as either a ``"server"`` or ``"client"``.
    :param host: Network name or address to bind to (as a server) or connect to (as a client).
    :param port: Network port number to listen on (as a server) or connect to (as a client).
    :param buffer_size: Size of buffer for messages, maximum message size.
    :param message_encoding: Character encoding used for string data (or JSON encoded structures).
    :param message_delimiter: Delimiter byte(s) used to separate message packets.
    :param structure_type: Structure type used to represent data.
    """

    def __init__(self, sinks=[], role="server", host="127.0.0.1", port=45454, buffer_size=2**20, message_encoding="utf8", message_delimiter="\x17", structure_type="json"):
        super().__init__(sinks=sinks)
        self._log = logging.getLogger("SocketDataFilter")

        self._host = host
        self._port = int(port)
        self._server = None
        self._connections = []
        self._buffer_size = buffer_size
        self._message_encoding = message_encoding
        self._message_delimiter = bytes(message_delimiter, "utf8")
        if structure_type in (None, "none", "json"):
            self._structure_type = structure_type
        else:
            self._log.warning("Data structure_type not supported.")
            self._structure_type = None
        # Get reference to event loop and schedule task (but loop probably isn't started yet)
        self.loop = asyncio.get_event_loop()
        if role == "server":
            self._connection_task = self.loop.create_task(self._start_server())  # For python 3.8+: , name="SocketDataFilter Server Connector")
        else:
            role = "client"
            self._connection_task = self.loop.create_task(self._start_client())  # For python 3.8+: , name="SocketDataFilter Client Connector")


    async def _start_server(self):
        """
        Coroutine to attempt to start the socket server.
        """
        self._server = None
        while True:
            try:
                self._server = await asyncio.start_server(self._handle_data, host=self._host, port=self._port, limit=self._buffer_size)
            except OSError:
                self._log.error(f"Unable to start server (port {self._port} already in use?)")
                await asyncio.sleep(5.0)
            else:
                self._log.info(f"Server started on {', '.join(str(sock.getsockname()) for sock in self._server.sockets)}")
                self._connections = []
                async with self._server:
                    await self._server.serve_forever()


    async def _start_client(self):
        """
        Coroutine to attempt to connect to a socket server.
        """
        while True:
            self._connections = []
            self._log.debug(f"Attempting to connect to server at {self._host}:{self._port}")
            try:
                reader, writer = await asyncio.open_connection(host=self._host, port=self._port, limit=self._buffer_size)
                self._log.debug(f"Connection established.")
            except Exception:
                self._log.debug("Unable to connect to server, will try again soon.")
                await asyncio.sleep(5.0)
            else:
                await self._handle_data(reader, writer)


    async def _handle_data(self, reader, writer):
        peer_name = writer.get_extra_info('peername')
        self._log.info(f"Connection established with {peer_name}.")
        self._connections.append(writer)
        while True:
            try:
                if self._message_delimiter:
                    # Multiple messages are expected, separated by a some delimiter bytes                
                    self._log.debug(f"Waiting for data block from {peer_name} delimited by {self._message_delimiter}")
                    data_bytes = await reader.readuntil(separator=self._message_delimiter)
                else:
                    # Message is entire data stream until connection closed
                    self._log.debug(f"Waiting for data from {peer_name}.")
                    data_bytes = await reader.read()
            except asyncio.LimitOverrunError:
                # Stream limit exceeded, message may be incomplete
                self._log.warning(f"Data block from {peer_name} exceeded buffer size.")
                data_bytes = await reader.read(self._buffer_size)
                # TODO: handle this better, could buffer and continue reading
            except asyncio.IncompleteReadError as ex:
                # Connection closed before message completed
                data_bytes = ex.partial
                self._log.info("Connection with {} closed{}".format(peer_name, f" (read {len(data_bytes)} bytes)." if len(data_bytes) else "."))
            except (ConnectionResetError, BrokenPipeError, OSError):
                self._log.info(f"Connection with {peer_name} closed.")
                break
            if len(data_bytes) == 0:
                break
            # Remove delimiter suffix if present
            if data_bytes[-len(self._message_delimiter):] == self._message_delimiter:
                data_bytes = data_bytes[:-len(self._message_delimiter)]
            # If a message encoding given, attempt to decode
            try:
                data = data_bytes.decode(self._message_encoding)
            except:
                self._log.warning(f"Failed to decode from {peer_name} data using encoding {self._message_encoding}, leaving as raw byte data.")
                data = data_bytes
            # Attempt to interpret as given structure type
            if self._structure_type == "json":
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    self._log.warning(f"Failed to decode data from {peer_name} as JSON structure.")
            self._log.debug(f"Received from {peer_name}: {data}")
            self.send(data)
            # Loop if delimited messages expected
            if reader.at_eof() or (not self._message_delimiter):
                break
        # Close the connection
        self._connections.remove(writer)
        try:
            writer.write_eof()
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except (ConnectionResetError, BrokenPipeError, OSError):
            self._log.debug("Exception when closing connection, broken or already closed?")


    def receive(self, data):
        """
        Accept the provided data and output it to any connected sockets.

        :param data: Data to send to connected sockets.
        """
        if data is None or data == [] or self._connections == []: return
        # Try to encode data to given format
        if self._structure_type == "json":
            try:
                data = json.dumps(data)
            except (TypeError, ValueError):
                self._log.warning("Failed to encode data as JSON structure.")
        # Encode strings as bytes using given character encoding
        if type(data) == str:
            try:
                data = bytes(data, self._message_encoding)
            except:
                self._log.warning(f"Failed to encode string data as {self._message_encoding}")
        # Don't know how to convert data to raw bytes without a structure of some sort
        if not type(data) == bytes:
            self._log.warning(f"Unable to convert data to bytes, can't send to socket connections.")
        else:
            for c in self._connections:
                c.write(data)
            if self._message_delimiter:
                c.write(self._message_delimiter)

