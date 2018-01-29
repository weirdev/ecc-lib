#pragma once

#ifndef BINARYMATRIX_H
#define BINARYMATRIX_H
#include "ecclib.h"
#include <string>
#include <fstream>
#include <iterator>
#include <vector>
#include <iostream>
#endif


namespace EccLib
{
	class BinaryMatrix
	{
	public:
		int rows;
		int columns;

		static ECCLIB_API BinaryMatrix Load(std::string file);

		unsigned char* MultiplyVector(unsigned char* data);
		bool ECCLIB_API GetElement(int row, int column);

	private:
		BinaryMatrix(int rows, int columns);

		int _memrows;
		unsigned char** _matrix;
	};
}