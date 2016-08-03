#!/usr/bin/env python3

import asyncio
from aiohttp import web, WSMsgType
import json
import os
import random
import time
import sys
import hashlib
import intelhex
import io

from . machine import Machine

# Observer pattern.  Observers can subscribe/unsubscibe to a subject.
# Notify method delivers the observable to observers.  Note that
# Subject classes implement the observer interface, and so can themselves
# subscribe to other Subjects.
class Subject:
    def __init__(self):
        self.observers = set()
    def subscribe(self, observer):
        self.observers.add(observer)
    def unsubscribe(self, observer):
        self.observers.remove(observer)
    async def notify(self, observable):
        for observer in self.observers:
            await observer.notify(observable)

# Connects a Subject to a web socket.  Anything received from the subject
# is sent to the websocket client.
class WebsocketSubscriber:
    def __init__(self, subject, ws):
        self.subject = subject
        self.subject.subscribe(self)
        self.ws = ws
        self.running = True
        self.q = asyncio.Queue(maxsize=10)

    async def notify(self, obs):

        if self.running == False:
            return

        try:
            self.q.put_nowait(obs)
        except asyncio.QueueFull:
            # Silently ignore errors when queue is full
            self.running = False
            pass

    async def run(self):
        while self.running:

            if self.ws.closed:
                self.running = False
                break

            if self.ws.exception() != None:
                self.running = False
                break

            try:
                obs = await asyncio.wait_for(self.q.get(), timeout=2)
            except asyncio.TimeoutError:
                # Timeout exception, create a chance to re-evaluate
                # self.running
                continue
            except Exception as e:
                print("WebsocketSubscriber:", e)

            try:
                await self.ws.send_str(obs)
            except Exception as e:
                print("WebsocketSubscriber:", e)
                self.running = False

    def close(self):
        self.running = False
        self.subject.unsubscribe(self)

class ProgramInterface:

    # Constructor
    def __init__(self, subject, machine):
        self.subject = subject
        self.machine = machine
        self.running = True

        self.queue = asyncio.Queue()

    # Close the listener
    def close(self):
        self.running = False

    async def handle(self, obj):
        await self.queue.put(obj)

    # Background task which responds to the websocket
    async def run(self):

        try:

            while self.running:

                try:
                    ev = self.queue.get_nowait()
                    image = ev["image"]
                except:
                    await asyncio.sleep(1)
                    continue
               
                await self.subject.notify("Flash image acquired.")

                try:
                    ih = intelhex.IntelHex()
                    with io.StringIO(image) as input:
                        ih.fromfile(input, format='hex')

                    out = io.StringIO()

                    ih.dump(tofile=out)

                    for v in io.StringIO(out.getvalue()):
                        await self.subject.notify(v.rstrip())
                        await asyncio.sleep(0.02)

                    h = hashlib.new('md5')
                    for start, end in ih.segments():
                        segment = [ih[i] for i in range(start, end)]
                        h.update(bytes(segment))
                    hash = h.hexdigest()

                    msg = "Image length %d" % len(image)
                    await self.subject.notify(msg)
                    msg = "Hash %s" % hash
                    await self.subject.notify(msg)

                except Exception as e:
                    await self.subject.notify("Exception: " + str(e))
                    await self.subject.notify("ERROR")
                    continue

                await asyncio.sleep(1)

                await self.subject.notify("Writing flash...")

                for start, end in ih.segments():
                    msg = "Segment %d .. %d" % (start, end)
                    await self.subject.notify(msg)

                progress = 100

                while progress > 0:
                    await self.subject.notify("Writing %d%%" % progress)
                    await asyncio.sleep(0.05)
                    progress -= 6.2

                await self.subject.notify("Write complete.")
                await asyncio.sleep(1)

                await self.subject.notify("Halting processor...")
                self.machine.halt()
                await asyncio.sleep(1)

                for start, end in ih.segments():
                    segment = [ih[i] for i in range(start, end)]
                    self.machine.load(segment, start)

                await self.subject.notify("Reset...")

                await self.machine.reset()

                await asyncio.sleep(0.21)

                await self.subject.notify("Operation complete.")

                await self.subject.notify("OK")

        except Exception as e:
            print("ProgramInterface:", e)

        self.running = False

# Web service for the programmer, serves a web socket
class Programmer:

    # Constructor
    def __init__(self, pages=None, listener=None):

        # Subjects for notification
        self.ws_subject = Subject()       # Main websocket subject

        # Where the static resources are located
        self.ixs = pages
        if self.ixs == None: self.ixs = "/usr/share/cm99019/"

        # Implement the web service listener
        self.listen = listener
        if self.listen == None: self.listen = "0.0.0.0:8080"

        self.machine = Machine()

        self.programmer = ProgramInterface(self.ws_subject, self.machine)

    # Main task, starts all other tasks and serves web resources
    async def run(self):

        # Start other background tasks
        loop = asyncio.get_event_loop()
        loop.create_task(self.machine.execute())
        loop.create_task(self.programmer.run())

        # GET /index.html
        async def get_ix(request):

            page = open(self.ixs + "/index.html", "rb").read()

            return web.Response(
                body=page,
                content_type="text/html"
            )

        # Implement HTTP redirect
        def redirect(path):
            async def f(request):
                raise web.HTTPFound(path)
            return f

        # Return a statisc resource, read from file.
        def get_type(type="text/html"):
            async def f(request):
                if ".." in request.path:
                    raise web.HTTPNotFound()
                if "/" in request.path[1:]:
                    raise web.HTTPNotFound()
                try:
                    page = open(self.ixs + request.path, "rb").read()
                except:
                    raise web.HTTPNotFound()
                return web.Response(
                    body=page,
                    content_type=type
                )
            return f

        # Main web application websocket
        async def get_ws(request):

            ws = web.WebSocketResponse()
            await ws.prepare(request)

            welcome = [
                "     ,------------------------------------.        /",
                "     |                                    |       //___",
                "     | **** CM99109 flash programmer **** |      /__  /",
                "     |                                    |        /_/",
                "     `------------------------------------'       //",
                "                                                  /",
            ]

            for v in welcome:
                await ws.send_str(v)

            # Now, subscribe to all new data from ws_subject
            subs = WebsocketSubscriber(self.ws_subject, ws)
            loop = asyncio.get_event_loop()
            task = loop.create_task(subs.run())

            try:

                # Loop until socket closed
                async for msg in ws:

                    # Socket close triggered when can't send on
                    # a WebsocketSubscriber
                    if subs.running == False: break

                    # If it's text, act on it, otherwise ignore.
                    # aiohttp deals with ERROR, CLOSED and PING/PONG.
                    if msg.type == WSMsgType.TEXT:

                        # JSON decode and send to appropriate subsytem
                        obj = json.loads(msg.data)
                        kind = list(obj.keys())[0]
                        if kind == 'flash':
                            await self.programmer.handle(obj["flash"])

            except Exception as e:
                print("get_ws:", e)
            finally:
                task.cancel()

            # Close websocket subscriber when tidying up
            subs.close()

            return ws

        # Web application routing defined here
        app = web.Application()
        app.router.add_get('/ws', get_ws);

        # Web task creation
        runner = web.AppRunner(app)
        await runner.setup()

        host = self.listen.split(":", 2)
        site = web.TCPSite(runner, host[0], host[1])
        await site.start()

        # Wait forever.
        while True:
            await asyncio.sleep(100)

