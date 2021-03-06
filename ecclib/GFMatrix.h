#pragma once

#ifndef GFMATRIX_H
#define GFMATRIX_H
#include "ecclib.h"
#include <string>
#include <fstream>
#include <iterator>
#include <vector>

namespace EccLib
{
	class GFMatrix
	{
	public:
		int rows;
		int columns;
		int m;
		unsigned char* primitive_polynomial;

		static ECCLIB_API GFMatrix* Load(std::string file);

		ECCLIB_API unsigned char* GetElement(int row, int column);
		ECCLIB_API unsigned char** MultiplyVector(unsigned char* data);
		static ECCLIB_API bool ElementZero(unsigned char* element, int m);
		
	private:
		GFMatrix(int rows, int columns, int m, unsigned char* primpoly);

		int _elementbytes;
		unsigned char** _matrix;
	};
}

#endif