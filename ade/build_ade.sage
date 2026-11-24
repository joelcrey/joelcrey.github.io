# Builds _data/ade.yml from the notes "Explicit adjacencies of simple singularities in positive characteristic".
# Run from the repository root:   sage ade/build_ade.sage _data/ade.yml [previous ade.yml to compare arrows with]
# Every family is checked with Singular: for a sample s != 0, F_s at the origin has the Milnor and Tjurina numbers
# of the target, and F_0 is the normal form of the source.
import sys, re
singular.lib("sing.lib")
N = 9
OUT = sys.argv[1]
CH = ["0", "5", "3", "2", "2e"]
P = {"0": 0, "5": 5, "3": 3, "2": 2, "2e": 2}
GF = {"5": "(5^4,a)", "3": "(3^6,a)", "2": "(2^8,a)", "2e": "(2^8,a)", "7": "(7^3,a)", "11": "(11^2,a)"}
# Right equivalence: key -> (contact characteristic whose families are used, p)
RIGHT = {"R0": ("0", 0), "R11": ("0", 11), "R7": ("0", 7), "R5": ("5", 5), "R3": ("3", 3), "R2": ("2", 2), "R2e": ("2e", 2)}
for k, (b, pp) in RIGHT.items(): P[k] = pp

def ring(c, field=None):
    v = "(x,y,z)" if c in ("2e", "R2e") else "(x,y)"
    singular.eval("ring r = %s,%s,ds;" % (field or P[c], v))
def inv(f, c, field=None):
    ring(c, field)
    singular.eval("poly f = %s;" % f)
    t = int(singular.eval("tjurina(f);")); m = int(singular.eval("milnor(f);"))
    return (None if m < 0 else m), t

def tex(s):
    s = s.replace("*", " ")
    s = re.sub(r"\b(c)(\d)\b", r"\1_\2", s)
    s = re.sub(r"\^(\d+)", lambda m: "^{%s}" % m.group(1) if len(m.group(1)) > 1 else "^" + m.group(1), s)
    s = re.sub(r"\^1(?!\d)", "", s)
    s = re.sub(r"\s*([+-])\s*", r" \1 ", s).strip()
    s = s.replace("( - ", "(-").replace("( + ", "(")
    if s.startswith("- "): s = "-" + s[2:]
    return s

# ---------------- nodes ----------------
nodes = {}
def node(id, fam, n, r, key, ch, f):
    d = nodes.setdefault(id, {"id": id, "family": fam, "n": n, "r": r, "key": key, "forms": []})
    d["forms"].append({"chars": ch, "nf": f})
odd = ["0", "5", "3"]
for k in range(1, N + 1): node("A%d" % k, "A", k, None, "A%d" % k, odd, "x^%d+y^2" % (k + 1))
for k in range(4, N + 1): node("D%d" % k, "D", k, None, "D%d" % k, odd, "x^2*y+y^%d" % (k - 1))
node("E6", "E", 6, None, "E6", ["0", "5"], "x^3+y^4")
node("E7", "E", 7, None, "E7", ["0", "5"], "x^3+x*y^3")
node("E8", "E", 8, None, "E8", ["0"], "x^3+y^5")
node("E8^0", "E", 8, 0, "E8^0", ["5"], "x^3+y^5")
node("E8^1", "E", 8, 1, "E8", ["5"], "x^3+y^5+x*y^4")
for id, key, f in [("E6^0", "E6^0", "x^3+y^4"), ("E6^1", "E6", "x^3+y^4+x^2*y^2"), ("E7^0", "E7^0", "x^3+x*y^3"),
                   ("E7^1", "E7", "x^3+x*y^3+x^2*y^2"), ("E8^0", "E8^0", "x^3+y^5"), ("E8^1", "E8^1", "x^3+y^5+x^2*y^3"),
                   ("E8^2", "E8", "x^3+y^5+x^2*y^2")]:
    node(id, "E", int(id[1]), int(id[3]), key, ["3"], f)
