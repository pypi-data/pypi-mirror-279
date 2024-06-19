#pragma once

#include <set>

namespace akida::hw {

enum class BasicType { none, HRC, CNP, FNP, VIT_BLOCK, SKIP_DMA };
enum class Type { none, HRC, CNP1, CNP2, FNP2, FNP3, VIT_BLOCK, SKIP_DMA };
using Types = std::set<Type>;

}  // namespace akida::hw