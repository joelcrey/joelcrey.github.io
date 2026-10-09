---
title: The Han–Monsky ring
category: math
series: han-monsky
series_part: 2
sagecell: true
sage_preload: /notes/han-monsky/hilbert_kunz.py
summary: The Grothendieck ring of k[T]-modules with nilpotent action, the δ- and λ-bases, and what we know about its multiplication table.
---

This post continues the [previous one](han-monsky-1-shape-of-hilbert-kunz-functions.html). To run the SageMath sessions, click **Load hilbert_kunz.py** first, then **Run** on any cell.

## Motivation

One may motivate this by trying to understand the function $D_k$:

(1) **The 2-variable case.** Say we want to compute $D(a,b)$ for positive integers $a\leq b$. Then,
$$D(a,b)=\dim_k\left(\frac{k[x,y]}{(x^a,y^b,x+y)}\right).$$
In this case, it is easy, because
$$\frac{k[x,y]}{(x^a,y^b,x+y)}\cong\frac{k[x]}{(x^a)},$$
and this has dimension $a$. So $D(a,b)=a$.

(2) **The 3-variable case.** If we want to do $D(a,b,c)$, then it is more subtle, because this is the dimension of
$$\frac{k[x,y,z]}{(x^a,y^b,z^c,x+y+z)}\cong\frac{k[x,y]}{(x^a,y^b,(x+y)^c)}.$$
For example, if $a,b,c$ do not satisfy the triangular inequality, so say $a+b<c$, then $(x^a,y^b,(x+y)^c)=(x^a,y^b)$. If, instead, they do satisfy the triangular inequality, then it is more complicated to give a general form.

(3) **From a dimension to decomposing a $k[T]$-module.** There is another perspective to this, which is studying the $k$-vector space
$$M_e:=\frac{k[x_1,\dots,x_n]}{(x_1^{a_1},\dots,x_n^{a_n})}$$
as a $k[T]$-module where $T$ acts like multiplication by $x_1^{d_1}+\dots+x_n^{d_n}$. By the structure theorem of finitely generated modules over a PID, this module has some decomposition as a direct sum of cyclic $k[T]$-modules:
$$M_e=\bigoplus\left(\frac{k[T]}{(T^i)}\right)^{\oplus a_i}.$$
In other words, take the matrix describing the $k$-linear action of $T$ in the $k$-vector space $M_e$ over the monomial basis, compute its Jordan form, and count how many Jordan blocks of each size it has; these are the numbers $a_i$. Note that $D_k=\dim_kM_e/TM_e=\sum a_i$.

(4) **Decomposing as tensor product of simpler $k[T]$-modules.** With this perspective, let us now do a two-variable example:

**Example 2.1.** Say we want to compute $D_k(3/2,4/3)$. If I have two $k[T]$-modules $M,N$, I can define a $k[T]$-module structure on the vector space $M\otimes_kN$ as $T(m\otimes n)=Tm\otimes n+m\otimes Tn$. With this (certainly arbitrary choice of a) product, I can decompose this vector space as a tensor product of simpler $k$-vector spaces:
$$M=\frac{k[x,y]}{(x^3,y^4)}=\frac{k[x]}{(x^3)}\otimes_k\frac{k[y]}{(y^4)},$$
and if we give the $T$-action given by $x^2$ and $y^3$, respectively, then this $k$-vector space isomorphism is actually also a $k[T]$-module isomorphism. I can compute the decomposition of each one of those simpler $k[T]$-modules, say:
$$M\cong\left(\frac{k[T]}{(T^2)}\oplus\frac{k[T]}{(T)}\right)\otimes_k\left(\frac{k[T]}{(T^2)}\oplus\left(\frac{k[T]}{(T)}\right)^{\oplus2}\right).\tag{2}$$
So the problem becomes a problem about decomposing products of these simpler $k[T]$-modules. However, with a different notation we can get way further: we will work in the Grothendieck ring $\Gamma_k$ of the isomorphism classes of these $k[T]$-modules.

