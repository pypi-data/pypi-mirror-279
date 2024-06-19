#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'chenli'

from aiohttp import web, hdrs
import aiohttp
import asyncio
import threading
import pprint


async def run_reverse_proxy(web_console_url, web_gui_url, reverse_ip, reverse_port):
    async def handler(request):
        proxyPath = request.match_info.get(
            'proxyPath', 'no proxyPath placeholder defined')

        baseUrl = web_gui_url

        if proxyPath == 'webconsole':
            baseUrl = web_console_url
        reqHeaders = request.headers.copy()

        # handle the websocket request
        if 'Upgrade' in reqHeaders['connection'] and 'websocket' in reqHeaders['upgrade'] and request.method == 'GET':

            if proxyPath not in ['webconsole', 'ws']:
                return web.Response(status=403)

            ws_server = web.WebSocketResponse()
            await ws_server.prepare(request)

            try:
                client_session = aiohttp.ClientSession(cookies=request.cookies)
                async with client_session.ws_connect(
                    baseUrl + proxyPath,
                ) as ws_client:

                    async def ws_forward(ws_from, ws_to):
                        async for msg in ws_from:
                            mt = msg.type
                            md = msg.data
                            if mt == aiohttp.WSMsgType.TEXT:
                                await ws_to.send_str(md)
                            elif mt == aiohttp.WSMsgType.BINARY:
                                await ws_to.send_bytes(md)
                            elif mt == aiohttp.WSMsgType.PING:
                                await ws_to.ping()
                            elif mt == aiohttp.WSMsgType.PONG:
                                await ws_to.pong()
                            elif ws_to.closed:
                                await ws_to.close(code=ws_to.close_code, message=msg.extra)
                            else:
                                raise ValueError(
                                    'unexpected message type: %s', pprint.pformat(msg))

                    # keep forwarding websocket data in both directions
                    task1 = asyncio.create_task(
                        ws_forward(ws_server, ws_client))
                    task2 = asyncio.create_task(
                        ws_forward(ws_client, ws_server))
                    await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)

                    return ws_server
            finally:
                await client_session.close()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=request.method,
                    url=baseUrl + proxyPath,
                    headers=reqHeaders,
                    allow_redirects=False,
                    data=request.content
                ) as resp:
                    proxy_response = web.StreamResponse(
                        status=resp.status,
                        reason=resp.reason,
                    )

                    # 转发目标服务器的所有响应头
                    for key, value in resp.headers.items():
                        proxy_response.headers[key] = value

                    # 如果目标服务器没有提供 content-type，不设置它
                    async def prepare_hook(response: web.StreamResponse) -> None:
                        if hdrs.CONTENT_TYPE not in resp.headers and 'application/octet-stream' == proxy_response.headers.get(hdrs.CONTENT_TYPE, ''):
                            del proxy_response.headers[hdrs.CONTENT_TYPE]
                        return None
                    request._prepare_hook = prepare_hook

                    await proxy_response.prepare(request)

                    # 读取并转发响应数据
                    async for chunk in resp.content.iter_chunked(4096):
                        await proxy_response.write(chunk)

                    await proxy_response.write_eof()
                    return proxy_response

    app = web.Application()
    app.router.add_route('*', '/{proxyPath:.*}', handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, reverse_ip, reverse_port)
    await site.start()
    actual_host = site._server.sockets[0].getsockname()[0]
    actual_port = site._server.sockets[0].getsockname()[1]
    if (actual_host == "0.0.0.0"):
        actual_host = "127.0.0.1"
    print(" INFO - 您可以访问 ", "http://" + actual_host + ":" + str(actual_port), " 查看策略绘制出的 K 线图形.")
    await asyncio.Event().wait()


def run_reverse_proxy_in_asyncio(web_console_url, web_gui_url, reverse_ip, reverse_port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_reverse_proxy(web_console_url, web_gui_url, reverse_ip, reverse_port))


def run_reverse_proxy_in_thread(web_console_url, web_gui_url, reverse_ip, reverse_port):
    t = threading.Thread(target=run_reverse_proxy_in_asyncio, args=(web_console_url, web_gui_url, reverse_ip, reverse_port))
    t.start()
