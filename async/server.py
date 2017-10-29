import asyncio
import socket


class ServerWrapper:
    @property
    def server(self):
        return self._server

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._server = None

    async def create(self):
        """
        Start server on the provided host:port
        :return: None
        """
        server = await asyncio.start_server(
            client_connected_cb=ServerWrapper.on_incoming_connections,
            host=self._host,
            port=self._port
        )
        self._server = server

    def get_main_socket(self):
        """
        Get first socket on server sockets array
        :return: socket._socket
        """
        return self._server.sockets[0]

    @staticmethod
    async def on_incoming_connections(client_reader, client_writer):
        """
        Socket server each client callback
        :param asyncio.StreamReader client_reader:
        :param asyncio.StreamWriter client_writer:
        :return: None
        """
        print('New user connected')
        await asyncio.sleep(10)
        data = 'Data...'.encode('utf-8')
        client_writer.write(data)
        client_writer.close()

    @staticmethod
    def default_protocol_factory(self):

        return asyncio.Protocol()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    sv_wrapper = ServerWrapper(
        host='localhost',
        port=5003
    )

    loop.run_until_complete(sv_wrapper.create())
    print(repr(sv_wrapper.server))

    loop.run_forever()