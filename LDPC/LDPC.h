#pragma once

#ifdef LDPC_EXPORTS
#define LDPC_API __declspec(dllexport)
#else
#define LDPC_API __declspec(dllimport)
#endif

using byte = unsigned char;

namespace LDPC
{
	LDPC_API std::vector<byte>* Encode(std::vector<byte> data);
	LDPC_API std::vector<byte>* Decode(std::vector<byte> data);
}