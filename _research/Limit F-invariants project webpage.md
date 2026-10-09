---
title: Limit F-invariants of the ADE singularities and the Fermat hypersurfaces
summary: Limits of the Hilbert–Kunz multiplicity and F-signature of reductions mod p, and their combinatorics.
slug: limit-f-invariants
order: 1
published: false   # unfinished: remove this line to publish
---

See the [arXiv](https://arxiv.org/abs/2609.39133) preprint of this project.

### Motivation: reduction mod $p$ and limit $F$-invariants
Given a certain set of equations with integer coefficients $f_1,\dots,f_r\in \mathbb{Z}[x_1,\dots,x_n]$, one may define reductions mod $p$ of such equations by passing to the quotient $\mathbb{Z}[x_1,\dots,x_n]\twoheadrightarrow \mathbb{F}_p[x_1,\dots,x_n]$. In general, it is expected that the properties of $\mathbb{C}[x_1,\dots,x_n]/(f_1,\dots,f_r)$ determines and is determined by the properties of most reductions mod $p$ $\mathbb{F}_p[x_1,\dots,x_n]/(f_1,\dots,f_r)$, i.e., at all but finitely many $p$, or perhaps at infinitely many values of $p$. Indeed, with the right setup, one can extract some of these from the usual properties of a flat family over a scheme.

Down at those reductions mod $p$, one may compute the Hilbert–Kunz multiplicity or the F-signature (or any numerical invariant) at every reduction mod $p$. There are lots of questions about the resulting sequence of numbers. Namely:
**Question.** Let $R = \mathbb{Q}[x_1,\dots,x_n]/(f_1,\dots,f_r)$ and $R_p = (\mathbb{F}_p[x_1,\dots,x_n]/(f_1,\dots,f_r))_{(x_1,\dots,x_n)}$ some reductions mod $p$. Does the sequence $e_\text{HK}(R_p)$ converge when $p\rightarrow \infty$?
We know that this limit converges in some particular cases, like for example, the diagonal hypersurfaces proven by [Gessel and Monsky in 2010](https://arxiv.org/abs/1007.2004), those of the form $x_1^{d_1}+\dots+x_n^{d_n}$. For an account of other solved cases, see the intro of [Brenner–Li–Miller](https://www.sciencedirect.com/science/article/pii/S0021869312004954).

### Combinatorial interpretation of the limit $F$-invariants of the $A_n$ singularities
In the case of the ring $R_{p,d}$, defined before, using this result for diagonal hypersurfaces, Gessel and Monsky showed the following striking formula:

**Theorem (Gessel–Monsky, 2010).** Let $p>0$ and $d\geq 2$. Then,$$\lim_{p\rightarrow \infty} e_\text{HK}(R_{p,d}) = 1+c_d,\quad \text{and} \quad \lim s(R_{p,d}) = 1-c_d$$where $c_d$ is the $d$-th coefficient of the Taylor expansion of the function $\sec x + \tan x = (1+\sin x)\sec x$. In other words, $d!\cdot c_d$ is the sequence of the [zig-zag numbers](https://oeis.org/A000111).

It is a natural question now whether others of the so-called "simple" singularities also have a combinatorial interpretation to the numerators of their limit Hilbert–Kunz multiplicities. In the case of the $A_n$ singularities, one quickly finds out that this is indeed the case:
**Theorem (2025).** Let $p>0$, $d\geq 2$, and define $S_{n,p,d} := \mathbb{F}_p[[x_1,\dots,x_n]]/(x_0^2+\dots+x_{d-1}^2+x_d^n),$ the power series at the origin of an $A_{n-1}$-singularity. Then, $$\lim_{p\rightarrow \infty} e_\text{HK}(S_{n,p,d}) = 1+c_d,\quad \text{and} \quad \lim s(S_{n,p,d}) = 1-c_d$$where $c_d$ is the $d$-th coefficient of the Taylor expansion of the function $\frac{n+1}{2}(\cos\frac{(n-1)x}{n+1}+\sin\frac{2x}{n+1})\sec x$. Combinatorially, $d!\cdot c_d = N_d(2,r),$ the number of $n$-signed alternating permutations of length $d$ (see Definition 3.10 and Proposition 3.11 in the arXiv preprint).
### The limit $F$-invariants of the non-diagonal ADE singularities
Gessel and Monsky's [results](https://arxiv.org/abs/1007.2004) for diagonal hypersurfaces also let us explore the values of the limit $F$-invariants for other diagonal ADE singularities, like $D_4$, $E_6$ and $E_8$, for which the Online Enciclopedia of Integer Sequence does produce some results. However, with those techniques, the non-diagonal ADE singularities, $D_n$ for $n\geq 5$, and $E_7$ in every dimension, were out of reach.

There are several generalisation of the $F$-invariants in the literature, one of them is [Mukhophadhyay and Meng](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70696)'s $h$-function. Later, Meng would develop the theory of the $h$-functions of hypersurfaces of the form $f+g$ where $f$ and $g$ have disjoint sets of variables, as well as the $h$-functions of binomials. These two ingredients and a bunch of computations yield the following result:
**Theorem (2026)** ...