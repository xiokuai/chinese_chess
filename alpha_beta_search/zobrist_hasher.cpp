#include "zobrist_hasher.h"
#include <random>

constexpr int OFFSET = 8; // Unsigned

ZobristHasher::ZobristHasher() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<uint64_t> dis;

    for (int x = 0; x < 10; ++x) {
        for (int y = 0; y < 9; ++y) {
            for (int piece = 1; piece <= 16; ++piece) {
                zobristTable[x][y][piece+OFFSET] = dis(gen);
             }
        }
    }
}

uint64_t ZobristHasher::getHash(int board[10][9]) const {
    uint64_t hash = 0;

    for (int x = 0; x < 10; ++x) {
        for (int y = 0; y < 9; ++y) {
            int piece = board[x][y];
            if (piece != 0) {
                int pieceIndex = piece + OFFSET; 
                hash ^= zobristTable[x][y][pieceIndex];
            }
        }
    }
    return hash;
}