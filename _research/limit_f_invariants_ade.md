---
title: Limit F-invariants of the ADE singularities and the Fermat hypersurfaces
summary: Limits of the Hilbert–Kunz multiplicity and F-signature of the ADE singularities, generating functions and their combinatorics.
slug: limit-f-invariants
order: 1
published: true
collapsible: closed
---
>See the [preprint](https://arxiv.org/abs/2609.39133) on the results I mention below.

# Reduction mod $p$ and limit $F$-invariants
Say $f_1,\dots,f_r\in \mathbb{Z}[x_1,\dots,x_n]$, and set $R_0 := \mathbb{Q}[x_1,\dots,x_n]/(f_1,\dots,f_r)$ and $R_p := (\mathbb{F}_p[x_1,\dots,x_n]/(f_1,\dots,f_r))_{(x_1,\dots,x_n)}$. In general, it is expected that the properties of $R_0$ determine and are determined by those properties verified by $R_p$ **at almost all** $p$, usually meaning all but finitely many primes $p$. Regarding $R_0$ and $R_p$ as fibers of a map $\mathbb{Z}\rightarrow \mathbb{Z}[x_1,\dots,x_n]/(f_1,\dots,f_r)$, and by generic freeness one may pass to a small enough open set to deduce such behaviour from the properties of flat families, or flat morphisms.

However, down at those reductions mod $p$, one may want to go further and compute the Hilbert–Kunz multiplicity or the F-signature (or any numerical invariant). There are lots of questions about the resulting sequence of numbers. Namely:

**Question.** Do the sequences $e_\text{HK}(R_p)$ or $s(R_p)$ converge when $p\rightarrow \infty$? Provided the limits exist, can we interpret their values?

We know that this limit converges in a few particular cases. For instance, the case of the diagonal hypersurfaces, those of the form $x_1^{d_1}+\dots+x_n^{d_n}$, was proven by [Gessel and Monsky](https://arxiv.org/abs/1007.2004) in 2010.  It follows from work of [Meng](https://arxiv.org/abs/2507.13898) that the limits also exist for all the ADE (or simple) singularities, and computing these is one of the main result of the project we will discuss below. For an account of other known cases, see the intro of [Brenner–Li–Miller](https://www.sciencedirect.com/science/article/pii/S0021869312004954).

## The limit $F$-invariants of the $A_n$ singularities and combinatorics
Set $S_{n,p,d} := \mathbb{F}_p[[x_1,\dots,x_{d+1}]]/(x_0^2+\dots+x_{d-1}^2+x_{d}^{n+1})$, the ring of germs at the origin of an $A_n$ singularity. In the case of the $A_1$ singularity, Gessel and Monsky showed the following striking formula:

**Theorem** (Gessel–Monsky, 2010). Let $p>0$ and $d\geq 2$. Then, $\lim_{p\rightarrow \infty} e_\text{HK}(S_{1,p,d}) = 1+c_d,$ and $\lim s(S_{1,p,d}) = 1-c_d$ where $c_d$ is the $d$-th coefficient of the Taylor expansion of the function $\sec x + \tan x = (1+\sin x)\sec x$. In other words, $d!\cdot c_d$ is the sequence of the [zig-zag numbers](https://oeis.org/A000111).

It is a natural question now whether the rest of the $A_n$ singularities also have a combinatorial interpretation to the numerators of their limit Hilbert–Kunz multiplicities. In the case of the $A_n$ singularities, a generalisation is proven to exist:

**Theorem** (Limit F-invariants of the $A_n$ singularities, 2026). Let $p>0$, $d\geq 2$, and define $S_{n,p,d} := \mathbb{F}_p[[x_1,\dots,x_n]]/(x_0^2+\dots+x_{d-1}^2+x_d^n),$ the power series at the origin of an $A_{n-1}$-singularity. Then, $\lim_{p\rightarrow \infty} e_\text{HK}(S_{n,p,d}) = 1+c_d,$ and $\lim s(S_{n,p,d}) = 1-c_d$ where $c_d$ is the $d$-th coefficient of the Taylor expansion of the function $\frac{n+1}{2}(\cos\frac{(n-1)x}{n+1}+\sin\frac{2x}{n+1})\sec x$.

One can see that $d!\cdot c_d$ is exactly $N_d(2,r)$, the number of $n$-signed alternating permutations of length $d$ (for a definition, see Definition 3.10 and Proposition 3.11 in the [preprint](https://arxiv.org/abs/2609.39133)).

## The limit $F$-invariants of the ADE singularities
Gessel and Monsky's result for diagonal hypersurfaces also let us explore the values of the limit $F$-invariants for other diagonal ADE singularities, like $D_4$, $E_6$ and $E_8$. However, the non-diagonal ADE singularities, $D_n$ for $n\geq 5$, and $E_7$ in every dimension, are out of the reach of this technique.

There are several generalisation of the $F$-invariants in the literature, one of them is [Mukhophadhyay and Meng](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70696)'s $h$-function. Later, Meng developed the theory of the $h$-functions of hypersurfaces of the form $f+g$ where $f$ and $g$ have disjoint sets of variables, as well as the $h$-functions of binomials. These two ingredients and a bunch of computations yield the following result:

**Theorem** (Limit $F$-invariants of the simple singularities, 2026). Let $d\ge 2$. Let $g(x,y)\in\mathbb Z[x,y]$ be as in the table below, and $R_d=\mathbb C[x_0,\dots,x_d]/(g(x_0,x_1)+x_2^2+\cdots+x_d^2).$ Then,$$e_{\mathrm{HK},\infty}(R_d)=1+\frac{c_d}{d!},\qquad s_\infty(R_d)=1-\frac{c_d}{d!},$$where $c_d/d!$ is the $d$-th Taylor coefficient of the function $F_g(z)$ below, and $T(z)=\sec z+\tan z$.

|                | $g(x,y)$       | $F_g(z)$                                                                                                                                                                                  |
| -------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| $A_n$, $n\ge1$ | $x^{n+1}+y^2$  | $\dfrac{n+1}{2}\,\dfrac{\cos\frac{(n-1)z}{n+1}+\sin\frac{2z}{n+1}}{\cos z}$                                                                                                               |
| $D_n$, $n\ge4$ | $x^2y+y^{n-1}$ | $\dfrac{(n-1)^2}{4(n-2)}\cos\dfrac{z}{n-1}+\dfrac{(n-3)^2}{4(n-2)}\cos\dfrac{z}{n-3}+\Big(1+\dfrac{(n-1)^2}{4(n-2)}\sin\dfrac{z}{n-1}+\dfrac{(n-3)^2}{4(n-2)}\sin\dfrac{z}{n-3}\Big)T(z)$ |
| $E_6$          | $x^3+y^4$      | $3\,\dfrac{\cos\frac z2+\sin\frac z2}{\cos z}\,\cos\dfrac z3$                                                                                                                             |
| $E_7$          | $x^3+xy^3$     | $\dfrac{27}{16}\Big(\cos\dfrac z9-\sin\dfrac{2z}9\Big)+\dfrac{27}{16}\Big(\sin\dfrac z9+\cos\dfrac{2z}9\Big)T(z)$                                                                         |
| $E_8$          | $x^3+y^5$      | $\dfrac{15}{4}\,\dfrac{\cos\frac{3z}5+\sin\frac{2z}5}{\cos z}\,\cos\dfrac z3$                                                                                                             |

Note that $n=1$, the $A_1$ row gives $F_g(z)=\sec z+\tan z$, recovering the formula by Gessel and Monsky.

## The $h$-functions of the $A_n$ singularities and Euler polynomials
It is not difficult to conclude from the integral equation for $h$-function mentioned above that the limit $h$-functions of the ADE singularities are piecewise polynomials in $\mathbb{Q}[x]$, with only finitely many breakpoints. 

In the case of the $A_n$ singularities, a closed form for these polynomials in terms of the dimension, and the parameter $n$, can be provided using the right basis of $\mathbb{Q}[x]$: the Euler polynomials. The [Euler polynomials](https://mathworld.wolfram.com/EulerPolynomial.html) are a set of polynomials given by the series $\dfrac{2e^{xz}}{e^z+1}=\sum_{k\ge0}E_k(x)\dfrac{z^k}{k!}$ which are important to combinatorics and number theory, and form a $\mathbb{Q}$-basis in $\mathbb{Q}[x]$ (not to confuse with the [Eulerian polynomials](https://oeis.org/wiki/Eulerian_polynomials), are also important in these fields, and also show in the proof of Gessel and Monsky's formula in a different way).


**Theorem** (Limit $h$-functions of the $A_n$ singularities, 2026). Let $n\ge 2$, $d\ge1$, and $f=x_0^n+x_1^2+\cdots+x_d^2$. Then
$$h_{f,\infty}(x)=\begin{cases}
x+c\,\big(E_{d+1}(x+a)-E_{d+1}(-x+a)\big) & x\in[0,a],\\[2pt]
x+c\,\big(E_{d+1}(x+a)+E_{d+1}(-x+1+a)\big) & x\in[a,1-a],\\[2pt]
x+c\,\big(-E_{d+1}(x-1+a)+E_{d+1}(-x+1+a)\big) & x\in[1-a,1],
\end{cases}$$
where $$a=\begin{cases}\tfrac1n & d \text{ even},\\[2pt] \tfrac12-\tfrac1n & d \text{ odd},\end{cases}\qquad c=(-1)^{\lfloor (d+1)/2\rfloor}\,\frac{2^{d-2}\,n}{(d+1)!}.$$

## The limit Hilbert–Kunz multiplicity of the Fermat hypersurface
Pushing the same techniques in Gessel and Monsky's result for the $A_1$ singularity, one may compute the limit Hilbert–Kunz multiplicities of the Fermat hypersurfaces, those diagonal hypersurfaces of the form $x_1^d+\dots+x_n^d$. After computing these limits for the Fermat cubics, Meng conjectured the shape of the generating function of the limit Hilbert–Kunz multiplicities of such singularities, which I could confirm in this project:
**Corollary** (Conjecture of C. Meng). For $d\ge 2$, the generating function of the limit Hilbert–Kunz multiplicities of the Fermat hypersurfaces
$$\sum_{n=0}^{\infty} e_{\mathrm{HK},\infty}\big(R^{(d)}_n\big)\,z^n$$
is a rational function on the functions $z$, $\cos(a_iz)$ and $\sin(a_iz)$, for some finitely many $a_i\in\mathbb Q(\zeta_{4d})\cap\mathbb R$ with $\zeta_{4d}=e^{\frac{\pi}{2d}i}$.
*Note* (typo in the preprint): indeed, $a_i\in \mathbb{Q}(\zeta_{4d})\cap \mathbb{R}$, contrary to what appears in the preprint, which says $\mathbb{Q}(\zeta_{2d})\cap \mathbb{R}$—this will be corrected in a later version.