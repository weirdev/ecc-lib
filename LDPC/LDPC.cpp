// LDPC.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "LDPC.h"

namespace LDPC
{
	LDPC_API std::vector<byte>* Encode(std::vector<byte> data)
	{
		return &data;
	}

	LDPC_API std::vector<byte>* Decode(std::vector<byte> data)
	{
		return &data;
	}
}