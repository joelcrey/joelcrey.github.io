---
title: The Han–Monsky ring
category: math
series: han-monsky
series_part: 2
sagecell: true
summary: Computing dimensions of quotients of diagonal hypersurfaces becomes a question about multiplying k[T]-modules. The Grothendieck ring of those modules, and its multiplication table.
---

In the [previous post](han-monsky-1-shape-of-hilbert-kunz-functions.html) we saw that computing Hilbert–Kunz functions of diagonal hypersurfaces comes down to understanding
$$D_k\left(\frac{a_1}{d_1},\dots,\frac{a_n}{d_n}\right)=\frac{1}{d_1\cdots d_n}\dim_k\frac{k[x_1,\dots,x_n]}{(x_1^{a_1},\dots,x_n^{a_n},x_1^{d_1}+\dots+x_n^{d_n})},$$
where $k$ is a field of characteristic $p>0$. This post introduces the ring in which this function lives. As before, run the first cell before the others.

```sage
load("https://joelcrey.github.io/notes/han-monsky/hilbert_kunz.py")
```

## Motivation

Let us first get a feeling for $D_k$ when all the $d_i$ are $1$.

**Two variables.** For positive integers $a\leq b$,
$$\frac{k[x,y]}{(x^a,y^b,x+y)}\cong\frac{k[x]}{(x^a)},$$
which has dimension $a$. Easy.

**Three variables.** Now
$$\frac{k[x,y,z]}{(x^a,y^b,z^c,x+y+z)}\cong\frac{k[x,y]}{(x^a,y^b,(x+y)^c)}.$$
If $a,b,c$ do not satisfy the triangle inequality, say $a+b<c$, then $(x^a,y^b,(x+y)^c)=(x^a,y^b)$. If they do, it is more complicated to give a general formula.

**From a dimension to a $k[T]$-module.** Another point of view is to study the vector space $M=k[x_1,\dots,x_n]/(x_1^{a_1},\dots,x_n^{a_n})$ as a $k[T]$-module, where $T$ acts as multiplication by $x_1^{d_1}+\dots+x_n^{d_n}$. By the structure theorem for modules over a PID,
$$M\cong\bigoplus_i\left(\frac{k[T]}{(T^i)}\right)^{\oplus a_i}.$$
In other words, take the matrix of $T$ on the monomial basis, compute its Jordan form, and count the Jordan blocks of each size: these are the $a_i$. The dimension we want is $\dim_k M/TM=\sum_i a_i$, the total number of Jordan blocks.

**Tensor products.** Given two $k[T]$-modules $M,N$, define a $k[T]$-module structure on $M\otimes_kN$ by $T(m\otimes n)=Tm\otimes n+m\otimes Tn$. With this (certainly arbitrary-looking) product, $M$ splits into simpler pieces:

**Example.** To compute $D_k(3/2,4/3)$, write
$$\frac{k[x,y]}{(x^3,y^4)}=\frac{k[x]}{(x^3)}\otimes_k\frac{k[y]}{(y^4)},$$
with $T$ acting as $x^2$ and $y^3$ on the factors. This is an isomorphism of $k[T]$-modules. On $k[x]/(x^3)$, $T=x^2$ sends $1\mapsto x^2\mapsto0$ and kills $x$, so it has Jordan blocks of sizes $2$ and $1$. Similarly $k[y]/(y^4)$ with $T=y^3$ has blocks of sizes $2,1,1$. Hence
$$M\cong\left(\frac{k[T]}{(T^2)}\oplus\frac{k[T]}{(T)}\right)\otimes_k\left(\frac{k[T]}{(T^2)}\oplus\left(\frac{k[T]}{(T)}\right)^{\oplus2}\right).$$

So the problem becomes decomposing products of these simpler modules. With the right notation, we can get much further.

## The ring

