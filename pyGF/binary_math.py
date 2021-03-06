import math
import binascii
import numpy as np
# Methods for performing polynomial arithmetic in GF(2^m)


class BinaryVector:
    def __init__(self, *args):
        if len(args) == 0:
            raise Exception()
        elif len(args) == 1:
            if isinstance(args[0], BinaryVector):
                self.m = args[0].m
                self.coeff = list(args[0].coeff)
            elif isinstance(args[0], int):
                self.m = args[0]
                self.coeff = [0] * (self.m + 1)
            elif hasattr(args[0], "__len__") and len(args[0]) > 0 and isinstance(args[0][0], np.integer):
                self.coeff = args[0]
                self.m = len(self.coeff) - 1
            else:
                raise Exception()
        elif len(args) == 2:
            self.m = args[0]
            if isinstance(args[1], int):
                self.coeff = inttobitlist(int(args[1]))
                self.coeff += [0]*(self.m + 1 - len(self.coeff))
            else:
                self.coeff = list(args[1])

    def addwithcarry(self, other):
        if isinstance(other, BinaryVector):
            if other.m != self.m:
                raise Exception("Vectors must be of same size. Sizes {} and {}".format(self.m, other.m))
            carry = 0
            s = BinaryVector(self.m)
            for i in range(self.m + 1):
                ss = self.coeff[i] + other.coeff[i] + carry
                s.coeff[i] = ss % 2
                carry = 1 if ss >= 2 else 0
            return s
        else:
            return self.addwithcarry(BinaryVector(self.m, other))
        
    def __add__(self, other):
        if isinstance(other, BinaryVector):
            if other.m > self.m:
                raise Exception("Right vector must not be larger than left vector. Sizes {} and {}".format(self.m, other.m))
            s = BinaryVector(self.m)
            for i in range(other.m + 1):
                s.coeff[i] = self.coeff[i] ^ other.coeff[i]
            return s
        else:
            return self + BinaryVector(self.m, other)

    def __sub__(self, other):
        return self + other

    def __mul__(self, other):
        if other.m != self.m:
            raise Exception("Vectors must be of same max order. Sizes {} and {}".format(self.m, other.m))
        modvect = BinaryVector(self.m + 1)
        modvect.coeff[0] = modvect.coeff[-1] = 1
        p = BinaryVector(self.m * 2)
        for i, b1 in enumerate(self.coeff):
            carry = 0
            pp = BinaryVector(self.m * 2)
            for j, b2 in enumerate(other.coeff):
                pp.coeff[i + j] = b1 & b2
            p += pp
            p %= modvect
        return BinaryVector(self.m, p.coeff[:self.m+1])

    def __mod__(self, other):
        if other.iszero():
            raise ZeroDivisionError()
        other = BinaryVector(other)
        retm = other.m
        while other.coeff[-1] == 0:
            other.m -= 1
            other.coeff = other.coeff[:-1]
        remainder = BinaryVector(self)
        if other.m > self.m:
            return remainder
        pos = self.m + 1
        while pos >= other.m + 1:
            if remainder.coeff[pos - 1] == 1:
                diff = BinaryVector(other.m, remainder.coeff[pos - other.m - 1:pos])
                diff += other
                remainder.coeff[pos - other.m - 1:pos] = diff.coeff
            pos -= 1
        return BinaryVector(retm, remainder.coeff[:retm+1])

    def iszero(self):
        return sum(self.coeff) == 0

    @property
    def degree(self):
        for i in range(self.m):
            if self.coeff[-i-1] != 0:
                return self.m - i
        return 0

    def __rshift__(self, y):
        shifted = BinaryVector(self)
        if y != 0:
            shifted.coeff[y:] = shifted.coeff[:-y]
            shifted.coeff[:y] = [0]*y
        return shifted

    def __eq__(self, other):
        if isinstance(other, BinaryVector):
            if other.m != self.m:
                raise Exception("Fields must be of same size.")
            return self.coeff == other.coeff
        else:
            return self == BinaryVector(self.m, other)

    def __str__(self):
        return str(self.coeff)

    def __repr__(self):
        return repr(self.coeff)

    def __hash__(self):
        return hash(tuple(self.coeff))

    def __int__(self):
        return bitlisttoint(self.coeff)

def inttobitlist(x):
    return [1 if digit=='1' else 0 for digit in bin(x)[2:][::-1]]

def bitlisttoint(bitlist, x=0, degree=0):
    return int(''.join('1' if b else '0' for b in bitlist[::-1]), 2)

if __name__ == "__main__":
    f1 = BinaryVector(2, [0, 0, 1])
    f2 = BinaryVector(2, [1, 1, 0])
    f3 = BinaryVector(2, [1, 1, 1, 0, 1, 1, 1, 0])
    f4 = BinaryVector(f1)
    print(f4)
    print(f3)
    print(f1 + f2)
    print(f1 * f2)
    print((f1 + 1) == (f1 + 1))