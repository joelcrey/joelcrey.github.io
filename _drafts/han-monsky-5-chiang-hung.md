---
title: Beyond diagonal hypersurfaces, with Chiang and Hung
category: math
series: han-monsky
series_part: 5
sagecell: true
summary: Chiang and Hung extended the Han–Monsky techniques to sums of monomials in disjoint variables. Their examples, a sign erratum, and new examples with terms linear in e.
---

Chiang and Hung [CH98] extended the techniques of Han and Monsky from diagonal hypersurfaces to
$$f=\sum_{i=1}^m\ \prod_{j=1}^{t_i}X_{i,j}^{d_{i,j}},$$
sums of monomials in pairwise disjoint sets of variables. Write $R=k[[X_{i,j}]]/(f)$ with $k=\mathbb F_p$. By [CH98, Theorem 1.1], the Hilbert–Kunz function has the form $\operatorname{HK}_e(R)=c\,p^{ae}+\sum\Delta(e)$, where $a=\dim R$, $c=e_\text{HK}(R)\in\mathbb Q$, and the $\Delta$'s come from the eigenvalues of an integer matrix $\tilde B$. Everything still happens in the [Han–Monsky ring](han-monsky-2-the-han-monsky-ring.html).

This post follows the third notebook accompanying the notes. As always, run the first cell before the others.

```sage
load("https://joelcrey.github.io/notes/han-monsky/hilbert_kunz.py")
```

The main function is `HK_function_disjoint_monomials(f)`, which takes the polynomial itself; every variable of the ring must appear in $f$. `FS_function_disjoint_monomials(f)` gives the F-signature function, and `HK_groebner(f, e)` is an independent check.

## The examples of Chiang and Hung

**Example 1** [CH98, p. 523]. $f=(XY)^4+T^4+U^4+W^4$ over $\mathbb F_5$:
$$\operatorname{HK}_e(R)=\frac{285166}{96099}\,5^{4e}+\frac{145}{311}\,3^{e}-\frac{752}{309}\,7^{e}.$$

```sage
S.<X,Y,T,U,W> = GF(5)[]
f = (X*Y)^4 + T^4 + U^4 + W^4
H = HK_function_disjoint_monomials(f)
print(H)
print([H(e) for e in range(4)], HK_groebner(f, 1), HK_groebner(f, 2))
```

**Example 2** [CH98, pp. 523–525]. $f=(XYZ)^4+T^4+U^4+W^4$ over $\mathbb F_5$:
$$\operatorname{HK}_e(R)=\frac{378803300}{125571523}\,5^{5e}-\frac{5837}{1561}\,3^{e}+\frac{53520}{13277}-\frac{4042}{1751}\,35^{e}.$$

**Erratum.** The paper prints $+\frac{5837}{1561}3^e$. With that sign, the value at $e=1$ is $14613201/1561$, which is not even an integer, while $\operatorname{HK}_1(R)=9339$.

```sage
S.<X,Y,Z,T,U,W> = GF(5)[]
f = (X*Y*Z)^4 + T^4 + U^4 + W^4
print(HK_function_disjoint_monomials(f))
print("Groebner basis, e = 1:", HK_groebner(f, 1))
```

**Example 3** [CH98, pp. 525–526]. $f=(XYZT)^6+U^6+W^6+V^6$ over $\mathbb F_7$, the example from the [first post](han-monsky-1-shape-of-hilbert-kunz-functions.html) with a coefficient linear in $e$. Where does it come from? The Jordan form of $\tilde B$ has $2\times2$ blocks for the eigenvalues $7$ and $49$. The block for $7$ produces the term $e\,7^e$; the block for $49$ gets coefficient $0$.

```sage
S.<X,Y,Z,T,U,W,V> = GF(7)[]
print(HK_function_disjoint_monomials((X*Y*Z*T)^6 + U^6 + W^6 + V^6))
B = matrix(QQ, ChiangHung(7, [4,1,1,1], [6,6,6,6]).At(1))
print(B.jordan_form())
```

**Unequal exponents** [CH98, p. 525]. If the exponents inside a monomial differ, [CH98, Eq. (21)] writes the function as a rational combination of functions of hypersurfaces with equal exponents inside every monomial. For instance, for $X^2Y^3Z^4+T^4+U^4+W^4$ over $\mathbb F_5$:

```sage
S.<X,Y,Z,T,U,W> = GF(5)[]
HK_function_disjoint_monomials(X^2*Y^3*Z^4 + T^4 + U^4 + W^4)
```

**Kunz's example** from the first post fits here too, since nonzero coefficients are allowed: over $\overline{\mathbb F}_p$ they can be absorbed by rescaling one variable in each monomial, and lengths do not change under field extension.

