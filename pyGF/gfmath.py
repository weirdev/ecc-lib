import math
import binascii
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
                self.coeff = [0] * self.m
            else:
                raise Exception()
        elif len(args) == 2:
            self.m = args[0]
            if isinstance(args[1], int):
                self.coeff = inttobitlist(args[1])
                self.coeff += [0]*(self.m-len(self.coeff))
            else:
                self.coeff = list(args[1])
        
    def __add__(self, other):
        if isinstance(other, BinaryVector):
            if other.m != self.m:
                raise Exception("Vectors must be of same size. Sizes {} and {}".format(self.m, other.m))
            carry = 0
            s = BinaryVector(self.m)
            for i in range(self.m):
                s.coeff[i] = self.coeff[i] ^ other.coeff[i]
            return s
        else:
            return self + BinaryVector(self.m, other)

    def __mul__(self, other):
        if other.m != self.m:
            raise Exception("Vectors must be of same size. Sizes {} and {}".format(self.m, other.m))
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
        return BinaryVector(self.m, p.coeff[:self.m])

    def __mod__(self, other):
        if other.coeff[-1] == 0:
            raise Exception("Leading coefficient cannot be zero.")
        remainder = BinaryVector(self.m, self.coeff)
        if other.m > self.m:
            return remainder
        pos = self.m        
        while pos >= other.m:
            if remainder.coeff[pos - 1] == 1:
                diff = BinaryVector(other.m, remainder.coeff[pos-other.m:pos])
                diff += other
                remainder.coeff[pos-other.m:pos] = diff.coeff
            pos -= 1
        return remainder

    def __eq__(self, other):
        if other.m != self.m:
            raise Exception("Fields must be of same size.")
        return self.coeff == other.coeff

    def __str__(self):
        return str(self.coeff)

def inttobitlist(x, bitlist=[]):
    if x == 0:
        if len(bitlist) > 0:
            return bitlist
        return [0]
    bitlist.append(x % 2)
    return inttobitlist(x//2, bitlist)

if __name__ == "__main__":
    f1 = BinaryVector(3, [0, 0, 1])
    f2 = BinaryVector(3, [1, 1, 0])
    f3 = BinaryVector(3, [1, 1, 1, 0, 1, 1, 1, 0])
    print(f3)
    print(f1 + f2)
    print(f1 * f2)
    print((f1 + 1) == (f1 + 1))