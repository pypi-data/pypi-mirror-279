#strong inequivalence for monadic recursion

from itertools import product


def check_inequivalence(F, P, G, f0, S1, S2):
    domain = range(2)  # Domain set D containing {0, 1}

    for interpretation in product(domain, repeat=len(F)):
        interpretations = dict(zip(F, interpretation))
        interpretations[f0] = 0  # Interpret f0 as 0 initially

        if not check_recursive_definition(interpretations, P, G, S1):
            return True  # S1 is undefined

        interpretations[f0] = 1  # Interpret f0 as 1 initially

        if not check_recursive_definition(interpretations, P, G, S2):
            return True  # S2 is undefined

        if interpretations[f0] != S2[f0]:
            return True  # Values for f0 differ

    return False


def check_recursive_definition(interpretations, P, G, S):
    for f in G:
        if f in S:
            p, alb = S[f]

            if p(interpretations) and not alb_defined(alb, interpretations, G):
                return False  # S is undefined for f

    return True


def alb_defined(alb, interpretations, G):
    for symbol in alb:
        if symbol in G and interpretations[symbol] != interpretations[symbol]:
            return False  # Some symbol in alb is undefined

    return True


# Example instance
F = {'f1', 'f2'}
P = {'p1', 'p2'}
G = {'g1', 'g2'}
f0 = 'g1'
S1 = {'g1': ('p1', ('f1',)), 'g2': ('p2', ('f1', 'g1'))}
S2 = {'g1': ('p1', ('f1',)), 'g2': ('p2', ('f2', 'g1'))}

# Check strong inequivalence
result = check_inequivalence(F, P, G, f0, S1, S2)
print("The two monadic recursion schemes are" + (" not" if result else "") + " strongly inequivalent.")