Note that, in order to compute the Hilbert–Kunz function, it would be nice to have an easier description of the decomposition of $M_e$, as a function of $e$. All this setup leads to this, ultimately yielding a functional equation for $D_k$.

**Definition 2.2.**

(1) ***$k$-objects.*** *a $k[T]$-module with nilpotent action of $T$, or equivalently, a $k[T]$-module that is finite-dimensional as $k$-vector space.*

(2) ***Product of $k$-objects.*** *We define their product as $T(m\otimes n)=Tm\otimes n+m\otimes Tn$.*

(3) ***Grothendieck ring of $k$-objects.*** *The relation $M-M'=N-N'$ if and only if $M\oplus N'\cong N\oplus M'$ is an equivalence class, and these operations distribute with the product of $k$-objects, so we can define $\Gamma_k$ the Grothendieck ring of $k$-objects, whose unit element is $k[T]/(T)=k$.*

(4) ***$\delta$-basis and $\lambda$-basis.*** *$\delta_i=k[T]/T^i$, and $\lambda_i:=(-1)^i(\delta_{i+1}-\delta_i)$. Note that we set $\delta_0=0$, and $\delta_1=\lambda_0$ is the unit.*

(5) ***Dimension and $\alpha$-map.*** *Finally, we define $\dim_k(M-N)=\dim_kM-\dim_kN$ and $\alpha(M-N):=\dim_k(M/TM)-\dim_k(N/TN)$. Note that $\alpha(\delta_i)=1$, $\alpha(\lambda_0)=1$ and $\alpha(\lambda_i)=0$ for $i\geq1$.*

**Example 2.3** (Back to the previous example with the $\delta$-basis). We continue with Example 2.1. Writing (2) in this language, we need to compute $(\delta_2+\delta_1)\cdot(\delta_2+2\delta_1)=\delta_2^2+3\delta_1\delta_2+2\delta_1^2$, and we only need to compute the product $\delta_2^2$—because $\delta_1$ is the unit in $\Gamma$, the rest of the products are clear. If the characteristic is, say, $p=2$, then, computing really is about explicitly writing what these are:
$$\delta_2^2=\frac{k[T,S]}{(T^2,S^2)}$$
with $T$-action $T+S$. We can guess that $\delta_2^2=2\delta_2$ because $\delta_2^2=a_1\delta_1+a_2\delta_2$ for some $a_1,a_2$, since $(T+S)^2=T^2+S^2=0$, so there are no cyclic summands of larger order. However, since $\dim_k\delta_2^2=4$ and $\alpha\delta_2^2=\dim_kk[T,S]/(T^2,S^2,T+S)=\dim_kk[T]/T^2=2$, we conclude that $\delta_2^2=2\delta_2$.

An alternative way of seeing this, noted to me by Kevin Tucker, is simply writing out the matrix representing the action of $T+S$ in a basis of monomials in $k[T,S]/(T^2,S^2)$, which is the matrix
$$M=\begin{pmatrix}0&0&0&0\\1&0&0&0\\1&0&0&0\\0&1&1&0\end{pmatrix},\qquad M^2=\begin{pmatrix}0&0&0&0\\0&0&0&0\\0&0&0&0\\2&0&0&0\end{pmatrix}.$$
Then, the number of Jordan blocks of size one will be $4-2\operatorname{rank}M+\operatorname{rank}M^2$, the number of Jordan blocks of size two is $\operatorname{rank}M-2\operatorname{rank}M^2+\operatorname{rank}M^3$.

```sage
G = HanMonskyRing(2)
print(G.delta(2)^2)
M = (G.delta(2) + G.delta(1)) * (G.delta(2) + 2*G.delta(1))
print(M)
print(M.alpha())    # alpha(M) = dim_k M/TM
HanMonskyRing(3).delta(2)^2
```

## The multiplication table of $\Gamma_k$

In this section, we compile everything about the representation ring in the literature to answer the following question:

**Question.** *Given $i,j$, compute $\delta_i\delta_j$ or $\lambda_i\lambda_j$. In other words, what is the multiplication table of $\Gamma_k$ in terms of the $\delta$-basis and the $\lambda$-basis?*

