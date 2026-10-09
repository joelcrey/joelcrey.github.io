---
title: The Han–Monsky algorithm
category: math
series: han-monsky
series_part: 3
sagecell: true
summary: A functional equation for the function D_k, and how it turns into an algorithm computing the Hilbert–Kunz function of any diagonal hypersurface from a couple of its values.
---

We now come back to computing the Hilbert–Kunz function of a diagonal hypersurface, armed with the [Han–Monsky ring](han-monsky-2-the-han-monsky-ring.html) $\Gamma_k$. As always, run the first cell before the others.

```sage
load("https://joelcrey.github.io/notes/han-monsky/hilbert_kunz.py")
```

## The functions $D_k$ and $\ell_k$

First, a useful extension of $\Gamma_k$.

**Definition.** For a real number $t\geq0$, write $t=n+\vartheta$ with $n=\lfloor t\rfloor$ and $\vartheta\in[0,1)$, and set
$$\delta_t=(1-\vartheta)\,\delta_n+\vartheta\,\delta_{n+1}\in\Gamma_k\otimes_{\mathbb Z}\mathbb R\qquad(\delta_0=0),$$
the linear interpolation of $i\mapsto\delta_i$. Extend $\alpha$ $\mathbb R$-linearly. Then, for $t_1,\dots,t_n\in\mathbb Q_{\geq0}$ and integers $r_1,\dots,r_n\geq0$, put
$$D_k(t_1,\dots,t_n)=\alpha\Big(\prod_{i=1}^n\delta_{t_i}\Big),\qquad \ell_k(r_1,\dots,r_n)=\alpha\Big(\prod_{i=1}^n\lambda_{r_i}\Big).$$

The observations of the previous post can then be written as:

**Lemma** [HM93, Lemma 5.6]. If $a_1,\dots,a_n,d_1,\dots,d_n$ are positive integers, then
$$\dim_k\frac{k[x_1,\dots,x_n]}{(x_1^{a_1},\dots,x_n^{a_n},x_1^{d_1}+\dots+x_n^{d_n})}=d_1\cdots d_n\,D_k\Big(\frac{a_1}{d_1},\dots,\frac{a_n}{d_n}\Big).$$

In particular, for $R=k[[x_1,\dots,x_n]]/(x_1^{d_1}+\dots+x_n^{d_n})$, the ideal $I=(x_1^{a_1},\dots,x_n^{a_n})$ and $\beta=(a_1/d_1,\dots,a_n/d_n)$,
$$\operatorname{HK}_e(R,I)=\ell\big(R/I^{[p^e]}\big)=d_1\cdots d_n\,D_k(p^e\beta).$$

```sage
# Groebner basis dimension vs d_1...d_n D_k(a/d)
for p in [2, 3, 5]:
    for a, d in [((3,4), (2,3)), ((5,4,3), (3,2,4)), ((7,5,6), (3,3,2))]:
        S = PolynomialRing(GF(p), len(a), 'x'); X = S.gens()
        dim = S.ideal([X[i]^a[i] for i in range(len(a))] + [sum(X[i]^d[i] for i in range(len(a)))]).vector_space_dimension()
        print(p, a, d, dim, prod(d) * D_k(p, [a[i]/d[i] for i in range(len(a))]))
```

## Two functional equations

A corollary of Monsky and Teixeira's results from the previous post is a functional equation for $\ell_k$:

**Theorem** ($\ell_k$ is $p$-multiplicative, [HM93, Theorem 4.5]). Let $q=p^e$, let $0\leq k_1,\dots,k_n<q$ and $r_1,\dots,r_n\geq0$. Then
$$\ell_k(qr+k)=\begin{cases}\ell_k(r)\,\ell_k(k_1,\dots,k_n)&\sum r_i\text{ even},\\ \ell_k(r)\,\ell_k(q-1-k_1,k_2,\dots,k_n)&\sum r_i\text{ odd}.\end{cases}$$

