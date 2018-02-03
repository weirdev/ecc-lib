from binary_math import BinaryVector

class GaloisField:
    def __init__(self, primitive_polynomial):
        m = primitive_polynomial.m
        GF = []
        GF.append(BinaryVector(m - 1))
        for i in range(m):
            GF.append(BinaryVector(m - 1, 2**i))
        GF.append(BinaryVector(m-1, primitive_polynomial.coeff[:-1]))
        for i in range(2**m-m-2):
            powm = GF[-1].coeff[-1] == 1
            new = GF[-1] >> 1
            if powm:
                new += GF[m+1]
            GF.append(new)
        self._GF = GF

    def index(self, value):
        for i, v in enumerate(self):
            if value == v:
                return i
        raise ValueError()

    def __len__(self):
        return len(self._GF)

    def __getitem__(self, idx):
        return self._GF[idx]
    
    def __setitem__(self, idx, value):
        self._GF[idx] = value

    def __iter__(self):
        return iter(self._GF)