One of the points of introducing the $\lambda$-basis is that its multiplication table is slightly easier to track, for several reasons. We will see later that the $\lambda$-basis also seemed to help answer a conjecture made by Han in her thesis [Han92], and this conjecture yielded the Hilbert–Kunz function of all diagonal hypersurfaces. Let us review some properties about the $\lambda$-basis to answer the question above.

**Lemma 2.4** (Theorem 3.2, [HM93]). *The $\mathbb Z$-submodule $\Lambda_e\subset\Gamma$ generated by $\{\lambda_k\}_{k\leq p^e-1}$ is multiplicatively closed. In other words, if $\lambda_i\lambda_j=\sum a_k\lambda_k$ and $i,j\leq p^e-1$, then $a_k=0$ for all $k\geq p^e$.*

**Example 2.5** ($\Lambda_1$ in characteristic 2). Now that we know this, let's compute the multiplication table of $\Lambda_1$ in characteristic 2. Obviously, since $\lambda_0=\delta_1=k[T]/(T)$ is the unit element of the ring, then we know that $\lambda_0^2=\lambda_0$ and $\lambda_0\lambda_1=\lambda_1$. Let us do $\lambda_1^2$ then.
$$\lambda_1^2=(\delta_2-\delta_1)^2=\delta_2^2-2\delta_2\delta_1+\delta_1^2=\delta_2^2-2\delta_2+\delta_1.$$
Note that this implies that
$$\dim_k(\lambda_1^2)=\dim_k(\delta_2^2-2\delta_2+\delta_1)=1\quad\text{and}\quad\alpha(\lambda_1^2)=1,$$
because $\delta_2^2=k[T,S]/(T^2,S^2,T+S)$ has dimension 2, so $\alpha(\lambda_1^2)=2-2+1=1$. Therefore, since $\lambda_1^2=a_0\lambda_0+a_1\lambda_1$, it can only be that $a_0=1$ and $a_1=0$.

Actually, a similar argument shows that, in general, $\lambda_q^2=0$ in every characteristic.

Due to this fact, we may identify the elements of $\Lambda_e$ with the matrices representing the action by multiplication over the $\lambda$-basis. We can start describing this representation for $\Lambda_1$ using Han and Monsky's formula:

**Lemma 2.6** ([HM93]). *The multiplication table of $\Lambda_1$ is given as follows: for $0\leq i\leq j\leq p-1$,*
$$\lambda_i\lambda_j=\sum_{k=j-i}^{\min(i+j,\,2p-2-i-j)}\lambda_k.$$

**Example 2.7** (Matrices for $\Lambda_1$ for $p=2,3,5$). For $p=2$, the matrices are $2\times2$, and $\lambda_0$ is always the identity:
$$\lambda_0=\begin{pmatrix}1&0\\0&1\end{pmatrix},\qquad\lambda_1=\begin{pmatrix}0&1\\1&0\end{pmatrix}.$$
For $p=3$, the matrices are $3\times3$: $\lambda_0$ is the identity, $\lambda_2$ is the antidiagonal matrix, and $\lambda_1$ is a cross of 1's with 0's in the corners:
$$\lambda_0=\begin{pmatrix}1&0&0\\0&1&0\\0&0&1\end{pmatrix},\qquad\lambda_1=\begin{pmatrix}0&1&0\\1&1&1\\0&1&0\end{pmatrix},\qquad\lambda_2=\begin{pmatrix}0&0&1\\0&1&0\\1&0&0\end{pmatrix}.$$
For $p=5$, the matrices are $5\times5$: $\lambda_0$ and $\lambda_4$ are the diagonal and antidiagonal, $\lambda_2$ is a filled diamond centered in the matrix, and $\lambda_1,\lambda_3$ are slanted diamonds (mirror images of each other):
$$\lambda_0=\begin{pmatrix}1&0&0&0&0\\0&1&0&0&0\\0&0&1&0&0\\0&0&0&1&0\\0&0&0&0&1\end{pmatrix},\qquad\lambda_1=\begin{pmatrix}0&1&0&0&0\\1&1&1&0&0\\0&1&1&1&0\\0&0&1&1&1\\0&0&0&1&0\end{pmatrix},$$
$$\lambda_2=\begin{pmatrix}0&0&1&0&0\\0&1&1&1&0\\1&1&1&1&1\\0&1&1&1&0\\0&0&1&0&0\end{pmatrix},\qquad\lambda_3=\begin{pmatrix}0&0&0&1&0\\0&0&1&1&1\\0&1&1&1&0\\1&1&1&0&0\\0&1&0&0&0\end{pmatrix},\qquad\lambda_4=\begin{pmatrix}0&0&0&0&1\\0&0&0&1&0\\0&0&1&0&0\\0&1&0&0&0\\1&0&0&0&0\end{pmatrix}.$$