A random test:

```sage
import random
random.seed(int(1))
ok = True
for p in [2, 3, 5]:
    for e in [1, 2]:
        q = p^e
        for _ in range(100):
            n = random.randint(2, 4)
            r = [random.randint(0, 5) for _ in range(n)]; k = [random.randint(0, q-1) for _ in range(n)]
            kk = k if sum(r) % 2 == 0 else [q-1-k[0]] + k[1:]
            ok = ok and ell_k(p, [q*r[i] + k[i] for i in range(n)]) == ell_k(p, r) * ell_k(p, kk)
ok
```

To compute Hilbert–Kunz functions we need $D_k$, and the point is that there is also a (more involved) functional equation for it:

**Theorem** [HM93, Theorem 4.13]. Let $q=p^e$, $u\in[0,q)^n$ and $r\in\mathbb Z_{\geq1}^n$. Then
$$D_k(qr+u)=\begin{cases}\ell_k(r)\,D_k(u_1,\dots,u_n)+q^{n-1}\phi_r(u/q)&\sum r_i\text{ even},\\ \ell_k(r)\,D_k(q-u_1,u_2,\dots,u_n)+q^{n-1}\phi_r(u/q)&\sum r_i\text{ odd},\end{cases}$$
where $\phi_r\in\mathbb Z[x_1,\dots,x_n]$ is a polynomial depending on $r$ and $p$ (see Theorem 3.4 of the [notes](/notes/han-monsky/han_monsky.pdf); it is `phi_r` in the code).

```sage
random.seed(int(2))
ok = True
for p in [2, 3, 5]:
    for e in [0, 1, 2]:
        q = p^e
        for _ in range(20):
            n = random.randint(2, 4)
            r = [random.randint(1, 4) for _ in range(n)]
            u = [min(QQ(random.randint(0, 6*q))/6, q - 1/6) for _ in range(n)]
            uu = u if sum(r) % 2 == 0 else [q - u[0]] + u[1:]
            lhs = D_k(p, [q*r[i] + u[i] for i in range(n)])
            rhs = ell_k(p, r) * D_k(p, uu) + q^(n-1) * phi_r(p, r, [x/q for x in u])
            ok = ok and lhs == rhs
ok
```

## From the functional equation to the algorithm

Here is the setup. Let $\beta\in\mathbb Q_{\geq0}^n$, and $\mu\geq1$ (we will have to find it!). Define:

1. $r=\lfloor\beta\rfloor$ and $z=\beta-r\in[0,1)^n$;
2. $R=\lfloor p^\mu\beta\rfloor$ and $z'=p^\mu\beta-R\in[0,1)^n$;
3. $t=R-p^\mu r\in\mathbb Z^n$.

By the $p$-multiplicativity of $\ell_k$, $\ell_k(R)=\ell^\sharp\,\ell_k(r)$, where $\ell^\sharp=\ell_k(t)$ if $\sum r_i$ is even, and $\ell^\sharp=\ell_k(p^\mu-1-t_1,t_2,\dots,t_n)$ if $\sum r_i$ is odd.

**Theorem** [HM93, Theorem 5.2]. If $z'=z$ and $\sum R_i\equiv\sum r_i\pmod2$, then
$$\frac{1}{p^{e(n-1)}}\Big(D_k(p^{e+\mu}\beta)-\ell^\sharp D_k(p^e\beta)\Big)$$
does not depend on $e\geq0$.

