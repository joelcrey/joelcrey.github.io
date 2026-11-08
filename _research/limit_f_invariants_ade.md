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
Say $f$ is a polynomial with integer coefficients, and consider $f_p$ its _reductions mod $p$_, i.e., considering its coefficients in $\mathbb{F}_p$. In general, it is expected that the behaviour of the singularities of $f$ is determined by and determines the behaviour of the singularities of $f_p$ at _almost all $p$_.

For instance, the dimension, or the (Hilbert–Samuel) multiplicity $V(f)$ with the dimension of $R$ at all but finitely many $p.$ Also whether $f$ has singularities or not, as well as several singularity types are determined by those of $f_p$ at almost all $p$.

However, the Hilbert–Kunz multiplicity and the $F$-signature present a much more interesting behaviour. In a few simpler cases, it may remain constant across most characteristics, but in general, it seems to remain non-constant. For instance, it may oscillate between to functions:
$$
e_\text{HK}\left(\dfrac{\mathbb{F}_p[[x,y,z]]}{(x^4+y^4+z^3)}\right) = \begin{cases}3+\frac{1}{p^2} & p \equiv 3,5 \pmod{8}\\
3 & p\equiv 1,7\pmod{8}\end{cases}
$$
example from [(Monsky, 2006)](https://www.sciencedirect.com/science/article/pii/S0021869306000238). For another example, in the case of the $A_1$ singularity, it was proven [(Pak et al, 2026)](https://arxiv.org/abs/2508.17915) that $e_{\text{HK}}(R_p)$ is an strictly decreasing rational function on $p$; for instance, in dimension $4$:
$$
\begin{align*}
e_\text{HK}\left(\dfrac{\mathbb{F}_p[[x,y,z,u,v]]}{(x^2+y^2+z^2+u^2+v^2)}\right) &= \dfrac{29p^2+15}{24p^2+12}, \text{for } p>2.\\
s\left(\dfrac{\mathbb{F}_p[[x,y,z,u,v]]}{(x^2+y^2+z^2+u^2+v^2)}\right) &= \dfrac{19p^2+9}{24p^2+12}, \text{for } p>2.
\end{align*}
$$
Note that in both cases, though, the Hilbert–Kunz multiplicity converges to a rational number; $29/24$ in the first case, and $3$ in the second. Indeed, whether this is always the case remains a wide open question:

**Question.** Do the sequences $e_\text{HK}(R_p)$ or $s(R_p)$ converge when $p\rightarrow \infty$? Provided the limits exist, can we interpret their values?

Some examples for which this limit is known is $x_1^{d_1}+\dots+x_n^{d_n}$, which was proven by [Gessel and Monsky](https://arxiv.org/abs/1007.2004) in 2010.  It follows from work of [Meng](https://arxiv.org/abs/2507.13898) that the limits also exist for all the ADE (or simple) singularities, and computing these is one of the main result of the project we will discuss below. For an account of other known cases, see the intro of [Brenner–Li–Miller](https://www.sciencedirect.com/science/article/pii/S0021869312004954).

## The limit $F$-invariants of the $A_n$ singularities and combinatorics
In the case of the $A_n$ singularities, with equation $f_n = x_0^2+\dots+x_{d-1}^2+x_d^{n+1}$, we can interpret the limits combinatorially. In the case of the $A_1$ singularity, Gessel and Monsky showed the following striking formula:

**Theorem** (Gessel–Monsky, 2010). The sequence $d\mapsto d!(\lim_{p\rightarrow \infty}e_{\text{HK}}(f_{1,p})-1)$ is the sequence of the [zig-zag numbers](https://oeis.org/A000111). The generating function of this sequence is $\sec x+ \tan x = (1+\sin x)\sec x$.

It is a natural question now whether the rest of the $A_n$ singularities also have a combinatorial interpretation to the numerators of their limit Hilbert–Kunz multiplicities. In the case of the $A_n$ singularities, a generalisation is proven to exist:

**Theorem** (Limit F-invariants of the $A_n$ singularities, 2026). The sequence $d\mapsto d!(\lim_{p\rightarrow \infty}e_{\text{HK}}(f_{n,p})-1)$ is the sequence $N_d(2,n+1)$, of $n+1$-signed alternating permutations of length $d$. The generating function of this sequence is $\frac{n+1}{2}(\cos\frac{(n-1)x}{n+1}+\sin\frac{2x}{n+1})\sec x$.

## The limit $F$-invariants of the ADE singularities
When we try to compute the limit $F$-invariants of other $ADE$ singularities, we quickly run into the issue that we cannot use Gessel and Monsky's result for $E_7$ and $D_n,n\geq 5$, because these are not diagonal. However, all these singularities are of the form $g(x,y)+x_1^2+...+x_k^2$, so we shall aim at obtaining generating functions like the ones above for their limit $F$-invariants.

Here is where a more sophisticated theory of $F$-invariants comes into play: instead of studying only the dimensions of quotients $\mathbb{F}_p[[\underline{x}]]/(f+\mathfrak{m}^{[p^e]})$, it becomes necessary studying the dimension of all quotients $\mathbb{F}_p[[\underline{x}]]/(f^a+\mathfrak{m}^{[p^e]})$, which in turn becomes a function$$h\left(\frac{a}{q}\right):= \frac{1}{q^n}\dim \frac{\mathbb{F}_p[[\underline{x}]]}{(f^a+\mathfrak{m}^{[p^e]})}.$$This produces a function on the rational numbers of $[0,1]$ of the form $\frac{a}{q}$ where $q$ are powers of the characteristic, which was studied by Monsky and Teixeira. This function can be extended to a continuous function on $[0,1]$, which yields a concave function whose derivative interpolates between the Hilbert–Kunz multiplicity and the F-signature of the hypersurfaces. This is the so-called $h$-function of the hypersurface $f$. The general theory of $h$-functions was introduced in [(Meng and Mukhopadhyay, 2023)](https://arxiv.org/abs/2310.10270).

Of course, in the same way we did above, we may consider taking the characteristic $p\rightarrow \infty$ to the limit, and consider the _limit $h$-function_ of a hypersurface, provided it converges at every $x$. Some examples of this function extracted from [(Caminata et al, 2024)]([https://arxiv.org/abs/2507.13898](https://arxiv.org/abs/2403.12863)) and [(Meng, 2026)](https://arxiv.org/abs/2507.13898): limit $h$-functions of the $A_1$ singularities, dimensions $1$ through $6$, and limit $h$-functions of certain binomials. Note the points in the graph - in these examples, the limit $h$-functions are piecewise polynomials, and the points are the breakpoints of the domain.
![[A_1_dim1through6.png|300]]![[some_binomials.png|300]]

Introducing this theory allows us to compute the generating functions of the limit $F$-invariants of these singularities.
**Theorem** (Limit $F$-invariants of the simple singularities, [Theorem 3.8, 4.14, 4.18](https://arxiv.org/abs/2609.39133)). Let $f = g(x_0,x_1)+x_2^2+\cdots+x_d^2.$ Then, the generating function of $$d\mapsto d!(e_{\mathrm{HK},\infty}(f)-1)$$is the function $F_g(z)$, in the table below, where we write $T(z)=\sec z+\tan z$.

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

In the case of the $A_n$ singularities, a closed form for these polynomials in terms of the dimension, and the parameter $n$, can be provided using the right $\mathbb{Q}$-basis of $\mathbb{Q}[x]$: the Euler polynomials. The [Euler polynomials](https://mathworld.wolfram.com/EulerPolynomial.html) are a set of polynomials given by the series $\dfrac{2e^{xz}}{e^z+1}=\sum_{k\ge0}E_k(x)\dfrac{z^k}{k!}$ which are important to combinatorics and number theory, and form a $\mathbb{Q}$-basis in $\mathbb{Q}[x]$ (not to confuse with the [Eulerian polynomials](https://oeis.org/wiki/Eulerian_polynomials), which are also important in these fields, and also show up in the proof of Gessel and Monsky's formula for different reasons).

**Theorem** (Limit $h$-functions of the $A_n$ singularities, [Theorem 3.4](https://arxiv.org/abs/2609.39133)). Let $n\ge 2$, $d\ge1$, and $f=x_0^n+x_1^2+\cdots+x_d^2$. Then
$$h_{f,\infty}(x)=\begin{cases}
x+c\,\big(E_{d+1}(x+a)-E_{d+1}(-x+a)\big) & x\in[0,a],\\[2pt]
x+c\,\big(E_{d+1}(x+a)+E_{d+1}(-x+1+a)\big) & x\in[a,1-a],\\[2pt]
x+c\,\big(-E_{d+1}(x-1+a)+E_{d+1}(-x+1+a)\big) & x\in[1-a,1],
\end{cases}$$
where $$a=\begin{cases}\tfrac1n & d \text{ even},\\[2pt] \tfrac12-\tfrac1n & d \text{ odd},\end{cases}\qquad c=(-1)^{\lfloor (d+1)/2\rfloor}\,\frac{2^{d-2}\,n}{(d+1)!}.$$

## The limit Hilbert–Kunz multiplicity of the Fermat hypersurface
A different direction in which one may want to generalise Gessel and Monsky's $\sec + \tan$ formula, which regard the quadrics $x_1^2+\dots+x_n^2$, is the case of the so-called Fermat hypersurfaces, those of the form $x_1^d+\dots+x_n^d$.

The theory of $h$-functions provides a method to compute these limit Hilbert–Kunz multiplicities computation; however, it is very involved to do so for a general $d$. The case of $d=2$ and $3$ brought Meng to state a conjecture about the generating function of these limits. Independently from the theory of $h$-functions, merely by generalising Gessel and Monsky's original computations, we obtain the following result:
**Corollary** (Conjecture of C. Meng, [Theorem 5.10](https://arxiv.org/abs/2609.39133)). For $d\ge 2$, the generating function of the limit Hilbert–Kunz multiplicities of the Fermat hypersurfaces
$$\sum_{n=0}^{\infty} e_{\mathrm{HK},\infty}\big(R^{(d)}_n\big)\,z^n$$
is a rational function on the functions $z$, $\cos(a_iz)$ and $\sin(a_iz)$, for some finitely many $a_i\in\mathbb Q(\zeta_{4d})\cap\mathbb R$ with $\zeta_{4d}=e^{\frac{\pi}{2d}i}$.
*Note* (typo in the preprint): indeed, $a_i\in \mathbb{Q}(\zeta_{4d})\cap \mathbb{R}$, contrary to what appears in the preprint, which says $\mathbb{Q}(\zeta_{2d})\cap \mathbb{R}$—this will be corrected in a later version.