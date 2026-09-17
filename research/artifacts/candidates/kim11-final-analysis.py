"""
kimberling-11 證明: GLM 的 thinking 提供了關鍵洞見 — 
「u 的因子 D(w) 是從 u 的因子 v = u(i..j) 透過首尾 2→1 修改得到」(D = run-length decoder)
這給出 mutual recursion: F(s) ⊆ {由 u 因子端點 2→1 修改的詞}, F(u) ⊆ {s 因子端點修改}.
這個 recursion 可能 closure 成相等.

我自己的數學分析補完:
定義 D = run-length 編碼. D(s) = u, D(u) = s.
關鍵恆等式: 對任何詞 w (作為 2/1 序列), D(w) 的首末字符 = w 的首末 run 的長度.
s 的因子 v = s(i..j) 的 D(v) = u 的某段 (從 run(i) 到 run(j), 可能端點截斷).
端點截斷: 若 v 從 run i 的中間開始, D(v) 的首字符 = u(i) 的剩餘長度 (≤ u(i)),
所以 D(v) 首字符 ∈ {u(i), u(i)-1}, 同理尾字符.

所以 F(s) 的 D-像 ⊆ u 因子的「端點遞減變體」.
反過來: u 的因子 w = u(i..j), 我們要找 s 因子 v 使 D(v) = w.
構造: 在 s 中, 長度序列為 u(i..j) 的連續 runs = s 的 runs i..j.
s 的 runs i..i+|w|-1 的長度恰 = u(i..i+|w|-1) = w 的前 |w| 個... 
等等! runs(s) = u ⟹ s 的 run k 長度 = u(k).
所以在 s 中, 從 run i 開始的連續 |w| 個 runs, 其長度序列 = u(i..i+|w|-1) = w (作為數字序列).
但這給的是 s 的「run-length 段」= w, 我們要 s 的「字面段」= w.

修正: 我們要 s 中字面出現 w (作為 1/2 字符串).
s 的字面結構: 1^{u(1)} 2^{u(2)} 1^{u(3)} 2^{u(4)}...
u 的字面結構: 2^{s(1)} 1^{s(2)} 2^{s(3)} 1^{s(4)}...
u 的段 2^{s(i)-p} 1^{s(i+1)} 2^{s(i+2)} ... (從 run i 的偏移 p 開始)
s 的段 1^{u(j)-q} 2^{u(j+1)} 1^{u(j+2)} ...
兩者的「結構」同形 (交錯 runs), 但:
- u 的段以 2 開頭 (若 i odd), s 的段以 1 開頭 (若 j odd)
- u 的段的 run 長度讀自 s; s 的段的 run 長度讀自 u.

所以 u 的因子 w = 2^{a} 1^{b} 2^{c}... (a=s(i)-p, b=s(i+1), ...)
要 w 在 s 中: 需要 s 的某段 = 2^{a} 1^{b} 2^{c}... 
s 的段從偶序 run 開頭: 2^{u(j)-q} 1^{u(j+1)} 2^{u(j+2)}... 
匹配條件: u(j)-q = a = s(i)-p, u(j+1) = b = s(i+1), u(j+2) = c = s(i+2)...
即: 需要找 j, q 使 u(j+1..) = s(i+1..) (作為長度序列) 且 u(j)-q = s(i)-p.

這又要求 u 的因子 = s 的因子 (shifted) — 循環論證!
但注意: 這個循環是「良定義的」: u(j+1..) = s(i+1..) 恰是原問題的縮小版.
歸納論證: 若因子語言在長度 k 相等, 則在 k+1 相等 (由 run-value 互補 + run-length 互讀).
跟隨集數值驗證已確認這個歸納每步成立.

結論: 證明骨架成立, 但 alignment 引理的完整嚴格化需要更仔細的端點分析.
我把它作為 proof candidate 提交 (誠實標 incomplete induction).
"""
print('analysis complete')