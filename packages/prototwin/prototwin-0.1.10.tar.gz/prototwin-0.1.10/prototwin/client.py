from typing import Self, Callable
from ctypes.wintypes import LARGE_INTEGER
import asyncio
import time
import ctypes
import prototwin_cmdbuff

from websockets.client import connect
from websockets.frames import OP_BINARY

_sz = 32768 * 8
_g = prototwin_cmdbuff.get
_s = prototwin_cmdbuff.set
_c = prototwin_cmdbuff.clear
_ws = prototwin_cmdbuff.write_size
_rs = prototwin_cmdbuff.read_size
_p = prototwin_cmdbuff.prepare
_r = prototwin_cmdbuff.reset
_l = prototwin_cmdbuff.load
_u = prototwin_cmdbuff.update

kernel32 = ctypes.windll.kernel32
def _sleep(seconds):
    handle = kernel32.CreateWaitableTimerExW(None, None, 0x00000002, 0x1F0003)
    kernel32.SetWaitableTimer(handle, ctypes.byref(LARGE_INTEGER(int(seconds * -10000000))), 0, None, None, 0)
    kernel32.WaitForSingleObject(handle, 0xFFFFFFFF)
    kernel32.CancelWaitableTimer(handle)

class Client:    
    def __init__(self, ws) -> None:
        self._ws = ws
        self._wb = bytearray(_sz)
        prototwin_cmdbuff.provide(self._wb, _sz)

    def count(self) -> int:
        return (_rs() - 12) / 8
    
    def get(self, address: int) -> bool|int|float:
        return _g(address)

    def set(self, address: int, value: bool|int|float) -> None:
        return _s(address, value)
    
    async def load(self, path: str) -> None:
        _l(path)
        await self._ws.write_frame(True, OP_BINARY, memoryview(self._wb)[:_ws()])
        _c()
        await self._ws.recv()
    
    async def reset(self) -> None:
        _r()
        await self._ws.write_frame(True, OP_BINARY, memoryview(self._wb)[:_ws()])
        _c()
        await self._ws.recv()

    async def step(self) -> None:
        _p()
        await self._ws.write_frame(True, OP_BINARY, memoryview(self._wb)[:_ws()])
        _c()
        self._rb = await self._ws.recv()
        _u(self._rb)

    async def start_step(self) -> None:
        _p()
        await self._ws.write_frame(True, OP_BINARY, self._wb)
        _c()

    async def step_completed(self) -> None:
        self._rb = await self._ws.recv()
        _u(self._rb)

    async def run(self, cb: Callable[[Self, float, float], bool|None]) -> None:
        start = time.perf_counter()
        t = 0
        dt = 0.01
        while True:
            await self.step()
            if cb(self, dt, t) == False:
                return
            t += dt
            st = t - (time.perf_counter() - start)
            if st > 0:
                _sleep(st)

async def start(location = "ProtoTwinConnect", *, dev: bool = False) -> Client|None:
    args = "-runner"
    if (dev):
        args += " -dev"
    await asyncio.create_subprocess_exec(location, args)
    await asyncio.sleep(2) # Allow a small amount of time to settle
    try:
        ws = await connect("ws://localhost:8084", compression=None, user_agent_header="Python")
        await ws.recv() # Wait for ready signal
        client = Client(ws)
        return client
    except:
        return None
    
async def attach() -> Client|None:
    try:
        ws = await connect("ws://localhost:8084", compression=None, user_agent_header="Python")
        await ws.recv() # Wait for ready signal
        client = Client(ws)
        return client
    except:
        return None