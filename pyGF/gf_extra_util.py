"""
Random galois field related functions not used as part of other processes. 
"""

from binary_math import BinaryVector
from gf import polyproductmonicdeg1vectorpolys, conjugates

def find_prim_elements(m):
    primeles = []
    e = BinaryVector(m, 2)
    i = 2
    while i < 2**(m+1):
        if is_primitive_element(e):
                primeles.append(e)
        i += 1
        e = e.addwithcarry(1)
    return primeles


def is_primitive_element(e):
    return irreducible(e) and divides_pow_x_n_m1(e)

def irreducible(e):
    raise NotImplementedError()

def divides_pow_x_n_m1(e):
    unity = BinaryVector(e.m, 1)
    checkorder = 1
    remainder = unity

    while checkorder < 2**e.m - 1:
        ccp = BinaryVector(checkorder)
        ccp.coeff[0] = ccp.coeff[-1] = 1
        remainder = ccp % e
        if DEBUG:
            print("CO", checkorder)
            print("Rem", remainder)
            print("CCP", ccp)
            print("E", e)
        if remainder.iszero():
            return False
        checkorder += 1
    ccp = BinaryVector(checkorder)
    ccp.coeff[0] = ccp.coeff[-1] = 1
    remainder = ccp % e
    if DEBUG:
        print("CO", checkorder)
        print("Rem", remainder)
        print("CCP", ccp)
        print("E", e)
    return remainder.iszero()

def minpoly(vector, gf):
    conj = conjugates(vector, gf)
    return polyproductmonicdeg1vectorpolys(conj, gf)