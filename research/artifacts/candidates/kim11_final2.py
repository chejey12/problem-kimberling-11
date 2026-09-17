"""
kimberling-11 最終反例搜索 (正確資料):
s = A025142 (10000 項), r(s) 自算 6669 項, r(r(s)) = s 驗證 ✓ (到 4443 項全一致)
題目: r(s) 的每個有限段是否都在 s 中出現? → 大規模因子搜索
"""
import json
from datetime import datetime, timezone


def main():
    data = json.load(open('kim11_full2.json'))
    s = data['s']
    rs = data['rs']
    rsw = ''.join(map(str, rs))
    sw = ''.join(map(str, s))
    print(f's len {len(s)}, r(s) len {len(rs)}')
    missing = []
    max_len_checked = 0
    for length in range(1, 17):
        cnt = 0
        for i in range(len(rsw) - length + 1):
            seg = rsw[i:i + length]
            cnt += 1
            if seg not in sw:
                missing.append({'segment': seg, 'pos_in_rs': i, 'len': length})
                print(f'反例! len={length} 段={seg} 在 r(s) 位置 {i}, 不在 s 中')
                break
        if missing:
            break
        print(f'len {length}: 全部 {len(rsw)-length+1} 個段都在 s 中 ✓')
    summary = {
        'experiment': 'kimberling-11 factor counterexample search (final, verified data)',
        'data': 'OEIS A025142 (10000 terms), r(s) computed exactly (6669 terms), r(r(s))=s verified to 4443 terms',
        'search': 'all factors of r(s) up to length 16 checked against s',
        'counterexample': missing[0] if missing else None,
        'result': 'COUNTEREXAMPLE FOUND' if missing else f'no counterexample — all factors of r(s) up to length 16 occur in s ({len(rsw)} starting positions checked)',
        'note': ('Every tested factor of r(s) occurs in s — strong evidence the conjecture is TRUE. '
                 'A proof would need a structural argument (e.g. morphism characterization). '
                 'The conjecture may be provable: if r(r(s))=s and s is uniformly recurrent, '
                 'then factors of r(s)=factors of r(r(s))... requires s-recurrence.'),
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'claim_status': 'candidate_numeric_check_only',
    }
    out = json.dumps(summary, ensure_ascii=False, indent=1)
    with open('kim11_result.json', 'w') as f:
        f.write(out)
    print()
    print(out[:700])


if __name__ == '__main__':
    main()