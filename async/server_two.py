import asyncio
import socket


class SocketServerWrapper:
    @property
    def socket(self):
        return self._socket

    def __init__(self, host, port, event_loop):
        """
        Creates a new instance of wrapper server
        Binds socket to given host, port and start listening
        :param str host:
        :param int port:
        :param asyncio.AbstractEventLoop event_loop:
        """
        self._host = host
        self._port = port
        self._loop = event_loop
        # Create socket, bind, and listen
        self._socket = self.create_socket()
        self._socket.bind((self._host, self._port))
        self._socket.setblocking(False)
        self._socket.listen(10)

    def start(self):
        """
        Create future for _start
        And run loop
        :return:
        """
        # self._loop.create_task(self._accept())
        self._loop.run_until_complete(self._accept())
        # print('asd')
        # self._loop.run_forever()

    async def _handle_accepted(self, connection, address):
        """
        Handle accepted connection
        :param socket.socket connection:
        :param address:
        :return:
        """
        while True:
            incoming_data = await self._loop.sock_recv(connection, 1024)
            data = 'Server received data'.encode('ascii')
            connection.send(data)

    async def _accept(self):
        """
        Accept a connection
        :return:
        """
        while (True):
            conn, addr = await self._loop.sock_accept(self._socket)
            self._loop.create_task(self._handle_accepted(conn, addr))

    @staticmethod
    def create_socket():
        """
        Creates a socket.socket instance
        :return:
        """
        return socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
        )


server = SocketServerWrapper(
    host='localhost',
    port=5003,
    event_loop=asyncio.get_event_loop()
)

server.start()