# char 2, odd dimension (curves)
def a_(m, r): return "x^2+y^%d" % (2 * m + 1) + ("+x*y^%d" % (2 * m - r) if r else "")
def d_(m, r): return "x^2*y+y^%d" % (2 * m) + ("+x*y^%d" % (2 * m - r) if r else "")
def A2(k, r=0): return "A%d" % k if k % 2 or k == 2 else "A%d^%d" % (k, r)
def D2(k, r=0): return "D%d" % k if k % 2 == 0 else "D%d^%d" % (k, r)
for k in range(1, N + 1):
    if k % 2: node("A%d" % k, "A", k, None, "A%d" % k, ["2"], "x^2+x*y^%d" % ((k + 1) // 2))
    else:
        m = k // 2
        for r in range(m): node(A2(k, r), "A", k, None if m == 1 else r, "A%d" % k if r == m - 1 else A2(k, r), ["2"], a_(m, r))
for k in range(4, N + 1):
    if k % 2 == 0: node("D%d" % k, "D", k, None, "D%d" % k, ["2"], "x^2*y+x*y^%d" % (k // 2))
    else:
        m = (k - 1) // 2
        for r in range(m): node(D2(k, r), "D", k, r, "D%d" % k if r == m - 1 else D2(k, r), ["2"], d_(m, r))
node("E6^0", "E", 6, 0, "E6^0", ["2"], "x^3+y^4")
node("E6^1", "E", 6, 1, "E6", ["2"], "x^3+y^4+x*y^3")
node("E7", "E", 7, None, "E7", ["2"], "x^3+x*y^3")
node("E8", "E", 8, None, "E8", ["2"], "x^3+y^5")
# char 2, even dimension (surfaces), Artin's normal forms
def dl(Nn, r):
    m = Nn // 2
    base = "z^2+x^2*y+x*y^%d" % m if Nn % 2 == 0 else "z^2+x^2*y+y^%d*z" % m
    return base + ("+x*y^%d*z" % (m - r) if r else "")
def DS(Nn, r): return "D%d^%d" % (Nn, r)
for k in range(1, N + 1): node("A%d" % k, "A", k, None, "A%d" % k, ["2e"], "z^%d+x*y" % (k + 1))
for Nn in range(4, N + 1):
    m = Nn // 2
    for r in range(m): node(DS(Nn, r), "D", Nn, r, "D%d" % Nn if r == m - 1 else DS(Nn, r), ["2e"], dl(Nn, r))
E6S = {0: "z^2+x^3+y^2*z", 1: "z^2+x^3+y^2*z+x*y*z"}
E7S = {0: "z^2+x^3+x*y^3", 1: "z^2+x^3+x*y^3+x^2*y*z", 2: "z^2+x^3+x*y^3+y^3*z", 3: "z^2+x^3+x*y^3+x*y*z"}
E8S = {0: "z^2+x^3+y^5", 1: "z^2+x^3+y^5+x*y^3*z", 2: "z^2+x^3+y^5+x*y^2*z", 3: "z^2+x^3+y^5+y^3*z", 4: "z^2+x^3+y^5+x*y*z"}
for n, S in [(6, E6S), (7, E7S), (8, E8S)]:
    top = max(S)
    for r, f in S.items(): node("E%d^%d" % (n, r), "E", n, r, "E%d" % n if r == top else "E%d^%d" % (n, r), ["2e"], f)

def nf(id, c):
    for fm in nodes[id]["forms"]:
        if c in fm["chars"]: return fm["nf"]
    raise Exception("%s not in %s" % (id, c))

# ---------------- families ----------------
fams = []
AR = "[Ar]"
GK = "[GK]"
def fam(chars, src, tgt, F, D=None, where=None, star=False, proof=None, source=None, note=None):
    fams.append(dict(chars=chars, src=src, tgt=tgt, F=F, D=D or F, where=where, star=star, proof=proof, source=source, note=note, sec1=SEC1 and source != AR))
SEC1 = True

PA = ("For $s \\neq 0$, $u = s + x$ is a unit and $F_s = u\\,(x^{K} + (u^{-1/2}y)^2)$; the square root of the unit $u$ exists "
      "since $p \\neq 2$. So $F_s$ is contact equivalent to $x^{K} + y^2$, an $A_{KM}$.")
PD = ("For $s \\neq 0$, $u = s + y$ is a unit and $F_s = u\\,((u^{-1/2}x)^2 y + y^{KM})$; the square root of the unit $u$ exists "
      "since $p \\neq 2$. So $F_s$ is contact equivalent to $x^2y + y^{KM}$, a $D_{KN}$.")
PAD = ("One checks the identity $(y - s^2)\\,F_s = \\big(x(y - s^2) + s^{KM}y\\big)^2 - y^{K}$. For $s \\neq 0$, $y - s^2$ is a unit and "
       "$X = x(y - s^2) + s^{KM}y$ is a coordinate, so $F_s$ is contact equivalent to $X^2 - y^{K}$, an $A_{KN}$.")
def sub(t, **kw):
    for k, v in kw.items(): t = t.replace(k, str(v))
    return t
# Section 1: every p != 2 (E_k read as E_k^0 in char 3; E_8 = E_8^0 in char 5)
def Ek(n, c):
    if c == "3": return "E%d^0" % n
    if c == "5" and n == 8: return "E8^0"
    return "E%d" % n
for c in odd:
    for k in range(2, N + 1):
        fam([c], "A%d" % k, "A%d" % (k - 1), "x^%d+s*x^%d+y^2" % (k + 1, k), proof=sub(PA, KM="%d" % (k - 1), K="%d" % k), source=AR)
    for k in range(5, N + 1):
        fam([c], "D%d" % k, "D%d" % (k - 1), "x^2*y+y^%d+s*y^%d" % (k - 1, k - 2), proof=sub(PD, KM="%d" % (k - 2), KN="%d" % (k - 1)), source=AR)
    for k in range(4, N + 1):
        br = "+".join("s^%d*y^%d" % (2 * i, k - 1 - i) for i in range(1, k - 2))
        fam([c], "D%d" % k, "A%d" % (k - 1), "x^2*y-y^%d-(%s)+2*s^%d*x*y-s^2*x^2" % (k - 1, br, k - 2),
            proof=sub(PAD, KM="%d" % (k - 2), KN="%d" % (k - 1), K="%d" % k), source=AR, note="With $s^2$ for $t$.")
    fam([c], Ek(6, c), "D5", "x^3+s*x^2*y+y^4")
    fam([c], Ek(6, c), "A5", "x^3+(y^2+s*x)^2", source=AR)
    fam([c], Ek(7, c), "D6", "x^3+s*x^2*y+x*y^3")
    fam([c], Ek(7, c), "A6", "16*s^3*x^2+x^3-4*s*x^2*y-8*s^2*x*y^2+y^3*(x+s*y)", source=AR)
    fam([c], Ek(8, c), "D7", "x^3+s^2*x^2*y+2*s*x*y^3+y^5")
    fam([c], Ek(7, c), Ek(6, c), "x^3+x*y^3+s*y^4", source=AR)
    fam([c], Ek(8, c), Ek(7, c) if c != "5" else "E7", "x^3+y^5+s*x*y^3", source=AR)
ARN_A7 = "s^5*(x-s^2*y)^2-x*(5*s^4*y^2+4*s*y^3)+x^3+4*s^6*y^3+5*s^3*y^4+y^5"
for c in ["0", "5"]:
    fam([c], Ek(8, c), "A7", ARN_A7, source=AR)
    fam([c], Ek(6, c), "D5", "(x-s*y)^2*(x+2*s*y)+y^4", source=AR, note="Valid for $p \\geq 5$.")
    fam([c], Ek(7, c), "D6", "(x-s*y)^2*(x+2*s*y)+y^3*(x-s*y)", source=AR, note="Valid for $p \\geq 5$.")
    fam([c], Ek(8, c), "D7", "(x-3*s^2*y)^2*(x+6*s^2*y)-18*s^3*y^4+6*s*x*y^3+y^5", source=AR,
        note="With $t^2$ for $t$ in the linear factors; the printed unfolding is a $D_7$ only for $t = 1$.")
SEC1 = False
# Section 2: characteristic 3
c = "3"
for src, tgt, F, st in [
    ("E6^0", "E6^1", "x^3+y^4+s*x^2*y^2", 0), ("E7^0", "E7^1", "x^3+x*y^3+s*x^2*y^2", 0), ("E8^0", "E8^1", "x^3+y^5+s*x^2*y^3", 0),
    ("E8^1", "E8^2", "x^3+y^5+x^2*y^3+s*x^2*y^2", 1), ("E7^1", "E6^1", "x^3+x*y^3+x^2*y^2+s*y^4", 1),
    ("E8^1", "E7^0", "x^3+y^5+x^2*y^3+s*x*y^3", 1), ("E8^2", "E7^1", "x^3+y^5+x^2*y^2+s*x*y^3", 1),
    ("E6^1", "D5", "x^3+s*x^2*y+y^4+x^2*y^2", 1), ("E6^1", "A5", "x^3+(y^2+s*x)^2+x^2*y^2", 1),
    ("E7^1", "D6", "x^3+s*x^2*y+x*y^3+x^2*y^2", 1),
    ("E7^1", "A6", "(1-s^3)^2*(x^3+x*y^3+x^2*y^2+s^3*y^4)-s^3*(1-s^3)*x^2*y+s^6*(1-s^3)*x*y^2+s^9*x^2", 1),
    ("E8^2", "D7", "x^3+s^2*x^2*y+2*s*x*y^3+y^5+x^2*y^2", 1),
    ("E8^2", "A7", "x^3+y^5+x^2*y^2+s*(1+s)*x*y^3+s^3*x^2*y-s^3*(1-s)*y^4+s^4*(1-s)*x*y^2-s^5*(1-s)*x^2", 1)]:
    fam([c], src, tgt, F, star=bool(st))
fam([c], "E8^0", "A8", "x^3+y^5+s^5*x^2-2*s^4*x*y^2-s*x*y^3+s^3*y^4", source=GK)
fam([c], "E8^0", "A8", ARN_A7, source=AR, note="Arnold's $A_7 \\leftarrow E_8$ unfolding [Kn, p. 597].")
# Section 3: characteristic 5
c = "5"
AB = dict(a="(1+s^2)", b="(3+s^2)")
A7E81 = "a^3*b^2*(x^3+y^5+s^25*x^2)-b^4*x*y^4+a^4*b^3*s^20*x*y^2-2*a^7*b*s^5*x*y^3+(2+s^10)*a*s^10*x^2*y-a^5*b^4*s^15*y^4"
fam([c], "E8^0", "E8^1", "x^3+y^5+s*x*y^4")
fam([c], "E8^1", "E7", "x^3+y^5+x*y^4+s*x*y^3", star=True)
fam([c], "E8^1", "D7", "x^3+s^2*x^2*y+2*s*x*y^3+y^5+x*y^4", star=True)
fam([c], "E8^1", "A7", re.sub(r"\b([ab])\b", lambda m: AB[m.group(1)], A7E81), D=A7E81, where="a = 1 + s^2,\\quad b = 3 + s^2", star=True)
# Section 4: characteristic 2, odd dimension (curves)
c = "2"
fam([c], "A2", "A1", "x^2+y^3+s*x*y")
for m in range(2, 6):
    if 2 * m - 1 <= N: fam([c], "A%d" % (2 * m - 1), A2(2 * m - 2, m - 2), "x^2+x*y^%d+s*y^%d" % (m, 2 * m - 1))
    if 2 * m <= N:
        fam([c], A2(2 * m, m - 1), "A%d" % (2 * m - 1), a_(m, m - 1) + "+s*x*y^%d" % m, star=m - 1 > 0)
        for r in range(m - 1): fam([c], A2(2 * m, r), A2(2 * m, r + 1), a_(m, r) + "+s*x*y^%d" % (2 * m - r - 1), star=r > 0)
        for r in range(2, m): fam([c], A2(2 * m, r), A2(2 * m - 2, r - 2), a_(m, r) + "+s*y^%d" % (2 * m - 1), star=True)
    if 2 * m + 1 <= N:
        fam([c], D2(2 * m + 1, m - 1), "D%d" % (2 * m), d_(m, m - 1) + "+s*x*y^%d" % m, star=True)
        for r in range(m - 1): fam([c], D2(2 * m + 1, r), D2(2 * m + 1, r + 1), d_(m, r) + "+s*x*y^%d" % (2 * m - r - 1), star=r > 0)
        for r in range(2, m): fam([c], D2(2 * m + 1, r), D2(2 * m - 1, r - 2), d_(m, r) + "+s*y^%d" % (2 * m - 2), star=True)
        for r in range(m): fam([c], D2(2 * m + 1, r), A2(2 * m, r), d_(m, r) + "+s*x^2", star=r > 0)
    if 2 * m <= N:
        if m >= 3: fam([c], "D%d" % (2 * m), D2(2 * m - 1, m - 2), "x^2*y+x*y^%d+s*y^%d" % (m, 2 * m - 2))
        fam([c], "D%d" % (2 * m), "A%d" % (2 * m - 1), "x^2*y+x*y^%d+s*x^2" % m)
for src, tgt, F, st in [
    ("E6^0", "E6^1", "x^3+y^4+s*x*y^3", 0), ("E6^0", "D5^0", "x^3+s*x^2*y+y^4", 0), ("E6^0", "A6^2", "x^3+y^4+s^2*x^2", 0),
    ("E6^1", "D5^1", "x^3+s*x^2*y+y^4+x*y^3", 1), ("E6^1", "A5", "x^3+y^4+x*y^3+s*x^2*(s+y)", 1),
    ("E7", "E6^1", "x^3+x*y^3+s*y^4", 0), ("E7", "D6", "x^3+s*x^2*y+x*y^3", 0), ("E8", "E7", "x^3+y^5+s*x*y^3", 0),
    ("E8", "E6^0", "x^3+y^5+s*y^4", 0), ("E8", "D7^2", "x^3+s^2*x^2*y+y^5", 0),
    ("E8", "A7", "x^3+y^5+s^5*x^2+s^9*y^2+s^4*x*y^2+s^3*y^4", 0)]:
    note = None
    if tgt == "A6^2": note = "Arnold's $A_5 \\leftarrow E_6$ unfolding mod $2$; [GK] use $s^4$."
    if (src, tgt) == ("E8", "A7"): note = "Arnold's $A_7 \\leftarrow E_8$ unfolding mod $2$."
    if (src, tgt) == ("E7", "E6^1"): note = "Arnold's $A_6 \\leftarrow E_7$ unfolding mod $2$."
    fam([c], src, tgt, F, star=bool(st), note=note, source=GK if tgt == "A6^2" else AR if (src, tgt) == ("E8", "A7") else None)
# Section 5: characteristic 2, even dimension (surfaces)
c = "2e"
for k in range(2, N + 1): fam([c], "A%d" % k, "A%d" % (k - 1), "z^%d+x*y+s*z^%d" % (k + 1, k))
for Nn in range(4, N + 1):
    m = Nn // 2
    for r in range(m - 1): fam([c], DS(Nn, r), DS(Nn, r + 1), dl(Nn, r) + "+s*x*y^%d*z" % (m - r - 1), star=r > 0)
    if Nn % 2 and Nn - 1 >= 4:
        for r in range(m): fam([c], DS(Nn, r), DS(Nn - 1, r), dl(Nn, r) + "+s*x^2", star=r > 0)
    if Nn % 2 == 0 and m >= 3:
        for r in range(m): fam([c], DS(Nn, r), DS(Nn - 1, max(r - 1, 0)), dl(Nn, r) + "+s*y^%d*z" % (m - 1), star=r > 0)
    for r in range(m): fam([c], DS(Nn, r), "A%d" % (Nn - 1), dl(Nn, r) + "+s*x*z", star=r > 0)
C7 = "s*y^2*z+s^3*x*z+s^2*x^2*y"; C8 = "s^3*y^2*z+s^5*x*z+s^2*x*y^3"
W7 = "c_7 = " + tex(C7); W8 = "c_8 = " + tex(C8)
def E(n, r): return {6: E6S, 7: E7S, 8: E8S}[n][r]
def efam(src_n, r, tgt, h, cterm=None):
    F = E(src_n, r) + "+" + h; D = F; where = None
    if cterm:
        F = E(src_n, r) + "+" + (C7 if cterm == 7 else C8) + ("+" + h if h else "")
        D = E(src_n, r) + "+c%d" % cterm + ("+" + h if h else ""); where = W7 if cterm == 7 else W8
    fam([c], "E%d^%d" % (src_n, r), tgt, F, D=D, where=where, star=r > 0)
efam(6, 0, "E6^1", "s*x*y*z")
for r in range(2): efam(6, r, "D5^%d" % r, "s*x^2*y"); efam(6, r, "A5", "s*x*z")
efam(7, 0, "E7^1", "s*x^2*y*z"); efam(7, 1, "E7^2", "s*y^3*z"); efam(7, 2, "E7^3", "s*x*y*z")
for r in range(4): efam(7, r, "E6^%d" % min(1, max(r - 2, 0)), "s*y^2*z"); efam(7, r, "D6^%d" % max(r - 1, 0), "s*x^2*y")
for r in range(2): efam(7, r, "A7", "", 7)
efam(7, 2, "A7", "s^2*x*y*z", 7); efam(7, 1, "A6", "s^4*x*y^2", 7); efam(7, 2, "A6", "s^3*z^2", 7); efam(7, 3, "A6", "s*z^2", 7)
efam(8, 0, "E8^1", "s*x*y^3*z"); efam(8, 1, "E8^2", "s*x*y^2*z"); efam(8, 2, "E8^3", "s*y^3*z"); efam(8, 3, "E8^4", "s*x*y*z")
for r in range(5): efam(8, r, "E7^%d" % max(r - 1, 0), "s*x*y^3")
for r in range(3): efam(8, r, "D8^%d" % r, "s*x^2*y")
for r in range(3, 5): efam(8, r, "D7^%d" % (r - 2), "s*x^2*y")
efam(8, 2, "D7^0", "s*x*y^2")
for r in range(2): efam(8, r, "A7", "", 8)
efam(8, 3, "A7", "s^2*x*y*z", 8); efam(8, 1, "A6", "s^8*x*y^2", 8); efam(8, 2, "A6", "", 8); efam(8, 4, "A6", "s*z^2", 8)
# fix: E6 superscripts in E_6^{max(r-2,0)} <- E_7^r (E_6 has r = 0, 1)
for f in fams:
    if f["chars"] == ["2e"] and f["src"].startswith("E7^") and f["tgt"].startswith("E6^"):
        r = int(f["src"][3]); f["tgt"] = "E6^%d" % max(r - 2, 0)

# One family per arrow and characteristic: where both the notes and a reference give one, keep the
# reference's (the first one with a source).
groups = {}
for f in fams: groups.setdefault((f["chars"][0], f["src"], f["tgt"]), []).append(f)
dropped = []
for k, g in groups.items():
    if len(g) > 1:
        keep = next((f for f in g if f["source"]), g[0])
        dropped += [(k, f["D"]) for f in g if f is not keep]
fams = [f for f in fams if not any(f["D"] == D_ and (f["chars"][0], f["src"], f["tgt"]) == k for k, D_ in dropped)]
print("dropped (arrow, family):", [(k, D_[:40]) for k, D_ in dropped])

# ---------------- checks ----------------
bad = 0
def at(F, sval): return F.replace("s", "(%s)" % sval)
for f in fams:
    c = f["chars"][0]
    for nm in (f["src"], f["tgt"]): nf(nm, c)
    # F_0 is (equivalent to) the source, F_s for sample s != 0 has the invariants of the target.
    # In characteristic p > 0 the Milnor number is not a contact invariant, so only tau is compared there.
    def key(mt): return mt if c == "0" else mt[1]
    if key(inv(at(f["F"], 0), c)) != key(inv(nf(f["src"], c), c)): print("F0 FAIL", c, f["src"], f["tgt"]); bad += 1
    want = key(inv(nf(f["tgt"], c), c))
    samples = ["2", "1/3", "-5/2"] if c == "0" else ["a", "a^5+1", "a^11"]
    for sv in samples:
        got = key(inv(at(f["F"], sv), c, None if c == "0" else GF[c]))
        if got != want: print("FAIL", c, f["src"], "->", f["tgt"], "s =", sv, "got", got, "want", want); bad += 1
# the identity behind A_{k-1} <- D_k
singular.eval("ring q = 0,(x,y,s),dp;")
for k in range(4, N + 1):
    br = "+".join("s^%d*y^%d" % (2 * i, k - 1 - i) for i in range(1, k - 2))
    F = "x^2*y-y^%d-(%s)+2*s^%d*x*y-s^2*x^2" % (k - 1, br, k - 2)
    singular.eval("poly h = (y-s^2)*(%s) - ((x*(y-s^2)+s^%d*y)^2 - y^%d);" % (F, k - 2, k))
    if singular.eval("h;").strip() != "0": print("identity fails k =", k); bad += 1
print("families", len(fams), "failures", bad)

# ---------------- edges ----------------
edges = {}
for f in fams:
    e = edges.setdefault((f["src"], f["tgt"]), {"from": f["src"], "to": f["tgt"], "chars": [], "unfoldings": []})
    for c in f["chars"]:
        if c not in e["chars"]: e["chars"].append(c)
    e["unfoldings"].append(f)
# implied arrows: those that are compositions of others, per characteristic
for e in edges.values(): e["implied"] = []
for c in CH:
    E_ = [e for e in edges.values() if c in e["chars"]]
    out = {}
    for e in E_: out.setdefault(e["from"], []).append(e["to"])
    def reach(u, skip):
        seen, st = set(), [w for w in out.get(u, []) if w != skip]
        while st:
            v = st.pop()
            if v in seen: continue
            seen.add(v); st += out.get(v, [])
        return seen
    for e in E_:
        if e["to"] in reach(e["from"], e["to"]): e["implied"].append(c)
# compare with the earlier diagram (chars 0, 5, 3, 2) and the covering list of Section 5
oldE = [(a, b, re.findall(r'"([^"]+)"', cs)) for a, b, cs in re.findall(r"  - from: (\S+)\n    to: (\S+)\n    chars: (\[.*?\])", open(sys.argv[2]).read())] if len(sys.argv) > 2 else []
for c in (["0", "5", "3", "2"] if oldE else []):
    o = set((a, b) for a, b, cs in oldE if c in cs)
    n = set((e["from"], e["to"]) for e in edges.values() if c in e["chars"] and c not in e["implied"])
    if o != n: print("covering differs in", c, "old only", sorted(o - n), "new only", sorted(n - o))
cov2e = sorted((e["from"], e["to"]) for e in edges.values() if "2e" in e["chars"] and "2e" not in e["implied"])
print("2e covering:", [a + ">" + b for a, b in cov2e if not (a[0] == "A" and b[0] == "A")])
# unexpected: the arrow does not exist between the characteristic-0 types
def typ(id): return re.sub(r"\^\d+", "", id)
o0 = {}
for e in edges.values():
    if "0" in e["chars"]: o0.setdefault(e["from"], set()).add(e["to"])
def clos0(u):
    seen, st = set(), list(o0.get(u, []))
    while st:
        v = st.pop()
        if v in seen: continue
        seen.add(v); st += list(o0.get(v, []))
    return seen
NOTES = {}
for e in edges.values():
    a, b = typ(e["from"]), typ(e["to"])
    if a != b and b not in clos0(a):
        e["unexpected"] = NOTES.get((e["from"], e["to"]),
            "Not possible in characteristic $0$ [Ar].")
ADJ = {"0": "[Ar]", "5": "[GK, §4.2]", "3": "[GK, §4.2]", "2": "[GK, §4.3]"}
ADJ2E = {("E8^0", "D8^0"): "[GK, §4.5], [Kn, §4]", ("E8^1", "D8^1"): "[GK, §4.5]", ("E8^2", "D8^2"): "[GK, §4.5]",
         ("E7^2", "A7"): "[GK, §4.5]; with $E_7^0 \\to E_7^1 \\to E_7^2$ it gives $E_7^0 \\to A_7$ [Kn, §4]"}
for e in edges.values():
    e["refs"] = {}
    for c in e["chars"]:
        if c in e["implied"]: continue
        r = ADJ.get(c) or (ADJ2E.get((e["from"], e["to"])) if c == "2e" else None)
        if (e["from"], e["to"]) == ("E8^0", "A8") and c == "3": r = "[GK, §4.2], [Kn, §4]"
        if r: e["refs"][c] = r
print("unexpected:", sorted(e["from"] + ">" + e["to"] + " " + ",".join(e["chars"]) for e in edges.values() if "unexpected" in e))

# ---------------- right equivalence ----------------
# Greuel and Nguyen Hong Duc (arXiv:1206.3742, Table 3.2(i), Theorem 3.3): in characteristic p > 2 the right
# simple singularities are A_k (k <= p - 2), D_k (4 <= k < p), and E_6, E_7 (p > 3), E_8 (p > 5); in
# characteristic 2 only A_1, in an even number of variables. We depart from the table for the E's: E_n deforms
# into A_{n-1} (contact families of Section 1), whose members have multiplicity 2 and mu >= tau(A_{n-1}) = n - 1,
# so they are not right simple when n - 1 >= p - 1 (Prop. 3.6(ii)), and by semicontinuity of the modality
# (Prop. 2.7) neither is E_n. So E_6 needs p >= 7, and E_7, E_8 need p >= 11.
def right_simple(id, key):
    b, pp = RIGHT[key]
    if "^" in id: return False
    fam_, n = id[0], int(id[1:])
    if pp == 0: return True
    if pp == 2: return key == "R2" and id == "A1"
    return (fam_ == "A" and n <= pp - 2) or (fam_ == "D" and n < pp) or (fam_ == "E" and n - 1 < pp - 1)
for key, (b, pp) in RIGHT.items():
    S = [id for id, d in nodes.items() if right_simple(id, key) and any(b in fm["chars"] for fm in d["forms"])]
    if key == "R11": S = [id for id in S if id not in ("A8", "A9", "D9")]   # drawn as A_7 <- ... <- A_{p-2}, D_8 <- ... <- D_{p-1}
    if key == "R7": S = [id for id in S if right_simple(id, key)]
    for id in S:
        f = "x*y" if key == "R2" else nf(id, b)
        nodes[id]["forms"].append({"chars": [key], "nf": f})
    # No arrows: adjacency is a contact notion, so the right view only lists the right simple classes.
print("right:", {k: sum(1 for d in nodes.values() if any(k in fm["chars"] for fm in d["forms"])) for k in RIGHT}, "classes")
CH += list(RIGHT)

# ---------------- invariants ----------------
for d in nodes.values():
    for fm in d["forms"]:
        fm["mu"], fm["tau"] = {}, {}
        for c in fm["chars"]:
            fm["mu"][c], fm["tau"][c] = inv(fm["nf"], c)

# ---------------- Singular checks with the classification libraries ----------------
singular.eval('LIB "classifyceq.lib";'); singular.eval('LIB "classify.lib";')
def lib_name(f, c):
    v = "x,y,z" if c == "2e" else "x,y"
    singular.eval("ring rc = %d,(%s),ds;" % (P[c], v)); singular.eval("poly F = %s;" % f)
    try:
        out = singular.eval("classifyCeq(F);" if P[c] else "classify(F);")
    except Exception as ex:
        return None, "ERR"
    if P[c]:
        m = re.findall(r"([ADE])\s*(?:\^\s*(\d+))?\s*\[(\d+)\]", out)
    else:
        m = re.findall(r"([ADE])\[(\d+)\]", out); m = [(a, "", b) for a, b in m]
    if not m: return None, out
    a, r, n = m[-1] if not P[c] else m[0]
    return a + n + ("^" + r if r else ""), out
calib, bad_lib = {}, []
# Only characteristics 0, 5, 3: in characteristic 2 classifyceq.lib misnames several normal forms
# (e.g. the surface D_7^2 comes out as D_4) and errors on others.
for c in ["0", "5", "3"]:
    for d in nodes.values():
        for fm in d["forms"]:
            if c in fm["chars"]:
                nm, out = lib_name(fm["nf"], c)
                if nm is None or (c, nm) in calib: bad_lib.append((c, d["id"], nm, calib.get((c, nm))))
                else: calib[(c, nm)] = d["id"]
print("library names that fail or collide:", bad_lib)
def norm(id): return re.sub(r"\^0$", "", id)
print("library names differing from ids:", sorted((c, i, n) for (c, n), i in calib.items() if norm(n) != norm(i) and n != i))
def expand(F, c):
    singular.eval("ring rc = %d,(%s),dp;" % (P[c], "x,y,z" if c == "2e" else "x,y"))
    singular.eval("poly G = %s;" % F); singular.eval("short = 0;")
    g = singular.eval("string(G);").strip()
    assert g, F
    return g
nsing = {"proof": 0, "sample": 0, "none": 0}
for f in fams:
    c = f["chars"][0]
    if c not in ("0", "5", "3"): continue
    tries = ["1"] if not f["star"] else [str(k) for k in range(1, P[c])]
    for sv in tries:
        G = expand(at(f["F"], sv), c)
        nm, out = lib_name(G, c)
        if nm is not None and calib.get((c, nm)) == f["tgt"]:
            lib = "classify" if c == "0" else "classifyCeq"
            res = re.findall(r"([ADE]\s*(?:\^\s*\d+)?\s*\[\d+\][^\n]*)", out)
            shown = (res[0] if P[c] else "normal form %s" % re.findall(r"[ADE]\[\d+\]", out)[-1]).strip()
            f["singular"] = 'LIB "%s.lib";\nring r = %d,(x,y),ds;\npoly F = %s;   // F_t at t = %s\n%s(F);   // %s' % (
                "classify" if c == "0" else "classifyceq", P[c], G, sv, lib, shown)
            f["singular_note"] = "Weighted homogeneous in $s$, so $s = 1$ suffices." if not f["star"] else "At $s = %s$ only; not a proof for generic $s$." % sv
            nsing["proof" if not f["star"] else "sample"] += 1
            break
    else:
        nsing["none"] += 1; print("no library confirmation:", c, f["src"], "->", f["tgt"])
print("singular snippets:", nsing)
# ---------------- YAML ----------------
CHECK = {
    "wh": "Weighted homogeneous in $s$: every $s \\neq 0$ gives the same type as $s = 1$, where the type was computed exactly.",
    "wh0": "Weighted homogeneous in $s$: every $s \\neq 0$ gives the same type as $s = 1$, where the type was computed exactly, over $\\mathbb{Q}$ and directly for every $p < 60$.",
    "star": "Not weighted homogeneous: the type was checked at $s = 0$ and at $20$ random values of $s$ in a finite field. Strong evidence, not a proof, that the generic member has this type.",
}
def q(s): return "'" + s.replace("'", "''") + "'"
# The unfoldings are computed with the parameter s; on the page it is called t.
def s2t_math(m): return re.sub(r"(?<![A-Za-z\\])s(?![A-Za-z])", "t", m)
def s2t(text): return re.sub(r"\$[^$]+\$", lambda m: s2t_math(m.group(0)), text)
def flow(l): return "[" + ", ".join('"%s"' % x for x in l) + "]"
L = ["# Simple (ADE) singularities and their adjacencies, by characteristic. Read by _includes/ade-map.html.",
     "# Generated from the notes \"Explicit adjacencies of simple singularities in positive characteristic\";",
     "# edit by hand or regenerate. Math is written as in Obsidian ($...$); nf, f and where are TeX without dollars.",
     "# Characteristic \"0\" also covers every p > 5; \"2\" is p = 2 in odd dimension (curves), \"2e\" in even dimension",
     "# (surfaces). For p != 2, add a nondegenerate quadratic form Q in further variables; for p = 2 see the notes.",
     "#",
     "# nodes: id (A6^2 means A_6^2), family, n, r (superscript or null), forms: per characteristics, normal",
     "#        form nf, Milnor number mu (of this normal form; null: infinite) and Tjurina number tau. In each",
     "#        characteristic the class with the largest superscript is drawn where the classical one is.",
     "# edges: `from` deforms into `to`; implied: characteristics where the arrow is a composition of others",
     "#        (drawn only on request); unfoldings: a family F_s with F_0 = from and F_s of type `to` for s != 0",
     "#        (for generic s when generic: true), with optional where, proof, note, source and a Singular check.",
     "",
     "chars:"]
CHN = {
 "0": ("0 or p > 5", "The classical diagram [Ar]."),
 "5": ("p = 5", "$E_8$ splits into $E_8^0$ and $E_8^1$ [GK, 1.2], [Art, §3]."),
 "3": ("p = 3", "$E_6$, $E_7$ split in two and $E_8$ in three [GK, 1.2], [Art, §3]."),
 "2": ("p = 2, odd dim.", "Plane curves; in $n = 2k$ variables add $x_3x_4 + \\dots + x_{n-1}x_n$ [GK, 1.2], [Kr]."),
 "2e": ("p = 2, even dim.", "Surfaces, Artin's normal forms [Art, §3], [GK, 1.2], [Kr]; in $n = 2k+1$ variables add $x_4x_5 + \\dots + x_{n-1}x_n$ [GK, 1.2]."),
 "R0": ("0", "Same classes as for contact equivalence [Ar], [GN, §3]."),
 "R11": ("p ≥ 11", "Right simple: $A_k$ ($k \\leq p - 2$), $D_k$ ($k \\leq p - 1$), $E_6$, $E_7$, $E_8$ [GN, Thm. 3.2]."),
 "R7": ("p = 7", "Right simple: $A_k$ ($k \\leq 5$), $D_k$ ($k \\leq 6$), $E_6$ [GN, Thm. 3.2]. $E_7$, $E_8$, listed in [GN, Table 3.2(i)], are left out by [GN, Prop. 2.7 and 3.6]. *Disclaimer: this departs from [GN] and is our own reading; it has not been confirmed by the authors.*"),
 "R5": ("p = 5", "Right simple: $A_1$, $A_2$, $A_3$, $D_4$ [GN, Thm. 3.2]. $E_6$, $E_7$, listed in [GN, Table 3.2(i)], are left out by [GN, Prop. 2.7 and 3.6]. *Disclaimer: this departs from [GN] and is our own reading; it has not been confirmed by the authors.*"),
 "R3": ("p = 3", "Only $A_1$ is right simple [GN, Thm. 3.2]."),
 "R2": ("p = 2, odd dim.", "Only $A_1 = x_1x_2 + \\dots + x_{n-1}x_n$ is right simple [GN, Thm. 3.3]."),
 "R2e": ("p = 2, even dim.", "No right simple singularities [GN, Thm. 3.3]."),
}
NFREF = {"0": "[Ar]", "5": "[GK, 1.2], [Art, §3]", "3": "[GK, 1.2], [Art, §3]", "2": "[GK, 1.2], [Kr]", "2e": "[Art, §3], [GK, 1.2], [Kr]",
         "R0": "[Ar]", "R11": "[GN, Table 3.2(i)]", "R7": "[GN, Table 3.2(i)]", "R5": "[GN, Table 3.2(i)]", "R3": "[GN, Table 3.2(i)]", "R2": "[GN, Thm. 3.3]", "R2e": "[GN, Thm. 3.3]"}
for c in CH:
    L.append("  - key: \"%s\"" % c); L.append("    label: \"%s\"" % CHN[c][0]); L.append("    equiv: %s" % ("right" if c in RIGHT else "contact"))
    if c == "R11": L.append("    ends: { A: \"A_{p-2}\", D: \"D_{p-1}\" }")
    L.append("    nf_ref: %s" % q(NFREF[c]))
    L.append("    note: %s" % q(CHN[c][1]))
L += ["", "nodes:"]
order = {"A": 0, "D": 1, "E": 2}
for d in sorted(nodes.values(), key=lambda d: (order[d["family"]], d["n"], d["r"] or 0)):
    L += ["  - id: %s" % d["id"], "    family: %s" % d["family"], "    n: %d" % d["n"], "    r: %s" % ("null" if d["r"] is None else d["r"]),
          "    forms:"]
    for fm in d["forms"]:
        L.append("      - chars: %s" % flow(fm["chars"]))
        L.append("        nf: %s" % q(tex(fm["nf"])))
        L.append("        mu: { %s }" % ", ".join('"%s": %s' % (c, "null" if m is None else m) for c, m in fm["mu"].items()))
        L.append("        tau: { %s }" % ", ".join('"%s": %d' % (c, t) for c, t in fm["tau"].items()))
        art = [c for c in fm["chars"] if c == "2e" and d["family"] != "A" or (c in ("3", "5") and d["family"] == "E" and (c == "3" or d["n"] == 8))]
        if art: L.append("        tau_ref: { %s }" % ", ".join('"%s": "[Art, §3]"' % c for c in art))
L += ["", "edges:"]
for e in edges.values():
    L += ["  - from: %s" % e["from"], "    to: %s" % e["to"], "    chars: %s" % flow(e["chars"])]
    if e["implied"]: L.append("    implied: %s" % flow(e["implied"]))
    if e.get("refs"): L.append("    refs: { %s }" % ", ".join('"%s": %s' % (k, q(v)) for k, v in e["refs"].items()))
    if e.get("via"):
        L.append("    via: { %s }" % ", ".join('"%s": %s' % (k, flow(v)) for k, v in e["via"].items()))
    if "unexpected" in e: L.append("    unexpected: %s" % q(e["unexpected"]))
    if e["unfoldings"]: L.append("    unfoldings:")
    for f in e["unfoldings"]:
        L.append("      - chars: %s" % flow(f["chars"]))
        L.append("        f: %s" % q(s2t_math(tex(f["D"]))))
        if f["where"]: L.append("        where: %s" % q(s2t_math(f["where"])))
        if f["star"]: L.append("        generic: true")
        if f["proof"]: L.append("        proof: %s" % q(s2t(f["proof"])))
        if f["note"]: L.append("        note: %s" % q(s2t(f["note"])))
        if f["source"]: L.append("        source: %s" % q(f["source"]))
        if f.get("singular"):
            L.append("        singular: |")
            L += ["          " + ln for ln in f["singular"].split("\n")]
            L.append("        singular_note: %s" % q(s2t(f["singular_note"])))

open(OUT, "w").write("\n".join(L) + "\n")
print("wrote", OUT, "nodes", len(nodes), "edges", len(edges))
