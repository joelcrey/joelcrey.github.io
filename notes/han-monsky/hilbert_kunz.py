r"""
hilbert_kunz.py -- representation-ring machinery and Hilbert-Kunz algorithms (SageMath)

Load it in a Sage session or notebook (same folder) with

    load("hilbert_kunz.py")

Contents
--------
1. The Han-Monsky ring in the lambda-basis, via Yoshida's matrices   [HM93, Yos09, MT06]
       base_lambda, theta, scale, base_p_digits, lambda_matrix,
       Lambda (element class), HanMonsky(p) (factory: G = HanMonsky(3); G(4)*G(6))
2. The Han-Monsky ring Gamma_k in the delta-basis, for arbitrary k-objects   [HM93 §2, CH98 §2]
       RepresentationRing(p)  (R = RepresentationRing(5); R.delta(3) * R.lam(4))
       RepElt (element class), delta(i,p), lam(i,p), psi(N,p),
       products: *  (Han-Monsky product),  .circ()  (circle product),
       invariants: .D() (= alpha, i.e. D_F of [CH98]), .dim(), .T(q);  conversions Lambda <-> RepElt
3. The Han-Monsky algorithm for diagonal hypersurfaces   [HM93 §5]
       find_period, eHK_diagonal, HK_function_diagonal, full_HK_function_diagonal,
       F_signature_diagonal, F_signature_function_diagonal, _hk_value
4. The Chiang-Hung algorithm for  f = sum_i prod_j X_{i,j}^{d_{i,j}}   [CH98],
   for the maximal ideal or any ideal (X_{i,j}^{a_{i,j}})
       hk(p, exps, e), hk_formula(p, exps), eHK(p, exps), hk_formula_raw(p, exps), brute(p, exps, e),
       all with an optional  ideal=[[a_11, a_12, ...], ...]  for I = (X_{i,j}^{a_{i,j}})  (default: maximal ideal),
       F-signature [HL02]:  fs(p, exps, e), fs_formula(p, exps), F_signature(p, exps), fs_brute(p, exps, e),
       ChiangHung(p, t, d, A)
       (the class ChiangHung(p, t, d, A) is the recursion of [CH, p. 516], with matrices At, Gt, ...)
5. Helpers named after the objects of the notes (han_monsky.tex)
       delta_t(t, p), D_k(p, ts), ell_k(p, rs), phi_r(p, r, x), theta_index(i, p), Phi_e(i, p, e)
6. Reader-friendly interface (the polynomial is given directly):
       HK_function_diagonal(f), FS_function_diagonal(f)                      [HM93, HL02]
       HK_function_disjoint_monomials(f), FS_function_disjoint_monomials(f)  [CH98, HL02]
       HanMonskyRing(p) (= RepresentationRing(p)), x.alpha(), HK_groebner(f, e)
       e.g.  S.<x,y> = GF(2)[];  HK_function_diagonal(x^5 + y^5)

References
----------
[HM93] C. Han, P. Monsky, Some surprising Hilbert-Kunz functions, Math. Z. 214 (1993) 119-135.
[CH98] L. Chiang, Y.-C. Hung, On Hilbert-Kunz functions of some hypersurfaces,
       J. Algebra 199 (1998) 499-527.
[MT06] P. Monsky, P. Teixeira, p-Fractals and power series II, J. Algebra 304 (2006) 237-255.
[Yos09] K.-i. Yoshida, Small Hilbert-Kunz multiplicity and (A_1)-type singularity (2009).
[HL02] C. Huneke, G. Leuschke, Two theorems about maximal Cohen-Macaulay modules,
       Math. Ann. 324 (2002) 391-404.
"""
from functools import lru_cache
from math import comb, gcd
import itertools

from sage.all import (Integer, ZZ, QQ, GF, SR, PolynomialRing, matrix, identity_matrix,
                      zero_matrix, vector, euler_phi, lcm, prod, floor, numerator,
                      denominator)


# ===========================================================================
# 1. The Han-Monsky ring in the lambda-basis (Yoshida's matrix representation)
# ===========================================================================

def base_lambda(p, k):
    r"""
    Multiplication matrix of the generator ``lambda_k`` in ``Lambda_1``.

    These are the building blocks (the elements of ``Lambda_1`` in the notation of
    [HM93]); every ``lambda_k`` in higher levels is assembled from them in
    ``lambda_matrix`` below.

    Parameters
    ----------
    p : prime
        The characteristic.
    k : int
        Index of the generator, with ``0 <= k <= p - 1``.

    Returns
    -------
    A ``p x p`` integer matrix, the multiplication-by-``lambda_k`` matrix in ``Lambda_1``.

    Notes
    -----
    The ``p == 2`` case is handled separately because the general formula below
    assumes ``p`` odd.  Reference: [HM93, Section 2].
    """
    p = Integer(p)
    if k > p - 1:
        raise ValueError("k must satisfy 0 <= k <= p - 1.")
    if not p.is_prime():
        raise ValueError("p must be prime.")
    if p == 2:
        return [identity_matrix(2), matrix([[0, 1], [1, 0]])][k]

    # Build the full list of generators, then return the k-th.
    # Each row 'lij' is the indicator of an interval [j0 - i0, i0 + j0], which encodes
    # the structure constants of the representation ring (a Clebsch-Gordan-type rule).
    def indicator_row(i0, j0):
        return [1 if (j0 - i0) <= t <= (i0 + j0) else 0 for t in range(p)]

    rows = []
    for i in range(p):
        for j in range(p):
            if j >= i and i + j <= p - 1:
                rows.append(indicator_row(i, j))
            elif j - i >= 0:
                rows.append(indicator_row(p - 1 - j, p - 1 - i))
            else:
                i0, j0 = j, i
                if i0 + j0 <= p - 1:
                    rows.append(indicator_row(i0, j0))
                else:
                    rows.append(indicator_row(p - 1 - j0, p - 1 - i0))

    generators = [matrix([rows[i + p * k] for i in range(p)]).transpose()
                  for k in range(p)]
    return generators[k]


def _level_of_size(p, size):
    """The n with p^n == size (exact integer computation)."""
    n, s = 0, 1
    while s < size:
        s *= p
        n += 1
    if s != size:
        raise ValueError("matrix size %d is not a power of %d" % (size, p))
    return n


def theta(p, M0):
    r"""
    The operator ``theta : Lambda_n -> Lambda_{n+1}`` of [MT06] (Theorem 2.11 of the notes):
    ``lambda_i |-> lambda_{p i}`` if ``i`` is even, ``lambda_{p i + p - 1}`` if ``i`` is odd.

    Given the multiplication matrix ``M0`` of some ``lambda_k`` at level ``n``,
    returns the multiplication matrix of ``theta(lambda_k)`` at level ``n + 1``.
    This is the lift that encodes the genuine "magnification by p" structure of
    the representation ring (as opposed to the trivial lift ``scale`` below).
    """
    p = Integer(p)
    n = _level_of_size(p, M0.nrows())

    # Detect which lambda_k this matrix represents: the position of the leading 1
    # in the first row. Its parity drives the placement rule below.
    k = list(M0[0]).index(1)
    parity = k % 2  # 0 (even) or 1 (odd)

    M = zero_matrix(ZZ, p ** (n + 1), p ** (n + 1))
    for a in range(p):
        for i in range(p ** n):
            for j in range(p ** n):
                # Choose the target row according to the parities of i, j, k.
                if (i % 2 == 0) == (j % 2 == 0):
                    row = p * j + parity * (p - 1) + (-1) ** parity * a
                else:
                    row = p * j + (p - 1) - parity * (p - 1) + (-1) ** (1 - parity) * a
                M[row, p * i + a] = M0[j, i]
    return M


def scale(p, M0):
    r"""
    The trivial lift ``Lambda_n -> Lambda_{n+1}`` given by ``M0 |-> I_p (x) M0``.

    Tensoring on the left with the ``p x p`` identity embeds a level-``n`` matrix
    into level ``n + 1`` without altering its representation-ring content.
    """
    return identity_matrix(ZZ, Integer(p)).tensor_product(M0)


def base_p_digits(p, n, k):
    r"""
    Base-``p`` digits of ``k`` as a length-``n`` list ``[a_0, a_1, ...]``,
    so that ``k = a_0 + a_1 * p + a_2 * p^2 + ...``.  Zero-padded on the right.
    """
    digits = []
    while k > 0:
        digits.append(k % p)
        k //= p
    if n > len(digits):
        digits += [0] * (n - len(digits))
    return digits


def lambda_matrix(p, n, k):
    r"""
    Multiplication matrix of ``lambda_k`` in ``Lambda_n`` (a ``p^n x p^n`` integer matrix).

    Writes ``k`` in base ``p``; the generator for the ``i``-th digit is pushed up ``i``
    times with ``theta`` and ``n - i - 1`` times with ``scale``; the results are multiplied.
    Reference: [HM93, Section 2], [Yos09].
    """
    p = Integer(p)
    if k >= p ** n:
        raise ValueError("lambda_%d is not in Lambda_%d." % (k, n))
    digits = base_p_digits(p, n, k)
    M = identity_matrix(ZZ, p ** n)
    for i in range(n):
        Mi = base_lambda(p, digits[i])
        for _ in range(i):
            Mi = theta(p, Mi)
        for _ in range(n - i - 1):
            Mi = scale(p, Mi)
        M = M * Mi
    return M


def _min_level(p, indices):
    r"""Smallest level ``n >= 1`` with ``p^n > max(indices)``."""
    m = max(indices) if indices else 0
    n = 1
    while p ** n <= m:
        n += 1
    return n