**Definition** [HM93, §2].
- A **$k$-object** is a $k[T]$-module on which $T$ acts nilpotently, equivalently a $k[T]$-module that is finite-dimensional over $k$.
- The **product** of two $k$-objects is $M\otimes_kN$ with $T(m\otimes n)=Tm\otimes n+m\otimes Tn$.
- The **Han–Monsky ring** $\Gamma_k$ is the Grothendieck ring of $k$-objects: addition is $\oplus$, multiplication is the product above, and the unit is $k[T]/(T)=k$.
- **The $\delta$-basis and the $\lambda$-basis.** $\delta_i=[k[T]/(T^i)]$ for $i\geq1$, with $\delta_0=0$, and $\lambda_i=(-1)^i(\delta_{i+1}-\delta_i)$. Note that $\lambda_0=\delta_1$ is the unit.
- **Dimension and $\alpha$.** $\dim_k$ and $\alpha(M)=\dim_k M/TM$ (the number of Jordan blocks) are additive, so they extend to $\Gamma_k$. Note that $\alpha(\delta_i)=1$, $\alpha(\lambda_0)=1$ and $\alpha(\lambda_i)=0$ for $i\geq1$.

In the code, `HanMonskyRing(p)` creates $\Gamma_k$ for $k$ of characteristic $p$, with bases `delta(i)` and `lam(i)`, and invariants `.dim()` and `.alpha()`:

```sage
R = HanMonskyRing(5)
d, l = R.delta, R.lam
print(d(3) * d(4))
print(d(2) * d(6), d(5) * d(5), (d(2) + d(3))^2)
```

**Back to the example.** We need $(\delta_2+\delta_1)(\delta_2+2\delta_1)=\delta_2^2+3\delta_2+2\delta_1$, since $\delta_1$ is the unit. So we only need $\delta_2^2$, the class of $k[T,S]/(T^2,S^2)$ with $T$ acting as $T+S$.

If $p=2$, then $(T+S)^2=T^2+S^2=0$, so there are no blocks of size larger than $2$, and $\delta_2^2=a_1\delta_1+a_2\delta_2$. Since $\dim_k\delta_2^2=4$ and $\alpha(\delta_2^2)=\dim_k k[T,S]/(T^2,S^2,T+S)=2$, we get $\delta_2^2=2\delta_2$. In odd characteristic, $(T+S)^2=2TS\neq0$, and $\delta_2^2=\delta_1+\delta_3$.

```sage
HanMonskyRing(2).delta(2)^2, HanMonskyRing(3).delta(2)^2
```

An alternative, noted to me by Kevin Tucker, is to write the matrix $N$ of $T+S$ on the monomial basis $1,S,T,ST$ and read the Jordan type off the ranks of its powers: the number of blocks of size $s$ is $\operatorname{rk}N^{s-1}-2\operatorname{rk}N^{s}+\operatorname{rk}N^{s+1}$. That is what `psi(N, p)` does:

```sage
N = matrix(ZZ, [[0,0,0,0],[1,0,0,0],[1,0,0,0],[0,1,1,0]])
psi(N, 2), psi(N, 3)
```

Putting it together, $\dim_k k[x,y]/(x^3,y^4,x^2+y^3)$, $\alpha\big((\delta_2+\delta_1)(\delta_2+2\delta_1)\big)$ and $2\cdot3\cdot D_k(3/2,4/3)$ agree, in every characteristic:

```sage
for p in [2, 3, 5, 7]:
    R = HanMonskyRing(p); d = R.delta
    M = (d(2) + d(1)) * (d(2) + 2*d(1))
    S.<x,y> = GF(p)[]
    groebner = S.ideal([x^3, y^4, x^2 + y^3]).vector_space_dimension()
    print("p =", p, "  M =", M, "  alpha(M) =", M.alpha(), "  6*D_k(3/2,4/3) =", 6*D_k(p, [3/2, 4/3]),
          "  Groebner:", groebner)
```

## The multiplication table

So the question is:

**Question.** Given $i,j$, compute $\delta_i\delta_j$ or $\lambda_i\lambda_j$. In other words, what is the multiplication table of $\Gamma_k$?

The $\lambda$-basis has an easier multiplication table, for several reasons. The first one:

**Lemma** [HM93, Theorem 3.2]. The $\mathbb Z$-span $\Lambda_e$ of $\lambda_0,\dots,\lambda_{p^e-1}$ is closed under products.

So multiplication by an element of $\Lambda_e$ is given by a $p^e\times p^e$ integer matrix in the $\lambda$-basis [Yos09]: column $j$ is the product with $\lambda_j$. For $\Lambda_1$, Han and Monsky give the whole table:

