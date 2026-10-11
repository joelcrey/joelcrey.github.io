---
title: On the Watanabe–Yoshida conjecture
summary: The strong form of the Watanabe–Yoshida conjecture for complete intersections and dimensions 2 through 7, for every characteristic.
order: 2
published: true
collapsible: closed
---
>In this page, I cover content from [this](https://arxiv.org/abs/2506.09019v3) preprint, and the last section of [this](https://arxiv.org/abs/2609.39133) preprint.

# The Watanabe–Yoshida conjecture

Let $R_{p,d} := \mathbb{F}_p[[x_0,\dots,x_d]]/(x_0^2+\dots+x_d^2)$ the ring of formal series at the origin of an ordinary double point of characteristic $p$.

**Conjecture (Watanabe–Yoshida, 2005).** Let $(R,\mathfrak{m},k)$ be an unmixed nonregular local ring of characteristic $p>0$. Then, $e_\text{HK}(R)\geq e_\text{HK}(R_{p,d})\geq 1+c_d.$ Furthermore, if the first equality holds, then $\widehat{R} \cong k[[x_0,\dots,x_d]]/(x_0^2+\dots+x_d^2)$.

The Watanabe–Yoshida conjecture thus roughly states that the $A_1$ singularity attains the infimum of the Hilbert–Kunz multiplicity, and is the only one to do so. The first part of the statement was known to be true for complete intersections and for unmixed local rings of dimension up to 7, always in characteristic $p>2$. 

**About the solution of the known cases.** A variety of techniques come into these solutions, mainly from deformation theory and local algebra, used to understand rings with small Hilbert–Kunz multiplicity. The cases up to dimension 7 were solved by Watanabe–Yoshida, Aberbach–Enescu, Enescu–Shimomoto and Aberbach–Cox-Steib in a series of papers from 2002 through 2023, and follow from a wonderful interplay between a careful analysis of lower bounds, local algebra and deformation theory arguments.

In this project, I settle the stronger part of the statement in complete intersections, and dimension up to 7, all of them including the cases of characteristic 2 and 0.

## On the Strong Watanabe–Yoshida conjecture

The strong form of the conjecture for complete intersections can be obtained after refinements of the results in Enescu and Shimomoto's solution of the complete intersection case in characteristic $p>2$. As a corollary, we also obtain the result for (formally unmixed) singularities of dimension up to 7:

**Theorem (2025).** Let $(R,\mathfrak{m},k)$ be an unmixed nonregular local ring of characteristic $p>0$. Then, if the dimension of $R$ is less than 7, or if $R$ is a complete intersection, then $e_\text{HK}(R)= e_\text{HK}(R_{p,d})$ implies that that $\widehat{R} \cong k[[x_0,\dots,x_d]]/(x_0^2+\dots+x_d^2)$.

The most technical part of the proof is showing that the Hilbert–Kunz multiplicity of an $A_2$ singularity is strictly greater than the Hilbert–Kunz multiplicity of an $A_1$ singularity in every characteristic and dimension. This is shown via Han and Monsky's machinery to study the Hilbert–Kunz functions of the diagonal hypersurfaces.

## On the characteristic 2 case

In characteristic 2, the main subtlety, as it is often the case, is the fact that the theory of quadratic forms differs from the case of characteristic $\neq 2$. Namely, the standard form of a nondegenerate quadratic form, or in other words, the equation of an $A_1$ singularity, changes slightly: if the dimension $d$ is odd, then the singularity is defined by the equation $Q_d := x_0x_1+...+x_{d-1}x_{d}$, and if $d$ is even, then by $Q_d := x_0x_1+...+x_{d-2}x_{d-1}+x_d^2$.

**Theorem (2022).** Let $(R,\mathfrak{m},k)$ be an unmixed nonregular local ring of characteristic 2. Then, if the dimension of $R$ is less than 7, or if $R$ is a complete intersection, then $e_\text{HK}(R)\geq e_\text{HK}(R_{2,d})$, with equality only if $\widehat{R} \cong k[[x_0,\dots,x_d]]/(Q_d)$.

See the classification of the ADE singularities by Greuel and Kröning: [Simple Singularities in positive characteristic](https://doi.org/10.1007/BF02570742).

## On the characteristic 0 case

>The result below is in [this preprint](https://arxiv.org/abs/2609.39133) on limit F-invariants. Also, see [[limit_f_invariants_ade|this post]] for context on reductions mod $p$.

Via reduction mod $p$, one can state the Watanabe–Yoshida conjecture in the characteristic zero case for the *limit Hilbert–Kunz multiplicity*. Indeed, this result can also be settled for all complete intersections and all singularities of dimension up to 7 by reduction mod $p$, as well as the strong form of the conjecture due to the fact that also the *limit* Hilbert–Kunz multiplicity of an $A_1$ and an $A_2$ singularity also differs:

**Theorem** (Watanabe–Yoshida conjecture in characteristic zero). Let $K$ be a field of characteristic $0$, and $R_{0,d} := K[x_0,\dots,x_d]/(x_0^2+\cdots+x_d^2).$ Let $(R,\mathfrak m,K)$ be a $d$-dimensional $K$-algebra of essentially finite type. Moreover, assume that $R$ is unmixed and nonregular. If either $2\le d\le 7$, or $R$ is a complete intersection of dimension $\ge 2$, then either $\liminf_{p\to\infty} e_{\mathrm{HK},p}(R) > e_{\mathrm{HK},\infty}(R_{0,d}),$ or $R$ is an $A_1$ singularity.

*Notation.* This definition of lim-inf Hilbert–Kunz multiplicity is based on recent work by [Liu and Pande]() on positivity of the limit $F$-signature for klt pairs: we define $e_{\mathrm{HK},p}(R)$ as the infimum of the Hilbert–Kunz multiplicities of the characteristic $p$ models of $R$ (the closed fibers of a family of reductions mod $p$); for $p\gg0$ it does not depend on the chosen family. We say $R$ is an $A_1$ singularity if $\widehat R\cong K[[x_0,\dots,x_d]]/(a_0x_0^2+\cdots+a_dx_d^2)$ with $a_i\in K$ nonzero.