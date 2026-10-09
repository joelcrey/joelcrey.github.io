---
title: On the shape of Hilbert–Kunz functions and diagonal hypersurfaces
category: math
series: han-monsky
series_part: 1
sagecell: true
sage_preload: /notes/han-monsky/hilbert_kunz.py
summary: The Hilbert–Kunz function is not eventually polynomial, not even quasi-polynomial. A tour of examples, and Han and Monsky's theorem on diagonal hypersurfaces.
---

In these notes, I explain the algorithm to compute the Hilbert–Kunz function and the F-signature function of any given diagonal hypersurface, i.e., of the form $x_1^{d_1}+\dots+x_n^{d_n}$, in any characteristic.

**Computations.** Some examples are followed by a short SageMath session, which you can run on this page. Click **Load hilbert_kunz.py** first, then **Run** on any cell. The cells share one Sage session.

## On the shape of Hilbert–Kunz functions

The Hilbert–Kunz function of a local ring is always of the following form [Mon83]: there is some $c\in\mathbb R_{\geq1}$ such that
$$\operatorname{HK}_e(R)=cp^{de}+\Delta_e,\quad\text{where }\Delta_e=O(p^{e(d-1)}).$$
It would be great if $\operatorname{HK}_e(R)$ is eventually polynomial as its sister the Hilbert–Samuel function. However, already in the case of dimension 1, Monsky showed in that same article that $\Delta_e$ can be a periodic function:

**Example 1.1.** Let $R=\mathbb F_2[[x,y]]/(x^5+y^5)$, then for all $e\geq0$,
$$\operatorname{HK}_e(R)=\begin{cases}5\cdot2^e-4 & e\text{ even},\\ 5\cdot2^e-6 & e\text{ odd}.\end{cases}$$

```sage
S.<x,y> = GF(2)[]
HK_function_diagonal(x^5 + y^5)
```

The next obvious guess is that they might be "quasi-polynomials" on the variable $p^e$, i.e., polynomials $c_n(e)p^{en}+\dots+c_1(e)p^e+c_0(e)$ whose coefficients $c_i(e)$ are periodic functions. This is also wrong, as we will see next, but here are several examples that might induce one to think that this is the case:

**Examples 1.2.**

(1) Kunz provided the example [Kun76, Example 4.3], which is $R=\mathbb F_p[[t,x_1,\dots,x_n]]/(t^n-x_1^{d_1}\cdots x_n^{d_n})$ for $p\nmid n\geq2$. Then, the Hilbert–Kunz function is a quasi-polynomial. For instance, if $p=5$, then for the hypersurface $t^3-x^2y^2z^2$ we obtain
$$\operatorname{HK}_e(R)=\frac{26}{9}\cdot5^{3e}-\frac83\cdot5^e+(-1)^e\frac{16}{9}\qquad e\geq1.$$
One can compute this directly from Monsky's example, or with the algorithm in [CH98].

(2) This observation was told to me by Ilya Smirnov. Given a ring $(R,\mathfrak m)$,
$$\operatorname{HK}_e(R[[t]])=p^e\operatorname{HK}_e(R).$$
This way, if you get a ring with quasi-polynomial Hilbert–Kunz function (like the two examples we have described so far), one can produce some trivial examples of higher-dimensional quasi-polynomial Hilbert–Kunz functions.

(3) Affine semigroup rings also give quasi-periodic Hilbert–Kunz functions.

In 1993, Han and Monsky [HM93] provided a setup and an algorithm to compute the Hilbert–Kunz function of the diagonal hypersurfaces, yielding interesting examples like the following:

**Example 1.3.** For all $e\geq0$,
$$\operatorname{HK}_e\left(\frac{\mathbb F_5[x,y,z,t]}{(x^4+y^4+z^4+t^4)}\right)=\frac{168}{61}5^{3e}-\frac{107}{61}3^e.$$

This example might suggest that Hilbert–Kunz functions are quasi-polynomial in several variables instead, like is the case above for the variables $5^e$ and $3^e$. Again, this is in general not the case, as some nasty examples below will showcase.

*Remark 1.4.* One could argue that this is the case for all diagonal hypersurfaces, looking at the theorem above: define $e\mapsto k(e)$ where $0\leq k(e)<\mu$ such that $e\equiv k(e)\pmod\mu$; we then have that
$$\ell^{\lfloor e/\mu\rfloor}=\ell^{\frac{e-k}{\mu}}=\ell^{-k(e)/\mu}\ell^{\frac e\mu},$$
which makes $\ell^{\lfloor e/\mu\rfloor}$ into a quasi-polynomial on the variable $\ell^{\frac1\mu}$. It is up to the reader to judge whether we want to allow irrational variables and hence be happy throwing diagonal hypersurfaces into the quasi-polynomial-in-several-variables drawer.