class Lambda:
    r"""
    An element of the Han-Monsky representation ring ``Gamma`` in characteristic ``p``,
    in the lambda-basis, stored as ``{index: coefficient}``.  Products are computed with
    Yoshida's matrices at the smallest level containing all indices.

    Build generators with ``G = HanMonsky(p)`` and ``G(k)``; use ``*`` and ``+``.
    ``.to_delta()`` converts to the delta-basis element ``RepElt``.
    """

    def __init__(self, p, coeffs):
        p = Integer(p)
        if not p.is_prime():
            raise ValueError("p must be prime.")
        self.p = p
        self.coeffs = {Integer(k): c for k, c in coeffs.items() if c != 0}

    def level(self):
        """Minimal level whose basis contains all generators of this element."""
        return _min_level(self.p, list(self.coeffs) or [0])

    def matrix(self, level=None):
        r"""Multiplication matrix of this element in the lambda-basis (default: minimal level)."""
        n = self.level() if level is None else level
        if any(k >= self.p ** n for k in self.coeffs):
            raise ValueError("level %d too small for indices %s" % (n, sorted(self.coeffs)))
        M = zero_matrix(ZZ, self.p ** n, self.p ** n)
        for k, c in self.coeffs.items():
            M += c * lambda_matrix(self.p, n, k)
        return M

    def __mul__(self, other):
        if isinstance(other, Lambda):
            if self.p != other.p:
                raise ValueError("characteristic mismatch: %d vs %d" % (self.p, other.p))
            n = _min_level(self.p, list(self.coeffs) + list(other.coeffs) or [0])
            column0 = (self.matrix(n) * other.matrix(n)).column(0)
            return Lambda(self.p, {k: column0[k] for k in range(len(column0))})
        return Lambda(self.p, {k: other * c for k, c in self.coeffs.items()})

    __rmul__ = __mul__

    def __add__(self, other):
        if self.p != other.p:
            raise ValueError("characteristic mismatch: %d vs %d" % (self.p, other.p))
        out = dict(self.coeffs)
        for k, c in other.coeffs.items():
            out[k] = out.get(k, 0) + c
        return Lambda(self.p, out)

    def __neg__(self):
        return Lambda(self.p, {k: -c for k, c in self.coeffs.items()})

    def __sub__(self, other):
        return self + (-other)

    def __eq__(self, other):
        return (isinstance(other, Lambda)
                and self.p == other.p and self.coeffs == other.coeffs)

    def to_delta(self):
        """The same element as a delta-basis ``RepElt``."""
        x = RepElt({}, self.p)
        for k, c in self.coeffs.items():
            x = x + c * lam(k, self.p)
        return x

    def __repr__(self):
        if not self.coeffs:
            return "0"
        parts = []
        for k in sorted(self.coeffs):
            c = self.coeffs[k]
            parts.append(("lambda_%d" % k) if c == 1 else ("%s*lambda_%d" % (c, k)))
        return " + ".join(parts)


def HanMonsky(p):
    r"""
    The Han-Monsky ring in characteristic ``p``: returns ``G`` with ``G(k) = lambda_k``.

        G = HanMonsky(3)
        G(4) * G(6)        # level inferred to be 2
    """
    p = Integer(p)
    return lambda k: Lambda(p, {Integer(k): Integer(1)})


# ===========================================================================
# 2. The Han-Monsky ring Gamma_k in the delta-basis (arbitrary k-objects)
# ===========================================================================

def _rank_mod(M, p):
    M = [row[:] for row in M]
    r = 0
    rows = len(M)
    cols = len(M[0]) if rows else 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r


@lru_cache(maxsize=None)
def _dd(i, j, p):
    """delta_i * delta_j: Jordan type of J_i (x) 1 + 1 (x) J_j over GF(p), from the ranks of
    T^k on the graded module F[x,y]/(x^i, y^j) with T = x + y.  Returns {size: multiplicity}.
    Slow; kept only as an independent check of the fast lambda-basis product ``_ll``."""
    if i > j:
        return _dd(j, i, p)

    def rk(k):
        tot = 0
        for d in range(0, i + j - 1):
            src = [(a, d - a) for a in range(i) if 0 <= d - a < j]
            tgt = [(a, d + k - a) for a in range(i) if 0 <= d + k - a < j]
            if not src or not tgt:
                continue
            idx = {v: n for n, v in enumerate(tgt)}
            M = [[0] * len(src) for _ in tgt]
            for s, (a, b) in enumerate(src):
                for c in range(k + 1):
                    key = (a + c, b + k - c)
                    if key in idx:
                        M[idx[key]][s] = (M[idx[key]][s] + comb(k, c)) % p
            tot += _rank_mod(M, p)
        return tot

    r = [i * j] + [rk(k) for k in range(1, i + j + 1)]
    out = {}
    for s in range(1, i + j):
        m = r[s - 1] - 2 * r[s] + r[s + 1]
        if m:
            out[s] = m
    return out


def _cc(i, j):
    """circle product delta_i o delta_j = 2(delta_1+...+delta_{i-1}) + (j-i+1) delta_i  [CH, p. 509]."""
    if i > j:
        i, j = j, i
    out = {k: 2 for k in range(1, i)}
    out[i] = out.get(i, 0) + (j - i + 1)
    return out


@lru_cache(maxsize=None)
def _ll(a, b, p):
    r"""
    lambda_a * lambda_b in characteristic p, as {k: coefficient of lambda_k}.

    Exact recursion on the base-p digits, using only [CH, Prop. 2.1, Prop. 2.5]:
    with q the largest power of p not exceeding max(a, b), write a = a1 q + a0,
    b = b1 q + b0 (a0, b0 < q).  Then lambda_a = lambda_{a1 q} lambda_{a0}  (Eq. (7)), so
        lambda_a lambda_b = (lambda_{a1 q} lambda_{b1 q}) * (lambda_{a0} lambda_{b0}),
    where the first factor is given by Eq. (15), the second recursively (indices < q), and
    lambda_{mq} lambda_k = lambda_{mq+k},  lambda_{mq-1} lambda_k = lambda_{mq-1-k}  (Eqs. (7), (8)).
    Cross-checked against Jordan types computed from ranks (``_dd``).
    """
    if a > b:
        a, b = b, a
    if a == 0:
        return {b: 1}
    q = 1
    while q * p <= b:
        q *= p
    a1, a0 = divmod(a, q)
    b1, b0 = divmod(b, q)
    base = _ll(a0, b0, p) if q > 1 else {0: 1}
    cp = min(a1, b1, p - 1 - a1, p - 1 - b1)
    m0 = abs(a1 - b1)
    out = {}
    for k in range(cp + 1):                     # lambda_{(m0+2k) q} * base
        idx = (m0 + 2 * k) * q
        for j, c in base.items():
            out[idx + j] = out.get(idx + j, 0) + c
    for k in range(1, cp + 1):                  # lambda_{(m0+2k) q - 1} * base
        idx = (m0 + 2 * k) * q - 1
        for j, c in base.items():
            out[idx - j] = out.get(idx - j, 0) + c
    return {k: v for k, v in out.items() if v}


def _delta_to_lam(c):
    """delta-coefficients -> lambda-coefficients  (delta_k = sum_{i<k} (-1)^i lambda_i)."""
    out = {}
    for k, v in c.items():
        for i in range(k):
            out[i] = out.get(i, 0) + (v if i % 2 == 0 else -v)
    return {i: v for i, v in out.items() if v != 0}


def _lam_to_delta(l):
    """lambda-coefficients -> delta-coefficients  (lambda_0 = delta_1, lambda_i = (-1)^i (delta_{i+1} - delta_i))."""
    out = {}
    for i, v in l.items():
        if i == 0:
            out[1] = out.get(1, 0) + v
        else:
            s = v if i % 2 == 0 else -v
            out[i + 1] = out.get(i + 1, 0) + s
            out[i] = out.get(i, 0) - s
    return {k: v for k, v in out.items() if v != 0}


class RepElt:
    r"""
    Element of the representation ring ``Gamma_F`` (char ``p``).

    Stored internally in the lambda-basis (``self.l``); ``self.c`` gives the coefficients in the
    delta-basis, ``delta_k = [F[T]/(T^k)]``.  Construct with delta-coefficients
    ``RepElt({k: c_k}, p)`` or lambda-coefficients ``RepElt(lam={k: c_k}, p=p)``.

    ``x * y``      Han-Monsky product (tensor product, T acting as T(x)1 + 1(x)T)
    ``x.circ(y)``  circle product (T acting as T(x)T)                     [CH, p. 509]
    ``x.D()``      alpha (= D_F of [CH, p. 502]): number of Jordan blocks = dim M/TM
    ``x.dim()``    dim_F
    ``x.T(q)``     T_q: coefficient of lambda_{q-1}                          [CH, p. 506]
    ``x.lam()``    coefficients in the lambda-basis;  ``x.to_lambda()``: as a ``Lambda``
    """
    __slots__ = ("l", "p", "basis")

    def __init__(self, c=None, p=None, basis="delta", lam=None):
        if p is None:
            raise ValueError("RepElt needs the characteristic p")
        self.p = int(p)
        if lam is not None:
            self.l = {int(k): v for k, v in lam.items() if v != 0}
        else:
            self.l = _delta_to_lam({int(k): v for k, v in (c or {}).items() if v != 0})
        self.basis = basis                   # only affects how the element is printed

    @property
    def c(self):
        """Coefficients in the delta-basis."""
        return _lam_to_delta(self.l)

    def _new(self, l, basis):
        return RepElt(p=self.p, basis=basis, lam=l)

    def _check(self, o):
        if self.p != o.p:
            raise ValueError("characteristic mismatch: %d vs %d" % (self.p, o.p))

    def _b(self, o=None):
        # printed in the lambda-basis only if every operand was
        return "lambda" if self.basis == "lambda" and (o is None or o.basis == "lambda") else "delta"

    def __add__(self, o):
        self._check(o)
        l = dict(self.l)
        for k, v in o.l.items():
            l[k] = l.get(k, 0) + v
        return self._new(l, self._b(o))

    def __neg__(self):
        return self._new({k: -v for k, v in self.l.items()}, self.basis)

    def __sub__(self, o):
        return self + (-o)

    def __rmul__(self, s):
        return self._new({k: s * v for k, v in self.l.items()}, self.basis)

    def __mul__(self, o):
        if not isinstance(o, RepElt):
            return self.__rmul__(o)
        self._check(o)
        out = {}
        p = self.p
        for i, a in self.l.items():
            for j, b in o.l.items():
                ab = a * b
                for k, m in _ll(i, j, p).items():
                    out[k] = out.get(k, 0) + ab * m
        return self._new(out, self._b(o))

    def __pow__(self, n):
        n = int(n)
        if n < 0:
            raise ValueError("negative powers are not defined")
        x = self._new({0: 1}, self.basis)            # the identity lambda_0 = delta_1
        for _ in range(n):
            x = x * self
        return x

    def circ(self, o):
        self._check(o)
        c = {}
        for i, a in self.c.items():
            for j, b in o.c.items():
                for k, m in _cc(i, j).items():
                    c[k] = c.get(k, 0) + a * b * m
        return RepElt(c, self.p)

    def __eq__(self, o):
        return isinstance(o, RepElt) and self.p == o.p and (self - o).l == {}

    def __hash__(self):
        return hash((self.p, tuple(sorted(self.l.items()))))

    def __bool__(self):
        return bool(self.l)

    def alpha(self):
        """alpha(M) = dim_k M/TM, the number of Jordan blocks of T ([Notes, Definition 2.2])."""
        return self.D()

    def D(self):
        return self.l.get(0, 0)             # D_F(lambda_k) = 1 if k = 0, else 0

    def dim(self):
        return sum(v if k % 2 == 0 else -v for k, v in self.l.items())   # dim lambda_k = (-1)^k

    def lam(self):
        return dict(self.l)

    def T(self, q):
        return self.l.get(q - 1, 0)

    def in_delta(self):
        """The same element, printed in the delta-basis."""
        return self._new(self.l, "delta")

    def in_lambda(self):
        """The same element, printed in the lambda-basis."""
        return self._new(self.l, "lambda")

    def to_lambda(self):
        return Lambda(self.p, self.lam())

    def matrix(self, level=None):
        """Yoshida's integer matrix of multiplication by this element, in the basis
        lambda_0, ..., lambda_{p^n - 1} (default: smallest level n that contains it)."""
        return self.to_lambda().matrix(level)

    @staticmethod
    def _fmt(coeffs, name):
        if not coeffs:
            return "0"
        parts = []
        for k in sorted(coeffs):
            v = coeffs[k]
            parts.append(("%s_%d" % (name, k)) if v == 1 else ("-%s_%d" % (name, k)) if v == -1
                         else ("%s*%s_%d" % (v, name, k)))
        return " + ".join(parts).replace("+ -", "- ")

    def __repr__(self):
        if self.basis == "lambda":
            return self._fmt(self.l, "lambda")
        return self._fmt(self.c, "delta")