*Proof.* This proof is the key to why the algorithm works. Let $q=p^e$, and assume first that $\sum R_i\equiv\sum r_i\equiv0\pmod 2$. By the functional equation, and using that $z'=z$,
$$\begin{aligned}D_k(p^{e+\mu}\beta)-\ell^\sharp D_k(p^e\beta)&=D_k\big(q(R+z)\big)-\ell^\sharp D_k\big(q(r+z)\big)\\&=\ell_k(R)D_k(qz)+q^{n-1}\phi_R(z)-\ell^\sharp\big(\ell_k(r)D_k(qz)+q^{n-1}\phi_r(z)\big)\\&=q^{n-1}\big(\phi_R(z)-\ell^\sharp\phi_r(z)\big).\end{aligned}$$
The term $\phi_R(z)-\ell^\sharp\phi_r(z)$ does not depend on $e$: $R$, $r$, $z$ and $t$ only depend on $p$, $\beta$ and $\mu$. The odd case is the same, keeping track of the different definitions of $\phi_r$ and $\ell^\sharp$. $\square$

There need not be such a $\mu$ for every $\beta$, but there is one after replacing $\beta$ by $p^{e_0}\beta$ for $e_0$ large enough. We will take this into account.

**Corollary.** Let $d_1,\dots,d_n\geq2$, $R=\mathbb F_p[[x_1,\dots,x_n]]/(x_1^{d_1}+\dots+x_n^{d_n})$, $I=(x_1^{a_1},\dots,x_n^{a_n})$ and $\beta=(a_1/d_1,\dots,a_n/d_n)$. Assume that there are integers $e_0\geq0$ and $\mu\geq1$ for which $p^{e_0}\beta$ satisfies the hypotheses of the theorem. Then, for every $e\geq e_0$,
$$\operatorname{HK}_e(R,I)=C\,p^{(n-1)e}+\Delta_e,\qquad\text{with }\Delta_{e+\mu}=\ell^\sharp\,\Delta_e.$$

*Proof.* Recall that $\operatorname{HK}_e(R,I)=d\,D_k(p^e\beta)$ with $d=d_1\cdots d_n$. The theorem says that there is a constant $A$ such that, for every $e\geq e_0$,
$$\operatorname{HK}_{e+\mu}(R,I)-\ell^\sharp\operatorname{HK}_e(R,I)=A\,p^{e(n-1)}.$$
By Monsky, $\operatorname{HK}_e(R,I)=C\,p^{e(n-1)}+\Delta_e$ with $\Delta_e=O(p^{e(n-2)})$. Plugging this in and dividing by $p^{e(n-1)}$,
$$\frac{\Delta_{e+\mu}-\ell^\sharp\Delta_e}{p^{e(n-1)}}=A+\ell^\sharp C-C\,p^{\mu(n-1)}.$$
The left side tends to $0$ as $e\to\infty$, and the right side does not depend on $e$, so both are $0$. $\square$

We can watch the constant appear. It equals $C\big(p^{\mu(n-1)}-\ell^\sharp\big)$:

```sage
for p, exps in [(5,[4,4,4,4]), (3,[6,6,6,5]), (7,[3,3,3,3])]:
    D = eHK_diagonal(p, exps, _data=True)
    mu, e0, lsh, n = D['mu'], D['e0'], D['lsh'], len(exps)
    HK = [_hk_value(p, exps, None, e) for e in range(e0 + mu + 3)]
    print(p, exps, " mu =", mu, " e0 =", e0, " l# =", lsh, " A =",
          [(HK[e+mu] - lsh*HK[e]) / p^(e*(n-1)) for e in range(e0, e0 + 3)],
          " C(p^(mu(n-1)) - l#) =", D['eHK'] * (p^(mu*(n-1)) - lsh))
```

## Finding $e_0$ and $\mu$

This is the number-theoretic input of [HM93, §5]. Let $\tilde\beta=(a_1/d_1,\dots,a_n/d_n)$.

1. **Strip $p$ from the denominators.** Let $e_0$ be the largest exponent with $p^{e_0}\mid d_i$ for some $i$, and $\beta=p^{e_0}\tilde\beta$, so that no denominator of $\beta$ is divisible by $p$.
2. **Find $\mu$.** If $\mu$ is a multiple of the multiplicative orders of $p$ modulo the denominators of $\beta$, then $z'=z$, and $R=r+(p^\mu-1)\beta$. For odd $p$, doubling $\mu$ makes the parity condition hold as well; for $p=2$, the parity of $\sum R_i-\sum r_i$ can be read off directly.

