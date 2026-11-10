import Mathlib     -- can Mathlib cho ky hieu ℤ va cac chien thuat norm_num

-- Trong Lean, ∀ va → thuc chat la mot: ∀ la kieu ham phu thuoc.
-- ∃ la mot cau truc quy nap voi mot constructor: ⟨nhan_chung, chung_minh⟩

-- 1) Chung minh mot menh de pho dung
theorem binh_phuong_khong_am : ∀ x : ℤ, 0 ≤ x * x := by
  intro x
  exact mul_self_nonneg x

-- 2) Chung minh mot menh de ton tai: cung cap nhan chung
theorem co_nghiem : ∃ x : ℤ, x + 3 = 7 := by
  exact ⟨4, by norm_num⟩

-- 3) Bac bo mot menh de pho dung bang phan vi du
theorem khong_phai_moi_so_duong : ¬ (∀ x : ℤ, 0 < x * x) := by
  intro h
  have h0 := h 0        -- ap dung gia thiet cho x = 0
  simp at h0            -- 0 < 0 la vo ly

-- 4) De Morgan cho luong tu (Mathlib da co san)
example (P : ℤ → Prop) : (¬ ∀ x, P x) ↔ ∃ x, ¬ P x :=
  not_forall

example (P : ℤ → Prop) : (¬ ∃ x, P x) ↔ ∀ x, ¬ P x :=
  not_exists

-- 5) Thu tu luong tu: chieu de
theorem doi_thu_tu (P : ℤ → ℤ → Prop) :
    (∃ y, ∀ x, P x y) → (∀ x, ∃ y, P x y) := by
  rintro ⟨y, hy⟩ x
  exact ⟨y, hy x⟩

-- 6) Chieu nguoc lai KHONG dung: Lean khong cho ta chung minh no.
--    Ta chi co the chung minh mot phan vi du cu the.
theorem khong_doi_nguoc_duoc :
    (∀ x : ℤ, ∃ y : ℤ, x + y = 0) ∧ ¬ (∃ y : ℤ, ∀ x : ℤ, x + y = 0) := by
  constructor
  · intro x
    exact ⟨-x, by ring⟩
  · rintro ⟨y, hy⟩
    have h0 := hy 0       -- 0 + y = 0  ⇒  y = 0
    have h1 := hy 1       -- 1 + y = 0  ⇒  y = -1
    omega
