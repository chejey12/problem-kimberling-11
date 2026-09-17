"""
kimberling-11 證明核心嘗試 (數學論證):
目標: 證明 r(s) 的每個有限因子都是 s 的因子.

已知結構 (交錯構造驗證):
s = 1^{u(1)} 2^{u(2)} 1^{u(3)} 2^{u(4)} ...  (s 的 run j: 值 1/2 交替, 長 u(j))
u = 2^{s(1)} 1^{s(2)} 2^{s(3)} 1^{s(4)} ...  (u 的 run j: 值 2,1 交替, 長 s(j))

關鍵: u 的因子 = u 的連續段. u = 2^{s(1)} 1^{s(2)} 2^{s(3)} 1^{s(4)} ...
s = 1^{u(1)} 2^{u(2)} 1^{u(3)} 2^{u(4)} ...

觀察 1: u 的「run 邊界對齊」因子: u(i..j) = 2^{s(i)} 1^{s(i+1)} ... (交替 run)
   這類段在 s 中的出現: s = 1^{u(1)} 2^{u(2)}...  若 s 中有相鄰 runs (1-run 長 a, 2-run 長 b),
   則 s 含段 2^b 1^{a'} 對某 — 不一定匹配 u(i..j).

觀察 2 (可能的核心): s 和 u 都是「自描述」系統. 
   s 的因子 = u 的因子的某種變換? 
   事實: runs(u) = s ⟹ u 的每個因子 w, 有 runs(w) 是 s 的因子 (子段的 run lengths 是 
   整體 run lengths 的子序列的因子化... 不精確).

觀察 2 (有用!): u 的因子 w 出現在 u 的位置 i. u = r(s). 
   u 的因子對應 s 中「連續 runs 的長度序列」. 
   即 w = (s 中從第 i 個 run 到第 j 個 run 的長度序列).
   要證: s 中存在連續段, 其 run lengths 恰為 w.
   即: 在 s 中找到連續 runs 其長度依序 = w.

這變成: s 的 run-length 序列 u 的每個因子在 s 中出現.
若 s 的因子集 = u 的因子集 (recurrence/uniform distribution), 則題目成立.
而 s = r(u) — s 是 u 的 run-length! s 的因子 vs u 的因子...

數值檢驗: 比較 s 和 u 的 factor complexity p_s(k) vs p_u(k) (k=1..20).
若 p_u(k) <= p_s(k) 且 u 的每個因子在 s 中 → 成立.
可能證明: u 和 s 的因子語言相同! 檢查: u 的因子集 == s 的因子集?
若 F(s) = F(u), 題目 trivially true. 
驗證: 對 k=1..15, 計算 F_s(k) 和 F_u(k) 集合是否相等.
"""
import json
from datetime import datetime, timezone


def runs_of(seq):
    out = []
    prev = seq[0]
    cnt = 1
    for x in seq[1:]:
        if x == prev:
            cnt += 1
        else:
            out.append(cnt)
            prev = x
            cnt = 1
    out.append(cnt)
    return out


def kolakoski_sqrt(n):
    s = [1, 1]
    u = [2]
    s_runs_done = 1
    u_runs_done = 1
    while len(s) < n or len(u) < n:
        j = s_runs_done + 1
        if j - 1 < len(u):
            v = 1 if j % 2 == 1 else 2
            s += [v] * u[j - 1]
            s_runs_done += 1
        j = u_runs_done + 1
        if j - 1 < len(s):
            v = 2 if j % 2 == 1 else 1
            u += [v] * s[j - 1]
            u_runs_done += 1
    return s[:n], u


def factors(seq, k):
    return {''.join(map(str, seq[i:i + k])) for i in range(len(seq) - k + 1)}


def main():
    s, u = kolakoski_sqrt(200000)
    sw = ''.join(map(str, s))
    uw = ''.join(map(str, u))
    print('factor complexity comparison (|F_s(k)| vs |F_u(k)| and set equality):')
    results = []
    for k in range(1, 21):
        Fs = factors(s, k)
        Fu = factors(u, k)
        subset = F_u_in_s = Fs >= factors(u, k) if False else factors(u, k).issubset(Fs)
        equal = Fs == factors(u, k)
        results.append({'k': k, 'p_s': len(Fs), 'p_u': len(factors(u, k)), 'u_subset_s': subset, 'equal': equal})
        print(f'k={k}: p_s={len(Fs)} p_u={len(factors(u,k))} u⊆s={subset} equal={equal}')
    summary = {
        'experiment': 'kimberling-11 factor complexity comparison',
        's_len': len(s),
        'results': results,
        'note': 'If F(r(s)) ⊆ F(s) for all tested k with large N, the factor sets may coincide — supporting a structural proof.',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'claim_status': 'candidate_numeric_check_only',
    }
    out = json.dumps(summary, ensure_ascii=False, indent=1)
    with open('kim11_complexity.json', 'w') as f:
        f.write(out)


if __name__ == '__main__':
    main()