import asyncio
import inspect

from nsanic.libs import tool_dt
from nsanic.libs.tool import json_encode


a = json_encode({'a': 12321, '': "啊得到完全的撒", 'dtr': tool_dt.cur_dt().date()})
print(a)


async def test1():
    print('test1')
    await asyncio.sleep(1)


def test2():
    print('test2')


class Test3:

    @staticmethod
    async def hha(sssa):
        print('hha')

    @staticmethod
    def ppp(adsad):
        print('ppp')


def is_async_func(func):
    if inspect.isfunction(func) or inspect.ismethod(func):
        return inspect.iscoroutinefunction(func)
    return False


print(is_async_func(Test3().hha), is_async_func(Test3().ppp))
