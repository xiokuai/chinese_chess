#pragma once
#include <cstdint>

class ZobristHasher {
public:
    ZobristHasher();
    uint64_t getHash(int board[10][9]) const;

private:
    uint64_t zobristTable[10][9][17]; // 16 pieces + 1 for empty
};