#pragma once

#include <string>

class BinaryMatrix
{
public:
	int rows;
	int columns;

	BinaryMatrix Load(std::string file);

	const unsigned char* MultiplyVector(const unsigned char* data);

private:
	BinaryMatrix(int rows, int columns);

	int _memrows;
	int _memcolumns;
	unsigned char** _matrix;
};