Note that all these matrices are symmetric and commute, and therefore are simultaneously diagonalisable, which would yield an orthogonal basis of elements of $\Lambda_e$. This perspective is exploited in [CR26, Men26a] to understand the Hilbert–Kunz multiplicities of quadrics better. The first reference in particular focuses more on the matrix representation, following the approach of [PSSY26], which originates from this matrix representation, together with the Han–Monsky algorithm.

```sage
G = HanMonskyRing(5)
print(G.lam(1).matrix())    # column j is lambda_1 * lambda_j
G.lam(1)^2
```

**Lemma 2.8.** *Let $i\geq0$, and let $i_0+i_1p+i_2p^2+\dots+i_{e-1}p^{e-1}$ its $p$-adic expansion. Then, $\lambda_i=\lambda_{i_0}\lambda_{i_1p}\cdots\lambda_{i_{e-1}p^{e-1}}$. In particular, if I want to know $\lambda_i\lambda_j$, I only need to care about the products $\lambda_{aq}\lambda_{bq}$.*

**Example 2.9.** With this lemma, and the observation that $\lambda_q^2=0$, we can now give a complete description of multiplication in the Han–Monsky ring in characteristic 2: indeed, to compute $\lambda_a\lambda_b$, first decompose $a$ and $b$ in their 2-adic decompositions $a_0+a_12+\dots+a_e2^e$ and $b_0+b_12+\dots+b_e2^e$, where $a_k,b_k\in\{0,1\}$; then $\lambda_a\lambda_b=\prod\lambda_{a_k2^k}\lambda_{b_k2^k}$. This product can be described with the concept of "nim sum": the nimsum of a tuple of zeros and ones is the component-wise sum modulo 2, denoted like
$$(a_0,\dots,a_e)\oplus(b_0,\dots,b_e)=(a_0+b_0\pmod 2,\dots,a_e+b_e\pmod2).$$
Thus, for instance,
$$\lambda_3\lambda_5=(\lambda_{0\cdot4}\lambda_{1\cdot2}\lambda_1)(\lambda_{1\cdot4}\lambda_{0\cdot2}\lambda_1)=\lambda_4\lambda_2\lambda_0=\lambda_6.$$

In terms of matrices, in characteristic 2 it is easy to observe what is going on. Let us denote $[\lambda_i]_2$ for the matrix representing the product by $\lambda_i$ in $\Lambda_2$, and $\otimes$ the Kronecker product of matrices:
$$[\lambda_1]=I_2\otimes J=\begin{pmatrix}0&1&0&0\\1&0&0&0\\0&0&0&1\\0&0&1&0\end{pmatrix},\qquad[\lambda_2]=J\otimes I_2=\begin{pmatrix}0&0&1&0\\0&0&0&1\\1&0&0&0\\0&1&0&0\end{pmatrix},$$
$$[\lambda_3]=[\lambda_1][\lambda_2]=J\otimes J=\begin{pmatrix}0&0&0&1\\0&0&1&0\\0&1&0&0\\1&0&0&0\end{pmatrix},\qquad[\lambda_0]=I_4.$$

The issue when trying to scale these observations to higher characteristics is that the Kronecker product description does not work exactly.

