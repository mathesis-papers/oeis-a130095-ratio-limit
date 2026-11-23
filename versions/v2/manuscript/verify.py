import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from math import isqrt
from pathlib import Path


LIMIT = 1000
COEFFICIENT_LIMIT = 120
PRIME_LIMIT = 10000
PUBLISHED = [
    1, 3, 6, 16, 35, 97, 234, 626, 1603, 4218,
    10947, 28767, 75026, 196654, 514269, 1346895,
    3524579, 9229159, 24157818, 63250217, 165580380,
    433505386, 1134903171, 2971244450, 7778742084,
    20365086102, 53316292776, 139584059112, 365435296163,
    956722544582,
]


def fibonacci_table(maximum):
    values = [0, 1]
    for index in range(2, maximum + 1):
        values.append(values[index - 1] + values[index - 2])
    return values


def fibonacci_mod(index, modulus):
    if index == 0:
        return 0, 1
    current, following = fibonacci_mod(index // 2, modulus)
    doubled = current * (2 * following - current) % modulus
    doubled_following = (current * current + following * following) % modulus
    if index % 2:
        return doubled_following, (doubled + doubled_following) % modulus
    return doubled, doubled_following


def mobius(index):
    sign = 1
    divisor = 2
    remaining = index
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            remaining //= divisor
            sign = -sign
            if remaining % divisor == 0:
                return 0
        while remaining % divisor == 0:
            remaining //= divisor
        divisor += 1
    if remaining > 1:
        sign = -sign
    return sign


def main():
    fibonacci = fibonacci_table(2 * LIMIT + 3)
    transform = [0] * (LIMIT + 1)
    for divisor in range(1, LIMIT + 1):
        for multiple in range(divisor, LIMIT + 1, divisor):
            transform[multiple] += fibonacci[2 * divisor - 1]

    for index in range(1, LIMIT + 1):
        direct = sum(
            fibonacci[2 * divisor - 1]
            for divisor in range(1, index + 1)
            if index % divisor == 0
        )
        assert transform[index] == direct
        remainder = direct - fibonacci[2 * index - 1]
        assert 0 <= remainder <= fibonacci[2 * (index // 2)] <= fibonacci[index]
        assert fibonacci[2 * index - 1] == (
            fibonacci[index] ** 2 + fibonacci[index - 1] ** 2
        )
        assert remainder * fibonacci[index] <= fibonacci[2 * index - 1]
        assert sum(fibonacci[2 * term - 1] for term in range(1, index + 1)) == fibonacci[2 * index]
        if index % 2 == 0:
            assert remainder >= fibonacci[index - 1]
        if index >= 2:
            leading = fibonacci[index - 1] if index % 2 == 0 else 0
            assert 0 <= remainder - leading <= fibonacci[2 * (index // 3)]

    assert transform[1:31] == PUBLISHED

    rational = [0] * (COEFFICIENT_LIMIT + 1)
    rational[1] = 1
    rational[2] = 2
    for index in range(3, COEFFICIENT_LIMIT + 1):
        rational[index] = 3 * rational[index - 1] - rational[index - 2]
    assert rational[1:] == [fibonacci[2 * index - 1] for index in range(1, COEFFICIENT_LIMIT + 1)]
    substituted = [0] * (COEFFICIENT_LIMIT + 1)
    for power in range(1, COEFFICIENT_LIMIT + 1):
        for index in range(1, COEFFICIENT_LIMIT // power + 1):
            substituted[power * index] += rational[index]
    assert substituted == transform[:COEFFICIENT_LIMIT + 1]

    standard = [0] * (LIMIT + 1)
    for divisor in range(1, LIMIT + 1):
        for multiple in range(divisor, LIMIT + 1, divisor):
            standard[multiple] += fibonacci[divisor]
    mobius_values = [0] + [mobius(index) for index in range(1, LIMIT + 1)]
    for index in range(1, LIMIT + 1):
        divisors = [divisor for divisor in range(1, index + 1) if index % divisor == 0]
        assert sum(mobius_values[divisor] * transform[index // divisor] for divisor in divisors) == fibonacci[2 * index - 1]
        assert sum(mobius_values[divisor] * standard[index // divisor] for divisor in divisors) == fibonacci[index]
        assert sum(fibonacci[divisor] for divisor in divisors) == standard[index]
    for index in range(1, COEFFICIENT_LIMIT + 1):
        logarithmic = sum((Fraction(fibonacci[divisor], divisor) / (index // divisor)
                           for divisor in range(1, index + 1) if index % divisor == 0), Fraction(0))
        assert logarithmic == Fraction(standard[index], index)

    matrix = ((1, 0), (0, 1))
    for index in range(1, LIMIT + 1):
        matrix = tuple((row[0] + row[1], row[0] + 2 * row[1]) for row in matrix)
        assert matrix[0][0] == fibonacci[2 * index - 1]
    assert ((2, 3), (3, 5)) != ((4, 3), (3, 7))

    primes = [index for index in range(2, PRIME_LIMIT + 1)
              if all(index % divisor for divisor in range(2, isqrt(index) + 1))]
    for prime in primes:
        residue = prime % 5
        expected_odd = 0 if prime == 5 else (3 if residue in (2, 3) else 2)
        expected_standard = 1 if prime == 5 else (0 if residue in (2, 3) else 2)
        assert (1 + fibonacci_mod(2 * prime - 1, prime)[0]) % prime == expected_odd % prime
        assert (1 + fibonacci_mod(prime, prime)[0]) % prime == expected_standard % prime

    parity_samples = []
    with localcontext() as context:
        context.prec = 500
        golden = (Decimal(1) + Decimal(5).sqrt()) / 2
        for index in [60, 61, 120, 121, 240, 241, 480, 481]:
            scaled = golden ** index * (Decimal(transform[index]) / Decimal(transform[index - 1]) - golden ** 2)
            target = golden ** 2 if index % 2 == 0 else -golden ** 3
            assert abs(scaled - target) < Decimal('0.1')
            parity_samples.append({'n': index, 'scaled_ratio_error': format(scaled, '.12f'),
                                   'target': format(target, '.12f')})

    report = {
        'arithmetic': 'exact integers',
        'status': 'pass',
        'fibonacci_definition': 'F_0=0, F_1=1, F_(n+2)=F_(n+1)+F_n',
        'transform_definition': 'a(n)=sum_{d|n} F_(2d-1), positive divisors',
        'identities_and_inequalities': {
            'indices': [1, LIMIT],
            'checks': [
                'divisor-sieve values equal independent direct divisor sums',
                '0 <= a(n)-F_(2n-1) <= F_(2 floor(n/2)) <= F_n',
                'F_(2n-1)=F_n^2+F_(n-1)^2',
                '(a(n)-F_(2n-1))*F_n <= F_(2n-1)',
                'sum_{j=1}^n F_(2j-1)=F_(2n)',
                'a(n)-F_(2n-1) >= F_(n-1) for even n',
                '0 <= R(n)-1_(2|n)*F_(n-1) <= F_(2 floor(n/3)) for n>=2',
                'Mobius inversion for both Fibonacci divisor transforms',
                '(M^n)_(1,1)=F_(2n-1), M=((1,1),(1,2))',
            ],
        },
        'published_terms': {'source': 'https://oeis.org/A130095/b130095.txt', 'indices': [1, 30], 'matched': 30},
        'generating_function_coefficients': {'powers': [0, COEFFICIENT_LIMIT], 'matched': COEFFICIENT_LIMIT + 1},
        'ordinary_transform_logarithmic_coefficients': {'powers': [1, COEFFICIENT_LIMIT], 'arithmetic': 'exact rationals'},
        'prime_congruences': {'primes_at_most': PRIME_LIMIT, 'primes_matched': len(primes),
                              'identities': ['Bala A130095', 'Somos A007435']},
        'parity_limit_samples': {'decimal_precision': 500, 'samples': parity_samples,
                                'coverage': 'Finite illustrations of the two written limiting formulas.'},
        'coverage': 'Finite checks supplement the written all-index proofs; limits follow from the proofs, not a finite prefix.',
        'verify_py_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
