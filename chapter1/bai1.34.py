"""Bài 1.34 - Sinh mọi tập con bằng đệ quy và mặt nạ bit."""
from __future__ import annotations

from time import perf_counter


def cac_tap_con_de_quy(values):
    values = tuple(values)
    if not values:
        return [()]
    head, *tail = values
    smaller = cac_tap_con_de_quy(tail)
    return smaller + [(head,) + subset for subset in smaller]


def cac_tap_con_mat_na(values):
    values = tuple(values)
    return [
        tuple(values[index] for index in range(len(values)) if mask & (1 << index))
        for mask in range(1 << len(values))
    ]


def cac_tap_con(values, method: str = "mat_na"):
    if method in {"de_quy", "đệ_quy", "recursive"}:
        return cac_tap_con_de_quy(values)
    if method in {"mat_na", "bitmask"}:
        return cac_tap_con_mat_na(values)
    raise ValueError("method phải là 'de_quy' hoặc 'mat_na'")


def benchmark(values) -> dict[str, float]:
    results = {}
    for name, function in (
        ("de_quy", cac_tap_con_de_quy),
        ("mat_na", cac_tap_con_mat_na),
    ):
        start = perf_counter()
        function(values)
        results[name] = perf_counter() - start
    return results


if __name__ == "__main__":
    A = ("a", "b", "c")
    print(cac_tap_con_de_quy(A))
    print(cac_tap_con_mat_na(A))
    print("benchmark:", benchmark(A))
