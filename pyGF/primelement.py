from gfmath import BinaryVector

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

if __name__ == "__main__":
    pp12 = BinaryVector(12, 7185)
    pp5 = BinaryVector(5, 37)
    pp6 = BinaryVector(6, 67)
    gf5 = make_GF(pp5)
    gf6 = make_GF(pp6)
    #print(conjugates(BinaryVector(4, [0,0,0,1,0]), gf5))
    gf12 = make_GF(pp12)
    #print(minpolyrootvectterms(BinaryVector(4, [0,0,0,1,0]), gf5))
    print(int(BCH_generatorpoly(4, gf12)))