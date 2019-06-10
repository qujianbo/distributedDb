'''
@author: qujb
@contact: 15210825203@163.com
@file: Redis_deploy.py
@time: 2019/6/6 下午8:28
@desc:
'''
from redis.client import Redis as PyRedis
from src.common.common import available_value


class Redis(PyRedis):
    # session = None

    def __init__(self, host, port, db=None, redis_password=None, decode_responses=True, enable=True,region="Beijing"):
        # print(host, str(port))
        self.enable = enable
        self.region = region
        super().__init__(host=host, port=port, db=db, password=redis_password, decode_responses=decode_responses)
        print(self.client_getname())

    def get(self, name, default=None):
        if not self.enable:
            return None
        res = super().get(name)
        # if decode: res = res.decode()
        return res if res else default

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        if not self.enable:
            return None
        return super().set(name, available_value(value), ex=ex, px=px, nx=nx, xx=xx)

    def delete_by_pattern(self, pattern):
        if not self.enable:
            return -1
        keys = self.keys(pattern=pattern)
        if keys == [] or keys == ():
            return 1
        return self.delete(*keys)

    def lpush(self, name, value):
        if not self.enable:
            return None

        return super().lpush(name,available_value(value))

    def rpush(self, name, value):
        if not self.enable:
            return None

        return super().rpush(name,available_value(value))