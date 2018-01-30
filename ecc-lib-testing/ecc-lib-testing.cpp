// https://docs.microsoft.com/en-us/cpp/build/walkthrough-creating-and-using-a-dynamic-link-library-cpp

#include "stdafx.h"
#include "ecc-lib-testing.h"

int main()
{
	test_matrix_encode();
	int s;
	std::cin >> s;
    return 0;
}

void testdummyencode() {
	unsigned char* data = &randomdata(20)[0];
	unsigned char encodeddata[20];
	EccLib::Functions::DummyEncode(data, encodeddata);
	comparearrays(data, encodeddata, 20);
	unsigned char decodeddata[20];
	EccLib::Functions::DummyDecode(encodeddata, decodeddata);
	comparearrays(data, decodeddata, 20);
}

std::vector<unsigned char> randomdata(int len) 
{
	std::random_device rd;   // non-deterministic generator  
	std::mt19937 gen(rd());  // to seed mersenne twister.
	std::uniform_int_distribution<> dist(0,255);
	std::vector<unsigned char> data;
	data.reserve(len);
	for (int i = 0; i < len; ++i)
	{
		data.push_back(dist(gen));
	}
	return data;
}

void comparearrays(unsigned char* v1, unsigned char* v2, unsigned int size)
{
	for (unsigned int i=0; i < size; ++i)
	{
		if (v1[i] != v2[i])
		{
			std::cout << "diffval" << std::endl;
			break;
		}
	}
	std::cout << "success" << std::endl;
}

void testload_matrix()
{
	EccLib::BinaryMatrix bm = EccLib::BinaryMatrix::Load(R"(C:\Users\Wesley\dev\ecc-lib\pyGF\test6mat)");
	for (int col = 0; col < 10; col++) {
		std::cout << "col " << col << std::endl;
		int row = 0;
		while (!bm.GetElement(row, col)) {
			row++;
		}
		std::cout << "True row " << row << std::endl;
	}
}

void test_matrix_encode()
{
	EccLib::BinaryMatrix bm = EccLib::BinaryMatrix::Load(R"(C:\Users\Wesley\dev\ecc-lib\pyGF\test6mat)");
	unsigned char* data = new unsigned char[6];
	for (int i = 0; i < 6; i++)
	{
		data[i] = (unsigned char)(i+1);
	}
	unsigned char* encoded = bm.MultiplyVector(data);
	for (int i = 0; i < 8; i++)
	{
		std::cout << (int)encoded[i] << std::endl;
	}
}