**Example 2.10.** In characteristic 3, note that $\lambda_3$ has the following matrix in $\Lambda_2$:
$$[\lambda_3]_2=\left(\begin{array}{ccc|ccc|ccc}0&0&0&1&0&0&0&0&0\\0&0&0&0&1&0&0&0&0\\0&0&0&0&0&1&0&0&0\\\hline1&0&0&0&0&1&1&0&0\\0&1&0&0&1&0&0&1&0\\0&0&1&1&0&0&0&0&1\\\hline0&0&0&1&0&0&0&0&0\\0&0&0&0&1&0&0&0&0\\0&0&0&0&0&1&0&0&0\end{array}\right),$$
which is not exactly $[\lambda_1]_1\otimes[\lambda_0]_1$. One needs to adjust for some "reflections".

```sage
G = HanMonskyRing(3)
A = G.lam(3).matrix()
B = G.lam(1).matrix().tensor_product(identity_matrix(3))
A.subdivide([3,6], [3,6])    # 3x3 blocks, as above
A, B    # left: [lambda_3]_2,  right: [lambda_1]_1 (x) [lambda_0]_1
```

```sage
A == B
```

The main result is the following, we refer the reader to [MT06] for the details:

**Theorem 2.11** (Monsky and Teixeira, [MT06], Meng, [Men26a]). *Define the following map*
$$\theta(\lambda_i):=\begin{cases}\lambda_{pi}&\text{even }i,\\ \lambda_{pi+p-1}&\text{odd }i.\end{cases}$$
*The $\mathbb Z$-linear extension to $\Gamma_k$ of this map is a ring homomorphism.*

This means that once we understand the multiplication table of $\Lambda_1$, then we understand the multiplication table of $\Gamma_k$: denote the $p$-adic expansion of $i$ by $i_0+i_1p+\dots+i_{e-1}p^{e-1}$;

**Proposition 2.12** (Monsky–Teixeira, [MT06], Meng, [Men26a]). *For $i=\sum_{k=0}^{e-1}i_kp^k$ with $0\leq i_k\leq p-1$, put*
$$a_k(i):=\begin{cases}i_k,&\sum_{r=k+1}^{e-1}i_rp^r\text{ even},\\ p-1-i_k,&\sum_{r=k+1}^{e-1}i_rp^r\text{ odd}.\end{cases}$$
*Then the $\mathbb Z$-linear map*
$$\Phi_e\colon\Lambda_e\longrightarrow\Lambda_1^{\otimes e},\qquad\lambda_i\longmapsto\lambda_{a_0(i)}\otimes\dots\otimes\lambda_{a_{e-1}(i)}$$
*is a ring isomorphism.*

## References

- [CR26] N. Cox-Steib and R. Redner. *The linear algebra of the Han–Monsky representation ring*. The Electronic Journal of Linear Algebra, 42:329–348, 2026.
- [Han92] C. Han. *The Hilbert–Kunz Function of a Diagonal Hypersurface*. Brandeis University, 1992.
- [HM93] C. Han and P. Monsky. *Some surprising Hilbert–Kunz functions*. Mathematische Zeitschrift, 214(1):119–135, 1993. [doi:10.1007/BF02572395](https://doi.org/10.1007/BF02572395).
- [Men26a] C. Meng. *Hilbert–Kunz multiplicity of quadrics decreases*, 2026. [arXiv:2606.04346](https://arxiv.org/abs/2606.04346).
- [MT06] P. Monsky and P. Teixeira. *P-Fractals and power series–II. Some applications to Hilbert–Kunz theory*. Journal of Algebra, 304(1):237–255, 2006. [doi:10.1016/j.jalgebra.2005.07.033](https://doi.org/10.1016/j.jalgebra.2005.07.033).
- [PSSY26] I. Pak, B. Shapiro, I. Smirnov, and K.-i. Yoshida. *Hilbert–Kunz multiplicity of quadrics via Ehrhart theory*, 2026. [arXiv:2508.17915](https://arxiv.org/abs/2508.17915).
