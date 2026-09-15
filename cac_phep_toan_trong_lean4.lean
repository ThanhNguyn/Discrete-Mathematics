-- Cac phep toan logic trong Lean 4:
--   ¬ p        phu dinh      (viet la  Not p)
--   p ∧ q      hoi           (And p q)
--   p ∨ q      tuyen         (Or p q)
--   p → q      keo theo      (kieu ham!)
--   p ↔ q      tuong duong   (Iff p q)

-- 1) Luat giao hoan cua phep hoi: chung minh thu cong
theorem hoi_giao_hoan (p q : Prop) : p ∧ q ↔ q ∧ p := by
  constructor
  · intro h
    exact ⟨h.2, h.1⟩
  · intro h
    exact ⟨h.2, h.1⟩

-- 2) Luat De Morgan (chieu de, dung cho logic truc giac)
theorem de_morgan_1 (p q : Prop) : ¬(p ∨ q) ↔ (¬p ∧ ¬q) := by
  constructor
  · intro h
    exact ⟨fun hp => h (Or.inl hp), fun hq => h (Or.inr hq)⟩
  · intro h hpq
    cases hpq with
    | inl hp => exact h.1 hp
    | inr hq => exact h.2 hq

-- 3) Modus ponens - hien nhien duoi goc nhin Curry-Howard:
--    ap dung mot ham cho mot doi so
theorem modus_ponens (p q : Prop) (hpq : p → q) (hp : p) : q := hpq hp

-- 4) Luat phan dao
theorem phan_dao (p q : Prop) (h : p → q) : ¬q → ¬p :=
  fun hnq hp => hnq (h hp)

-- 5) Chien thuat `tauto` giai tu dong moi hang dung menh de
theorem vi_du_tauto (p q r : Prop) :
    (p → q) → (q → r) → (p → r) := by
  intro hpq hqr hp
  exact hqr (hpq hp)
