import asyncio
import helper.http as http_helper


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

        # TODO: Handle incoming connections with an async handler so we can receive multiple connections without blocking

        incoming_data = await client_reader.read(2048)

        print('BROWSER REQUEST DATA')
        print(incoming_data)

        data = http_helper.status_ok_response('<h1>Hello world!<h1>')
        client_writer.write(data.encode('utf-8'))
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