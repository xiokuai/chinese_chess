#pragma once

#ifdef _WIN32
    #define DLL_EXPORT __declspec(dllexport)
#else
    #define DLL_EXPORT
#endif

extern "C" DLL_EXPORT float search(int data[10][9], int depth, int result[4], bool reverse = false);
extern "C" DLL_EXPORT void all_operations(int data[10][9], int i, int j, int operation[18][2]);
