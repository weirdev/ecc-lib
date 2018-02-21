from binary_math import BinaryVector, bitlisttoint, inttobitlist
from gf import GaloisField
import numpy as np
import scipy.linalg
import array
import sys
import operator

DEBUG = False

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

def BCH_generatormatrix(n, k, genpoly, systematic=True):
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

"""
bits = '100000001'
padded_bits = bits + '0' * (8 - len(bits) % 8)
padded_bits
    '1000000010000000'
list(int(padded_bits, 2).to_bytes(len(padded_bits) // 8, 'big'))
    [128, 128]
"""

def writegenmatrix(matrix, filename):
    with open(filename, 'wb') as matrixfile:
        # num rows, num columns
        matrixfile.write(matrix.shape[0].to_bytes(4, byteorder='little'))
        matrixfile.write(matrix.shape[1].to_bytes(4, byteorder='little'))

        rows = matrix.shape[0]
        byteremainder = 8 - (rows % 8)

        if byteremainder != 8:
            z = np.zeros((matrix.shape[0] + byteremainder, matrix.shape[1]), np.bool)
            z[:-byteremainder,:] = matrix
            matrix = z
            rows += byteremainder
        for column in matrix.T:
            matrixfile.write(bytearray(bitlisttoint(column[bl*8:bl*8+8]) for bl in range(rows // 8)))
            # ###In column[bl*8:bl*8+8][::-1], the [::-1]
        
def readgenmatrix(filename):
    with open(filename, 'rb') as matrixfile:
        rows = int.from_bytes(matrixfile.read(4), byteorder='little')
        columns = int.from_bytes(matrixfile.read(4), byteorder='little')
        matrix = np.ndarray((rows, columns), np.bool)
        paddedrows = rows
        byteremainder = 8 - (rows % 8)
        if rows % 8 != 0:
            paddedrows += byteremainder
        for column in matrix.T:
            cbytes = matrixfile.read(paddedrows // 8)
            for j, byte in enumerate(cbytes):
                if (j+1)*8 < rows:
                    bits = inttobitlist(byte)
                    bits += [0] * (8-len(bits))
                    column[j*8:(j+1)*8] = bits
                else:
                    bits = inttobitlist(byte)
                    bits += [0] * (8-byteremainder-len(bits))
                    column[j*8:] = bits
    return matrix

def BCH_paritycheckmatrix(gf, m, t):
    # Each element of the parity check matrix (H) is a BinaryVector
    # Representing an element of GF(2^m)
    def H_fromlocation(y , x):
        return gf[((y+1)*x)%(2**m-1)+1]
    
    return np.fromfunction(np.vectorize(H_fromlocation), (2*t, 2**m-1), dtype=BinaryVector)

def writeparitycheckmatrix(matrix, m, filename):
    def gfelementtobytes(e):
        byteremainder = (8 - (e.m+1) % 8) % 8
        bits = e.coeff + [0] * byteremainder
        return bytearray(bitlisttoint(e.coeff[bl*8:bl*8+8]) for bl in range(len(bits) // 8))
        

    with open(filename, 'wb') as matrixfile:
        # num rows, num columns
        matrixfile.write(matrix.shape[0].to_bytes(4, byteorder='little'))
        matrixfile.write(matrix.shape[1].to_bytes(4, byteorder='little'))
        # m = number of bits per matrix element
        matrixfile.write(m.to_bytes(4, byteorder='little'))

        for row in matrix:
            for element in row:
                matrixfile.write(gfelementtobytes(element))

def readparitycheckmatrix(filename):
    def bytestogfelement(bs, m):
        coeffs = []
        for b in bs:
            bl = inttobitlist(b)
            coeffs.extend(bl)
            coeffs.extend([0]*(8-len(bl)))
        return BinaryVector(m-1, coeffs[:m])

    with open(filename, 'rb') as matrixfile:
        rows = int.from_bytes(matrixfile.read(4), byteorder='little')
        columns = int.from_bytes(matrixfile.read(4), byteorder='little')
        m = int.from_bytes(matrixfile.read(4), byteorder='little')
        matrix = np.ndarray((rows, columns), BinaryVector)

        bytesperelement = (m + ((8 - m % 8) % 8)) // 8

        for r in range(rows):
            for c in range(columns):
                matrix[r][c] = bytestogfelement(matrixfile.read(bytesperelement), m)
        return matrix

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test" or sys.argv[1] == "6":
            pp6 = BinaryVector(6, 67)
            gf6 = GaloisField(pp6)
            gp6 = BCH_generatorpoly(3, gf6)
            gm6 = BCH_generatormatrix(2**6 - 1, 2**6 - 1 - 18, gp6)
            writegenmatrix(gm6, 'test6mat')
            #rm = readgenmatrix("test6mat")
            #print(True if np.array_equal(rm, gm6) else False)
        elif sys.argv[1] == "large" or sys.argv[1] == "12":
            pp12 = BinaryVector(12, 7185)
            gf12 = GaloisField(pp12)
            gp12 = BCH_generatorpoly(4, gf12)
            gm12 = BCH_generatormatrix(2**12 - 1, 2**12 - 1 - 48, gp12)
            writegenmatrix(gm12, '4095_4047_matrix')
            #rm = readgenmatrix("4095_4047_matrix")
            #print(True if np.array_equal(rm, gm12) else False)
        elif sys.argv[1] == "Htest" or sys.argv[1] == "H6":
            pp6 = BinaryVector(6, 67)
            gf6 = GaloisField(pp6)
            H6 = BCH_paritycheckmatrix(gf6, 6, 3)
            writeparitycheckmatrix(H6, 6, "pc6mat")
            rm = readparitycheckmatrix("pc6mat")
            print(rm)
            print(True if np.array_equal(rm, H6) else False)
        elif sys.argv[1] == "Hlarge" or sys.argv[1] == "H12":
            pp12 = BinaryVector(12, 7185)
            gf12 = GaloisField(pp12)
            H12 = BCH_paritycheckmatrix(gf12, 12, 4)
            writeparitycheckmatrix(H12, 12, "4095_4047_check_matrix")
            rm = readparitycheckmatrix("4095_4047_check_matrix")
            print(True if np.array_equal(rm, H12) else False)
        else:
            print("Unknown parameter name \"{}\"".format(sys.argv[1]))
    else:
        print("Missing required argument")

    #pp5 = BinaryVector(5, 37)
    #gf5 = make_GF(pp5)