**A remark on Monsky's example** [CH98, p. 526]. The paper reports a $p=19$ example printed as $XYZT+U^{19}+V^{19}+W^{19}$. As printed, its Hilbert–Kunz function is a single term $c\,19^{6e}$, and the same happens for $p=3,5$. So the printed hypersurface is probably missing exponents. The multiplicity in the paper, $\frac{19017043668514596550}{70272691919506647}$, does not occur for $(XYZT)^a+U^b+V^b+W^b$ with $a,b\leq38$, so the intended hypersurface remains unclear.

```sage
for p in [3, 5, 19]:
    S.<X,Y,Z,T,U,V,W> = GF(p)[]
    print(HK_function_disjoint_monomials(X*Y*Z*T + U^p + V^p + W^p))
```

## New examples: linear coefficients in fewer variables

Example 3 needs 7 variables. Here is one with 6:

**Example.** $f=(XYZ)^6+U^4+V^4+W^4$ over $\mathbb F_5$:
$$\operatorname{HK}_e(R)=\frac{381550975}{125651966}\,5^{5e}-\frac{74448}{29767}\,35^{e}+\frac{163746985}{352557458}-\frac{361260}{13277}\,e\qquad(e\geq0).$$
The linear coefficient sits on the base $1=p^0$, so the function contains a bare term $-\frac{361260}{13277}\,e$.

```sage
S.<X,Y,Z,U,V,W> = GF(5)[]
f = (X*Y*Z)^6 + U^4 + V^4 + W^4
H = HK_function_disjoint_monomials(f)
print(H)
print([H(e) for e in range(4)])
print("Groebner basis, e = 1, 2:", HK_groebner(f, 1), HK_groebner(f, 2))
```

This is the smallest example found in a search over $\sum_i(X_{i,1}\cdots X_{i,t_i})^{d_i}$ with $d_i\leq 8,9,10,12$ for $p=2,3,5,7$. There were **no** linear coefficients with at most 5 variables and $p\leq7$, with 6 variables and $p\in\{2,3\}$, or with 7 variables and $p=2$.

It belongs to the family $(XYZ)^{p+1}+U^{p-1}+V^{p-1}+W^{p-1}$:

| $p$ | linear term |
|---|---|
| 3 | none |
| 5 | $-\frac{361260}{13277}\,e$ |
| 7 | $-\frac{1365280}{8403}\,e$ |
| 11 | $-\frac{1414380528}{1529975}\,e$ |

It appears to hold for every $p\geq5$. This is an observation, not a theorem. Try other primes:

```sage
p = 7
S.<X,Y,Z,U,V,W> = GF(p)[]
HK_function_disjoint_monomials((X*Y*Z)^(p+1) + U^(p-1) + V^(p-1) + W^(p-1))
```

With the ideal $(X,Y,Z,U,V,W^2)$ instead of the maximal ideal, the linear term disappears. The optional argument `ideal` gives one exponent per variable, in the order of the ring:

```sage
S.<X,Y,Z,U,V,W> = GF(5)[]
HK_function_disjoint_monomials((X*Y*Z)^6 + U^4 + V^4 + W^4, ideal=[1,1,1,1,1,2])
```

## F-signature functions

If $f$ contains a pure power $Y^d$, the [Huneke–Leuschke trick](han-monsky-4-f-signature.html) works as for diagonal hypersurfaces: take $I$ generated by all the other variables, so that $R/I=k[Y]/(Y^d)$, $\ell(R/I)=d$ and $u=Y^{d-1}$. Then $I+(u)$ is again a monomial ideal, and
$$\operatorname{FS}_e(R)=d\,q^{\dim R}-\operatorname{HK}_e\big(R,I+(u)\big).$$

Now $A_n$ can be written as $XY+Z^{n+1}$, which is not diagonal:

```sage
p = 7
for n in range(1, 7):
    print("A_%d = XY + Z^%d:  s = %s" % (n, n+1, F_signature(p, [[1,1],[n+1]])))
S.<X,Y,Z> = GF(p)[]
FS_function_disjoint_monomials(X*Y + Z^4)
```

Example 1 has $\operatorname{FS}_e=1$ for every $e$ (F-pure, but not strongly F-regular), and Example 3 is not F-pure:

```sage
S.<X,Y,T,U,W> = GF(5)[]
print(FS_function_disjoint_monomials((X*Y)^4 + T^4 + U^4 + W^4))
S.<X,Y,Z,T,U,W,V> = GF(7)[]
print(FS_function_disjoint_monomials((X*Y*Z*T)^6 + U^6 + W^6 + V^6))
```

