#pragma once

#ifndef GFMATRIX_H
#define GFMATRIX_H
#include "ecclib.h"
#include <string>
#include <fstream>
#include <iterator>
#include <vector>
#include <iostream>

namespace EccLib
{
	class GFMatrix
	{
	public:
		int rows;
		int columns;
		int m;

		static ECCLIB_API GFMatrix* Load(std::string file);

		ECCLIB_API unsigned char* GetElement(int row, int column);
		ECCLIB_API unsigned char** MultiplyVector(unsigned char* data);
		static ECCLIB_API bool ElementZero(unsigned char* element, int m);
		
	private:
		GFMatrix(int rows, int columns, int m);

		int _elementbytes;
		unsigned char** _matrix;
	};
}


#endif