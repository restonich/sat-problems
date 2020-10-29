import argparse
from pysat.solvers import Glucose4

def build_formula(n, k):
    formula = []
    variables = {}
    n += 1
    k += 1

    # Match each variable with distinct number
    cur = 1
    for i in range(1, n-1):
        for j in range(i+1, n):
            for c in range(1, k):
                variables[(i,j,c)] = cur
                cur += 1

    # Rule that each edge is painted
    S1 = []
    for i in range(1, n-1):
        for j in range(i+1, n):
            disjunct = []
            for c in range(1, k):
                disjunct.append(variables[(i,j,c)])

            S1.append(disjunct)

    formula.extend(S1)

    # Rule that each edge is painted in exactly one color
    S2 = []
    for i in range(1, n-1):
        for j in range(i+1, n):
            for c1 in range(1, k-1):
                disjunct = []
                for c2 in range(c1+1, k):
                    disjunct.append(-variables[(i,j,c1)])
                    disjunct.append(-variables[(i,j,c2)])

                S2.append(disjunct)

    formula.extend(S2)

    # Rule that each triangle is not painted in one color
    S3 = []
    for i in range(1, n-2):
        for j in range(i+1, n-1):
            for l in range(j+1, n):
                for c in range(1, k):
                    disjunct = []
                    disjunct.append(-variables[(i,j,c)])
                    disjunct.append(-variables[(j,l,c)])
                    disjunct.append(-variables[(i,l,c)])
                    S3.append(disjunct)

    formula.extend(S3)

    return formula

def find_clique(k):
    max_clique = 2
    n = 2

    while True:
        formula = build_formula(n, k)

        with Glucose4(bootstrap_with=formula) as solver:
            if solver.solve():
                max_clique = n
            else:
                break

        print("Clique of size {} for {} color(s) exists".format(n, k))
        n += 1

    print("--------")
    print("Clique of size {} is maximum for {} color(s)".format(max_clique, k))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Finds max clique painted in COLORS colors such that each triangle is not painted in one color")
    parser.add_argument('k', metavar='COLORS', type=int, help="Number of colors")

    args = parser.parse_args()

    if args.k < 1:
        raise Exception("COLORS should be > 0")

    find_clique(args.k)

