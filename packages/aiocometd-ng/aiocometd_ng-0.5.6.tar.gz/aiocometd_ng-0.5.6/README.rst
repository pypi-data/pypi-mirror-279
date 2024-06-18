aiocometd-ng
=========

aicometd-ng is a Python 3.10+ compatible fork of https://github.com/robertmrk/aiocometd

Usage
-----

.. code-block:: python

    import asyncio

    from aiocometd import Client

    async def chat():

        # connect to the server
        async with Client("http://example.com/cometd") as client:

                # subscribe to channels
                await client.subscribe("/chat/demo")
                await client.subscribe("/members/demo")

                # listen for incoming messages
                async for message in client:
                    topic = message["channel"]
                    data = message["data"]
                    print(f"{topic}: {data}")

    if __name__ == "__main__":
        asyncio.run(chat())

Install
-------

.. code-block:: bash

    pip install aiocometd-ng

Requirements
------------

- Python 3.10+
- aiohttp_

.. _aiohttp: https://github.com/aio-libs/aiohttp/
.. _aiocometd: https://github.com/robertmrk/aiocometd
.. _CometD: https://cometd.org/
.. _Comet: https://en.wikipedia.org/wiki/Comet_(programming)
.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _Bayeux: https://docs.cometd.org/current/reference/#_bayeux
.. _ext: https://docs.cometd.org/current/reference/#_bayeux_ext
.. _cli_example: https://github.com/robertmrk/aiocometd/blob/develop/examples/chat.py
.. _aiocometd-chat-demo: https://github.com/robertmrk/aiocometd-chat-demo
