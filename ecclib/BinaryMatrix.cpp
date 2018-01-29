#include "stdafx.h"
#include "BinaryMatrix.h"

// Dont use bitset -- offers poor sequential access
// ~2MB to store matrix in bytes containing 8 bits of data each
// ~16MB to store matrix with each bit in its own byte
// Start by implementing with compressed storage
// Need to decide on internal data structure, single array or array of arrays
// Leaning to array of arrays

namespace EccLib
{
	// TODO: Handle systems with non 8-bit words
	// TODO: Standardize byteorder/support 
	// _matrix is defined as an array of columns, not rows
	BinaryMatrix::BinaryMatrix(int r, int c)
	{
		std::cout << r << std::endl;
		int s;
		std::cin >> s;
		this->rows = r;
		this->columns = c;

		this->_memrows = (int)r / 8;
		if (r % 8 != 0) {
			this->_memrows++;
		}

		this->_matrix = new unsigned char*[c];
		for (int i = 0; i < c; i++)
		{
			this->_matrix[i] = new unsigned char[this->_memrows];
		}
	}

	BinaryMatrix BinaryMatrix::Load(std::string file)
	{
		std::ifstream input(file, std::ios::binary);
		// copies all data into buffer
		std::vector<unsigned char> buffer((
			std::istreambuf_iterator<char>(input)),
			(std::istreambuf_iterator<char>()));
		
		int r = 0;
		int idx = 3;
		for (; idx >= 0; idx--)
		{
			r = (r << 8) | buffer[idx];
		}
		std::cout << "r " << r << std::endl;
		int c = 0;
		idx = 7;
		for (; idx >= 4; idx--)
		{
			c = (c << 8) | buffer[idx];
		}
		std::cout << "c " << c << std::endl;
		BinaryMatrix bm = BinaryMatrix(r, c);
		idx = 8;
		for (int i=0; i < bm.columns; i++)
		{
			for (int j = 0; j < bm._memrows; j++)
			{
				bm._matrix[i][j] = buffer[idx];
				idx++;
			}
		}
		return bm;
	}

	bool BinaryMatrix::GetElement(int row, int column)
	{
		unsigned char cell = this->_matrix[column][(int)row / 8];
		std::cout << "cell " << (int)cell << std::endl;
		return (cell & (1 << (row % 8))) != 0;
	}

	unsigned char* BinaryMatrix::MultiplyVector(unsigned char* data)
	{
		return data;
	}
}