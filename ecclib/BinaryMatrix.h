#pragma once

#include <string>

class BinaryMatrix
{
	BinaryMatrix(int rows, int columns);

	BinaryMatrix Load(std::string file, int rows, int columns);

	const unsigned char* MultiplyVector(const unsigned char* data);

};