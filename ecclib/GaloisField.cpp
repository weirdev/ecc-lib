#include "stdafx.h"
#include "GaloisField.h"

namespace EccLib
{
	GaloisField::GaloisField(unsigned char* primitive_polynomial, int m)
	{
		int m_bytes = m / 8;
		int rem = m % 8;
		if (rem != 0)
		{
			m_bytes++;
		}
		this->m = m;
		this->m_bytes;
		int elementcount = (1 << m) + 1;
		unsigned char** gf = new unsigned char*[elementcount];
		this->fieldpositions = new int[elementcount];
		// gf[0] = 0
		gf[0] = new unsigned char[m_bytes];
		for (int e = 0; e < m_bytes; e++)
		{
			gf[0][e] = 0;
			this->fieldpositions[0] = 0;
		}
		// gf[i] = 2**(i-1) for i = 1...m
		gf[1] = new unsigned char[m_bytes];
		gf[1][0] = 1;
		for (int e = 1; e < m_bytes; e++)
		{
			gf[1][e] = 0;
		}
		this->fieldpositions[1] = 1;
		for (int i = 2; i < m+1; i++)
		{
			gf[i] = LeftShiftGFElement(gf[i - 1]);
			this->fieldpositions[1 << (i - 1)] = i;
		}
		// gf[m+1] = trailing terms of primitive polynomial
		gf[m + 1] = primitive_polynomial;
		if (rem == 0)
		{
			gf[m + 1] = new unsigned char[m_bytes];
			for (int e = 0; e < m_bytes - 1; e++)
			{
				gf[m + 1][e] = primitive_polynomial[e];
			}
		}
		else
		{
			gf[m + 1] = primitive_polynomial;
			gf[m + 1][m_bytes - 1] ^= 1 << rem;
		}
		this->fieldpositions[GFElementAsInt(gf[m + 1])] = m + 1;
		// gf[k] for k=m+2...2^m-1+2
		for (int i = m + 2; i < elementcount; i++)
		{
			bool carry;
			if (rem == 0)
			{
				carry = (gf[i - 1][m_bytes - 1] & 8) != 0;
			}
			else
			{
				carry = (gf[i - 1][m_bytes - 1] & (1 << (rem - 1))) != 0;
			}
			gf[i] = LeftShiftGFElement(gf[i - 1]);
			if (carry)
			{
				if (rem != 0)
				{
					gf[i][m_bytes - 1] ^= (1 << rem);
				}
				for (int e = 0; e < m_bytes; e++)
				{
					gf[i][e] ^= gf[m + 1][e];
				}
			}
			this->fieldpositions[GFElementAsInt(gf[i])] = i;
		}
		this->GF = gf;
	}
	unsigned char* GaloisField::MultiplyGFElements(unsigned char * e1, unsigned char * e2)
	{
		int e1power = GFElementAsInt(e1) - 1;
		int e2power = GFElementAsInt(e2) - 1;
		if (e1power == -1 || e2power == -1)
		{
			return GF[0];
		}
		return this->GF[((e1power + e2power) % (1 << m)) + 1];
	}
	unsigned char * GaloisField::InvertGFElement(unsigned char * e)
	{
		int epower = GFElementAsInt(e) - 1;
		if (epower == -1)
		{
			throw std::invalid_argument("Cannot invert zero element");
		}
		if (epower == 0)
		{
			return GF[1];
		}
		return this->GF[(1 << m) - epower + 1];
	}
	unsigned char* GaloisField::LeftShiftGFElement(unsigned char* e)
	{
		unsigned char* shifte = new unsigned char[this->m_bytes];
		bool carry;
		for (int i = 0; i < this->m_bytes - 1; i++)
		{
			bool carrynext = (e[i] & 8) != 0;
			shifte[i] = e[i] << 1;
			if (carry)
			{
				shifte[i] |= 1;
			}
			carry = carrynext;
		}
		shifte[this->m_bytes - 1] = e[this->m_bytes - 1] << 1;
		if (carry)
		{
			shifte[this->m_bytes - 1] |= 1;
		}
		int rem = m % 8;
		if (rem != 0)
		{
			shifte[this->m_bytes - 1] ^= (1 << rem);
		}
		return shifte;
	}

	int GaloisField::GFElementAsInt(unsigned char* e)
	{
		int val = 0;
		for (int i = 0; i < this->m_bytes; i++)
		{
			val += e[i] << (i * 8);
		}
		return val;
	}
	
	bool GaloisField::GFElementsEqual(unsigned char * e1, unsigned char * e2)
	{
		for (int i = 0; i < this->m_bytes; i++)
		{
			if (e1[i] != e2[i])
			{
				return false;
			}
		}
		return true;
	}
}
