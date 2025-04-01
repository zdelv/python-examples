from collections.abc import Generator
from typing import Any
from collections import deque
import contextvars
import random

KEY = contextvars.ContextVar("key", default=1234)
SUSPEND = object()


def run(*args: Generator[Any, None, Any]):
    coros = deque((idx, a) for idx, a in enumerate(args))
    contexts = [contextvars.Context()] * len(args)
    rets = [None] * len(args)
    while coros:
        idx, coro = coros.pop()
        try:
            ret = contexts[idx].run(next, coro)
        except StopIteration as e:
            ret = e.value

        if ret is SUSPEND:
            print(f"Coro {idx} suspended")
            coros.appendleft((idx, coro))
        else:
            print(f"Coro {idx} finished")
            rets[idx] = ret
    return rets


def coro1(x: int):
    KEY.set(random.randint(1, 1000))
    y = yield from coro2(x)
    return y


def coro2(y: int):
    key = KEY.get()
    yield SUSPEND
    print(key)
    return y + 1


rets = run(*(coro1(x) for x in range(4)))
print(rets)
