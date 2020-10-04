import pickle
from pickle import UnpicklingError

from redis import Redis as _Redis

from swiper_zl.config import REDIS


class Redis(_Redis):

    def set(self, name, value, ex=None, px=None, nx=False, xx=False, keepttl=False):
        pickle_data = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        return super().set(name, pickle_data, ex, px, nx, xx, keepttl)

    def get(self, name, default=None):

        pickle_data = super().get(name)

        if pickle_data is None:
            return default

        try:
            value = pickle.loads(pickle_data)
        except (KeyError, EOFError, UnpicklingError):
            print("youwu")
            return pickle_data
        else:
            return value


rds = Redis(**REDIS)
