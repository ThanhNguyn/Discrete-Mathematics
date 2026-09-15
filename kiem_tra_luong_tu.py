"""Danh gia menh de co luong tu tren mien huu han."""


def for_all(mien, P):
    """∀x ∈ mien: P(x)  -- tra ve (gia_tri, phan_vi_du)."""
    for x in mien:
        if not P(x):
            return False, x               # tim thay phan vi du
    return True, None


def exists(mien, P):
    """∃x ∈ mien: P(x)  -- tra ve (gia_tri, nhan_chung)."""
    for x in mien:
        if P(x):
            return True, x                # tim thay nhan chung
    return False, None


def exists_unique(mien, P):
    """∃!x ∈ mien: P(x)."""
    ds = [x for x in mien if P(x)]
    return (len(ds) == 1), (ds[0] if len(ds) == 1 else None)


if __name__ == "__main__":
    Z = range(-20, 21)

    print(for_all(Z, lambda x: x * x >= 0))       # (True, None)
    print(for_all(Z, lambda x: x * x > 0))        # (False, 0)
    print(exists(Z, lambda x: x + 3 == 7))        # (True, 4)
    print(exists_unique(Z, lambda x: x + 3 == 7)) # (True, 4)

    # Luong tu long nhau:  ∀x ∃y (x + y = 0)
    print(for_all(Z, lambda x: exists(Z, lambda y: x + y == 0)[0]))
    # >>> (True, None)

    #                      ∃y ∀x (x + y = 0)
    print(exists(Z, lambda y: for_all(Z, lambda x: x + y == 0)[0]))
    # >>> (False, None)   -- dung nhu Dinh ly 1.3 du bao
