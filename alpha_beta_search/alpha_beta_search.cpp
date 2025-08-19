/// alpha-beta search

#include <algorithm>
#include <unordered_map>
#include <utility>
#include <vector>
#include <string>
#include <cmath>
#include <mutex>

#include "alpha_beta_search.h"
#include "zobrist_hasher.h"

// the coordinate of chess
using Coordinate = std::pair<int, int>;

// a valid operation
using Operation = std::pair<Coordinate, Coordinate>;

ZobristHasher zobristHasher; // Zobrist hashing for board state


// score of each chess
constexpr int SCORE_TABLE[9] = {
	{0},        // ?
	{10000},      // 帥
	{2},        // 仕
	{2},        // 相
	{1},        // 兵
	{2},        // 兵(过河)
	{5},        // 馬
	{6},        // 砲
	{9},       //  车
};


const std::unordered_map<int, std::vector<Coordinate>> DELTA = {
	{1, {{0, 1}, {0, -1}, {1, 0}, {-1, 0}}},
	{2, {{-1, -1}, {-1, 1}, {1, 1}, {1, -1}}},
	{3, {{-2, -2}, {-2, 2}, {2, 2}, {2, -2}}},
	{6, {{1, 2}, {1, -2}, {-1, 2}, {-1, -2}, {2, 1}, {2, -1}, {-2, 1}, {-2, -1}}},
	{71, {{1, 0}, {2, 0}, {3, 0}, {4, 0}, {5, 0}, {6, 0}, {7, 0}, {8, 0}, {9, 0}}},
	{72, {{-1, 0}, {-2, 0}, {-3, 0}, {-4, 0}, {-5, 0}, {-6, 0}, {-7, 0}, {-8, 0}, {-9, 0}}},
	{73, {{0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}, {0, 8}}},
	{74, {{0, -1}, {0, -2}, {0, -3}, {0, -4}, {0, -5}, {0, -6}, {0, -7}, {0, -8}}},
};


// default Operation
constexpr Operation OPERATION = { {-1, -1}, {-1, -1} };


// Node of the min-max searching tree
class Node {
public:
	float score;
	Operation operation;

	Node(float score, Operation operation = OPERATION) 
		: score(score), operation(operation) {}
};


// Cache for evaluation results
static std::unordered_map<uint64_t, float> evaluation_cache;
std::mutex evaluation_cache_mutex; // Mutex for thread-safe access to the cache

// Optimized evaluate function
static inline float evaluate(int data[10][9]) {
	uint64_t hash = zobristHasher.getHash(data);
	
	std::lock_guard<std::mutex> lock(evaluation_cache_mutex);

	auto it = evaluation_cache.find(hash);
	if (it != evaluation_cache.end()) {
		return it->second;
	}

	float score = 0.0f;
	for (int i = 0; i < 10; ++i) {
		for (int j = 0; j < 9; ++j) {
			int value = data[i][j];
			score += value < 0 ? -SCORE_TABLE[-value] : SCORE_TABLE[value];
		}
	}

	evaluation_cache[hash] = score;
	return score;
}


// get all valid coordinates on board
static inline std::vector<Coordinate> valid_coordinate(int data[10][9], bool reverse = false) {
	std::vector<Coordinate> valid_coordinates;
	for (int i = 0; i < 10; ++i)
		for (int j = 0; j < 9; ++j)
			if ((reverse && data[i][j] < 0) || (!reverse && data[i][j] > 0))
				valid_coordinates.emplace_back( i, j );
	return valid_coordinates;
}


// change the data of board
static inline void process(int data[10][9], int si, int sj, int ei, int ej) {
	int piece = data[si][sj];
	data[si][sj] = 0;
	data[ei][ej] = piece;

	int promote = (piece == -4) * (ei >= 5) * -1 + (piece == 4) * (ei <= 4);
	data[ei][ej] += promote;
}

