"""Sinh bang chan ly cho mot cong thuc menh de bat ky."""
from itertools import product

# Cac phep toan logic co ban, dinh nghia truc tiep tren bool
NOT = lambda p: not p
AND = lambda p, q: p and q
OR = lambda p, q: p or q
XOR = lambda p, q: p != q
IMP = lambda p, q: (not p) or q          # p -> q
IFF = lambda p, q: p == q                # p <-> q


def bang_chan_ly(bien, cong_thuc, ten="F"):
    """In bang chan ly.

    bien      : danh sach ten bien, vi du ["p", "q"]
    cong_thuc : ham nhan cac gia tri bool theo dung thu tu `bien`
    """
    n = len(bien)
    header = " | ".join(f"{v:^3}" for v in bien) + f" || {ten:^5}"
    print(header)
    print("-" * len(header))
    for vals in product([True, False], repeat=n):
        kq = cong_thuc(*vals)
        dong = " | ".join(f"{('T' if v else 'F'):^3}" for v in vals)
        print(f"{dong} || {('T' if kq else 'F'):^5}")


if __name__ == "__main__":
    # Cong thuc (p AND NOT q) -> r
    bang_chan_ly(["p", "q", "r"],
                 lambda p, q, r: IMP(AND(p, NOT(q)), r),
                 ten="(p^¬q)->r")