As already hinted above, Hilbert–Kunz functions might not even look like periodic-function combinations of powers. A few years after Han and Monsky's results, Chiang and Hung, building on these techniques, produced an algorithm to compute the Hilbert–Kunz function of any hypersurface of the form $\sum_{i=0}^m\prod_j^{n_j}x_{i,j}^{d_{i,j}}$.

**Example 1.5** (Example [CH98]). For every $e\geq0$,
$$\begin{aligned}\operatorname{HK}_e\left(\frac{\mathbb F_7[[x,y,z,s,t,u,v]]}{((xyzs)^6+t^6+u^6+v^6)}\right)&=\frac{2050747718345259}{429658164277013}\cdot7^{6e}-\frac{267597}{74480}\cdot7^{3e}\\&\quad+\left(\frac{164565}{2801}e-\frac{312186671451}{878707312}\right)7^e+\frac{104440051}{294115}\cdot3^e.\end{aligned}$$
Since $(y,z,s,t,u,v)$ is a parameter ideal and minimal reduction of the maximal, and $x^5$ is a socle element, we can use

```sage
S.<x,y,z,s,t,u,v> = GF(7)[]
HK_function_disjoint_monomials((x*y*z*s)^6 + t^6 + u^6 + v^6)
```

All these examples have in common that their Hilbert–Kunz series
$$\operatorname{HKS}(z):=\sum\operatorname{HK}_e(R)z^e,$$
are rational functions. The fact that a singularity has rational Hilbert–Kunz series implies having rational Hilbert–Kunz multiplicity, as one may deduce from the theory of generating functions. We have known for some years now, however, that irrational Hilbert–Kunz multiplicities exists [Bre13], and we have explicit conjectural examples of this fact that showcase the mysterious forms the Hilbert–Kunz function can attain:

**Example 1.6.** Let $H=x^3+y^3+xyz+uv\in\mathbb F_2[[x,y,z,u,v]]$, which is conjectured to have irrational Hilbert–Kunz multiplicity [Mon08]. In the observation after Corollary 2.7 in *op. cit.*, it is shown that
$$\operatorname{HKS}(z)=\frac{1}{(1-4z)(1-16z)}+\frac{2z(1-6z)(1+2z)^{1/2}}{(1-2z)^{3/2}(1-4z)(1-16z)}.$$
One may transform this into a closed form for the Hilbert–Kunz function, and in this case, Claude Opus suggests the following. Let
$$\begin{aligned}f_e(x)&:=\sum_{k=0}^{e-1}\binom{k}{\lfloor k/2\rfloor}x^k,\\ f(x)&:=\lim_{e\to\infty}f_e(x)=\frac{1}{2x}\left(\sqrt{\frac{1+2x}{1-2x}}-1\right),\quad|x|<\frac12.\end{aligned}$$
Then,
$$\operatorname{HK}_e(R)=c_0(e)\,2^{4e}+c_1(e)\,2^{2e}+c_2(e)\,2^e,$$
where
$$\begin{aligned}c_0(e)&=\frac{61}{42}+\frac1{16}\cdot\frac5{21}f_e\big(\tfrac1{16}\big)\xrightarrow[e\to\infty]{}\frac43+\frac{5}{14\sqrt7},\\ c_1(e)&=-\frac16+\frac1{12}f_e\big(\tfrac14\big)\xrightarrow[e\to\infty]{}\frac{\sqrt3-2}{6},\\ c_2(e)&=-\frac27\big(1+f_e\big(\tfrac12\big)\big)=-\frac17\big(4e+3-(-1)^e\big)\binom{e}{\lfloor e/2\rfloor}\frac1{2^e}\sim-\frac47\sqrt{\frac{2e}{\pi}}\xrightarrow[e\to\infty]{}-\infty,\end{aligned}$$

### The diagonal hypersurfaces

As we mentioned above, Han and Monsky showed the following result:

**Theorem 1.7** ([HM93]). *Let $p$ be a prime number and $(d_1,\dots,d_n)\in\mathbb Z_{\geq2}$. Then,*
$$\operatorname{HK}_e\left(\frac{\mathbb F_p[[x_1,\dots,x_n]]}{(x_1^{d_1}+\dots+x_n^{d_n})}\right)=cp^{(n-1)e}+c_1(e)\ell^{\lfloor e/\mu\rfloor},\quad\text{for all }e\geq e_0.$$
*where $e_0,\ell,\mu$ are non-negative integers (often $\ell\neq p$), $e\mapsto c_e$ is a periodic function of period $\mu$, and $c\geq1$ a rational number. Also, when $n\geq3$, then $p^{(n-3)\mu}\geq\ell\geq0$, and if $p=2$ or $n=2,3$, then $\ell\in\{0,1\}$.*

The goal of these notes is explaining the tools that go into the proof of this fact, using it to effectively compute the Hilbert–Kunz function of a diagonal hypersurface, and give an idea of the general argument. The interest here relies on the fact that, even decades later, the machinery behind this example keeps providing insights of the Hilbert–Kunz function of hypersurfaces [CH98, MT04, MT06, Cas25, Men26b, PSSY26].

