"""Bài 1.33 - BitSet và phép toán tập hợp."""
from __future__ import annotations

from time import perf_counter


class BitSet:
    """Tập số nguyên không âm, lưu bằng một số nguyên làm mặt nạ bit."""

    def __init__(self, values=()):
        self._bits = 0
        for value in values:
            self.add(value)

    @classmethod
    def _from_bits(cls, bits: int) -> "BitSet":
        result = cls()
        result._bits = bits
        return result

    def add(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("BitSet chỉ nhận số nguyên không âm")
        self._bits |= 1 << value

    def __contains__(self, value: int) -> bool:
        return isinstance(value, int) and value >= 0 and bool(
            self._bits & (1 << value)
        )

    def __len__(self) -> int:
        return self._bits.bit_count()

    def __iter__(self):
        bits = self._bits
        while bits:
            lowest = bits & -bits
            yield lowest.bit_length() - 1
            bits ^= lowest

    def __repr__(self) -> str:
        return f"BitSet({list(self)!r})"

    def __eq__(self, other) -> bool:
        return isinstance(other, BitSet) and self._bits == other._bits

    def la_tap_con(self, other: "BitSet") -> bool:
        self._check_other(other)
        return self._bits & ~other._bits == 0

    def giao_nhieu(self, *others: "BitSet") -> "BitSet":
        bits = self._bits
        for other in others:
            self._check_other(other)
            bits &= other._bits
        return self._from_bits(bits)

    def __le__(self, other: "BitSet") -> bool:
        return self.la_tap_con(other)

    @staticmethod
    def _check_other(other) -> None:
        if not isinstance(other, BitSet):
            raise TypeError("toán hạng phải là BitSet")


def benchmark(n: int = 100_000) -> dict[str, float]:
    """So sánh phép kiểm tra tập con BitSet và set."""
    values = range(n)
    bitset = BitSet(values)
    normal = set(values)
    start = perf_counter()
    _ = bitset <= bitset
    bitset_time = perf_counter() - start
    start = perf_counter()
    _ = normal <= normal
    set_time = perf_counter() - start
    return {"bitset": bitset_time, "set": set_time}


if __name__ == "__main__":
    a = BitSet([1, 2, 4])
    b = BitSet([0, 1, 2, 3, 4])
    print("a <= b:", a <= b)
    print("giao:", a.giao_nhieu(b))
    print("benchmark:", benchmark())
