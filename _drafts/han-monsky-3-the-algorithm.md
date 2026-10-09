---
title: The Han–Monsky algorithm
category: math
series: han-monsky
series_part: 3
summary: A functional equation for D_k, and how it yields the Hilbert–Kunz function of a diagonal hypersurface from a few of its values.
---

We now come back to computing the Hilbert–Kunz function of a diagonal hypersurface, using the [Han–Monsky ring](han-monsky-2-the-han-monsky-ring.html). First, a useful extension of $\Gamma$:

**Definition 3.1.** *For a real number $t\geq0$ write $t=n+\vartheta$ with $n=\lfloor t\rfloor$ and $\vartheta\in[0,1)$, and set*
$$\delta_t:=(1-\vartheta)\,\delta_n+\vartheta\,\delta_{n+1}\ \in\ \Gamma_k\otimes_{\mathbb Z}\mathbb R\qquad(\delta_0=0),$$
*so that $t\mapsto\delta_t$ is the linear interpolation of $i\mapsto\delta_i$. Extend $\alpha$ $\mathbb R$-linearly. Then, for $t_1,\dots,t_n\in\mathbb Q$ put $D_k(t_1,\dots,t_n):=\alpha\big(\prod_{i=1}^n\delta_{t_i}\big)$, and for integers $r_1,\dots,r_n\geq0$ put $\ell_k(r_1,\dots,r_n):=\alpha\big(\prod_{i=1}^n\lambda_{r_i}\big)$.*

We can write out observations at the beginning as:

**Lemma 3.2** (Lemma 5.6, [HM93]). *If $a_1,\dots,a_n,d_1,\dots,d_n$ are non-negative integers, then*
$$\dim_k\left(\frac{k[x_1,\dots,x_n]}{(x_1^{a_1},\dots,x_n^{a_n},x_1^{d_1}+\dots+x_n^{d_n})}\right)=d_1\cdots d_nD_k(a_1/d_1,\dots,a_n/d_n).$$

A corollary of Monsky and Teixeira's result above is a functional equation for $\ell_k$:

**Theorem 3.3** (The $\ell$ function is $p$-multiplicative, Theorem 4.5, [HM93]). *Let $q=p^e$ for some $e\geq0$, let $k_1,\dots,k_n<q$ and $r_1,\dots,r_n\geq0$. Then,*
$$\ell_k(qr+k)=\begin{cases}\ell(r)\ell(k_1,\dots,k_n)&\text{if }\sum r_i\text{ even},\\ \ell(r)\ell(q-1-k_1,k_2,\dots,k_n)&\text{if }\sum r_i\text{ odd}.\end{cases}$$

To compute Hilbert–Kunz functions of diagonal hypersurfaces, we need to compute $D_k$, and the point is that we can also get a (more involved) functional equation for $D_k$:

**Theorem 3.4** (Theorem 4.13, [HM93]). *Let $q=p^e$ for some $e\geq0$, $u=(u_1,\dots,u_n)\in[0,q)^n$, and $r=(r_1,\dots,r_n)\in\mathbb Z^n_{\geq1}$.*
$$D(qr+u)=\begin{cases}\ell(r)D(u_1,\dots,u_n)+q^{n-1}\phi_r\left(\frac uq\right)&\sum r_i\text{ even},\\ \ell(r)D(q-u_1,u_2,\dots,u_n)+q^{n-1}\phi_r\left(\frac uq\right)&\sum r_i\text{ odd},\end{cases}$$
*where $\phi_r\in\mathbb Z[x_1,\dots,x_n]$ is the polynomial*
$$\phi_r(x)=\begin{cases}\sum_{A\subsetneq\{1,\dots,n\}}n_Ax_A&\sum r_i\text{ even}\\ \sum_{A\subsetneq\{1,\dots,n\}}n_Ax_A-\ell(r_1,\dots,r_n)\prod_{i=2}^nx_i&\sum r_i\text{ odd}\end{cases}$$
*for $n_A:=\alpha\Big(\big(\prod_{i\in A}(-1)^{r_i}\lambda_{r_i}\big)\big(\prod_{j\notin A}\delta_{r_j}\big)\Big)$ and $x_A:=\prod_{i\in A}x_i$. In other words, if $z=(z_1,\dots,z_n)\in[0,1]^n$ and $z^*=(1-z_1,\dots,z_n)$,*
$$D(p^e(r+z))=\begin{cases}\ell(r)D(qz)+q^{n-1}\phi_r(z)&\sum r_i\text{ even},\\ \ell(r)D(qz^*)+q^{n-1}\phi_r(z)&\sum r_i\text{ odd}.\end{cases}$$

The setup when you give me a diagonal hypersurface is the following: let $\beta\in\mathbb Q^n_{\geq0}$, and $p,\mu>0$ ($\mu$ has to be found!). We define the following data:

1. $r:=\lfloor\beta\rfloor$ and $z:=\beta-r\in[0,1]^s$.
2. $R:=\lfloor p^\mu\beta\rfloor$ and $z':=p^\mu\beta-R\in[0,1]^s$.
3. $t=R-p^\mu r\in\mathbb Z^s$.

Note that $\ell(R)=\ell^\sharp\ell(r)$ where if $\sum r_i$ even, $\ell^\sharp:=\ell(t)$, and if $\sum r_i$ odd, then $\ell^\sharp:=\ell(p^\mu-1-t_1,t_2,\dots,t_n)$.