Unusual terms carry over to F-signature functions: a sign-alternating term $(-4)^e$, and a term $6^{\lfloor e/2\rfloor}$ coming from the eigenvalues $\pm\sqrt6$:

```sage
S.<X,Y,T,U,W> = GF(7)[]
print(FS_function_disjoint_monomials((X*Y)^2 + T^3 + U^3 + W^3))
print(FS_function_disjoint_monomials((X*Y)^3 + T^3 + U^3 + W^6))
```

And here is a strongly F-regular ring whose F-signature function has a term linear in $e$: $XYZT+U^6+V^4+W^4$ over $\mathbb F_7$. Its F-signature is positive.

```sage
p, exps = 7, [[1,1,1,1],[6],[4],[4]]
S.<X,Y,Z,T,U,V,W> = GF(p)[]
print(FS_function_disjoint_monomials(X*Y*Z*T + U^6 + V^4 + W^4))
print("s(R) =", F_signature(p, exps))
print("FS_1:", fs(p, exps, 1), "  colon formula:", fs_brute(p, exps, 1))
```

Note that different monomials of $f$ must use different variables. So, for example, $D_n=X^2+Y^2Z+Z^{n-1}$ and $E_7=X^2+Y^3+YZ^3$ are outside the scope of this algorithm.

## How the algorithm works

We follow Example 1, $f=(XY)^4+T^4+U^4+W^4$ over $\mathbb F_5$, so $t=(2,1,1,1)$, $d=(4,4,4,4)$ and $a=\sum t_i-1=4$.

**Step A: equal exponents** [CH98, Eq. (21), Corollary 1]. As above, reduce to the case where the exponents inside each monomial are equal.

**Step B: the state space.** The recursion runs over the $p$-adic digits $b_i(\mu)$ of $1/d_i$ [CH98, p. 512]. Everything at step $\mu$ only depends on the pairs $(b_i(\mu),\,p^\mu\bmod d_i)$. The index set $J$ consists of tuples $\sigma$ with $\sigma_i\in\{0^*,0,1,\dots,t_i-2\}$, where $0^*$ is printed as $-1$.

```sage
X = ChiangHung(5, [2,1,1,1], [4,4,4,4])
print(X)
print("J =", X.J)
print("digits of 1/4 in base 5:", [X.b(0, mu) for mu in range(6)])
```

**Step C: the integer recursion** [CH98, p. 516]:
$$\tilde v(n,\mu)=\tilde A(\mu)\,\tilde v(n,\mu+1)+p^{a(n-\mu)}\,\tilde\Gamma(\mu),\qquad \operatorname{HK}_n(R)=\text{second entry of }\tilde v(n,0).$$
The paper prints, for $\mu\geq1$, the matrix $\tilde A(\mu)$ below, $\tilde\Gamma(\mu)=(0,1852,248,1000)$ and $\tilde v(1,1)=(1,1839,249,1001)$ [CH98, p. 523]. Running the recursion by hand for $n=3$:

```sage
print(matrix(ZZ, X.At(1)))
print("Gamma~(1) =", X.Gt(1), "   v~(1,1) =", X.vbase(1))
n = 3
v = vector(ZZ, X.vbase(n))
for mu in range(n-1, -1, -1):
    v = matrix(ZZ, X.At(mu))*v + 5^(X.a*(n-mu))*vector(ZZ, X.Gt(mu))
print("by hand:", v[1], "   X.hk(3):", X.hk(3))
```

**Step D: closed form** [CH98, p. 517]. The data is periodic in $\mu$ after $\rho$ steps, with period $\omega$; here $\rho=0$ and $\omega=1$. So $\tilde v(n,0)=C\,\tilde B^{\tau(n)}\Phi(n)+p^{an}\mathbf z$ with $\tilde B=\tilde A(1)$, and the Jordan form of $\tilde B$ determines which exponentials appear in the Hilbert–Kunz function:

```sage
print("rho, omega =", X.period())
print("eigenvalues of B~:", matrix(QQ, X.At(1)).eigenvalues())
```

The eigenvalues $7$ and $3$ are exactly the bases $7^e$ and $3^e$ in the formula of Example 1.

## References

- [CH98] L. Chiang, Y.-C. Hung, *On Hilbert–Kunz functions of some hypersurfaces*, J. Algebra 199 (1998), 499–527, [doi](https://doi.org/10.1006/jabr.1997.7206).
- [HM93] C. Han, P. Monsky, *Some surprising Hilbert–Kunz functions*, Math. Z. 214 (1993), 119–135, [doi](https://doi.org/10.1007/BF02572395).
