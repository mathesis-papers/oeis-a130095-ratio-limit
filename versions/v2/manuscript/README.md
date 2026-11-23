# Adamson's Fibonacci divisor-transform conjecture: sharp ratio errors

Haobo Ma (ChronoAI Pte Ltd, Singapore), followed by Wenlin Zhang (National
University of Singapore; ChronoAI Pte Ltd, Singapore).

For positive integers, let `a(n) = sum_{d|n} F_(2d-1)`, with `F_0=0` and
`F_1=1`. The note proves `a(n)/a(n-1) -> ((1+sqrt(5))/2)^2`, together with
`0 <= a(n)-F_(2n-1) <= F_n`. It also supplies a general exponential
divisor-transform estimate and coefficientwise proofs of Bala's two
generating-function formulas. It proves the sharp scaled ratio-error limits
`phi^(2m)*(a(2m)/a(2m-1)-phi^2) -> phi^2` and
`phi^(2m+1)*(a(2m+1)/a(2m)-phi^2) -> -phi^3`, with
`phi=(1+sqrt(5))/2`, and supplies proofs of Bala's and Somos's prime
congruences, the ordinary-transform generating functions, and Möbius inversion.
The standard Fibonacci-transform asymptotic
is credited to Václav Kotešovec's formula in OEIS A007435, May 21, 2018.
The underlying odd-Fibonacci ratio calculation is credited to Wolfdieter
Lang, OEIS A001519, March 30, 2020; its displayed matrix sign is corrected
to `M^2=3M-I` for `M=((1,1),(1,2))`, and its Binet prefactor to
`1/(2*phi-1)=1/sqrt(5)` rather than `1/(2*phi+1)`.

## Files and rebuilding

- `note.tex`: self-contained LaTeX, including its bibliography.
- `note.pdf`: readable mathematical note.
- `metadata.json`: title, creators, license, problem identity, and coverage.
- `verify.py`: supplementary exact-integer checks, using Python 3's standard library.
- `checks.json`: deterministic output of the finite checks.

Build with Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, run `pdflatex note.tex` twice. The bibliography is inline;
BibTeX is unnecessary. Run the finite checks with:

```sh
python3 verify.py > checks-new.json
diff -u checks.json checks-new.json
```

## Mathematical coverage

The pinned scientific source is
https://github.com/the-omega-institute/trureturing/blob/d51b6958b717911d2705676a6e9bf473b3b6f324/D5/S3/Arith/Divisors/OeisA130095RatioLimit.lean.
Its declaration `D5.S3.Arith.Divisors.OeisA130095RatioLimit.result` states
the full eventual epsilon-N ratio limit. Its definition `a` uses positive
divisors and the same Fibonacci convention as the note for `n>=1`.

The general transform proposition, sharp parity limits, generating functions,
matrix correction, inversion, and prime congruences have written proofs in
the note and are not assertions of that Lean declaration.
The checker establishes only
the finite ranges recorded in `checks.json`; the limiting assertions have
all-index proofs. The checks cover indices 1 through 1000, generating-function
coefficients through degree 120, both prime congruences through prime 9973,
and eight illustrative scaled ratio errors at 500-digit precision.

## License

CC BY 4.0, identifier `cc-by-4.0`:
https://creativecommons.org/licenses/by/4.0/.
