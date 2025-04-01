from collections.abc import Generator
from typing import Any
from collections import deque

SUSPEND = object()


def run(*args: Generator[Any, None, Any]):
    coros = deque((idx, a) for idx, a in enumerate(args))
    rets = [None] * len(args)
    while coros:
        idx, coro = coros.pop()
        try:
            ret = next(coro)
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
    y = yield from coro2(x)
    return y


def coro2(y: int):
    yield SUSPEND
    return y + 1


rets = run(*(coro1(x) for x in range(4)))
print(rets)
