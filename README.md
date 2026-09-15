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

Neu lenh ket thuc ma khong co thong bao loi thi file da duoc Lean kiem tra thanh cong.

## Kiem tra ket qua

`decide` trong file `bang_chan_tri_bool.lean` dung duoc voi Lean co ban.

File `cac_phep_toan_trong_lean4.lean` dung chung minh truc tiep cho dinh ly cuoi, nen khong can Mathlib. Neu muon dung tactic `tauto` trong cac bai khac, can tao project Lake co Mathlib va them dong sau vao dau file:

```lean
import Mathlib
```
