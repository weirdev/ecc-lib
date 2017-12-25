from gfmath import BinaryVector

def findprimelements(m):
    primeles = []
    e = BinaryVector(m, 2)
    i = 2
    while i < m**2:
        if isprimelement(e):
            primeles.append(e)
        e += 1
        i += 1
    return primeles

def isprimelement(e):
    zero = BinaryVector(e.m)
    unity = BinaryVector(e.m, 1)
    eorder = 2
    print("e: {}".format(e))
    ep = BinaryVector(e)
    while ep != unity and ep != zero:
        eorder += 1
        ep *= e
        print(ep)
    return eorder == (2**e.m - 1)

if __name__ == "__main__":
    for e in findprimelements(1):
        print(e)