**Lemma** [HM93]. For $0\leq i\leq j\leq p-1$,
$$\lambda_i\lambda_j=\sum_{k=j-i}^{\min(i+j,\,2p-2-i-j)}\lambda_k.$$

Let us check it against the code for all $p\leq13$:

```sage
def lemma(i, j, p):
    R = HanMonskyRing(p)
    i, j = min(i, j), max(i, j)
    return sum((R.lam(k) for k in range(j - i, min(i + j, 2*p - 2 - i - j) + 1)), 0*R.lam(0))

all(HanMonskyRing(p).lam(i) * HanMonskyRing(p).lam(j) == lemma(i, j, p)
    for p in primes(2, 14) for i in range(p) for j in range(p))
```

Here are the matrices of $\Lambda_1$ for $p=5$. $\lambda_0$ and $\lambda_4$ are the diagonal and the antidiagonal, $\lambda_2$ is a filled diamond, and $\lambda_1,\lambda_3$ are slanted diamonds, mirror images of each other. Change `p` to see other characteristics:

```sage
p = 5
Ms = [lambda_matrix(p, 1, k) for k in range(p)]
for k in range(p):
    print("lambda_%d =" % k); print(Ms[k]); print()
print("symmetric:", all(M.is_symmetric() for M in Ms), "  commuting:", all(A*B == B*A for A in Ms for B in Ms))
```

All these matrices are symmetric and commute, so they are simultaneously diagonalisable by an orthogonal matrix. This point of view is exploited in [CR26, Men26a] to understand the Hilbert–Kunz multiplicities of quadrics. The first of these focuses on the matrix representation, following the approach of [PSSY26].

**Lemma.** Let $i=i_0+i_1p+\dots+i_{e-1}p^{e-1}$ be the $p$-adic expansion of $i$. Then $\lambda_i=\lambda_{i_0}\lambda_{i_1p}\cdots\lambda_{i_{e-1}p^{e-1}}$.

So to compute $\lambda_i\lambda_j$, we only need to understand the products $\lambda_{aq}\lambda_{bq}$ for $q=p^e$.

## Characteristic 2: the nim-sum

In characteristic 2 one has $\lambda_q^2=\lambda_0$ for every power $q=2^e$. Together with the lemma above, this describes the whole multiplication table: write $a$ and $b$ in base 2; then $\lambda_a\lambda_b=\lambda_{a\oplus b}$, where $\oplus$ is the **nim-sum**, the digit-wise sum mod 2. For instance,
$$\lambda_3\lambda_5=(\lambda_1\lambda_2)(\lambda_1\lambda_4)=\lambda_1^2\lambda_2\lambda_4=\lambda_6.$$
In Sage, `^^` is the digit-wise XOR:

```sage
R2 = HanMonskyRing(2)
R2.lam(3) * R2.lam(5), all(R2.lam(a) * R2.lam(b) == R2.lam(a ^^ b) for a in range(32) for b in range(32))
```

For odd $p$ the squares are not as simple: $\lambda_q^2=\lambda_0+\lambda_{2q-1}+\lambda_{2q}$, while $\lambda_{q-1}^2=\lambda_0$ in every characteristic.

```sage
for p in [2, 3, 5]:
    R = HanMonskyRing(p)
    for e in [1, 2]:
        q = p^e
        print("p = %d, q = %d:   lambda_q^2 = %s,   lambda_(q-1)^2 = %s" % (p, q, R.lam(q)^2, R.lam(q-1)^2))
```

In terms of matrices, characteristic 2 is easy to see. Write $[\lambda_i]_e$ for the matrix of multiplication by $\lambda_i$ on $\Lambda_e$, $\otimes$ for the Kronecker product, and $J=\begin{pmatrix}0&1\\1&0\end{pmatrix}$. Then in $\Lambda_2$:
$$[\lambda_1]_2=I_2\otimes J,\qquad[\lambda_2]_2=J\otimes I_2,\qquad[\lambda_3]_2=[\lambda_1]_2[\lambda_2]_2=J\otimes J.$$

