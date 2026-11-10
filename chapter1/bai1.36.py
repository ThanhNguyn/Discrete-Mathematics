"""Bài 1.36 - Ba phiên bản thuật toán Warshall."""
from __future__ import annotations

from time import perf_counter
import random


def warshall_vong_lap(matrix):
    result = [list(map(bool, row)) for row in matrix]
    n = len(result)
    if any(len(row) != n for row in result):
        raise ValueError("ma trận phải vuông")
    for k in range(n):
        for i in range(n):
            if result[i][k]:
                for j in range(n):
                    result[i][j] = result[i][j] or result[k][j]
    return result


def warshall_bit(matrix):
    rows = [sum((1 << j) for j, value in enumerate(row) if value) for row in matrix]
    n = len(rows)
    if any(len(row) != n for row in matrix):
        raise ValueError("ma trận phải vuông")
    for k in range(n):
        mask = 1 << k
        for i in range(n):
            if rows[i] & mask:
                rows[i] |= rows[k]
    return [[bool(row & (1 << j)) for j in range(n)] for row in rows]


def warshall_numpy(matrix):
    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("Cài numpy để dùng warshall_numpy") from exc
    result = np.asarray(matrix, dtype=bool).copy()
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError("ma trận phải vuông")
    for k in range(result.shape[0]):
        result |= result[:, k, None] & result[k, :]
    return result


def benchmark(sizes=(10, 30, 60), seed=1):
    rng = random.Random(seed)
    results = []
    for size in sizes:
        matrix = [[rng.random() < 0.2 for _ in range(size)] for _ in range(size)]
        row = {"n": size}
        for name, function in (
            ("vong_lap", warshall_vong_lap),
            ("bit", warshall_bit),
        ):
            start = perf_counter()
            function(matrix)
            row[name] = perf_counter() - start
        try:
            start = perf_counter()
            warshall_numpy(matrix)
            row["numpy"] = perf_counter() - start
        except RuntimeError:
            row["numpy"] = None
        results.append(row)
    return results


if __name__ == "__main__":
    print(benchmark())