// Optimized possible_destination function
static std::vector<Coordinate> possible_destination(int data[10][9], int i, int j) {
	std::vector<Coordinate> possible_destinations;
	int id = data[i][j];
	int abs_id = std::abs(id);
	int ni, nj;

	int _delta[3][2] = { {id < 0 ? 1 : -1, 0}, { 0, 1 }, {0, -1} };

	switch (abs_id) {
	case 1:
		for (const auto& delta : DELTA.at(1)) {
			ni = i + delta.first;
			nj = j + delta.second;
			if (((0 <= ni && ni <= 2) || (7 <= ni && ni <= 9)) && 3 <= nj && nj <= 5)
				if (id * data[ni][nj] <= 0)
					possible_destinations.emplace_back(ni, nj);
		}
		break;

	case 2:
		for (const auto& delta : DELTA.at(2)) {
			ni = i + delta.first;
			nj = j + delta.second;
			if (((0 <= ni && ni <= 2) || (7 <= ni && ni <= 9)) && 3 <= nj && nj <= 5)
				if (id * data[ni][nj] <= 0)
					possible_destinations.emplace_back(ni, nj);
		}
		break;

	case 3:
		for (const auto& delta : DELTA.at(3)) {
			ni = i + delta.first;
			nj = j + delta.second;
			if (0 <= ni && ni <= 9 && 0 <= nj && nj <= 8 && (i < 5 ? ni < 5 : ni > 4))
				if (id * data[ni][nj] <= 0)
					if (data[(ni + i) / 2][(nj + j) / 2] == 0)
						possible_destinations.emplace_back(ni, nj);
		}
		break;

	case 4:
		ni = i + (id < 0 ? 1 : -1), nj = j;
		if (id * data[ni][nj] <= 0)
			possible_destinations.emplace_back(ni, nj);
		break;

	case 5:
		for (const auto& delta : _delta) {
			ni = i + delta[0], nj = j + delta[1];
			if (0 <= ni && ni <= 9 && 0 <= nj && nj <= 8)
				if (id * data[ni][nj] <= 0)
					possible_destinations.emplace_back(ni, nj);
		}
		break;

	case 6:
		for (const auto& delta : DELTA.at(6)) {
			ni = i + delta.first;
			nj = j + delta.second;
			if (0 <= ni && ni <= 9 && 0 <= nj && nj <= 8)
				if (id * data[ni][nj] <= 0) {
					int mid_i = i + delta.first / 2, mid_j = j + delta.second / 2;
					if (data[mid_i][mid_j] == 0)
						possible_destinations.emplace_back(ni, nj);
				}
		}
		break;

	case 7:
		for (const auto& deltas : { DELTA.at(71), DELTA.at(72), DELTA.at(73), DELTA.at(74) }) {
			bool stepping_stone = false;
			for (auto& delta : deltas) {
				ni = i + delta.first;
				nj = j + delta.second;
				if (0 <= ni && ni <= 9 && 0 <= nj && nj <= 8) {
					if (stepping_stone) {
						int key = id * data[ni][nj];
						if (key != 0) {
							if (key < 0) {
								possible_destinations.emplace_back(ni, nj);
								break;
							}
							else break;
						}
					}
					else {
						if (id * data[ni][nj] != 0) stepping_stone = true;
						else possible_destinations.emplace_back(ni, nj);
					}
				}
			}
		}
		break;

	case 8:
		for (const auto& deltas : { DELTA.at(71), DELTA.at(72), DELTA.at(73), DELTA.at(74) }) {
			for (auto& delta : deltas) {
				ni = i + delta.first, nj = j + delta.second;
				if (0 <= ni && ni <= 9 && 0 <= nj && nj <= 8) {
					if (id * data[ni][nj] == 0)
						possible_destinations.emplace_back(ni, nj);
					else if (id * data[ni][nj] < 0) {
						possible_destinations.emplace_back(ni, nj);
						break;
					}
					else break;
				}
			}
		}
		break;

	default:
		throw id;
	}

	return possible_destinations;
}


// recover the data of board after operating
static inline void recover(int data[10][9], int si, int sj, int ei, int ej, int sv, int ev) {
	data[si][sj] = sv;
	data[ei][ej] = ev;
}


