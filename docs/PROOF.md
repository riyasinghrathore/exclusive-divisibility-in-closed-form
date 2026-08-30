# TermBoost — Correctness Proof of the O(1) Formula

*Companion proof for the TermBoost repository. A rendered copy is linked from
the project website (see [Hosting](#hosting-this-proof)).*

---

## 1. Problem statement

Fix integers $a, b$ with

$$1 < a < b, \qquad \gcd(a,b) = 1 .$$

Call a positive integer **valid** if it is divisible by $a$ or by $b$ **but not
both**:

$$V \;=\; \{\, x \in \mathbb{Z}_{>0} : (a \mid x)\ \operatorname{XOR}\ (b \mid x) \,\}.$$

Given $n \ge 1$, we want $V_{(n)}$, the $n$-th smallest element of $V$.

Because $\gcd(a,b)=1$, a number is divisible by both $a$ and $b$ **iff** it is
divisible by $ab$. So the excluded "both" set is exactly the multiples of $ab$.

We prove the closed form computed by
[`formula`](../src/termboost/algorithms.py):

$$
\boxed{\;
V_{(n)} \;=\; q\,ab \;+\; \min\!\big(a(i+1),\ b(j+1)\big),
\quad
\begin{aligned}
s &= a+b, & p &= a+b-2,\\
q &= \left\lfloor \tfrac{n-1}{p}\right\rfloor, & r &= n - qp \in [1,p],\\
i &= \left\lfloor \tfrac{rb}{s}\right\rfloor, & j &= \left\lfloor \tfrac{ra}{s}\right\rfloor .
\end{aligned}
\;}
$$

The whole computation is a fixed number of integer operations, hence $O(1)$.

---

## 2. A counting function

For $x \ge 0$ let

$$C(x) \;=\; \big|\,V \cap [1,x]\,\big|
\;=\; \left\lfloor \tfrac{x}{a}\right\rfloor
     + \left\lfloor \tfrac{x}{b}\right\rfloor
     - 2\left\lfloor \tfrac{x}{ab}\right\rfloor .$$

*Why the $-2$:* $\lfloor x/a\rfloor$ counts multiples of $a$ and
$\lfloor x/b\rfloor$ counts multiples of $b$; a multiple of $ab$ is counted in
**both** terms, so subtracting $2\lfloor x/ab\rfloor$ removes it entirely
(rather than the $-1$ of ordinary inclusion–exclusion, which would merely
deduplicate it). $C$ is non-decreasing, and $C(x)-C(x-1)=1$ exactly when
$x \in V$. Hence

$$V_{(n)} \;=\; \min\{\, x : C(x) = n \,\}
          \;=\; \min\{\, x : C(x) \ge n \,\}. \tag{2.1}$$

Equation (2.1) is exactly what the [`binary_search`](../src/termboost/algorithms.py)
baseline evaluates.

---

## 3. Periodicity: $p = a+b-2$ valid numbers per block

**Lemma 1.** $x \in V \iff x + ab \in V$, and each half-open block
$(kab,\ (k{+}1)ab]$ contains exactly $p = a+b-2$ valid numbers.

*Proof.* Divisibility by $a$, by $b$, and by $ab$ are all invariant under
$x \mapsto x+ab$, so membership in $V$ is periodic with period $ab$. Count $V$
inside $(0, ab]$:

* multiples of $a$: $\ a, 2a, \dots, ba{=}ab$ — that is $b$ of them;
* multiples of $b$: $\ b, 2b, \dots, ab$ — that is $a$ of them;
* the single value $ab$ is divisible by both and is therefore **excluded**.

The multiples of $a$ other than $ab$ ($b-1$ of them) and the multiples of $b$
other than $ab$ ($a-1$ of them) are disjoint (a common element would be a
multiple of $ab$). Hence $|V \cap (0,ab]| = (b-1)+(a-1) = a+b-2 = p.$ $\qquad\blacksquare$

**Consequence (period stripping).** Write $n = qp + r$ with
$q=\lfloor (n-1)/p\rfloor$ and $r = n-qp \in [1,p]$. By Lemma 1,

$$V_{(n)} \;=\; q\,ab \;+\; W_r, \tag{3.1}$$

where $W_r$ is the $r$-th valid number in the first block, i.e. the $r$-th valid
number in $(0, ab]$. It remains to find $W_r$ for $r \in [1,p]$.

This is illustrated in `figures/fig2_period.png`.

---

## 4. Key arithmetic lemma

Throughout, $s = a+b$. Since $\gcd(a,b)=1$,

$$\gcd(s,a) = \gcd(a+b,a) = \gcd(b,a) = 1,
\qquad \gcd(s,b) = 1. \tag{4.1}$$

**Lemma 2.** For every $r$ with $1 \le r \le s-2\ (=p)$,

$$\left\lfloor \tfrac{rb}{s}\right\rfloor
+ \left\lfloor \tfrac{ra}{s}\right\rfloor
= r - 1 .$$

*Proof.* The two exact fractions sum to an integer:

$$\frac{rb}{s} + \frac{ra}{s} = \frac{r(a+b)}{s} = r .$$

Writing each as integer part plus fractional part
($x=\lfloor x\rfloor + \{x\}$),

$$\left\lfloor \tfrac{rb}{s}\right\rfloor + \left\lfloor \tfrac{ra}{s}\right\rfloor
= r - \Big(\{\tfrac{rb}{s}\} + \{\tfrac{ra}{s}\}\Big).$$

The bracket is a sum of two fractional parts whose total $r$ is an integer, so
$\{rb/s\}+\{ra/s\} \in \{0,1\}$. It equals $0$ **iff** both fractional parts
vanish, i.e. $s \mid rb$ and $s \mid ra$. By (4.1), $s\mid rb \iff s\mid r$; but
$1 \le r \le s-2 < s$ forces $s \nmid r$. Hence each fractional part is nonzero,
their sum is $1$, and the claim follows. $\qquad\blacksquare$

`figures/fig4_invariant.png` shows both halves of this argument: $i+j = r-1$ and
the fractional-part sum pinned at $1$.

Define, for $r \in [1,p]$,

$$i = \left\lfloor \tfrac{rb}{s}\right\rfloor,
\qquad j = \left\lfloor \tfrac{ra}{s}\right\rfloor,
\qquad\text{so } i + j = r-1 \ \text{ by Lemma 2.} \tag{4.2}$$

---

## 5. Two strict inequalities

**Lemma 3.** With $i,j$ as in (4.2) and $1 \le r \le p$,

$$a\,i \;<\; b\,(j+1)
\qquad\text{and}\qquad
b\,j \;<\; a\,(i+1).$$

*Proof.* From $i = \lfloor rb/s\rfloor$ we get $is \le rb$, i.e.
$i(a+b) \le rb$, i.e. $ia \le (r-i)b$. By (4.2) $r-i = j+1$, so
$ia \le (j+1)b$. Equality would give $i(a+b)=rb$, i.e. $s\mid rb$, i.e.
$s\mid r$ by (4.1) — impossible for $1\le r\le s-2$. Hence $ai < b(j+1)$.

Symmetrically, $j = \lfloor ra/s\rfloor \Rightarrow js \le ra \Rightarrow
jb \le (r-j)a = (i+1)a$, strict by the same coprimality argument, giving
$bj < a(i+1)$. $\qquad\blacksquare$

---

## 6. Main theorem

**Theorem.** For $1 \le r \le p$, the $r$-th valid number in the first block is

$$W_r \;=\; \min\big(a(i+1),\ b(j+1)\big).$$

Together with (3.1) this proves the boxed formula of §1.

*Proof.* Put $A = a(i+1)$ (the $(i{+}1)$-th multiple of $a$) and
$B = b(j+1)$ (the $(j{+}1)$-th multiple of $b$), and $M = \min(A,B)$. For
$v < ab$ there is no multiple of $ab$ in $[1,v]$, so §2 gives
$C(v) = \lfloor v/a\rfloor + \lfloor v/b\rfloor$.

First, $A \ne B$ on this range: $A=B$ means $b \mid a(i+1)$, so $b\mid(i+1)$
and $a\mid(j+1)$; the smallest such case is $i+1=b,\ j+1=a$, giving
$A=ab$ and $r=i+j+1=a+b-1 = s-1 > p$. So for $r\le p$ we have $M < ab$, and $M$
is strictly one of $A, B$.

Assume $M = A \le B$ (the case $M=B$ is symmetric). Compute $C(A)$:

* $\lfloor A/a\rfloor = i+1$ since $A = a(i+1)$.
* By Lemma 3, $bj < a(i+1) = A$, and $A \le B = b(j+1)$ with $A\ne B$ gives
  $A < b(j+1)$. Hence $bj < A < b(j+1)$, so $\lfloor A/b\rfloor = j$.

Therefore $C(A) = (i+1) + j = r$ by (4.2). Also $A$ is a multiple of $a$ and,
from $bj < A < b(j+1)$, **not** a multiple of $b$; so $A \in V$. Thus
$C(A)=r$ and $A\in V$.

Finally $A$ is the *first* value with count $r$: for any $v < A$,
$\lfloor v/a\rfloor \le i$ (as $A$ is the $(i{+}1)$-th multiple of $a$) and, since
$v < A \le B = b(j+1)$, $\lfloor v/b\rfloor \le j$; hence
$C(v) \le i + j = r-1 < r$. By (2.1), $A = \min\{v : C(v)\ge r\} = W_r$.

So $W_r = A = \min(A,B)$. $\qquad\blacksquare$

**Boundary check ($r = p$).** Lemma 2 still applies ($p = s-2$). One finds
$W_p = ab - a$ (the largest valid number below $ab$, namely $(b{-}1)a$, since
$ab-a > ab-b$ as $a<b$). Combined with (3.1) this reproduces the "$\text{filler}-a$"
special case of the original driver when $p \mid n$.

---

## 7. Complexity

| Method | Work per query | Notes |
|---|---|---|
| Brute force | $O(V_{(n)}) = O(n\cdot ab/(a+b))$ | reference oracle only |
| Binary search | $O(\log(na))$ | evaluates (2.1) |
| **Formula** | $O(1)$ | one `divmod`, two `//`, one `min` |

`figures/fig3_staircase.png` shows $W_r$ landing on the counting staircase
near the density line $v\,(1/a+1/b)$; `figures/fig5_benchmark.png` shows the
measured $O(1)$ vs $O(\log n)$ scaling.

---

## 8. Empirical corroboration

Beyond the proof, the identity is checked in code (`tests/test_correctness.py`):

* **Exhaustive** vs. brute force for every coprime pair $a<b<50$ and every
  $n$ up to $2$ periods $+5$ (covers all block boundaries).
* **Period boundaries** $n = kp-1, kp, kp+1$ for all coprime pairs $<60$.
* **Validity/rank**: the returned $x$ satisfies $x\in V$, $C(x)=n$, $C(x{-}1)=n{-}1$.
* **Large random**: $5\times10^4$ cases with $a,b\le10^5$, $n\le10^7$ — formula
  matches binary search exactly.

All pass with **zero** mismatches. See the repository `README.md` for the
benchmark numbers.

---

## 9. Hosting this proof

The website write-up should link here. Suggested markup (replace the URL with
your repo's canonical location):

```html
<p>
  Full correctness proof (math + figures):
  <a href="https://github.com/&lt;you&gt;/TermBoost/blob/main/docs/PROOF.md">docs/PROOF.md</a>
</p>
```

The GitHub-Flavored-Markdown math in this file renders directly on GitHub. To
publish a standalone page, convert with e.g.
`pandoc docs/PROOF.md -o proof.html --mathjax` and drop the figures in
`docs/figures/` alongside it.
