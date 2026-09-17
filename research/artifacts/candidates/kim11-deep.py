"""
kimberling-11 證明嘗試 (T1/T3 路線):
主張: s = A025142 (r(r(s))=s, s(1)=1, s ≠ r(s)), 則 r(s) 的每個有限因子都出現在 s 中.

觀察: s 與 u = r(s) 滿足:
- s 的 run 值交替 (1,2,1,2,...), run 長度依序 = u(1), u(2), ...
- u 的 run 值交替 (2,1,2,1,...), run 長度依序 = s(1), s(2), ...

關鍵結構事實: 
s = 1^{u(1)} 2^{u(2)} 1^{u(3)} 2^{u(4)} ...
u = 2^{s(1)} 1^{s(2)} 2^{s(3)} 1^{s(4)} ...

證明策略: r(s) = u 的每個因子出現在 s 中.
u 本身是「2^{s(1)} 1^{s(2)} 2^{s(3)} ...」的 run lengths.
u 的因子 w = u(i..j). 要證 w 是 s 的因子.

觀察: u 是 2,1 開頭的交錯 run 結構. u 的因子有兩種: 
以 2 開頭 (若對齊 run 邊界) 或任意位置.
s 以 1 開頭: s = 1^{u(1)} 2^{u(2)} 1^{u(3)}...

實際計算的強證據: len<=16 全部出現.
深入: 計算 r(s) 中「最長的不在 s 中的因子」不存在 → 檢查更長因子 (len 17..32) + 統計 s 的 factor complexity vs r(s) 的.
若 s 的 p-複雜度 (不同因子數) >= r(s) 的對應值, 且已知結構... 
先做大規模 factor 對照 (s 擴展到 100k 項), 並比較 factor complexity 曲線.
"""
import json
from datetime import datetime, timezone


def runs_of(seq):
    out = []
    if not seq:
        return out
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
    """構造 s: r(r(s))=s. 用交錯構造: s 的 run i 長度 = u(i), u 的 run j 長度 = s(j)."""
    s = [1, 1]  # run1: 1×2 (u(1)=2)
    u = [2]
    # 逐步: s 的 run 2 長度 = u(2) — 但 u(2) 未知, 需從 s 得: u = runs(s), 
    # u(2) = s 的第2個 run 長度 = s(3)? 不對.
    # 用雙指針法: 同時生成 s 和 u.
    # s 的第 j 個 run: 值 = 1 if j odd else 2, 長度 = u[j-1]
    # u 的第 j 個 run: 值 = 2 if j odd else 1, 長度 = s[j-1]
    # 從 s(1)=1 開始: 第一個 run (1的 run) 長度 u(1) — 未知. 
    # 由 r(r(s))=s 且 s(1)=1: u(1) = |第一個 1-run|. 
    # Kimberling 頁面: s = 1,1,2,... → u(1) = 2, u(2) = 1, ...
    # 生成: 交錯推進 — 用已知的開頭 (1,1) 和 u(1)=2, 然後:
    # u 的 run j 長度 = s(j): u run1 (值2) 長 s(1)=1 → u=[2]
    # u run2 (值1) 長 s(2)=1 → u=[2,1]
    # s run2 (值2) 長 u(2)=1 → s=[1,1,2]
    # u run3 (值2) 長 s(3)=2 → u=[2,1,2,2]
    # s run3 (值1) 長 u(3)=2 → s=[1,1,2,1,1]
    # s run4 (值2) 長 u(4)=2 → s=[1,1,2,1,1,2,2]
    # u run4 (值1) 長 s(4)=1 → u=[2,1,2,2,1]
    # 交錯規則: 交替生成 s-run 和 u-run, 每個的長度從對方序列讀下一個值.
    s = [1, 1]
    u = [2]
    s_runs_done = 1
    u_runs_done = 1
    while len(s) < n or len(u) < n:
        # 生成 s 的下一個 run (run j = s_runs_done+1): 值, 長度 = u[s_runs_done] (0-indexed: u[s_runs_done])
        j = s_runs_done + 1
        if j - 1 < len(u):
            v = 1 if j % 2 == 1 else 2
            ln = u[j - 1]
            s += [v] * ln
            s_runs_done += 1
        # 生成 u 的下一個 run: 值 = 2 if j odd else 1, 長度 = s[j-1]
        j = u_runs_done + 1
        if j - 1 < len(s):
            v = 2 if j % 2 == 1 else 1
            ln = s[j - 1]
            u += [v] * ln
            u_runs_done += 1
        # 保護: 若 u 已夠長但 s 沒進展 → 用 u 生成 s
        if j - 1 >= len(s) and j - 1 >= len(u):
            break
    return s[:n], u


def main():
    s, u = kolakoski_sqrt(100000)
    # 驗證
    calc_u = runs_of(s)
    ok1 = calc_u[:len(u)] == u[:len(calc_u)] if len(calc_u) <= len(u) else u == calc_u[:len(u)]
    calc_s = runs_of(u)
    ok2 = calc_s[:min(len(s), len(calc_s))] == s[:min(len(s), len(calc_s))]
    print('r(s) consistent:', ok1, '| r(u) consistent:', ok2)
    # factor 搜索: u 的所有因子 (len<=30) 在 s 中?
    sw = ''.join(map(str, s))
    uw = ''.join(map(str, u))
    missing = []
    for length in range(1, 31):
        for i in range(len(uw) - length + 1):
            seg = uw[i:i + length]
            if seg not in sw:
                missing.append({'segment': seg, 'pos': i, 'len': length})
                break
        if missing:
            print(f'len {length}: MISSING {missing[-1]}')
            break
        else:
            print(f'len {length}: all present ({len(uw)-length+1} positions)')
    summary = {
        'experiment': 'kimberling-11 extended factor search + structural construction',
        'construction': 'interleaved run-length generation, r(r(s))=s verified',
        's_len': len(s), 'u_len': len(u),
        'r_s_eq_u': ok1, 'r_u_eq_s': ok2,
        'missing_factors': missing,
        'result': 'COUNTEREXAMPLE' if missing else f'no counterexample: all factors of r(s) up to length 30 occur in s (N=100000)',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'claim_status': 'candidate_numeric_check_only',
    }
    out = json.dumps(summary, ensure_ascii=False, indent=1)
    with open('kim11_deep.json', 'w') as f:
        f.write(out)
    print()
    print(out[:600])


if __name__ == '__main__':
    main()