The code searches for the smallest $\mu$ that works. Following [HM93, §5], it accepts a slightly larger set of $\mu$'s: $z'$ may also be obtained from $z$ by changes of sign mod 1 in an even number of coordinates (with the same parity condition), or in an odd number of coordinates (with the opposite parity).

```sage
find_period(3, [6,6,6,5], verbose=True)
```

## Assembling the Hilbert–Kunz function

With $\mu$ and $e_0$ in hand, we only need:

- $\ell^\sharp$, which is $\alpha(\lambda_{t_1}\cdots\lambda_{t_n})$ (after the reflection $t_1\mapsto p^\mu-1-t_1$ if $\sum r_i$ is odd), the $(0,0)$ entry of a product of matrices of $\Lambda_\mu$;
- two values, $\operatorname{HK}_{e_0}(R,I)$ and $\operatorname{HK}_{e_0+\mu}(R,I)$. The code computes them by brute force, as dimensions of quotients over $\mathbb F_p$.

By the corollary, writing $\Delta_{e_0}=-y$, they satisfy the $2\times2$ linear system
$$\operatorname{HK}_{e_0}(R,I)=C\,p^{(n-1)e_0}-y,\qquad\operatorname{HK}_{e_0+\mu}(R,I)=C\,p^{(n-1)(e_0+\mu)}-y\,\ell^\sharp,$$
whose solution gives the Hilbert–Kunz multiplicity $C=e_\text{HK}(R,I)$ and the correction term. The other residue classes of $e$ mod $\mu$ are filled in with $\operatorname{HK}_{e_0+1},\dots,\operatorname{HK}_{e_0+\mu-1}$. Here are the intermediate quantities for Han and Monsky's example $x^4+y^4+z^4+t^4$ over $\mathbb F_5$:

```sage
eHK_diagonal(5, [4,4,4,4], verbose=True)
```

And the final result, for any diagonal hypersurface you like. `ideal=[a_1, ..., a_n]` replaces $\mathfrak m$ by $(x_1^{a_1},\dots,x_n^{a_n})$:

```sage
S.<x,y,z,t> = GF(3)[]
H = HK_function_diagonal(x^6 + y^6 + z^6 + t^5)
print(H)
print(H(3), HK_groebner(x^6 + y^6 + z^6 + t^5, 3))
```

Finally, the bound on $\ell=\ell^\sharp$ from Han and Monsky's theorem in the [first post](han-monsky-1-shape-of-hilbert-kunz-functions.html), in a few cases:

```sage
for p, exps in [(2,[5,5]), (7,[3,3,3]), (5,[4,4,4,4]), (7,[3,3,3,3]), (3,[6,6,6,5]), (2,[3,3,3,3]), (5,[4,4,4,4,4])]:
    D = eHK_diagonal(p, exps, _data=True)
    n, mu, lsh = len(exps), D['mu'], D['lsh']
    bound = p^((n-3)*mu) if n >= 3 else 1
    print("p = %d, exps = %s:  mu = %d, e0 = %d, l# = %d,  bound p^((n-3)mu) = %d" % (p, exps, mu, D['e0'], lsh, bound))
```

In the [next post](han-monsky-4-f-signature.html), the same algorithm computes F-signature functions.

## References

- [HM93] C. Han, P. Monsky, *Some surprising Hilbert–Kunz functions*, Math. Z. 214 (1993), 119–135, [doi](https://doi.org/10.1007/BF02572395).
- [MT06] P. Monsky, P. Teixeira, *p-Fractals and power series II*, J. Algebra 304 (2006), 237–255, [doi](https://doi.org/10.1016/j.jalgebra.2005.07.033).
