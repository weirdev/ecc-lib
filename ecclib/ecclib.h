#pragma once

#ifdef ECCLIB_EXPORTS
#define ECCLIB_API __declspec(dllexport)
#else
#define ECCLIB_API __declspec(dllimport)
#endif

#ifndef ECCLIB_H
#define ECCLIB_H

#include <string>

namespace EccLib
{
	class BinaryMatrix;
	class GFMatrix;

	class Functions
	{
	public:
		static ECCLIB_API void DummyEncode(unsigned char data[20], unsigned char encoded[20]);
		static ECCLIB_API void DummyDecode(unsigned char data[20], unsigned char decoded[20]);
	};

	class BCH
	{
	public:
		ECCLIB_API BCH(std::string generatormatrixfile, std::string paritycheckmatrixfile, int m, int t);
		ECCLIB_API unsigned char* Encode(unsigned char* data);
		ECCLIB_API unsigned char* Decode(unsigned char* data);

		// Temporarily public for testing
		ECCLIB_API unsigned char** ComputeSyndrome(unsigned char* data);
		ECCLIB_API bool CheckSyndrome(unsigned char** syndrome);
		ECCLIB_API unsigned char* ComputErrorLocationPolynomial(unsigned char** syndrome);
	private:
		BinaryMatrix* _generatormatrix;
		GFMatrix* _paritycheckmatrix;
		int t;
		int m;
	};
}


#endif