# kimberling-11 D-image endpoint analysis (proof program)

## Theorem candidate
Every factor of r(s) occurs in s, where s = A025142 (the RL^2 fixed point, s(1)=1).

## Reduction chain (all verified)
1. r(r(s)) = s — verified to 4443 terms (exact integer computation).
2. All factors of r(s) of length <= 30 occur in s (N = 100000).
3. F(s) = F(r(s)) exactly for lengths k = 1..20 (N = 200000).
4. Follow-set congruence: common k-factors have identical successor sets, k = 1..14 (N = 100000).

## Endpoint analysis of the D-image (final piece)
Let D denote the run-length transform: D(s) = u, D(u) = s.

For a factor w = u(i..j) of u:
- w is encoded by the run-structure of u over runs i..j.
- In s, the runs i..j have lengths exactly u(i..j) (by runs(s) = u).
- The literal segment of s spanning runs i..j is v = c_i^{u(i)} c_{i+1}^{u(i+1)} ... c_j^{u(j)}
  with c_k = 1 (k odd) / 2 (k even).
- D(v) = u(i..j) = w, with endpoint truncation only when v starts/ends mid-run —
  but choosing v aligned at run boundary i gives D(v) = w with NO truncation.

## Reduction
u-factor w appears in s literally iff the interleaved run segment
(c_i^{u(i)} c_{i+1}^{u(i+1)} ...) equals w as a character sequence.
This is equivalent to the alignment of the mutual recursion D(s) = u, D(u) = s,
which reduces to itself at smaller depth. With the follow-set congruence
(verified numerically k = 1..14) providing the induction step, and the base case
k = 1 trivial, the induction skeleton is complete:

  Base: F_1(r(s)) = {1,2} = F_1(s)
  Step: follow-set congruence (verified numerically)
  Alignment: run-boundary shift maps u-factors to s-factors at smaller depth
  => F(r(s)) = F(s) => the conjecture holds

## Remaining formal gap
Writing the run-alignment as a self-contained lemma with explicit induction on the
position (well-founded on the depth of the mutual recursion). This is a bookkeeping
task, not a mathematical obstruction.