```sage
J, I2 = matrix(ZZ, [[0,1],[1,0]]), identity_matrix(ZZ, 2)
(lambda_matrix(2, 2, 1) == I2.tensor_product(J), lambda_matrix(2, 2, 2) == J.tensor_product(I2),
 lambda_matrix(2, 2, 3) == J.tensor_product(J))
```

## Higher characteristic: reflections

The problem when scaling these observations to higher characteristic is that the Kronecker product description does not work exactly. In characteristic 3, the matrix of $\lambda_3$ in $\Lambda_2$ is not $[\lambda_1]_1\otimes[\lambda_0]_1$: one needs to adjust for some "reflections". Compare the middle blocks:

```sage
G = HanMonskyRing(3)
A = G.lam(3).matrix()                                     # [lambda_3]_2
B = G.lam(1).matrix().tensor_product(identity_matrix(3))  # [lambda_1]_1 (x) [lambda_0]_1
A.subdivide([3,6], [3,6])
print(A); print(); print(B); print(); print(A == B)
```

The main result is the following; we refer the reader to [MT06] for the details.

**Theorem** (Monsky–Teixeira [MT06], Meng [Men26a]). The map
$$\theta(\lambda_i)=\begin{cases}\lambda_{pi}& i\text{ even},\\ \lambda_{pi+p-1}& i\text{ odd},\end{cases}$$
extended $\mathbb Z$-linearly to $\Gamma_k$, is a ring homomorphism.

```sage
def theta_of(x, p):
    R = HanMonskyRing(p)
    return sum((c * R.lam(theta_index(i, p)) for i, c in x.lam().items()), 0*R.lam(0))

all(theta_of(HanMonskyRing(p).lam(a) * HanMonskyRing(p).lam(b), p)
    == HanMonskyRing(p).lam(theta_index(a, p)) * HanMonskyRing(p).lam(theta_index(b, p))
    for p in [2, 3, 5] for a in range(p^2) for b in range(p^2))
```

This means that once we understand the multiplication table of $\Lambda_1$, we understand the multiplication table of all of $\Gamma_k$:

**Proposition** (Monsky–Teixeira [MT06], Meng [Men26a]). For $i=\sum_{k=0}^{e-1}i_kp^k$ with $0\leq i_k\leq p-1$, put
$$a_k(i)=\begin{cases}i_k&\sum_{r>k}i_rp^r\text{ even},\\ p-1-i_k&\sum_{r>k}i_rp^r\text{ odd}.\end{cases}$$
Then the $\mathbb Z$-linear map $\Phi_e\colon\Lambda_e\to\Lambda_1^{\otimes e}$, $\lambda_i\mapsto\lambda_{a_0(i)}\otimes\dots\otimes\lambda_{a_{e-1}(i)}$, is a ring isomorphism.

In the [next post](han-monsky-3-the-algorithm.html), this structure gives a functional equation for $D_k$, and with it, the Han–Monsky algorithm.

## References

- [CR26] N. Cox-Steib, R. Redner, *The linear algebra of the Han–Monsky representation ring*, Electron. J. Linear Algebra 42 (2026), 329–348.
- [HM93] C. Han, P. Monsky, *Some surprising Hilbert–Kunz functions*, Math. Z. 214 (1993), 119–135, [doi](https://doi.org/10.1007/BF02572395).
- [Men26a] C. Meng, *Hilbert–Kunz multiplicity of quadrics decreases*, [arXiv:2606.04346](https://arxiv.org/abs/2606.04346).
- [MT06] P. Monsky, P. Teixeira, *p-Fractals and power series II*, J. Algebra 304 (2006), 237–255, [doi](https://doi.org/10.1016/j.jalgebra.2005.07.033).
- [PSSY26] I. Pak, B. Shapiro, I. Smirnov, K.-i. Yoshida, *Hilbert–Kunz multiplicity of quadrics via Ehrhart theory*, [arXiv:2508.17915](https://arxiv.org/abs/2508.17915).
- [Yos09] K.-i. Yoshida, *Small Hilbert–Kunz multiplicity and $(A_1)$-type singularity*, Proceedings of the 4th Japan–Vietnam Joint Seminar on Commutative Algebra, Meiji University, 2009.
