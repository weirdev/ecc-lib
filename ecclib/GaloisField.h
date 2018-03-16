#pragma once

#ifndef GALOISFIELD_H
#define GALOISFIELD_H

#include <stdexcept>

namespace EccLib
{
	class GaloisField
	{
	public:
		GaloisField(unsigned char* primitive_polynomial, int m);
		unsigned char* MultiplyGFElements(unsigned char* e1, unsigned char* e2);
		unsigned char* InvertGFElement(unsigned char* e);
		bool GFElementsEqual(unsigned char* e1, unsigned char* e2);
		unsigned char** GF;
	private:
		int* fieldpositions; // Int to int mapping of gfelements to their powers
		int m;
		int m_bytes;
		unsigned char* LeftShiftGFElement(unsigned char* e);
		int GFElementAsInt(unsigned char* e);
	};
}

#endif