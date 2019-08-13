import asyncio
from proxybroker import Broker

async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        print(dir(proxy))
        print('Found proxy: %s:%s' % (proxy.host, proxy.port))

proxies = asyncio.Queue()
broker = Broker(proxies)
tasks = asyncio.gather(
    broker.find(types=['HTTP', 'HTTPS'], limit=1),
    show(proxies))


loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)