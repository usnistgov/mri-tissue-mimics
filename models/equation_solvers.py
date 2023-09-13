import sympy
import numpy as np


def solve_sympy_equations(equations, variables, starting_point=None):
    if starting_point is None:
        starting_point = [0.1, 0.1]
    return sympy.nsolve(equations, variables, starting_point,
                        verify=False)  # verify = False is used when the eq is very steep


def solve_quad_eq_positive_only(a, b, c):
    solutions = []
    if a == 0:
        concentration = -c / b
        if concentration > 0:
            solutions = [concentration]
    else:
        intercepts = np.array([(-b + np.sqrt(b ** 2 - 4 * a * c)) / 2 / a,
                                   (-b - np.sqrt(b ** 2 - 4 * a * c)) / 2 / a])
        intercepts = intercepts[intercepts > 0]
        if len(intercepts) > 0:
            solutions = list(intercepts)
    return solutions
