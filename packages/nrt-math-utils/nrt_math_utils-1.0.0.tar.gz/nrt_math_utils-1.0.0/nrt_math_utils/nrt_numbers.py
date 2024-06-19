from typing import Optional

import numpy

from nrt_collections_utils.collections_utils import CollectionsUtil


class DecimalNumber:
    DEFAULT_PERC = 6

    __perc: int = DEFAULT_PERC

    __number: Optional[float] = None
    __local_perc: Optional[int] = None

    def __init__(self, number, perc: int = None):
        if perc is not None:
            self.__local_perc = perc
        else:
            self.__local_perc = DecimalNumber.__perc

        self.__number = round(float(number), self.__local_perc)

    def get_perc(self=None):
        return self.__local_perc if self else DecimalNumber.__perc

    @property
    def number(self) -> float:
        return self.__number

    def __add__(self, other):
        return DecimalNumber(self.__number + float(other), perc=self.__local_perc)

    def __sub__(self, other):
        return DecimalNumber(self.__number - float(other), perc=self.__local_perc)

    def __mul__(self, other):
        return DecimalNumber(self.__number * float(other), perc=self.__local_perc)

    def __truediv__(self, other):
        return DecimalNumber(self.__number / float(other), perc=self.__local_perc)

    def __pow__(self, power, modulo=None):
        return DecimalNumber(self.number ** float(power))

    def __neg__(self):
        return DecimalNumber(-self.number)

    def __eq__(self, other) -> bool:
        return self.number == float(DecimalNumber(other, perc=self.__local_perc))

    def __ne__(self, other) -> bool:
        return self.number != float(DecimalNumber(other, perc=self.__local_perc))

    def __gt__(self, other) -> bool:
        return self.number > float(DecimalNumber(other, perc=self.__local_perc))

    def __ge__(self, other):
        return self.number >= float(DecimalNumber(other, perc=self.__local_perc))

    def __lt__(self, other):
        return self.number < float(DecimalNumber(other, perc=self.__local_perc))

    def __le__(self, other):
        return self.number <= float(DecimalNumber(other, perc=self.__local_perc))

    def __float__(self):
        return self.number

    def __int__(self):
        return int(self.number)

    def __abs__(self):
        if self.number < 0:
            return DecimalNumber(-self.number)

        return DecimalNumber(self.number)

    def __round__(self, n=None):
        return DecimalNumber(round(self.__number, n))

    def __radd__(self, other):
        if CollectionsUtil.is_iter(other):
            return \
                DecimalNumber(
                    sum([float(num) for num in other]) + self.__number,
                    perc=self.__local_perc)

        return DecimalNumber(float(other) + self.__number, perc=self.__local_perc)

    def __rsub__(self, other):
        return DecimalNumber(float(other) - self.__number, perc=self.__local_perc)

    def __rmul__(self, other):
        if CollectionsUtil.is_iter(other):
            return \
                DecimalNumber(
                    numpy.prod([float(num) for num in other]) * self.__number,
                    perc=self.__local_perc)

        return DecimalNumber(float(other) * self.__number, perc=self.__local_perc)

    def __rtruediv__(self, other):
        return DecimalNumber(float(other) / self.__number, perc=self.__local_perc)

    def __str__(self):
        return str(self.number)

    def __setattr__(self, key, value):
        if key == '_DecimalNumber__number':
            self.__dict__[key] = round(float(value), self.__get_perc())
        else:
            self.__dict__[key] = value

    def __get_perc(self) -> int:
        return self.__local_perc

    @classmethod
    def set_perc(cls, perc: int):
        cls.__perc = perc

    @classmethod
    def dict_with_decimal_to_dict_with_float(cls, dict_: dict) -> dict:
        d = {}

        for k, v in dict_.items():
            if isinstance(v, DecimalNumber):
                d[k] = float(v)
            elif isinstance(v, dict):
                d[k] = cls.dict_with_decimal_to_dict_with_float(v)
            else:
                d[k] = v

        return d


def set_decimal_number_perc(perc: int):
    DecimalNumber.set_perc(perc)
