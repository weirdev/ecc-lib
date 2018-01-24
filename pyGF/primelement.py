from gfmath import BinaryVector, bitlisttoint, inttobitlist
import numpy as np
import scipy.linalg

DEBUG = False

def findprimelements(m):
    primeles = []
    e = BinaryVector(m, 2)
    i = 2
    while i < 2**(m+1):
        if is_primitive_element:
                primeles.append(e)
        i += 1
        e = e.addwithcarry(1)
    return primeles

def is_primitive_element(e):
    return irreducible(e) and divides_pow_x_n_m1(e)

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

def irreducible(e):
    div = BinaryVector(e.degree, 2)
    while div.degree < e.degree:
        if (e % div).iszero():
            return str(div), str(e % div)
        div = div.addwithcarry(1)
    return True

def make_GF(primitive_polynomial):
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
    return GF

def minpoly(vector, gf):
    conj = conjugates(vector, gf)
    return polyproductmonicdeg1vectorpolys(conj, gf)

def minpolyrootvectterms(vector, gf):
    return conjugates(vector, gf)

def polyproductmonicdeg1vectorpolys(vectorterms, gf):
    m = gf[0].m + 1
    fieldorder = 2**m - 1
    vectorpoly = [BinaryVector(m-1) for _ in range(len(vectorterms) + 1)]
    vectorpoly[0] += 1
    gfexpbyvect = {v: exp for exp, v in enumerate(gf[1:])}
    # Vector poly = 1
    # For each root, multiply vector poly by (root + x)
    for root in vectorterms:
        # Vector poly times root
        vptr = []
        for term in vectorpoly:
            if not term.iszero():
                vptr.append(gf[((gfexpbyvect[term] + gfexpbyvect[root]) % fieldorder) + 1])
            else:
                vptr.append(BinaryVector(m-1))
        # Vector poly times x (the term we drop should always be zero, as the degree of vectorpoly increases by only 1 each iteration)
        vptx = [BinaryVector(m-1)] + vectorpoly[:-1]
        vectorpoly = [tr + tx for tr, tx in zip(vptr, vptx)]
    for term in vectorpoly:
        if not term.iszero() and term != 1:
            raise Exception("Coefficients should come from GF(2)")
    return BinaryVector(m, [1 if t==1 else 0 for t in vectorpoly])

def conjugates(vector, gf):
    m = vector.m + 1
    fieldorder = 2**m - 1
    vexp = gf.index(vector) - 1
    conj = []
    for _ in range(m):
        conj.append(gf[vexp + 1])
        vexp = (vexp * 2) % fieldorder
    if gf[vexp + 1] == vector:
        return conj
    raise Exception("vector^(2^m) should == vector")

def BCH_generatorpoly(t, gf):
    genpolyrootterms = set()
    # Add as roots the roots of the minimum polynomials of alpha^1, alpha^3, ..., alpha^(2*t-1)
    for exp in range(1, 2*t, 2):
        genpolyrootterms.update(minpolyrootvectterms(gf[exp + 1], gf))
    return polyproductmonicdeg1vectorpolys(genpolyrootterms, gf)

def generatormatrix(n, k, genpoly, systematic=True):
    genmat = scipy.linalg.toeplitz([1]+[0]*(k-1), genpoly.coeff + [0]*(k-1))
    if not systematic:
        return genmat
    else:
        return reduce_echlonform(genmat)
    
def reduce_echlonform(echlonform_matrix):
    matrix = echlonform_matrix
    for column in range(1, min(matrix.shape)): # Each column that has an element on the main diagonal
        for row in range(0, column):
            if matrix[row, column]:
                matrix[row] = matrix[row] ^ matrix[column]
    return matrix

def writegenmatrix(matrix, filename):
    with open(filename, 'wb') as matrixfile:
        # num rows, num columns
        matrixfile.write(matrix.shape[0].to_bytes(4, byteorder='big'))
        matrixfile.write(matrix.shape[1].to_bytes(4, byteorder='big'))

        rows = matrix.shape[0]
        byteremainder = rows % 8

        if byteremainder != 0:
            z = np.zeros((matrix.shape[0] + byteremainder, matrix.shape[1]), np.bool)
            z[:-byteremainder,:] = matrix
            matrix = z
            rows += byteremainder
        for column in matrix.T:
            matrixfile.write(bytearray(bitlisttoint(column[bl*8:bl*8+8]) for bl in range(rows // 8)))
        
def readgenmatrix(filename):
    with open(filename, 'rb') as matrixfile:
        rows = int.from_bytes(matrixfile.read(4), byteorder='big')
        columns = int.from_bytes(matrixfile.read(4), byteorder='big')
        matrix = np.ndarray((rows, columns), np.bool)
        paddedrows = rows
        byteremainder = rows % 8
        if rows % 8 != 0:
            paddedrows += 8 - (rows % 8)
        for column in matrix.T:
            cbytes = matrixfile.read(paddedrows // 8)
            for j, b in enumerate(cbytes):
                if (j+1)*8 < rows:
                    bits = inttobitlist(b)
                    bits += [0] * (8-len(bits))
                    column[j*8:(j+1)*8] = bits
                else:
                    bits = inttobitlist(b)
                    bits += [0] * (byteremainder-len(bits))
                    column[j*8:] = bits
    return matrix

if __name__ == "__main__":
    pp12 = BinaryVector(12, 7185)
    #pp5 = BinaryVector(5, 37)
    #pp6 = BinaryVector(6, 67)
    #gf5 = make_GF(pp5)
    #gf6 = make_GF(pp6)
    gf12 = make_GF(pp12)
    #gp6 = BCH_generatorpoly(3, gf6)
    gp12 = BCH_generatorpoly(4, gf12)
    gm12 = generatormatrix(2**12 - 1, 2**12 - 1 - 48, gp12)
    print(gm12.shape)
    #gm6 = generatormatrix(2**6 - 1, 2**6 - 1 - 18, gp6)

    writegenmatrix(gm12, '4095_4047_matrix')
    rm = readgenmatrix("4095_4047_matrix")
    print(rm)
    print(True if np.array_equal(rm, gm12) else False)