**Theorem 3.5** (Theorem 5.2). *If $z'=z$ and $\sum R_i\equiv\sum r_i\pmod2$, then*
$$\frac{1}{p^{e(n-1)}}\big(D(p^{e+\mu}\beta)-\ell^\sharp D(p^e\beta)\big)$$
*is constant over $e\geq0$.*

*Proof.* This proof is the key that explains why the algorithm works. Let $q=p^e$, and let us start assuming $\sum R_i\equiv\sum r_i\equiv0\pmod2$. By the previous result, and using that $z'=z$, we have that
$$\begin{aligned}D(p^{e+\mu}\beta)-\ell^\sharp D(p^e\beta)&=D(q(R+z))-\ell^\sharp D(q(r+z))\\&=\ell(R)D(qz)+q^{n-1}\phi_R(z)-\ell^\sharp\big(\ell(r)D(qz)+q^{n-1}\phi_r(z)\big)\\&=q^{n-1}\big(\phi_R(z)-\ell^\sharp\phi_r(z)\big).\end{aligned}$$
Given that $\sum R_i$ and $\sum r_i$ have the same parity, then the term $\phi_R(z)-\ell^\sharp\phi_r(z)$ does not depend on $e$—note that the variables $R,r,z$ and $t$ only depend on $p,\beta$ and $\mu$. The same proof follows for the other parity case, noting the difference in the definitions of $\phi_r$ and $\ell^\sharp$. $\square$

For any $e$, there need not be such $\mu$, but if $e$ is large enough, there will. We will take this into account.

**Corollary 3.6.** *Let $p>0$ and $d_i\geq2$ for $i=1,\dots,n$. Then,*
$$\frac{\mathbb F_p[[x_1,\dots,x_n]]}{(x_1^{d_1}+\dots+x_n^{d_n})}$$
*and*
$$I=(x_1^{a_1},\dots,x_n^{a_n}).$$
*Set $\beta=\left(\frac{a_1}{d_1},\dots,\frac{a_n}{d_n}\right)\in\mathbb Q_{>0}$, and assume that there are some integers $e_0\geq0$ and $\mu\geq1$ such that $z'=z$ and $\sum R_i\equiv\sum r_i\pmod2$. Then, for every $e\geq e_0$,*
$$\operatorname{HK}_e\left(\frac{\mathbb F_p[[x_1,\dots,x_n]]}{(x_1^{d_1}+\dots+x_n^{d_n})},(x_1^{a_1},\dots,x_n^{a_n})\right)=Cp^{(n-1)e}+\Delta_e$$
*such that $C$ is an integer, and $\Delta_{e+\mu}=\ell^\sharp\Delta_e$.*

*Proof.* Recall that $\operatorname{HK}_e(R,I)=d_1\cdots d_nD(p^e\beta)$. Say $d=d_1\cdots d_n$. The previous theorem says that, for some constant $A$, for every $e\geq e_0$ we have that
$$\frac1d\operatorname{HK}_{e+\mu}(R,I)-\ell^\sharp\frac1d\operatorname{HK}_e(R,I)=\tilde Ap^{e(n-1)},$$
or, equivalently, setting $A=\tilde Ad$,
$$\operatorname{HK}_{e+\mu}(R,I)-\ell^\sharp\operatorname{HK}_e(R,I)=Ap^{e(n-1)}.$$
We also know by Monsky that $\operatorname{HK}_e(R,I)=Cp^{e(n-1)}+\Delta_e$ for some function $\Delta_e=O(p^{e(n-2)})$. If we plug this into the equation above, and divide by $p^{e(n-1)}$, we obtain that for all $e\geq e_0$,
$$\frac{1}{p^{e(n-1)}}\big(\Delta_{e+\mu}-\ell^\sharp\Delta_e\big)=A+\ell^\sharp C-Cp^{\mu(n-1)}.$$
Since the left side converges to 0 when $e\to\infty$, but the right side does not depend on $e$, we conclude that $\Delta_{e+\mu}=\ell^\sharp\Delta_e$, and the result follows. $\square$

## How to find $e_0$, $\mu$ and $\ell$: number theoretical input

One can always find such numbers making Corollary 3.6 work. Given any tuple of positive rationals
$$\tilde\beta:=\left(\frac{a_1}{d_1},\dots,\frac{a_n}{d_n}\right).$$
with $a_i,d_i\geq1$, we prepare some data:

1. $e_0:=\max_i\{s:p^s\mid d_i\text{ for some }i\}$,
2. $\mu=\min\{p^{k+e_0}\equiv1\pmod{d_i}\text{ for all }i\}$.

Put $\beta:=p^{e_0}\tilde\beta$. It is then easy to check the following:

**Lemma 3.7.** *With $r,z,R,z'$ defined from $\beta$ as in the setup above:*

*(a) for every multiple $\mu'$ of $\mu$ we have $z'=z$ and $R=r+(p^{\mu'}-1)\beta$;*

*(b) if $p$ is odd and $\mu=2\mu_0$, then moreover $R_i\equiv r_i\pmod2$ for every $i$, so $\sum R_i\equiv\sum r_i\pmod2$;*

*(c) if $p=2$, then for every multiple $\mu$ of $\mu_0$, $\sum_iR_i-\sum_ir_i\equiv\sum_ib_i\pmod2$.*

*In particular, you can apply 3.5.*

In the [next post](han-monsky-4-f-signature.html), we use this to compute F-signature functions.

## References

- [HM93] C. Han and P. Monsky. *Some surprising Hilbert–Kunz functions*. Mathematische Zeitschrift, 214(1):119–135, 1993. [doi:10.1007/BF02572395](https://doi.org/10.1007/BF02572395).
