import struct
from random import randint
from time import time
from uuid import UUID
from math import trunc


class RangeError(Exception):
    pass


class UUIDGenerator:
    MAX_COUNTER = 4398046511103
    MAX_INT = 2**32-1

    def __init__(self):
        self.counter = 0
        self.timestamp = 0

    @staticmethod
    def _get_v7(unix: int, rand_a: int, rand_bhi: int, rand_blo: int) -> UUID:
        if (unix < 0
                or rand_a < 0
                or rand_bhi < 0
                or rand_blo < 0
                or unix > 281474976710655
                or rand_a > 0xfff
                or rand_bhi > 1073741823
                or rand_blo > 4294967295):
            raise RangeError("invalid field value")

        res = bytearray(16)

        res[0] = trunc(unix / 2 ** 40) & 0xff
        res[1] = trunc(unix / 2 ** 32) & 0xff
        res[2] = trunc(unix / 2 ** 24) & 0xff
        res[3] = trunc(unix / 2 ** 16) & 0xff
        res[4] = trunc(unix / 2 ** 8) & 0xff
        res[5] = unix & 0xff
        res[6] = (0x70 | (rand_a >> 8)) & 0xff
        res[7] = rand_a & 0xff
        res[8] = (0x80 | (rand_bhi >> 24)) & 0xff
        res[9] = (rand_bhi >> 16) & 0xff
        res[10] = (rand_bhi >> 8) & 0xff
        res[11] = rand_bhi & 0xff
        res[12] = (rand_blo >> 24) & 0xff
        res[13] = (rand_blo >> 16) & 0xff
        res[14] = (rand_blo >> 8) & 0xff
        res[15] = rand_blo & 0xff

        return UUID(bytes=bytes(res))

    def _random(self) -> int:
        return randint(0, self.MAX_INT)

    # Initializes the counter at a 42-bit random integer.
    def _reset_counter(self) -> None:
        self.counter = (self._random() << 10) + (self._random() & 0x3ff)

    def generate7(self) -> UUID:
        unix = trunc(time()*1000)

        if unix > self.timestamp:
            self.timestamp = unix
            self._reset_counter()
        else:
            # go on with previous timestamp if new one is not much smaller
            self.counter += 1
            if self.counter > self.MAX_COUNTER:
                # increment timestamp at counter overflow
                self.timestamp += 1
                self._reset_counter()

        return self._get_v7(self.timestamp, self.counter >> 30, self.counter & (2 ** 30 - 1), self._random())


