// ecclib.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "ecclib.h"

namespace EccLib
{
	void Functions::DummyEncode(unsigned char data[20], unsigned char encoded[20])
	{
		for (int i = 0; i < 20; i++)
		{
			encoded[i] = data[i];
		}
	}

	void Functions::DummyDecode(unsigned char data[20], unsigned char decoded[20])
	{
		for (int i = 0; i < 20; i++)
		{
			decoded[i] = data[i];
		}
	}

	void BCH::Encode(unsigned char data[506], unsigned char encoded[512])
	{

	}

	void BCH::Decode(unsigned char data[512], unsigned char decoded[506])
	{

	}
}