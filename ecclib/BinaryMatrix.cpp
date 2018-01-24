#include "stdafx.h"
#include "BinaryMatrix.h"

// Dont use bitset -- offers poor sequential access
// ~2MB to store matrix in bytes containing 8 bits of data each
// ~16MB to store matrix with each bit in its own byte
// Start by implementing with compressed storage
// Need to decide on internal data structure, single array or array of arrays
// Leaning to array of arrays
#include <fstream>
#include <iterator>
#include <vector>

// TODO: Handle systems with non 8-bit words
// TODO: Standardize byteorder/support 
// _matrix is defined as an array of columns, not rows
BinaryMatrix::BinaryMatrix(int rows, int columns)
{
	BinaryMatrix::rows = rows;
	BinaryMatrix::columns = columns;

	BinaryMatrix::_memrows = (int)rows / 8;
	BinaryMatrix::_memcolumns = (int)columns / 8;

	BinaryMatrix::_matrix = new unsigned char*[_memcolumns];
	for (int i = 0; i < BinaryMatrix::_memcolumns; i++)
	{
		BinaryMatrix::_matrix[i] = new unsigned char[_memrows];
	}
}

BinaryMatrix BinaryMatrix::Load(std::string file)
{
	std::ifstream input(file, std::ios::binary);
	// copies all data into buffer
	std::vector<char> buffer((
		std::istreambuf_iterator<char>(input)),
		(std::istreambuf_iterator<char>()));


	BinaryMatrix bm = BinaryMatrix(buffer[0], buffer[1]);
	int idx = 2;

	for (int i; i < _memcolumns; i++)
	{
		for (int j = 0; j < _memrows; j++)
		{
			bm._matrix[i][j] = buffer[idx];
			idx++;
		}
	}
}

const unsigned char* BinaryMatrix::MultiplyVector(const unsigned char* data)
{
	return data;
}
