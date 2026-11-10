# Discrete Mathematics - Lean 4

## Cac file Lean

- `cac_phep_toan_trong_lean4.lean`: giao hoan, De Morgan, modus ponens, phan dao va suy dien truc tiep.
- `logic_co_dien_lean4.lean`: luat bai trung, De Morgan chieu con lai va phan chung.
- `bang_chan_tri_bool.lean`: kiem tra cac hang dung tren `Bool` bang `decide`.

## Cai Lean 4

Cai extension **Lean 4** trong VS Code. Neu VS Code chua co Lean toolchain, mo Command Palette (`Ctrl+Shift+P`) va chon lenh cai Lean 4.

Kiem tra cai dat trong PowerShell:

```powershell
lean --version
lake --version
```

## Chay file

Mo PowerShell tai thu muc nay:

```powershell
cd "D:\25112107_NguyenTuanThanh\Discrete-Mathematics"
lean .\logic_co_dien_lean4.lean
lean .\bang_chan_tri_bool.lean
lean .\cac_phep_toan_trong_lean4.lean
```

## Bai lap trinh Chương 1

Các bài 1.33–1.39 và Dự án 1.3 nằm trong thư mục `chapter1`:

```powershell
python .\chapter1\bai1.33.py
python .\chapter1\bai1.34.py
python .\chapter1\bai1.35.py
python .\chapter1\bai1.36.py
python .\chapter1\bai1.37.py
python .\chapter1\bai1.38.py
python .\chapter1\bai1.39.py
python .\chapter1\du_an_1_3.py
```

Các phần vẽ biểu đồ của bài 1.36 và 1.39 dùng `numpy`/`matplotlib` nếu
được cài đặt; các thuật toán chính vẫn chạy được không cần hai thư viện này.

Neu lenh ket thuc ma khong co thong bao loi thi file da duoc Lean kiem tra thanh cong.

## Kiem tra ket qua

`decide` trong file `bang_chan_tri_bool.lean` dung duoc voi Lean co ban.

File `cac_phep_toan_trong_lean4.lean` dung chung minh truc tiep cho dinh ly cuoi, nen khong can Mathlib. Neu muon dung tactic `tauto` trong cac bai khac, can tao project Lake co Mathlib va them dong sau vao dau file:

```lean
import Mathlib
```
