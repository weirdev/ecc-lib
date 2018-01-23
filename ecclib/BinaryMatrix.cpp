#include "stdafx.h"
#include "BinaryMatrix.h"

// Dont use bitset -- offers poor sequential access
// ~2MB to store matrix in bytes containing 8 bits of data each
// ~16MB to store matrix with each bit in its own byte
// Start by implementing with compressed storage
// Need to decide on internal data structure, single array or array of arrays
// Leaning to array of arrays
BinaryMatrix::BinaryMatrix(int rows, int columns)
{

}

BinaryMatrix BinaryMatrix::Load(std::string file, int rows, int columns)
{
	return BinaryMatrix(rows, columns);
}

const unsigned char* BinaryMatrix::MultiplyVector(const unsigned char* data)
{
	return data;
}
