---
title: On the Watanabe–Yoshida conjecture
summary: The strong form of the Watanabe–Yoshida conjecture for complete intersections, and the characteristic 2 case.
order: 2
---

See the [arXiv](https://arxiv.org/abs/2506.09019v3) preprint of this project.

Let $R_{p,d} := \mathbb{F}_p[[x_0,\dots,x_d]]/(x_0^2+\dots+x_d^2)$ the ring of formal series at the origin of an ordinary double point of characteristic $p$.

**Conjecture (Watanabe–Yoshida, 2005).** Let $(R,\mathfrak{m},k)$ be an unmixed nonregular local ring of characteristic $p>0$. Then,

$$e_\text{HK}(R)\geq e_\text{HK}(R_{p,d})\geq 1+c_d.$$

Furthermore, if the first equality holds, then $\widehat{R} \cong k[[x_0,\dots,x_d]]/(x_0^2+\dots+x_d^2)$.

### On the Strong Watanabe–Yoshida conjecture

The Watanabe–Yoshida conjecture thus roughly states that the $A_1$ singularity attains the infimum of the Hilbert–Kunz multiplicity, and is the only one to do so. This second part of the statement is what we call the "Strong" Watanabe–Yoshida conjecture. The goal of this project was settling the strong form of the conjecture for complete intersections, building on results by Enescu and Shimomoto. As a corollary, we also obtain the result in dimension up to 7 for general (unmixed) singularities:

**Theorem (2025).** Let $(R,\mathfrak{m},k)$ be an unmixed nonregular local ring of characteristic $p>0$. Then, if the dimension of $R$ is less than 7, or if $R$ is a complete intersection, then $e_\text{HK}(R)= e_\text{HK}(R_{p,d})$ implies that that $\widehat{R} \cong k[[x_0,\dots,x_d]]/(x_0^2+\dots+x_d^2)$.

### On the characteristic 2 case of the conjecture

Back in 2022, before I started my PhD at BCAM, I had the opportunity of doing an internship under the supervision of Ilya Smirnov. He suggested that we try to fill in some gaps in the literature of the Watanabe–Yoshida conjecture regarding characteristic 2.

The subtlety is that, in characteristic 2, the equation of an $A_1$ changes slightly (see the classification of [Simple Singularities in positive characteristic](https://doi.org/10.1007/BF02570742)). If the dimension $d$ is odd, then the singularity is defined by the equation $Q_d = x_0x_1+...+x_{d-1}x_{d}$, and if $d$ is even, then by $Q_d = x_0x_1+...+x_{d-2}x_{d-1}+x_d^2$.

**Theorem (2022).** Let $(R,\mathfrak{m},k)$ be an unmixed nonregular local ring of characteristic 2. Then, if the dimension of $R$ is less than 7, or if $R$ is a complete intersection, then $e_\text{HK}(R)\geq e_\text{HK}(R_{2,d})$, with equality only if $\widehat{R} \cong k[[x_0,\dots,x_d]]/(Q_d)$
