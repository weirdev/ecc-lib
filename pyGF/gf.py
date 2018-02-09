from binary_math import BinaryVector

class GaloisField:
    def __init__(self, primitive_polynomial):
        m = primitive_polynomial.m
        GF = []
        # Zero
        GF.append(BinaryVector(m - 1))
        # alpha^i for i = 0..m-1
        for i in range(m):
            GF.append(BinaryVector(m - 1, 2**i))
        # alpha^m always equals the first m terms of the primitive 
        # polynomial with which the field is constructed
        GF.append(BinaryVector(m-1, primitive_polynomial.coeff[:-1]))
        # alpha^i for i = m+1..(2^m)-1
        for _ in range(2**m-m-2):
            # alpha^(i+1) = (alpha^i)*alpha
            # if alpha^i has component alpha^(m-1)
            # then alpha(i+1) would have component alpha^(m) which is not allowed
            # thus we add alpha^m's components to the other components of alpha^(i+1)
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
