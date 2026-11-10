"""Bài 1.39 - Đo va chạm của ba hàm băm trên chuỗi tiếng Việt."""
from __future__ import annotations

from collections import Counter
import random


def hash_python(text: str, table_size: int) -> int:
    return hash(text) % table_size


def hash_da_thuc(text: str, table_size: int) -> int:
    value = 0
    for character in text:
        value = (value * 31 + ord(character)) % table_size
    return value


def hash_cong(text: str, table_size: int) -> int:
    return sum(ord(character) for character in text) % table_size


def tao_du_lieu(so_luong=10_000, seed=1):
    rng = random.Random(seed)
    prefixes = ("sinh viên", "giảng viên", "môn học", "lập trình", "toán rời rạc")
    adjectives = ("đại cương", "nâng cao", "thực hành", "ứng dụng", "cơ sở")
    result = set()
    while len(result) < so_luong:
        result.add(f"{rng.choice(prefixes)} {rng.choice(adjectives)} {len(result):05d}")
    return sorted(result)


def do_va_cham(texts=None, table_size=1024):
    if table_size <= 0:
        raise ValueError("table_size phải dương")
    texts = tao_du_lieu() if texts is None else list(texts)
    functions = {
        "python": hash_python,
        "da_thuc_31": hash_da_thuc,
        "cong": hash_cong,
    }
    results = {}
    for name, function in functions.items():
        buckets = Counter(function(text, table_size) for text in texts)
        groups = Counter(buckets.values())
        results[name] = {
            "so_chuoi": len(texts),
            "so_o_bi_dung": len(buckets),
            "so_o_va_cham": sum(size > 1 for size in buckets.values()),
            "so_chuoi_trong_va_cham": sum(
                size for size in buckets.values() if size > 1
            ),
            "phan_bo_do_dai_nhom": dict(sorted((size, count) for size, count in groups.items())),
            "max_nhom": max(buckets.values(), default=0),
        }
    return results


def ve_bieu_do(results, output_path):
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Cài matplotlib để vẽ biểu đồ") from exc
    labels = list(results)
    values = [results[label]["so_o_va_cham"] for label in labels]
    plt.bar(labels, values)
    plt.ylabel("Số ô có va chạm")
    plt.title("So sánh va chạm hàm băm")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


if __name__ == "__main__":
    for name, result in do_va_cham().items():
        print(name, result)