### Key point: proving a functional equation

For the rest of the notes, set $k$ be a field of characteristic $p$. The computation of the Hilbert–Kunz function of these hypersurfaces is about trying to understand the following function:
$$\left(\frac{a_1}{d_1},\dots,\frac{a_n}{d_n}\right)\overset{D_k}{\longmapsto}\frac{1}{d_1\cdots d_n}\dim_k\left(\frac{k[x_1,\dots,x_n]}{(x_1^{a_1},\dots,x_n^{a_n},x_1^{d_1}+\dots+x_n^{d_n})}\right).\tag{1}$$
For this, Han would define a particular function $\ell:\mathbb Z_{\geq0}\to\mathbb Z$, and then one of the main theorem of her thesis is the following:

**Theorem 1.8** (Han–Monsky, [Han92]). *Let $q=p^e$ for some $e\geq0$, $r=(r_1,\dots,r_n)\in\mathbb Z^n_{\geq1}$, $z=(z_1,\dots,z_n)\in[0,1]^n$ and $z^*=(1-z_1,\dots,z_n)$. Then,*
$$D(p^e(r+z))=\begin{cases}\ell(r)D(qz)+q^{n-1}\phi_r(z)&\sum r_i\text{ even},\\ \ell(r)D(qz^*)+q^{n-1}\phi_r(z)&\sum r_i\text{ odd}.\end{cases}$$
*where $\phi_r$ is a certain polynomial that depends on $r$ and $p$.*

In her thesis, Han showed that this functional equation held provided that the $\ell$ function had a particular property, called being "$p$-multiplicative", and she proved it for $p>2$ and $n=2,3$ or $p=2$ and $n\geq1$. However, Monsky later developed the theory of the representation ring, which reinterpreted $D_k$ and $\ell_k$, and showed that $\ell$ is indeed $p$-multiplicative, which implies the functional equation in full generality. We nowadays have a better language for all this, and it equates to understanding the multiplication table of the representation ring, which we will talk about in the [next post](han-monsky-2-the-han-monsky-ring.html).

## References

- [Bre13] H. Brenner. *Irrational Hilbert–Kunz multiplicities*, 2013. [arXiv:1305.5873](https://arxiv.org/abs/1305.5873).
- [Cas25] J. Castillo-Rey. *Strong Watanabe–Yoshida conjecture for Complete Intersections*, 2025. [arXiv:2506.09019](https://arxiv.org/abs/2506.09019).
- [CH98] L. Chiang and Y.-C. Hung. *On Hilbert–Kunz functions of some hypersurfaces*. Journal of Algebra, 199(2):499–527, 1998. [doi:10.1006/jabr.1997.7206](https://doi.org/10.1006/jabr.1997.7206).
- [Han92] C. Han. *The Hilbert–Kunz Function of a Diagonal Hypersurface*. Brandeis University, 1992.
- [HM93] C. Han and P. Monsky. *Some surprising Hilbert–Kunz functions*. Mathematische Zeitschrift, 214(1):119–135, 1993. [doi:10.1007/BF02572395](https://doi.org/10.1007/BF02572395).
- [Kun76] E. Kunz. *On Noetherian Rings of Characteristic p*. American Journal of Mathematics, 98(4):999–1013, 1976. [doi:10.2307/2374038](https://doi.org/10.2307/2374038).
- [Men26b] C. Meng. *Limits of F-invariants and Riemann–Stieltjes integral*, 2026. [arXiv:2507.13898](https://arxiv.org/abs/2507.13898).
- [Mon83] P. Monsky. *The Hilbert–Kunz Function*. Mathematische Annalen, 263:43–50, 1983. [doi:10.1007/BF01457082](https://doi.org/10.1007/BF01457082).
- [Mon08] P. Monsky. *Rationality of Hilbert–Kunz multiplicities: A likely counterexample*. Michigan Mathematical Journal, 57:605–613, 2008. [doi:10.1307/mmj/1220879427](https://doi.org/10.1307/mmj/1220879427).
- [MT04] P. Monsky and P. Teixeira. *P-Fractals and power series–I. Some 2 variable results*. Journal of Algebra, 280(2):505–536, 2004. [doi:10.1016/j.jalgebra.2004.05.016](https://doi.org/10.1016/j.jalgebra.2004.05.016).
- [MT06] P. Monsky and P. Teixeira. *P-Fractals and power series–II. Some applications to Hilbert–Kunz theory*. Journal of Algebra, 304(1):237–255, 2006. [doi:10.1016/j.jalgebra.2005.07.033](https://doi.org/10.1016/j.jalgebra.2005.07.033).
- [PSSY26] I. Pak, B. Shapiro, I. Smirnov, and K.-i. Yoshida. *Hilbert–Kunz multiplicity of quadrics via Ehrhart theory*, 2026. [arXiv:2508.17915](https://arxiv.org/abs/2508.17915).
