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
Say $f\in \mathbb{Z}[x_1,\dots,x_n]$ is a polynomial with integer coefficients, and consider $f_p\in\mathbb{F}_p[x_1,\dots,x_n]$ its _reductions mod $p$_. In general, it is expected that the behaviour of the ring $R = \mathbb{C}[[\underline{x}]]/(f)$ is determined by and determines the behaviour of the rings $R_p=\mathbb{F}_p[[\underline{x}]]/(f_p)$ at _almost all $p$_. For instance, the dimension, or the (Hilbert–Samuel) multiplicity of $R_p$ coincides with the dimension of $R$ at all but finitely many $p$. 

However, the Hilbert–Kunz multiplicity and the $F$-signature present a much more interesting behaviour: sometimes, $e_{\text{HK}}(R_p)$ can be a rational function on $p$, or quasi-rational (this is, oscillating between several rational functions), or strictly decreasing with $p$. Actually, apart from a few particular cases, the following question remains open in general:

**Question.** Do the sequences $e_\text{HK}(R_p)$ or $s(R_p)$ converge when $p\rightarrow \infty$? Provided the limits exist, can we interpret their values?

Some examples for which this limit is known is $x_1^{d_1}+\dots+x_n^{d_n}$, which was proven by [Gessel and Monsky](https://arxiv.org/abs/1007.2004) in 2010.  It follows from work of [Meng](https://arxiv.org/abs/2507.13898) that the limits also exist for all the ADE (or simple) singularities, and computing these is one of the main result of the project we will discuss below. For an account of other known cases, see the intro of [Brenner–Li–Miller](https://www.sciencedirect.com/science/article/pii/S0021869312004954).

## The limit $F$-invariants of the $A_n$ singularities and combinatorics
In the case of the $A_n$ singularities, with equation $f_n = x_0^2+\dots+x_{d-1}^2+x_d^{n+1}$, we can interpret the limits combinatorially. In the case of the $A_1$ singularity, Gessel and Monsky showed the following striking formula:

**Theorem** (Gessel–Monsky, 2010). The sequence $d\mapsto d!(\lim_{p\rightarrow \infty}e_{\text{HK}}(f_{1,p})-1)$ is the sequence of the [zig-zag numbers](https://oeis.org/A000111). The generating function of this sequence is $\sec x+ \tan x = (1+\sin x)\sec x$.

It is a natural question now whether the rest of the $A_n$ singularities also have a combinatorial interpretation to the numerators of their limit Hilbert–Kunz multiplicities. In the case of the $A_n$ singularities, a generalisation is proven to exist:

**Theorem** (Limit F-invariants of the $A_n$ singularities, 2026). The sequence $d\mapsto d!(\lim_{p\rightarrow \infty}e_{\text{HK}}(f_{n,p})-1)$ is the sequence $N_d(2,n+1)$, of $n+1$-signed alternating permutations of length $d$. The generating function of this sequence is $\frac{n+1}{2}(\cos\frac{(n-1)x}{n+1}+\sin\frac{2x}{n+1})\sec x$.

## The limit $F$-invariants of the ADE singularities
When we try to compute the limit $F$-invariants of other $ADE$ singularities, we quickly run into the issue that we cannot use Gessel and Monsky's result for $E_7$ and $D_n,n\geq 5$, because these are not diagonal. However, all these singularities are of the form $g(x,y)+x_1^2+...+x_k^2$, so we shall aim at obtaining generating functions like the ones above for their limit $F$-invariants.

Here is where a more sophisticated theory of $F$-invariants comes into play: instead of studying only the dimensions of quotients $\mathbb{F}_p[[\underline{x}]]/(f+\mathfrak{m}^{[p^e]})$, it becomes necessary studying the dimension of all quotients $\mathbb{F}_p[[\underline{x}]]/(f^a+\mathfrak{m}^{[p^e]})$, which in turn becomes a function$$h\left(\frac{a}{q}\right):= \frac{1}{q^n}\dim \frac{\mathbb{F}_p[[\underline{x}]]}{(f^a+\mathfrak{m}^{[p^e]})}.$$This produces a function on the rational numbers of $[0,1]$ of the form $\frac{a}{q}$ where $q$ are powers of the characteristic, which was studied by Monsky and Teixeira. This function can be extended to a continuous function on $[0,1]$, which yields a concave function whose derivative interpolates between the Hilbert–Kunz multiplicity and the F-signature of the hypersurfaces. This is the so-called $h$-function of the hypersurface $f$, introduced by Meng and Mukhopadhyay.

Of course, in the same way we did above, we may consider passing to the limit, to consider the limit version of the $h$-function, provided it converges at every $x$. Some examples of this function extracted from [Meng's preprint](https://arxiv.org/abs/2507.13898): the first picture is the limit $h$-functions of the $A_1$ singularities between dimensions $1$ and $6$; the second picture are limit $h$-functions of certain binomials. Note the points in the graph - these examples are piecewise polynomials, and the points are the breakpoints of the domain.
![[A_1_dim1through6.png|300]]![[some_binomials.png|300]]

Introducing this theory allows us to compute the generating functions of the limit $F$-invariants of these singularities.
**Theorem** (Limit $F$-invariants of the simple singularities, 2026). Let $f = g(x_0,x_1)+x_2^2+\cdots+x_d^2.$ Then, the generating function of $$d\mapsto d!(e_{\mathrm{HK},\infty}(f)-1)$$is the function $F_g(z)$, in the table below, where we write $T(z)=\sec z+\tan z$.

|                | $g(x,y)$       | $F_g(z)$                                                                                                                                                                                  |
| -------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| $A_n$, $n\ge1$ | $x^{n+1}+y^2$  | $\dfrac{n+1}{2}\,\dfrac{\cos\frac{(n-1)z}{n+1}+\sin\frac{2z}{n+1}}{\cos z}$                                                                                                               |
| $D_n$, $n\ge4$ | $x^2y+y^{n-1}$ | $\dfrac{(n-1)^2}{4(n-2)}\cos\dfrac{z}{n-1}+\dfrac{(n-3)^2}{4(n-2)}\cos\dfrac{z}{n-3}+\Big(1+\dfrac{(n-1)^2}{4(n-2)}\sin\dfrac{z}{n-1}+\dfrac{(n-3)^2}{4(n-2)}\sin\dfrac{z}{n-3}\Big)T(z)$ |
| $E_6$          | $x^3+y^4$      | $3\,\dfrac{\cos\frac z2+\sin\frac z2}{\cos z}\,\cos\dfrac z3$                                                                                                                             |
| $E_7$          | $x^3+xy^3$     | $\dfrac{27}{16}\Big(\cos\dfrac z9-\sin\dfrac{2z}9\Big)+\dfrac{27}{16}\Big(\sin\dfrac z9+\cos\dfrac{2z}9\Big)T(z)$                                                                         |
| $E_8$          | $x^3+y^5$      | $\dfrac{15}{4}\,\dfrac{\cos\frac{3z}5+\sin\frac{2z}5}{\cos z}\,\cos\dfrac z3$                                                                                                             |

Note that $n=1$, the $A_1$ row gives $F_g(z)=\sec z+\tan z$, recovering the formula by Gessel and Monsky.

## The $h$-functions of the $A_n$ singularities and Euler polynomials
As we already hinted above, one can show that the limit $h$-functions of the ADE singularities are piecewise polynomials in $\mathbb{Q}[x]$, with only finitely many breakpoints (more general $h$-function may be piecewise polynomials with countably many breakpoints).

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