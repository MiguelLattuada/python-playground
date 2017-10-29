class FutureOperationWrapper:

    @property
    def result(self):
        return self._result

    def __init__(self, operation):
        self._result = None
        self._operation = operation
        self._future = asyncio.Future()
        self._future.add_done_callback(self.done_callback)

    def done_callback(self, future_instance):
        """
        Future done callback
        :param asyncio.Future future_instance:
        :return:
        """
        self._result = future_instance.result()

    async def run(self):
        """
        Run asynchronous operation
        :return: None
        """
        operation_result = await self._operation()
        self._future.set_result(operation_result)


if __name__ == '__main__':
    import asyncio

    def read_operation():
        print('Read operation started')
        data = open(
            file='../data/index.json',
            mode='r',
            encoding='utf-8'
        )
        print('Read operation ended')
        return data.read()

    async def wait_operation():
        print('Operation 1 started')
        await asyncio.sleep(2)
        print('Operation 1 ended')
        return 'Waited 23'


    async def wait_operation_2():
        print('Operation 2 started')
        await asyncio.sleep(1)
        print('Operation 2 ended')
        return 'Waited 23'

    wrappers = [
        FutureOperationWrapper(wait_operation),
        FutureOperationWrapper(wait_operation_2)
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            *[wrapper.run() for wrapper in wrappers]
        )
    )
    print([wrapper.result for wrapper in wrappers])