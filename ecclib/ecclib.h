#pragma once

#ifdef ECCLIB_EXPORTS
#define ECCLIB_API __declspec(dllexport)
#else
#define ECCLIB_API __declspec(dllimport)
#endif


namespace EccLib
{
	class Functions
	{
	public:
		static ECCLIB_API void DummyEncode(unsigned char data[20], unsigned char encoded[20]);
		static ECCLIB_API void DummyDecode(unsigned char data[20], unsigned char decoded[20]);
	};

	class BCH
	{
	public:
		static ECCLIB_API void Encode(unsigned char data[506], unsigned char encoded[512]);
		static ECCLIB_API void Decode(unsigned char data[512], unsigned char decoded[506]);
	};
}