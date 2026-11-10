"""Bài 1.35 - Kiểm tra các tính chất của một quan hệ."""
from __future__ import annotations

import random


def _validate_matrix(matrix):
    rows = [list(row) for row in matrix]
    size = len(rows)
    if any(len(row) != size for row in rows):
        raise ValueError("ma trận quan hệ phải vuông")
    return rows, size


def kiem_tra_quan_he(matrix) -> dict[str, bool]:
    M, n = _validate_matrix(matrix)
    return {
        "phan_xa": all(M[i][i] for i in range(n)),
        "doi_xung": all(M[i][j] == M[j][i] for i in range(n) for j in range(n)),
        "phan_doi_xung": all(
            i == j or not (M[i][j] and M[j][i])
            for i in range(n)
            for j in range(n)
        ),
        "bac_cau": all(
            not (M[i][j] and M[j][k]) or M[i][k]
            for i in range(n)
            for j in range(n)
            for k in range(n)
        ),
    }


def thong_ke_ngau_nhien(size: int = 5, samples: int = 100, seed: int = 1):
    if size < 0 or samples < 0:
        raise ValueError("size và samples phải không âm")
    rng = random.Random(seed)
    counts = {
        name: 0
        for name in ("phan_xa", "doi_xung", "phan_doi_xung", "bac_cau")
    }
    for _ in range(samples):
        matrix = [[rng.choice((False, True)) for _ in range(size)] for _ in range(size)]
        for name, value in kiem_tra_quan_he(matrix).items():
            counts[name] += value
    return {name: count / samples if samples else 0.0 for name, count in counts.items()}


if __name__ == "__main__":
    print(thong_ke_ngau_nhien())