// Optimized valid_operation function
static bool valid_operation(int data[10][9], Operation operation) {
	int si = operation.first.first, sj = operation.first.second;
	int ei = operation.second.first, ej = operation.second.second;
	bool reverse = data[si][sj] < 0;
	int key_id = reverse ? -1 : 1;
	int sv = data[si][sj], ev = data[ei][ej];

	process(data, si, sj, ei, ej);

	std::vector<Coordinate> valid_coordinates = valid_coordinate(data, !reverse);
	for (const auto& coordinate : valid_coordinates) {
		if (std::abs(data[coordinate.first][coordinate.second]) >= 5) {
			for (const auto& destination : possible_destination(data, coordinate.first, coordinate.second)) {
				if (data[destination.first][destination.second] == key_id) {
					recover(data, si, sj, ei, ej, sv, ev);
					return false;
				}
			}
		}
	}

	for (int i = 0; i < 3; ++i) {
		for (int j = 3; j <= 5; ++j) {
			if (data[i][j] == -1) {
				for (int ni = i + 1; ni < 10; ++ni) {
					if (data[ni][j] == 0) continue;
					if (data[ni][j] == 1) {
						recover(data, si, sj, ei, ej, sv, ev);
						return false;
					}
					break;
				}
			}
		}
	}

	recover(data, si, sj, ei, ej, sv, ev);
	return true;
}


// get all operations
static std::vector<Operation> get_operations(int data[10][9], bool reverse = false) {
	std::vector<Operation> valid_operations;

	auto get_valid_destinations = [&](int x, int y) {
		std::vector<std::pair<int, int>> destinations;
		for (const auto& destination : possible_destination(data, x, y)) {
			Operation op{ {x, y}, destination };
			if (valid_operation(data, op)) {
				destinations.push_back(destination);
			}
		}
		return destinations;
		};

	for (const auto& coordinate : valid_coordinate(data, reverse)) {
		for (const auto& destination : get_valid_destinations(coordinate.first, coordinate.second)) {
			valid_operations.emplace_back(Operation{ coordinate, destination });
		}
	}

	std::sort(valid_operations.begin(), valid_operations.end(), [&data](const Operation& a, const Operation& b) {
		int a_score = SCORE_TABLE[abs(data[a.second.first][a.second.second])];
		int b_score = SCORE_TABLE[(abs(data[b.second.first][b.second.second]))];
		return a_score > b_score;
		});

	return valid_operations;
}


// update the data of node
static inline std::pair<float, float> update(Node& node, Node& child, const Operation& op, float alpha, float beta, bool reverse = false) {
	float temp = node.score;
	if (!reverse)
		alpha = node.score = std::max(node.score, child.score);
	else
		beta = node.score = std::min(node.score, child.score);
	if (node.score != temp)
		node.operation = op;
	return { alpha, beta };
}


// Optimized alpha_beta_search function
static Node alpha_beta_search(int data[10][9], int depth, bool reverse = false, float alpha = -INFINITY, float beta = INFINITY) {
	if (depth == 0) {
		float score = evaluate(data);
		return Node(score);
	}
	
	Node node = Node(reverse ? beta : alpha);
	auto operations = get_operations(data, reverse);
	for (const auto& op : operations) {
		int si = op.first.first, sj = op.first.second, ei = op.second.first, ej = op.second.second;
		int sv = data[si][sj], ev = data[ei][ej];
		process(data, si, sj, ei, ej);
		Node child = alpha_beta_search(data, depth - 1, !reverse, alpha, beta);
		std::tie(alpha, beta) = update(node, child, op, alpha, beta, reverse);
		recover(data, si, sj, ei, ej, sv, ev);
		if (alpha >= beta) break;
	}

	return node;
}


// API for Python
extern "C" DLL_EXPORT float search(int data[10][9], int depth, int result[4], bool reverse) {
	Node node = alpha_beta_search(data, depth, reverse);
	if (node.operation == OPERATION) {
		std::vector<Operation> operations = get_operations(data, reverse);
		if (!operations.empty())
		node.operation = get_operations(data, reverse)[0];
	}
	result[0] = node.operation.first.first;
	result[1] = node.operation.first.second;
	result[2] = node.operation.second.first;
	result[3] = node.operation.second.second;
	return node.score;
}


// API for Python
extern "C" DLL_EXPORT void all_operations(int data[10][9], int i, int j, int operation[18][2]) {
	for (int i = 0; i < 18; ++i)
		operation[i][0] = -1;
	int count = 0;
	for (auto& destination : possible_destination(data, i, j))
		if (valid_operation(data, { { i, j }, destination })) {
			std::tie(operation[count][0], operation[count][1]) = destination;
			++count;
		}
}