def delta(i, p):
    """delta_i = [F[T]/(T^i)] in characteristic p (delta_0 = 0)."""
    return RepElt({i: 1} if i >= 1 else {}, p)


def lam(i, p):
    """lambda_i = (-1)^i (delta_{i+1} - delta_i), lambda_0 = delta_1.  Printed in the lambda-basis."""
    return RepElt(p=p, basis="lambda", lam={int(i): 1})


class RepresentationRing:
    r"""
    The representation ring Gamma in characteristic p, for computing by hand:

        R = RepresentationRing(5)
        d, l = R.delta, R.lam
        d(3) * d(4)              # delta_2 + 2*delta_5
        l(7) * l(4)              # printed in the lambda-basis
        (d(2) + 3*l(4))^2        # sums, multiples, powers; mixed input prints in the delta-basis
        x.in_lambda(), x.in_delta(), x.matrix()
    """

    def __init__(self, p):
        p = Integer(p)
        if not p.is_prime():
            raise ValueError("p must be prime.")
        self.p = int(p)

    def delta(self, i):
        return delta(int(i), self.p)

    def lam(self, i):
        return lam(int(i), self.p)

    def one(self):
        return self.delta(1)

    def __repr__(self):
        return "Representation ring of k[T] in characteristic %d" % self.p


def psi(N, p):
    r"""
    psi(M) = class of the F-object (F^n, T = N) in Gamma, for a nilpotent square matrix ``N``
    over GF(p) (or over ZZ, reduced mod p): its Jordan type, from the ranks of N^k.
    """
    N = matrix(GF(Integer(p)), N)
    n = N.nrows()
    r = [n]
    P = identity_matrix(GF(Integer(p)), n)
    while r[-1] > 0:
        P = P * N
        r.append(P.rank())
        if len(r) > n + 2:
            raise ValueError("matrix is not nilpotent")
    r.append(0)
    c = {}
    for s in range(1, len(r) - 1):
        m = r[s - 1] - 2 * r[s] + r[s + 1]
        if m:
            c[s] = m
    return RepElt(c, p)


# ===========================================================================
# 3. The Han-Monsky algorithm for diagonal hypersurfaces  [HM93, §5]
# ===========================================================================

def find_period(p, exps, ideal=None, verbose=False, talk=False):
    r"""
    Find the period ``mu`` and threshold ``e0`` for the Han-Monsky algorithm.

    Implements the search of [HM93, Section 5]: it normalises ``beta = (a_i/d_i)``
    so that no denominator is divisible by ``p`` (this defines ``e0``), then finds
    the least ``mu`` for which the magnified vector ``p^mu * beta`` returns to the
    same sign-equivalence class as ``beta``, with a matching parity condition.

    Parameters
    ----------
    p : prime
    exps : list of int (d_1,...,d_s)   -- hypersurface x_1^d_1+...+x_s^d_s
    ideal : list of int (a_1,...,a_s)  -- m-primary ideal (x_1^a_1,...,x_s^a_s); default all 1
    verbose : bool                     -- print intermediate quantities
    talk : bool                        -- return a sentence instead of the tuple

    Returns
    -------
    (mu, e0, new_beta)
    """
    p = Integer(p)
    exps = [Integer(d) for d in exps]
    ideal = [Integer(1)] * len(exps) if ideal is None else [Integer(a) for a in ideal]

    beta = vector([ideal[i] / exps[i] for i in range(len(exps))])

    # Step 1: strip p from the denominators to find e0.
    e0 = 0
    for d in exps:
        while d % p ** (e0 + 1) == 0:
            e0 += 1
    new_beta = p ** e0 * beta
    fracs = [(numerator(x), denominator(x)) for x in new_beta]
    r = vector([int(x) for x in new_beta])

    # The two sign-equivalence classes (product of signs +1 vs -1) of [HM93, Sec 5].
    units = list(itertools.product([1, -1], repeat=len(exps)))
    class_z = [[u[i] * fracs[i][0] % fracs[i][1] for i in range(len(exps))]
               for u in units if prod(u) == 1]
    class_z_star = [[u[i] * fracs[i][0] % fracs[i][1] for i in range(len(exps))]
                    for u in units if prod(u) == -1]

    # Step 2: try mu = 1, 2, ... up to the a-priori bound max_mu.
    max_mu = lcm([euler_phi(den) for (_, den) in fracs])
    if verbose:
        print("Maximum mu:", max_mu)

    def matches(mu):
        z_prime = [p ** mu * num % den for (num, den) in fracs]
        R = [int(x) for x in p ** mu * new_beta]
        same_parity = (sum(R) % 2 == sum(r) % 2)
        in_z = z_prime in class_z
        in_z_star = z_prime in class_z_star
        if verbose:
            print("mu=%d  z'=%s  z~z'=%s  z*~z'=%s  parity=%s"
                  % (mu, z_prime, in_z, in_z_star, same_parity))
        return (in_z and same_parity) or (in_z_star and not same_parity)

    mu = 1
    while not matches(mu) and mu < max_mu:
        mu += 1
    if talk:
        return 'Period mu = ' + str(mu) + ', e0 = ' + str(e0)
    return mu, e0, new_beta


def _hk_value(p, exps, ideal, e):
    r"""
    Brute-force value of the Hilbert-Kunz function at level ``e``:

        dim_{F_p}  F_p[x]/( sum x_i^{d_i},  x_1^{a_1 p^e}, ..., x_s^{a_s p^e} ),

    computed as an ``F_p``-vector-space dimension (Groebner basis).
    """
    p = Integer(p)
    if ideal is None:
        ideal = len(exps) * [1]
    s = len(exps)
    ring = PolynomialRing(GF(p), s, 'x')
    xs = ring.gens()
    hypersurface = sum(xs[i] ** exps[i] for i in range(s))
    frobenius = [xs[i] ** (ideal[i] * p ** e) for i in range(s)]
    return ring.ideal([hypersurface] + frobenius).vector_space_dimension()


def eHK_diagonal(p, exps, ideal=None, verbose=False,
                 return_HK_function=False, full_HK_function=False, _data=False):
    r"""
    Hilbert-Kunz multiplicity (or function) of a diagonal hypersurface via [HM93].

        R = F_p[x_1,...,x_s] / (x_1^{d_1} + ... + x_s^{d_s})

    Needs two explicit values of the Hilbert-Kunz function (``_hk_value``) and the
    magnification number ``lsh`` = ``l#`` (from the level-``mu`` lambda matrices).

    Parameters
    ----------
    p : prime
    exps : list of int (d_1,...,d_s)
    ideal : list of int (a_1,...,a_s), default all 1
    verbose : bool
    return_HK_function : bool
        If True, return a string giving the Hilbert-Kunz *function*.  When ``mu > 1``
        the identity only holds along the residue class ``e mod mu`` (``HK_(mu e) = ...``).
    full_HK_function : bool
        If True (and ``return_HK_function`` True), give all ``mu`` residue classes.
    """
    p = Integer(p)
    exps = [Integer(d) for d in exps]
    ideal = [Integer(1)] * len(exps) if ideal is None else [Integer(a) for a in ideal]
    if verbose:
        print("Original beta:", vector([1 / d for d in exps]))

    mu, e0, beta = find_period(p, exps, ideal)
    if verbose:
        print("mu =", mu, ", e0 =", e0, ", new beta =", beta)

    dim = len(exps) - 1
    r = vector([floor(x) for x in beta])
    z = beta - r
    t = vector([floor(x) for x in p ** mu * z])

    if verbose:
        print("sum(r) odd:", sum(r) % 2 != 0, "(sum r =", sum(r), ")")
    if sum(r) % 2 != 0:
        t[0] = p ** mu - 1 - t[0]

    # l# (lsh): the magnification number, from the level-mu lambda matrices.
    lsh = prod(lambda_matrix(p, mu, ti) for ti in t)[0, 0]
    if verbose:
        print("t-vector =", t, " so l# =", lsh)

    # Two explicit Hilbert-Kunz values, then solve the 2x2 linear system.
    HKe0 = _hk_value(p, exps, ideal, e0)
    HKe0mu = _hk_value(p, exps, ideal, e0 + mu)

    eHK = (HKe0mu - HKe0 * lsh) / ((p ** (mu * dim) - lsh) * p ** (e0 * dim))

    if _data:
        Deltas = [eHK * p ** ((e0 + k) * dim) - _hk_value(p, exps, ideal, e0 + k) for k in range(mu)]
        return dict(eHK=eHK, lsh=lsh, mu=mu, e0=e0, dim=dim, Deltas=Deltas)
    if not return_HK_function:
        return eHK

    # --- function-valued output ---
    e = SR.var('e')
    if not full_HK_function:
        Delta = eHK * p ** (e0 * dim) - HKe0
        return ('HK_(%se) = %s - %s  for e >= %s'
                % (mu, eHK * p ** (dim * (mu * e)), Delta * lsh ** e, e0))

    Deltas = [eHK * p ** ((e0 + k) * dim) - _hk_value(p, exps, ideal, e0 + k)
              for k in range(mu)]
    if len(Deltas) == 1:
        pieces = "%s for all e" % Deltas[0]
    else:
        m = SR.var('m')
        pieces = ", ".join("%s for e = %s" % (Deltas[i], mu * m + i)
                           for i in range(len(Deltas)))
    if mu > 1:
        if e0 > 0:
            return ('%s - Delta_(e-%s) * %s^floor((e-%s)/%s)  for e >= %s,  where Delta_e is %s'
                    % (eHK * p ** (dim * e), e0, lsh, e0, mu, e0, pieces))
        return ('%s - Delta_e * %s^floor(e/%s)  for e >= %s,  where Delta_e is %s'
                % (eHK * p ** (dim * e), lsh, mu, e0, pieces))
    if e0 > 0:
        return ('%s - Delta_(e-%s) * %s^(e-%s)  for e >= %s,  where Delta_e is %s'
                % (eHK * p ** (dim * e), e0, lsh, e0, e0, pieces))
    return ('%s - Delta_e * %s^e  for e >= %s,  where Delta_e is %s'
            % (eHK * p ** (dim * e), lsh, e0, pieces))


def HK_function_diagonal(p, exps, ideal=None, verbose=False):
    """Hilbert-Kunz function (one residue class) of the diagonal hypersurface."""
    return eHK_diagonal(p, exps, ideal, verbose, return_HK_function=True)


