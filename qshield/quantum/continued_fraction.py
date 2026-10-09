import math
from fractions import Fraction
from typing import Optional

def extract_order_from_measurement(s: int, Q: int, N: int, a: int) -> Optional[int]:
    """
    Applies the continued fractions algorithm to convert measured phase s/Q into
    the candidate period r of f(x) = a^x mod N.
    """
    if s == 0:
        return None

    # Find rational approximation s/Q with denominator <= N
    frac = Fraction(int(s), int(Q)).limit_denominator(int(N))
    candidate_r = int(frac.denominator)

    # Check if a^r = 1 mod N
    if pow(int(a), candidate_r, int(N)) == 1:
        return candidate_r

    # Test small integer multiples of the denominator
    for multiplier in range(2, 6):
        test_r = candidate_r * multiplier
        if pow(int(a), test_r, int(N)) == 1:
            return test_r

    return None
