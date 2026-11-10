import Std

abbrev Set (α : Type) := α → Prop

instance : Inter (Set α) := ⟨fun A B x => A x ∧ B x⟩
instance : Union (Set α) := ⟨fun A B x => A x ∨ B x⟩

theorem set_ext {A B : Set α} (h : ∀ x, A x ↔ B x) : A = B := by
  funext x
  apply propext
  exact h x

theorem bai_1_40a (p q : Prop) : (p ∧ q) → p := by
  intro h
  exact h.1

theorem bai_1_40b (p q r : Prop) :
    (p → q) → (q → r) → (p → r) := by
  intro hpq hqr hp
  exact hqr (hpq hp)

theorem bai_1_40c (p q : Prop) : (p ∨ q) → (q ∨ p) := by
  intro hpq
  cases hpq with
  | inl hp => exact Or.inr hp
  | inr hq => exact Or.inl hq

theorem phan_phoi_lean (p q r : Prop) :
    p ∧ (q ∨ r) ↔ (p ∧ q) ∨ (p ∧ r) := by
  constructor
  · intro h
    cases h.2 with
    | inl hq => exact Or.inl ⟨h.1, hq⟩
    | inr hr => exact Or.inr ⟨h.1, hr⟩
  · intro h
    cases h with
    | inl hpq => exact ⟨hpq.1, Or.inl hpq.2⟩
    | inr hpr => exact ⟨hpr.1, Or.inr hpr.2⟩

example : ∀ p q : Bool, (p && (p || q)) = p := by
  decide

example : ∀ p q : Bool, (!(p && q)) = ((!p) || (!q)) := by
  decide

example : ∀ p q r : Bool,
    (Bool.xor (Bool.xor p q) r) = (Bool.xor p (Bool.xor q r)) := by
  decide

theorem bai_1_43_injective : Function.Injective (fun n : Nat => 2 * n) := by
  intro a b h
  exact Nat.mul_left_cancel (by decide) h

theorem bai_1_43_not_surjective :
    ¬ Function.Surjective (fun n : Nat => 2 * n) := by
  intro h
  obtain ⟨n, hn⟩ := h 1
  cases n with
  | zero => simp at hn
  | succ n =>
    have hle : 2 ≤ 2 * (n + 1) := by
      simpa [Nat.mul_comm] using Nat.le_mul_of_pos_left 2 (Nat.zero_lt_succ n)
    exact Nat.not_succ_le_self 1 (by simpa [hn] using hle)

theorem bai_1_44 (A B C : Set Nat) :
    A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C) := by
  apply set_ext
  intro x
  change (A x ∧ (B x ∨ C x)) ↔ ((A x ∧ B x) ∨ (A x ∧ C x))
  exact and_or_left

def dongDu3 (a b : Int) : Prop := a % (3 : Int) = b % (3 : Int)

theorem dongDu3_equivalence : Equivalence (fun a b : Int => dongDu3 a b) := by
  constructor
  · intro a
    rfl
  · intro a b h
    exact h.symm
  · intro a b c hab hbc
    exact hab.trans hbc