def full_HK_function_diagonal(p, exps, ideal=None, verbose=False):
    """Full Hilbert-Kunz function (all residue classes) of the diagonal hypersurface."""
    return eHK_diagonal(p, exps, ideal, verbose,
                        return_HK_function=True, full_HK_function=True)


def _socle_ideal_diagonal(exps):
    """[HL02]: with x_j a variable of smallest exponent d_j, I = (x_i : i != j) is a parameter
    ideal (a minimal reduction of m), l(R/I) = d_j = e(R), the socle of R/I is x_j^{d_j - 1},
    and I + (u) = (x_i : i != j) + (x_j^{d_j - 1}).  Returns (d_j, exponents of I + (u))."""
    j = min(range(len(exps)), key=lambda i: exps[i])
    I_delta = [1] * len(exps)
    I_delta[j] = exps[j] - 1
    return exps[j], I_delta


def F_signature_diagonal(p, exps, verbose=False):
    """F-signature of the diagonal hypersurface:  s(R) = e(R) - e_HK(I + (u))  [HL02], with
    I = (x_i : i != j) for a variable x_j of smallest exponent (see _socle_ideal_diagonal)."""
    exps = [Integer(d) for d in exps]
    dj, I_delta = _socle_ideal_diagonal(exps)
    if dj == 1:
        return Integer(1)                       # x_j appears linearly: R is regular
    return dj - eHK_diagonal(p, exps, I_delta, verbose)


def F_signature_function_diagonal(p, exps, verbose=False):
    """F-signature function  FS_e = e(R) q^dim - HK_e(I + (u))  [HL02] of the diagonal
    hypersurface, as a string in the style of full_HK_function_diagonal."""
    p = Integer(p)
    exps = [Integer(d) for d in exps]
    dj, I_delta = _socle_ideal_diagonal(exps)
    dim = len(exps) - 1
    e = SR.var('e')
    if dj == 1:
        return '%s  for e >= 0  (R is regular)' % (p ** (dim * e))
    D = eHK_diagonal(p, exps, I_delta, verbose, _data=True)
    s_ = dj - D['eHK']
    mu, e0, lsh, Deltas = D['mu'], D['e0'], D['lsh'], D['Deltas']
    if len(Deltas) == 1:
        pieces = "%s for all e" % Deltas[0]
    else:
        m = SR.var('m')
        pieces = ", ".join("%s for e = %s" % (Deltas[i], mu * m + i) for i in range(len(Deltas)))
    lead = s_ * p ** (dim * e)
    if mu > 1:
        if e0 > 0:
            return ('%s + Delta_(e-%s) * %s^floor((e-%s)/%s)  for e >= %s,  where Delta_e is %s'
                    % (lead, e0, lsh, e0, mu, e0, pieces))
        return ('%s + Delta_e * %s^floor(e/%s)  for e >= %s,  where Delta_e is %s'
                % (lead, lsh, mu, e0, pieces))
    if e0 > 0:
        return ('%s + Delta_(e-%s) * %s^(e-%s)  for e >= %s,  where Delta_e is %s'
                % (lead, e0, lsh, e0, e0, pieces))
    return ('%s + Delta_e * %s^e  for e >= %s,  where Delta_e is %s' % (lead, lsh, e0, pieces))


# ===========================================================================
# 4. The Chiang-Hung algorithm  [CH98]
# ===========================================================================

def _clean(p, exps):
    return int(p), [[int(x) for x in e] for e in exps]


def _K(x, r, d, t, p):
    """K_i(x) [CH, p. 512] = psi of F[X_1..X_t]/(X^(r+x d)) with T = (X_1...X_t)^d."""
    if x == 0:
        return r ** t * lam(0, p)
    e = r ** t * (-1) ** x * lam(x, p) + ((r + d) ** t - r ** t) * delta(x, p)
    for j in range(1, x):
        e = e + (-2 * (r + j * d) ** t + (r + (j + 1) * d) ** t + (r + (j - 1) * d) ** t) * delta(x - j, p)
    return e


def _Dl(l, q, p):
    """D^l(q) [CH, p. 505] = delta_q o ... o delta_q (l times)."""
    e = delta(q, p)
    for j in range(1, q):
        e = e + (-2 * j ** l + (j + 1) ** l + (j - 1) ** l) * delta(q - j, p)
    return e


class ChiangHung:
    r"""
    The recursion of [CH98] for  f = sum_i (X_{i,1} ... X_{i,t_i})^{d_i}   (equal exponents
    inside each monomial, [CH, Eq. (1)]).

    ``J``           the index set (0* is encoded as -1), in the linear order of [CH, p. 513]
    ``b(i, mu)``    p-adic digits of 1/d_i;   ``pm(i, mu)`` = p^mu mod d_i
    ``At(mu)``      the integer matrix tilde A(mu)        [CH, p. 516]
    ``Gt(mu)``      the integer vector tilde Gamma(mu)    [CH, p. 516]
    ``vbase(n)``    tilde v(n, n) (start of the recursion)
    ``run(n, stop)``tilde v(n, stop) via  v(n,mu) = A(mu) v(n,mu+1) + p^{a(n-mu)} Gamma(mu)
    ``hk(n)``       e_n;   ``direct(n)``: e_n computed directly in Gamma (small n only)
    ``period()``    (rho, omega);   ``formula()``: closed form [CH, p. 517]
    """

    def __init__(self, p, t, d, A=None):
        p, t, d = int(p), [int(x) for x in t], [int(x) for x in d]
        self.p, self.t, self.d, self.m = p, list(t), list(d), len(t)
        # ideal powers: monomial i is computed modulo (X_{i,j}^{A_i q})_j   (A_i = 1: the maximal ideal)
        self.ipow = [1] * len(t) if A is None else [int(x) for x in A]
        self.a = sum(t) - 1
        self.I = [[-1] + list(range(ti)) for ti in t]          # -1 stands for 0*
        allI = list(itertools.product(*self.I))
        self.notJ = [x for x in allI if any(x[i] == t[i] - 1 for i in range(self.m))]
        self.J = sorted([x for x in allI if x not in self.notJ], key=self._key)
        self._cacheA, self._cacheG = {}, {}

    def __repr__(self):
        mon = " + ".join("(%s)^%d" % ("".join("X%d%d" % (i + 1, j + 1) for j in range(ti)), di)
                         if ti > 1 else "X%d1^%d" % (i + 1, di)
                         for i, (ti, di) in enumerate(zip(self.t, self.d)))
        out = "Chiang-Hung recursion for f = %s over GF(%d)" % (mon, self.p)
        if any(x != 1 for x in self.ipow):
            out += ", ideal powers A = %s" % self.ipow
        return out

    def _key(self, sig):                                          # linear order, p. 513
        k = []
        for j in [-1] + list(range(max(self.t))):
            S = [i + 1 for i in range(self.m) if sig[i] == j]
            k.append((-len(S), S))
        return k

    def b(self, i, mu):
        """mu-th p-adic digit of A_i/d_i (mu = 0: the integer part, which may exceed p - 1)."""
        Ai = self.ipow[i]
        return Ai // self.d[i] if mu == 0 else (Ai * self.p ** mu // self.d[i]) % self.p

    def pm(self, i, mu):
        """A_i p^mu mod d_i  (= p^mu mod d_i for the maximal ideal)."""
        return (self.ipow[i] * self.p ** mu) % self.d[i]

    def state(self, mu):
        return tuple((self.b(i, mu), self.pm(i, mu)) for i in range(self.m))

    def G0(self, q):
        p = self.p
        if q % 2 == 0:                       # only for p = 2
            return lam(q, p) + lam(0, p)
        e = RepElt({}, p)
        for k in range(p):
            e = e + (-1) ** (p - 1 - k) * lam(k * q, p)
        return (-1) ** ((p - 1) * q) * e

    def Gel(self, e, l, q):
        p = self.p
        x = RepElt({}, p)
        for k in range(1, p):
            x = x + (k ** l * (-1) ** ((p - 1 - k) * q)) * lam((p - 1 - k) * q, p)
        return comb(e, l) * x

    def L(self, i, l, mu, q):
        p, ti, di, bi = self.p, self.t[i], self.d[i], self.b(i, mu)
        x = RepElt({}, p)
        for k in range(1, bi + 1):
            x = x + (di ** (ti - l) * (self.pm(i, mu) + (k - 1) * di) ** l
                     * (-1) ** ((bi - k) * q)) * lam((bi - k) * q, p)
        return comb(ti, l) * x

    def _coef(self, i, si, ni, mu, q):
        p, ti = self.p, self.t[i]
        if si == -1:
            if ni == -1:
                bq = self.b(i, mu) * q
                return (-1) ** bq * lam(bq, p)
            return self.L(i, ni, mu, q)
        if ni == -1 or ni < si:
            return None
        if ni == si:
            return p ** si * self.G0(q)
        return p ** si * self.Gel(ti - si, ni - si, q)

    def A(self, sig, nu, mu, q):
        """A_{sigma,nu}(mu) in Gamma  [CH, p. 514]."""
        x = lam(0, self.p)
        for i in range(self.m):
            c = self._coef(i, sig[i], nu[i], mu, q)
            if c is None:
                return RepElt({}, self.p)
            x = x * c
        return x

    def W(self, A, q):
        """W_q(A)  [CH, p. 505]."""
        u, p = A.lam(), self.p
        return [[u.get((p - 1) * q, 0), u.get(p * q - 1, 0)],
                [u.get(q - 1, 0), u.get(0, 0)]]

    def At(self, mu):
        st = self.state(mu)
        if st not in self._cacheA:
            q, n = self.p, len(self.J)
            M = [[0] * (2 * n) for _ in range(2 * n)]
            for a_, sig in enumerate(self.J):
                for b_, nu in enumerate(self.J):
                    w = self.W(self.A(sig, nu, mu, q), q)
                    for x in range(2):
                        for y in range(2):
                            M[2 * a_ + x][2 * b_ + y] = w[x][y]
            self._cacheA[st] = M
        return self._cacheA[st]

    def Gt(self, mu):
        st = self.state(mu)
        if st not in self._cacheG:
            q, out = self.p, []
            for sig in self.J:
                x = RepElt({}, self.p)
                for nu in self.notJ:
                    A = self.A(sig, nu, mu, q)
                    if not A.l:
                        continue
                    w = 1
                    for i in range(self.m):
                        if nu[i] == -1:
                            w *= self.pm(i, mu) ** self.t[i]
                    x = x + w * (A * delta(q, self.p))
                out += [x.T(self.p * q), x.D()]
            self._cacheG[st] = out
        return self._cacheG[st]

    def vbase(self, n):
        p, out = self.p, []
        for sig in self.J:
            x = lam(0, p)
            for i in range(self.m):
                if sig[i] == -1:
                    x = x * _K(self.b(i, n), self.ipow[i] * p ** n % self.d[i], self.d[i], self.t[i], p)
                else:
                    x = x * (p ** sig[i] * _Dl(self.t[i] - sig[i], p, p))
            out += [x.T(p), x.D()]
        return out

    def run(self, n, stop=0):
        v = self.vbase(n)
        for mu in range(n - 1, stop - 1, -1):
            A, Gm = self.At(mu), self.Gt(mu)
            v = [sum(A[r][c] * v[c] for c in range(len(v))) + self.p ** (self.a * (n - mu)) * Gm[r]
                 for r in range(len(v))]
        return v

    def hk(self, n):
        return self.run(int(n))[1]

    def direct(self, n):
        p = self.p
        x, Q = lam(0, p), p ** int(n)
        for i in range(self.m):
            Qi = self.ipow[i] * Q
            x = x * _K(Qi // self.d[i], Qi % self.d[i], self.d[i], self.t[i], p)
        return x.D()

    def period(self):
        seen, mu = {}, 1
        while True:
            key = tuple(Ai * self.p ** (mu - 1) % di for Ai, di in zip(self.ipow, self.d))
            if key in seen:
                mu1 = seen[key]
                return mu1 - 1, mu - mu1
            seen[key] = mu
            mu += 1

    def formula_sympy(self):
        """Closed form via sympy's Jordan form (slow reference implementation of ``formula``)."""
        import sympy as sp
        p, a = int(self.p), int(self.a)
        rho, omega = (int(x) for x in self.period())
        N = 2 * len(self.J)
        Am = lambda mu: sp.Matrix(self.At(mu))
        Gm = lambda mu: sp.Matrix(self.Gt(mu))
        C, b = sp.eye(N), sp.zeros(N, 1)
        for k in range(rho + 1):
            b += sp.Integer(p) ** (a * (rho - k)) * C * Gm(k)
            C = C * Am(k)
        B, v = sp.eye(N), sp.zeros(N, 1)
        for k in range(1, omega + 1):
            v += sp.Integer(p) ** (a * (omega - k)) * B * Gm(rho + k)
            B = B * Am(rho + k)
        u = sp.Integer(p) ** a * (sp.Integer(p) ** (a * omega) * sp.eye(N) - B).inv() * v
        z = sp.Integer(p) ** (-a * (rho + 1)) * C * u + sp.Integer(p) ** (-a * rho) * b
        n = sp.Symbol('n', integer=True, positive=True)
        Pm, Jd = B.jordan_form()
        Pinv = Pm.inv()
        out = {}
        for kappa in range(omega):
            nk = rho + 1 + kappa
            Phi = sp.Matrix(self.run(nk, stop=nk - kappa)) - sp.Integer(p) ** (a * kappa) * u
            tau = (n - rho - 1 - kappa) / omega
            kk = sp.Symbol('kk', integer=True, nonnegative=True)
            Jk = Jd ** kk
            if not isinstance(Jk, sp.MatrixBase):
                Jk = Jk.as_explicit()
            expr = (C * Pm * Jk * Pinv * Phi)[1].subs(kk, tau) + (sp.Integer(p) ** (sp.Integer(a) * n) * z)[1]
            expr = sp.expand(sp.powsimp(sp.expand(expr), force=True))
            expr = expr.replace(lambda x: x.is_Pow and x.base == 0, lambda x: sp.Integer(0))
            expr = expr.replace(lambda x: isinstance(x, sp.KroneckerDelta), lambda x: sp.Integer(0))
            out[kappa] = sp.nsimplify(expr)
        n0 = rho + 1
        if any(Jd[i, i] == 0 for i in range(N)) or any(f.has(sp.KroneckerDelta) for f in out.values()):
            n0 += omega * N
        return n0, omega, out

    def _closed_form_data(self):
        """The rational data of [CH, p. 517]: C, B~, u, z (Sage matrices/vectors over QQ)."""
        p, a = int(self.p), int(self.a)
        rho, omega = (int(x) for x in self.period())
        N = 2 * len(self.J)
        P = QQ(p)
        A = lambda mu: matrix(QQ, self.At(mu))
        Gv = lambda mu: vector(QQ, self.Gt(mu))
        C, b = identity_matrix(QQ, N), vector(QQ, [0] * N)
        for k in range(rho + 1):
            b += P ** (a * (rho - k)) * (C * Gv(k))
            C = C * A(k)
        B, v = identity_matrix(QQ, N), vector(QQ, [0] * N)
        for k in range(1, omega + 1):
            v += P ** (a * (omega - k)) * (B * Gv(rho + k))
            B = B * A(rho + k)
        u = P ** a * (P ** (a * omega) * identity_matrix(QQ, N) - B).solve_right(v)
        z = P ** (-a * (rho + 1)) * (C * u) + P ** (-a * rho) * b
        return C, B, u, z

    def eHK(self):
        """The Hilbert-Kunz multiplicity: the coefficient of p^{a n} [CH, p. 517] (exact)."""
        return self._closed_form_data()[3][1]

    def formula(self):
        r"""
        Closed form [CH, p. 517]: (n0, omega, {kappa: sympy expr in n}).

        With tau = (n - rho - 1 - kappa)/omega,  tilde v(n, 0) = C B^tau Phi + p^{a n} z.
        The sequence  s(tau) = (row 2 of C) B^tau Phi  is split along the generalized eigenspaces
        ker g(B)^m of the irreducible factors g^m of the characteristic polynomial of B (exact
        rational linear algebra).  On each piece  s_g(tau) = sum_{roots r of g} P_r(tau) r^tau
        with deg P_r < m, fitted from deg(g)*m values of s_g; only these small systems involve
        algebraic numbers.  Eigenvalue 0 only contributes for small n (handled through n0).
        """
        import sympy as sp
        p, a = int(self.p), int(self.a)
        rho, omega = (int(x) for x in self.period())
        N = 2 * len(self.J)
        P = QQ(p)
        C, B, u, z = self._closed_form_data()
        w = C.row(1)

        # generalized eigenspaces over QQ
        x = PolynomialRing(QQ, 'x').gen()
        blocks, cols = [], []
        for g, m in B.charpoly().factor():
            K = (g(B) ** m).right_kernel_matrix().transpose()
            blocks.append((g, m, K.ncols()))
            cols.append(K)
        Kall = cols[0]
        for K in cols[1:]:
            Kall = Kall.augment(K)
        has_zero = any(g == x for g, _, _ in blocks)

        q = lambda t: sp.Rational(int(t.numerator()), int(t.denominator()))
        n = sp.Symbol('n', integer=True, positive=True)
        kk = sp.Symbol('kk', integer=True, nonnegative=True)
        roots_cache = {}
        out = {}
        for kappa in range(omega):
            nk = rho + 1 + kappa
            Phi = vector(QQ, self.run(nk, stop=nk - kappa)) - P ** (a * kappa) * u
            coords = Kall.solve_right(Phi)
            expr = sp.Integer(0)
            pos = 0
            for (g, m, d), K in zip(blocks, cols):
                yg = K * coords[pos:pos + d]
                pos += d
                if g == x:
                    continue                       # eigenvalue 0: no contribution for large n
                vals, y = [], yg
                for _ in range(d):
                    vals.append(w * y)
                    y = B * y
                if all(t == 0 for t in vals):
                    continue
                if g not in roots_cache:
                    gs = sp.Poly([q(c) for c in reversed(g.list())], sp.Symbol('x'))
                    roots_cache[g] = sp.roots(gs, multiple=True) or list(sp.Poly(gs).all_roots())
                rts = roots_cache[g]
                if g.degree() == 1:
                    lam0 = -q(g[0]) / q(g[1])
                    # P(tau) lam0^tau with deg P < m: fit P from its values at tau = 0..m-1
                    M = sp.Matrix(m, m, lambda t, j: sp.Integer(t) ** j)
                    cvec = M.LUsolve(sp.Matrix([q(vals[t]) / lam0 ** t for t in range(m)]))
                    expr += sum(cvec[j] * kk ** j for j in range(m)) * lam0 ** kk
                else:
                    terms = [(r, j) for r in rts for j in range(m)]
                    M = sp.Matrix(d, d, lambda t, c: sp.Integer(t) ** terms[c][1] * terms[c][0] ** t)
                    cvec = M.LUsolve(sp.Matrix([q(t) for t in vals]))
                    expr += sum(_exact(cvec[c]) * kk ** terms[c][1] * terms[c][0] ** kk
                                for c in range(d))
            tau = (n - rho - 1 - kappa) / omega
            expr = expr.subs(kk, tau) + sp.Integer(p) ** (sp.Integer(a) * n) * q(z[1])
            expr = sp.expand(sp.powsimp(sp.expand(expr), force=True))
            out[kappa] = expr
        n0 = rho + 1
        if has_zero:
            n0 += omega * N
        return n0, omega, out


def _clean_ideal(exps, ideal):
    """The ideal exponents in the same nested shape as ``exps``.  ``ideal`` may be None (the
    maximal ideal), a nested list like ``exps``, or a flat list with one entry per variable."""
    if ideal is None:
        return [[1] * len(e) for e in exps]
    ideal = list(ideal)
    if all(not isinstance(x, (list, tuple)) for x in ideal):
        flat = [int(x) for x in ideal]
        if len(flat) != sum(len(e) for e in exps):
            raise ValueError("the ideal needs one exponent per variable")
        out, pos = [], 0
        for e in exps:
            out.append(flat[pos:pos + len(e)])
            pos += len(e)
        return out
    out = [[int(x) for x in a] for a in ideal]
    if [len(a) for a in out] != [len(e) for e in exps]:
        raise ValueError("the ideal must have the same shape as exps")
    return out


def _reduce(exps, ideal=None):
    r"""
    Step A [CH, Eq. (21), Corollary 1], for the ideal (X_{i,j}^{a_{i,j}}):

        e_n(f) = sum_terms  coef * p^{k n} * e_n(f_term),

    where in each f_term every monomial has equal exponents d_i and an equal ideal power A_i.
    Returns a list of (coef in QQ, k, t, d, A).

    Monomial i only enters through  N_i(L) = prod_j (a_{i,j} q - L d_{i,j})^+  (the number of
    basis monomials m with m and T^L m both nonzero), on which its class in Gamma depends
    linearly.  Hence (a_j, d_j) -> (c a_j, c d_j) multiplies the class by c, which brings all
    a_{i,j} to A_i = lcm_j a_{i,j}; then  (Aq - L d_j)^+ (Aq - L D)^+ =
    (d_j/D) ((Aq - L D)^+)^2 + A q (1 - d_j/D) (Aq - L D)^+  for d_j <= D is Eq. (21).
    """
    ideal = _clean_ideal(exps, ideal)
    per = []
    for e, a in zip(exps, ideal):
        A = 1
        for x in a:
            A = A * x // gcd(A, x)
        scale = QQ(1)
        dd = []
        for ej, aj in zip(e, a):
            scale *= QQ(aj) / A
            dd.append(ej * (A // aj))
        dd.sort(reverse=True)
        D = dd[0]
        poly = {0: QQ(1)}
        for dj in dd[1:]:
            new = {}
            for k, c in poly.items():
                new[k] = new.get(k, 0) + c * QQ(dj) / D
                new[k + 1] = new.get(k + 1, 0) + c * (1 - QQ(dj) / D) * A
            poly = new
        terms = []
        for k, c in poly.items():
            if c == 0:
                continue
            s_, A_, D_ = len(e) - k, A, D
            g = gcd(A_, D_)                       # (gA, gD) -> (A, D): class multiplied by g^s
            terms.append((scale * c * g ** s_, k, s_, D_ // g, A_ // g))
        per.append(terms)
    out = []
    for choice in itertools.product(*per):
        coef = QQ(1)
        for c, _, _, _, _ in choice:
            coef *= c
        out.append((coef, sum(x[1] for x in choice), [x[2] for x in choice],
                    [x[3] for x in choice], [x[4] for x in choice]))
    return out


def hk(p, exps, n, ideal=None):
    """e_n(f, I) = dim_F F[X]/(I^{[p^n]}, f), for f given by exponent lists (one list per
    monomial) and I = (X^{a}) given by ``ideal`` (default: the maximal ideal)."""
    p, exps = _clean(p, exps)
    n = int(n)
    tot = QQ(0)
    for coef, k, t, d, A in _reduce(exps, ideal):
        tot += coef * p ** (k * n) * int(ChiangHung(p, t, d, A).hk(n))
    assert tot.denominator() == 1
    return Integer(tot)


def eHK(p, exps, ideal=None):
    """Hilbert-Kunz multiplicity of f with respect to I = (X^{a}) (default: the maximal ideal),
    exact; no eigenvalues needed.  Every Step-A term contributes: the term with p^{k n} has
    one variable less per unit of k, so p^{k n} * p^{(a - k) n} = p^{a n}."""
    p, exps = _clean(p, exps)
    return sum(coef * ChiangHung(p, t, d, A).eHK() for coef, k, t, d, A in _reduce(exps, ideal))


def hk_formula_raw(p, exps, ideal=None):
    """Closed form as data: (n0, period, {r: sympy expr in n}), valid for n >= n0 and
    n = n0 + r (mod period); n0 is a safe (possibly too large) bound."""
    import sympy as sp
    p, exps = _clean(p, exps)
    n = sp.Symbol('n', integer=True, positive=True)
    parts = []
    for coef, k, t, d, A in _reduce(exps, ideal):
        n0, om, fs = ChiangHung(p, t, d, A).formula()
        parts.append((sp.Rational(int(coef.numerator()), int(coef.denominator())), k, n0, om, fs))
    N0 = max(x[2] for x in parts)
    L = 1
    for x in parts:
        L = L * x[3] // gcd(L, x[3])
    res = {}
    for r in range(L):
        nn = N0 + r
        e = sp.Integer(0)
        for coeff, k, n0, om, fs in parts:
            e += coeff * sp.Integer(p) ** (sp.Integer(int(k)) * n) * fs[(nn - n0) % om]
        res[r] = sp.expand(sp.powsimp(sp.expand(e), force=True))
    for L2 in range(1, L + 1):
        if L % L2 == 0 and all(sp.simplify(res[r] - res[r % L2]) == 0 for r in range(L)):
            res, L = {r: res[r] for r in range(L2)}, L2
            break
    return N0, L, res


def _exact(x):
    """Exact simplification of an algebraic expression (never numerical: sympy's nsimplify
    evaluates numbers in floating point and guesses closed forms, so it is not used)."""
    import sympy as sp
    x = sp.expand(sp.radsimp(sp.expand(x)))
    if x.is_number and not x.is_Rational:
        x = sp.simplify(x)
    return x


def _split_terms(expr, n):
    import sympy as sp
    out = {}
    for term in sp.Add.make_args(sp.expand(sp.powsimp(sp.expand(expr), force=True))):
        coef, dep = term.as_independent(n, as_Add=False)
        base, poly = sp.Integer(1), sp.Integer(1)
        for fac, ex in dep.as_powers_dict().items():
            if fac == n:
                poly *= n ** ex
            elif fac.is_Pow or ex.has(n):
                m = sp.simplify(ex / n)
                base *= fac ** m
            else:
                coef *= fac ** ex
        base = _exact(base)
        out[base] = out.get(base, sp.Integer(0)) + coef * poly
    return out


def _base_str(b, p, var):
    """How a base is printed: b -> 'b^e' (powers of p as 'p^(k*e)');
    ('root', k, m) -> 'm^floor(e/k)'  (an irrational base whose k-th power m is rational)."""
    if isinstance(b, tuple):
        return "%s^floor(%s/%d)" % (b[2], var, b[1])
    if b == 1:
        return None
    if b < 0:
        return "(%s)^%s" % (b, var)
    k, x = 0, b
    while x % p == 0:
        x, k = x // p, k + 1
    if x == 1:
        return "%d^%s" % (p, var) if k == 1 else "%d^(%d*%s)" % (p, k, var)
    return "%s^%s" % (b, var)


def _base_size(b):
    import sympy as sp
    if isinstance(b, tuple):
        return float(sp.Abs(b[2])) ** (1.0 / b[1])
    return float(sp.Abs(b))


def _root_order(b, kmax=24):
    """Smallest k >= 1 with b^k rational (None if there is none up to kmax)."""
    import sympy as sp
    for k in range(1, kmax + 1):
        if _exact(b ** k).is_rational:
            return k
    return None


def _rationalize(split, L, N0):
    """Irrational bases b with b^k rational for some k (e.g. +-sqrt(3), 5*99^(1/3), complex
    roots of unity times these) are rewritten with  b^e = b^(e mod k) * (b^k)^floor(e/k):
    the key becomes ('root', k, b^k) and the coefficient absorbs b^(e mod k), which is
    determined on each residue class once the period is a multiple of k."""
    import sympy as sp
    orders = {}
    for d in split.values():
        for b in d:
            if b not in orders and not _exact(b).is_rational:
                orders[b] = _root_order(b)
    ks = [k for k in orders.values() if k]
    if not ks:
        return split, L
    L2 = L
    for k in ks:
        L2 = L2 * k // gcd(L2, k)
    split = {r: split[r % L] for r in range(L2)}
    new = {}
    for r, d in split.items():
        e_res = N0 + r
        nd = {}
        for b, P in d.items():
            k = orders.get(b)
            if not k:
                key, val = b, P
            else:
                key, val = ('root', k, _exact(b ** k)), P * b ** (e_res % k)
            nd[key] = nd.get(key, sp.Integer(0)) + val
        new[r] = {key: (_exact(v) if isinstance(key, tuple) else v)
                  for key, v in nd.items()}
    return new, L2


def _tidy(txt):
    """Clean up a leading sign when the first term is absent:  ' + x' -> 'x',  ' - x' -> '-x'."""
    txt = txt.strip()
    if txt.startswith("+ "):
        txt = txt[2:]
    elif txt.startswith("- "):
        txt = "-" + txt[2:]
    return txt or "0"


class _HKResult(str):
    """A plain string that shows its line breaks when displayed in Sage/Jupyter."""
    def __repr__(self):
        return str(self)


def hk_formula(p, exps, ideal=None, var="e"):
    """The Hilbert-Kunz function as a string: compact form with Delta's, then an explicit
    formula for each residue class.  The 'e >= e0' bound is the true starting point."""
    p, exps = _clean(p, exps)
    N0, L, res = hk_formula_raw(p, exps, ideal)
    a = sum(len(e) for e in exps) - 1
    return _format_formula(p, a, N0, L, res, lambda m: int(hk(p, exps, m, ideal)), var)


def _format_formula(p, a, N0, L, res, value_at, var="e"):
    """Shared printer: res = {residue: sympy expr in n} (valid for n >= N0, n = N0 + r mod L),
    value_at(m) = exact value at m (used to find the true starting point)."""
    import sympy as sp
    n = sp.Symbol('n', integer=True, positive=True)
    start = N0
    while start > 0:
        m = start - 1
        if sp.simplify(res[(m - N0) % L].subs(n, m) - value_at(m)) == 0:
            start = m
        else:
            break
    split = {r: _split_terms(e, n) for r, e in res.items()}
    split, L = _rationalize(split, L, N0)
    bases = set()
    for d in split.values():
        bases |= set(d)
    lead = sp.Integer(p) ** a
    c = split[0].get(lead, sp.Integer(0))
    others = sorted([b for b in bases if b != lead and any(split[r].get(b, sp.Integer(0)) != 0 for r in split)],
                    key=_base_size, reverse=True)
    ev = sp.Symbol(var)
    fmt = lambda x: str(x).replace("**", "^")
    head = "" if c == 0 else (_base_str(lead, p, var) if c == 1 else "%s*%s" % (fmt(c), _base_str(lead, p, var)))
    names = ["Delta_%s" % var] if len(others) == 1 else ["Delta%d_%s" % (i + 1, var) for i in range(len(others))]
    body, wheres = head, []
    for name, b in zip(names, others):
        vals = {r: sp.expand(split[r].get(b, sp.Integer(0)).subs(n, ev)) for r in split}
        sign = "+"
        if all(v.is_number and v < 0 for v in vals.values()):
            sign, vals = "-", {r: -v for r, v in vals.items()}
        bs = _base_str(b, p, var)
        body += " %s %s" % (sign, name if bs is None else "%s * %s" % (name, bs))
        if len(set(vals.values())) == 1:
            wheres.append("%s is %s for all %s" % (name, fmt(vals[0]), var))
        else:
            cases = ", ".join("%s if %s = %d mod %d" % (fmt(v), var, (N0 + r) % L, L) for r, v in sorted(vals.items()))
            wheres.append("%s is %s" % (name, cases))
    out = "%s  for %s >= %d" % (_tidy(body), var, start)
    if wheres:
        out += ",  where " + ";  ".join(wheres)

    def explicit(r):
        txt = head
        for b in others:
            v = sp.expand(split[r].get(b, sp.Integer(0)).subs(n, ev))
            if v == 0:
                continue
            bs = _base_str(b, p, var)
            if v.is_number:
                sg, v = ("-", -v) if v < 0 else ("+", v)
                piece = fmt(v) if bs is None else ("%s" % bs if v == 1 else "%s*%s" % (fmt(v), bs))
            else:
                sg, piece = "+", "(%s)" % fmt(v) + ("" if bs is None else "*%s" % bs)
            txt += " %s %s" % (sg, piece)
        return _tidy(txt)

    cases = sorted(((N0 + r) % L, r) for r in split)
    lines = [out, "Explicitly:"]
    for cls, r in cases:
        cond = "for all %s >= %d" % (var, start) if L == 1 else \
            "%s = %d mod %d (%s >= %d)" % (var, cls, L, var, start)
        lines.append("  %s:  %s" % (cond, explicit(r)))
    return _HKResult("\n".join(lines))


def _socle_ideal(exps, var=None):
    r"""
    The Huneke-Leuschke setup [HL02] for f = sum_i prod_j X_{i,j}^{d_{i,j}}: pick a monomial
    that is a pure power Y^d (a one-variable list [d] in ``exps``; ``var`` = its index, default:
    the one with the smallest d).  Then I = (all other variables) is a parameter ideal of
    R = k[X]/(f), R/I = k[Y]/(Y^d), l(R/I) = d, the socle element is u = Y^{d-1}, and
    I + (u) = (other variables, Y^{d-1}).   Returns (index, d, ideal exponents of I + (u)).
    """
    pure = [i for i, e in enumerate(exps) if len(e) == 1]
    if not pure:
        raise ValueError("f has no monomial that is a power of a single variable, so there is no "
                         "monomial parameter ideal I with I + (u) of the form (X^a); "
                         "the Huneke-Leuschke reduction used here does not apply")
    if var is None:
        var = min(pure, key=lambda i: exps[i][0])
    elif var not in pure:
        raise ValueError("monomial %d is not a pure power of one variable" % var)
    d = exps[var][0]
    ideal = [[1] * len(e) for e in exps]
    ideal[var] = [d - 1]
    return var, d, ideal


def fs(p, exps, n, var=None):
    """F-signature function FS_e(R) at e = n, via [HL02]:  FS_e = d q^{dim R} - HK_e(R, I + (u))."""
    p, exps = _clean(p, exps)
    _, d, ideal = _socle_ideal(exps, var)
    dim = sum(len(e) for e in exps) - 1
    if d == 1:
        return Integer(p) ** (dim * int(n))       # Y appears linearly: R is regular
    return d * Integer(p) ** (dim * int(n)) - hk(p, exps, n, ideal)


def F_signature(p, exps, var=None):
    """F-signature s(R) = lim FS_e / q^{dim R} = d - e_HK(R, I + (u))  [HL02], exact."""
    p, exps = _clean(p, exps)
    _, d, ideal = _socle_ideal(exps, var)
    if d == 1:
        return QQ(1)
    return d - eHK(p, exps, ideal)


def fs_formula_raw(p, exps, var=None):
    """F-signature function as data: (n0, period, {r: sympy expr in n})."""
    import sympy as sp
    p, exps = _clean(p, exps)
    _, d, ideal = _socle_ideal(exps, var)
    a = sum(len(e) for e in exps) - 1
    n = sp.Symbol('n', integer=True, positive=True)
    if d == 1:
        return 0, 1, {0: sp.Integer(p) ** (a * n)}
    N0, L, res = hk_formula_raw(p, exps, ideal)
    return N0, L, {r: sp.expand(d * sp.Integer(p) ** (a * n) - f) for r, f in res.items()}


def fs_formula(p, exps, var=None, sym="e"):
    """The F-signature function as a string (same layout as hk_formula)."""
    p, exps = _clean(p, exps)
    N0, L, res = fs_formula_raw(p, exps, var)
    a = sum(len(e) for e in exps) - 1
    return _format_formula(p, a, N0, L, res, lambda m: int(fs(p, exps, m, var)), sym)


def fs_brute(p, exps, n, var=None):
    r"""Independent check of FS_e: for Gorenstein R = S/(f) with parameter ideal I and socle u,
    FS_e = l(S / ((I^{[q]} + (f)) : u^q))  (Groebner basis; no Hilbert-Kunz machinery)."""
    p, exps = _clean(p, exps)
    j, d, _ = _socle_ideal(exps, var)
    nv = sum(len(e) for e in exps)
    R = PolynomialRing(GF(p), nv, 'x')
    xs = R.gens()
    f, pos, ypos = R(0), 0, None
    for i, e in enumerate(exps):
        mono = R(1)
        for x in e:
            mono *= xs[pos] ** x
            if i == j:
                ypos = pos
            pos += 1
        f += mono
    q = Integer(p) ** int(n)
    Iq = R.ideal([f] + [xs[k] ** q for k in range(nv) if k != ypos])
    u = xs[ypos] ** (d - 1)
    return Iq.quotient(R.ideal([u ** q])).vector_space_dimension()


def brute(p, exps, n, ideal=None):
    """Independent check: dim_F F_p[X]/(X_1^{a_1 p^n}, ..., f) by a Groebner basis computation."""
    p, exps = _clean(p, exps)
    flat = [x for a in _clean_ideal(exps, ideal) for x in a]
    nv = sum(len(e) for e in exps)
    R = PolynomialRing(GF(p), nv, 'x')
    xs = R.gens()
    f, pos = R(0), 0
    for e in exps:
        mono = R(1)
        for x in e:
            mono *= xs[pos] ** x
            pos += 1
        f += mono
    q = Integer(p) ** int(n)
    return R.ideal([f] + [x ** (a * q) for x, a in zip(xs, flat)]).vector_space_dimension()



# ===========================================================================
# 5. Helpers named after the objects of the notes (han_monsky.tex)
# ===========================================================================

def delta_t(t, p):
    r"""
    ``delta_t`` for a rational ``t >= 0`` (Definition 3.1 of the notes): writing
    ``t = n + v`` with ``n = floor(t)``, ``delta_t = (1 - v) delta_n + v delta_{n+1}``
    (``delta_0 = 0``), an element of ``Gamma_k (x) QQ``.
    """
    t = QQ(t)
    n = floor(t)
    v = t - n
    return (1 - v) * delta(n, p) + v * delta(n + 1, p)


def D_k(p, ts):
    r"""
    ``D_k(t_1, ..., t_n) = alpha(delta_{t_1} ... delta_{t_n})`` (Definition 3.1 of the notes).
    By [HM93, Lemma 5.6] (Lemma 3.2 of the notes), for integers ``a_i, d_i``,
    ``dim_k k[x]/(x_i^{a_i}, sum x_i^{d_i}) = d_1 ... d_n D_k(a_1/d_1, ..., a_n/d_n)``.
    """
    x = delta(1, p)
    for t in ts:
        x = x * delta_t(t, p)
    return x.D()


def ell_k(p, rs):
    r"""``ell_k(r_1, ..., r_n) = alpha(lambda_{r_1} ... lambda_{r_n})`` (Definition 3.1 of the notes)."""
    x = lam(0, p)
    for r in rs:
        x = x * lam(int(r), p)
    return x.D()


def phi_r(p, r, x):
    r"""
    The polynomial ``phi_r`` of [HM93, Theorem 4.13] (Theorem 3.4 of the notes), evaluated at
    ``x = (x_1, ..., x_n)``:  ``sum_{A proper subset} n_A x_A``, minus
    ``ell_k(r) x_2 ... x_n`` when ``sum r_i`` is odd, where
    ``n_A = alpha( prod_{i in A} (-1)^{r_i} lambda_{r_i} * prod_{j not in A} delta_{r_j} )``.
    """
    n = len(r)
    total = 0
    for size in range(n):
        for A in itertools.combinations(range(n), size):
            y = lam(0, p)
            for i in range(n):
                y = y * (((-1) ** r[i]) * lam(r[i], p) if i in A else delta(r[i], p))
            total += y.D() * prod([x[i] for i in A])
    if sum(r) % 2:
        total -= ell_k(p, r) * prod(x[1:])
    return total


def theta_index(i, p):
    r"""``theta(lambda_i) = lambda_{theta_index(i)}`` [MT06] (Theorem 2.11 of the notes)."""
    return p * i if i % 2 == 0 else p * i + p - 1


def Phi_e(i, p, e):
    r"""
    The digits ``(a_0(i), ..., a_{e-1}(i))`` of Proposition 2.12 of the notes, i.e.
    ``Phi_e(lambda_i) = lambda_{a_0} (x) ... (x) lambda_{a_{e-1}}`` in ``Lambda_1^{(x) e}``.
    """
    ds = [(i // p ** k) % p for k in range(e)]
    out = []
    for k in range(e):
        s = sum(ds[r] * p ** r for r in range(k + 1, e))
        out.append(ds[k] if s % 2 == 0 else p - 1 - ds[k])
    return tuple(out)


# ===========================================================================
# 6. Reader-friendly interface: functions of the polynomial itself
# ===========================================================================
#
#   S.<x,y,z,t> = GF(5)[]
#   HK_function_diagonal(x^4 + y^4 + z^4 + t^4)        # Han-Monsky   [HM93]
#   HK_function_disjoint_monomials((x*y)^4 + z^4 + t^4) # Chiang-Hung  [CH98]
#   FS_function_diagonal(x^3 + y^3 + z^3)               # F-signature  [HL02]
#   G = HanMonskyRing(5);  G.delta(2) * G.delta(3);  G.lam(2).matrix()
#
# The result prints as one formula per residue class of e, and can be evaluated: H(3).

HanMonskyRing = RepresentationRing


def _monomial_blocks(f):
    """Exponent lists of f, one per monomial, checking that the monomials of f use pairwise
    disjoint sets of variables.  Variables of the ring that f does not involve are ignored:
    R = k[[x_1..x_n]]/(f) is taken over the variables of f only, so one ring S.<x,y,z,t>
    serves for f = x^2 + y^2 as well.  Nonzero coefficients are allowed: over an algebraic
    closure they can be absorbed by rescaling one variable of each monomial, and lengths do
    not change under field extension.  Returns (p, exps, variable positions)."""
    P = f.parent()
    k = P.base_ring()
    if not (hasattr(k, "characteristic") and k.is_finite()):
        raise ValueError("f must be a polynomial over a finite field, e.g. GF(5)[x,y]")
    p = Integer(k.characteristic())
    exps, positions, used = [], [], set()
    for ev in f.exponents():
        ev = list(ev) if hasattr(ev, "__iter__") else [ev]
        support = [i for i, a in enumerate(ev) if a > 0]
        if not support:
            raise ValueError("f must not have a constant term")
        if used & set(support):
            raise ValueError("the monomials of f must involve disjoint sets of variables")
        used |= set(support)
        exps.append([int(ev[i]) for i in support])
        positions.append(support)
    return p, exps, positions


def _ideal_exponents(positions, ideal, ngens):
    """{ring variable position: a_i} from ideal = [a_1, ...], given either for all the ring
    variables or only for the variables of f (both in the order of the ring variables)."""
    used = sorted(i for block in positions for i in block)
    ideal = [int(a) for a in ideal]
    if len(ideal) == ngens:
        return {i: ideal[i] for i in used}
    if len(ideal) == len(used):
        return dict(zip(used, ideal))
    raise ValueError("ideal needs one exponent per variable of f (%d) or of the ring (%d)"
                     % (len(used), ngens))


def _ideal_shape(positions, ideal, ngens):
    """ideal = [a_1, ...] (see _ideal_exponents) -> nested shape of exps."""
    if ideal is None:
        return None
    a = _ideal_exponents(positions, ideal, ngens)
    return [[a[i] for i in block] for block in positions]


def _power(base, expo):
    """'5^(3e)', '3^e', '3^(e/2)', '3^((e - 1)/2)'; expo is a string in e."""
    if expo == "e":
        return "%s^e" % base
    return "%s^(%s)" % (base, expo)


def _term(coef, power):
    """'+ 168/61 * 5^(3e)', '- 4', '+ 3^e' (power may be None for a constant)."""
    sign = "-" if coef < 0 else "+"
    c = abs(coef)
    if power is None:
        return "%s %s" % (sign, c)
    return "%s %s" % (sign, power if c == 1 else "%s * %s" % (c, power))


def _class_condition(cls, period, start):
    first = start + ((cls - start) % period)
    if period == 1:
        return "for e >= %d" % start
    if period == 2:
        return "for %s e >= %d" % ("even" if cls % 2 == 0 else "odd", first)
    return "for e = %d mod %d, e >= %d" % (cls, period, first)


def _top_level_terms(body):
    """Split 'a - b * c^e + (d + e) * f' into ['a', ' - b * c^e', ' + (d + e) * f']."""
    terms, depth, start, i = [], 0, 0, 0
    while i < len(body):
        ch = body[i]
        depth += (ch == "(") - (ch == ")")
        if depth == 0 and i > 0 and body[i:i + 3] in (" + ", " - "):
            terms.append(body[start:i])
            start = i
            i += 3
            continue
        i += 1
    terms.append(body[start:])
    return terms


class HilbertKunzFunction:
    """A function e |-> value, valid for e >= start, given by one formula per residue class
    of e modulo the period.  Printing shows the formulas; H(e) evaluates."""

    def __init__(self, name, lines, value, start, period):
        self._name, self._lines, self._value = name, lines, value
        self.start, self.period = start, period

    def __call__(self, e):
        return self._value(int(e))

    def __repr__(self):
        width = max(len(body) for body, _ in self._lines)
        if width <= 60:
            return "\n".join("%s_e = %s   %s" % (self._name, body.ljust(width), cond)
                             for body, cond in self._lines)
        out = []                       # long formulas: one line per group of terms
        for body, cond in self._lines:
            pieces, cur = [], ""
            for term in _top_level_terms(body):
                if cur and len(cur) + len(term) > 60:
                    pieces.append(cur)
                    cur = term.lstrip()
                else:
                    cur += term
            pieces.append(cur)
            pad = " " * (len(self._name) + 5)
            out.append("%s_e = %s" % (self._name, pieces[0]))
            out += [pad + piece for piece in pieces[1:]]
            out.append(pad + cond)
        return "\n".join(out)

    __str__ = __repr__


def _han_monsky_function(name, p, exps, ideal, lead, sign, value_at):
    """value(e) = lead * p^(dim e) + sign * Delta_k * lsh^m  for e = e0 + k + mu m  (the
    shape of [Notes, Corollary 3.6]), with Delta_k from eHK_diagonal, printed per class."""
    D = eHK_diagonal(p, exps, ideal, _data=True)
    mu, e0, lsh, dim, Deltas = D['mu'], D['e0'], D['lsh'], D['dim'], D['Deltas']

    def formula(e):
        k = (e - e0) % mu
        return lead * p ** (dim * e) + sign * Deltas[k] * lsh ** ((e - e0 - k) // mu)

    if lsh == 0:                       # Delta_e = 0 from e0 + mu on: only the leading term
        start = e0 + mu
        formula = lambda e: lead * p ** (dim * e)
    else:
        start = e0
    while start > 0 and formula(start - 1) == value_at(start - 1):
        start -= 1
    lead_power = _power(p, "e" if dim == 1 else "%de" % dim)
    lines = []
    for cls in sorted({c % mu for c in range(start, start + mu)}):
        k = (cls - e0) % mu
        body = "" if lead == 0 else ("%s * %s" % (lead, lead_power) if lead != 1 else lead_power)
        coef = sign * Deltas[k]
        if coef != 0 and lsh != 0:
            c0 = (e0 + k) % mu                       # exponent of lsh is (e - c0)/mu - shift
            coef = coef / QQ(lsh) ** ((e0 + k - c0) // mu)
            if lsh == 1:
                power = None
            elif mu == 1:
                power = _power(lsh, "e")
            else:
                power = _power(lsh, "e/%d" % mu if c0 == 0 else "(e - %d)/%d" % (c0, mu))
            body = (body + " " + _term(coef, power)) if body else _term(coef, power).lstrip("+ ")
        if not body:
            body = "0"
        if body.startswith("- "):
            body = "-" + body[2:]
        lines.append((body, _class_condition(cls, mu, start)))

    def value(e):
        return formula(e) if e >= start else value_at(e)
    return HilbertKunzFunction(name, lines, value, start, mu)


def HK_function_diagonal(f, ideal=None):
    r"""
    Hilbert-Kunz function e |-> HK_e(R, I) = l(R / I^[p^e]) of R = k[[x_1..x_n]]/(f) for a
    diagonal polynomial f = x_1^{d_1} + ... + x_n^{d_n} over a finite field, computed with
    the Han-Monsky algorithm [HM93], [Notes, Section 3].  ``ideal = [a_1, ..., a_n]`` replaces
    the maximal ideal by (x_1^{a_1}, ..., x_n^{a_n}).

        sage: S.<x,y> = GF(2)[]
        sage: HK_function_diagonal(x^5 + y^5)
        HK_e = 5 * 2^e - 4   for even e >= 0
        HK_e = 5 * 2^e - 6   for odd e >= 1

    (For backward compatibility, HK_function_diagonal(p, exps) still returns the old string.)
    """
    if f in ZZ:                                                    # old signature (p, exps)
        return eHK_diagonal(f, ideal, None, False, return_HK_function=True)
    p, exps, pos = _monomial_blocks(f)
    if any(len(b) != 1 for b in exps):
        raise ValueError("f is not diagonal; try HK_function_disjoint_monomials(f)")
    exps = [b[0] for b in exps]
    idl = None if ideal is None else [b[0] for b in _ideal_shape(pos, ideal, f.parent().ngens())]
    D = eHK_diagonal(p, exps, idl, _data=True)
    return _han_monsky_function("HK", p, exps, idl, D['eHK'], -1,
                                lambda e: _hk_value(p, exps, idl, e))


def FS_function_diagonal(f):
    r"""
    F-signature function e |-> FS_e(R) of R = k[[x_1..x_n]]/(f), f = x_1^{d_1} + ... + x_n^{d_n},
    via Huneke-Leuschke [HL02], [Notes, Proposition 4.1 and Lemma 4.2]:
    FS_e(R) = d_j p^{(n-1)e} - HK_e(R, (x_1, ..., x_j^{d_j - 1}, ..., x_n)).
    """
    p, exps, pos = _monomial_blocks(f)
    if any(len(b) != 1 for b in exps):
        raise ValueError("f is not diagonal")
    exps = [Integer(b[0]) for b in exps]
    dj, I = _socle_ideal_diagonal(exps)
    dim = len(exps) - 1
    if dj == 1:
        raise ValueError("R is regular: FS_e = p^(%d e)" % dim)
    D = eHK_diagonal(p, exps, I, _data=True)
    return _han_monsky_function("FS", p, exps, I, dj - D['eHK'], +1,
                                lambda e: dj * p ** (dim * e) - _hk_value(p, exps, I, e))


def _pretty_explicit(expr, cls, period):
    """Tidy one explicit formula printed by _format_formula, for the class e = cls mod period."""
    import re
    def fl(m):
        k = int(m.group(1))
        if period % k:
            return m.group(0)
        c = cls % k
        return "(e/%d)" % k if c == 0 else "((e - %d)/%d)" % (c, k)
    expr = re.sub(r"floor\(e/(\d+)\)", fl, expr)
    expr = re.sub(r"(\d)\*e\b", r"\1e", expr)                      # 5^(3*e) -> 5^(3e)
    expr = expr.replace("*", " * ")
    expr = re.sub(r"\^\((e/\d+)\)", r"^(\1)", expr)
    return expr


def _parse_formula(txt):
    """[(class, period, start, expr)] from the 'Explicitly:' part of hk_formula / fs_formula."""
    import re
    out = []
    lines = txt.split("Explicitly:")[1].strip("\n").split("\n")
    for line in lines:
        line = line.strip()
        m = re.match(r"for all e >= (\d+):\s+(.*)$", line)
        if m:
            out.append((0, 1, int(m.group(1)), m.group(2)))
            continue
        m = re.match(r"e = (\d+) mod (\d+) \(e >= (\d+)\):\s+(.*)$", line)
        out.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)))
    return out


def _formula_object(name, txt, value):
    cases = _parse_formula(txt)
    period, start = cases[0][1], cases[0][2]
    lines = [(_pretty_explicit(expr, cls, period), _class_condition(cls, period, start))
             for cls, period, start, expr in cases]
    return HilbertKunzFunction(name, lines, value, start, period)


def HK_function_disjoint_monomials(f, ideal=None):
    r"""
    Hilbert-Kunz function e |-> HK_e(R, I) of R = k[[X]]/(f), where f is a sum of monomials in
    pairwise disjoint sets of variables, f = sum_i prod_j X_{i,j}^{d_{i,j}} (for instance
    (x*y)^4 + z^4 + t^4 + w^4), computed with the Chiang-Hung algorithm [CH98].
    ``ideal = [a_1, ..., a_N]`` (one exponent per ring variable) replaces the maximal ideal.

        sage: S.<x,y,z,t,w> = GF(5)[]
        sage: HK_function_disjoint_monomials((x*y)^4 + z^4 + t^4 + w^4)
        HK_e = 285166/96099 * 5^(4e) - 752/309 * 7^e + 145/311 * 3^e   for e >= 0
    """
    p, exps, pos = _monomial_blocks(f)
    idl = _ideal_shape(pos, ideal, f.parent().ngens())
    return _formula_object("HK", str(hk_formula(p, exps, idl)), lambda e: hk(p, exps, e, idl))


def FS_function_disjoint_monomials(f):
    r"""F-signature function of k[[X]]/(f), f a sum of monomials in disjoint variables, one of
    which is a pure power Y^d (Huneke-Leuschke [HL02] together with [CH98])."""
    p, exps, pos = _monomial_blocks(f)
    return _formula_object("FS", str(fs_formula(p, exps)), lambda e: fs(p, exps, e))


def HK_groebner(f, e, ideal=None):
    r"""Independent check: HK_e(R, I) = dim_k k[X]/(f, X_1^{a_1 p^e}, ..., X_N^{a_N p^e}),
    computed directly with a Groebner basis (slow, but uses no theory at all)."""
    P = f.parent()
    p = Integer(P.base_ring().characteristic())
    _, _, pos = _monomial_blocks(f)
    a = {i: 1 for block in pos for i in block} if ideal is None else _ideal_exponents(pos, ideal, P.ngens())
    used = sorted(a)                                     # work over the variables of f only
    Q = PolynomialRing(P.base_ring(), [str(P.gen(i)) for i in used])
    g = Q(f)
    q = p ** int(e)
    return Q.ideal([g] + [Q.gen(j) ** (a[i] * q) for j, i in enumerate(used)]).vector_space_dimension()
