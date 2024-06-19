#pragma once

#include <cstdint>
#include <vector>

namespace akida::hw {

struct Ident {
  uint8_t col;
  uint8_t row;
  uint8_t id;
  bool operator==(const Ident& other) const {
    return col == other.col && row == other.row && id == other.id;
  }
  bool operator!=(const Ident& other) const { return !(*this == other); }
  bool operator<(const Ident& other) const {
    return (col < other.col) || ((col == other.col) && (row < other.row)) ||
           ((col == other.col) && (row == other.row) && (id < other.id));
  }
};

using IdentVector = std::vector<Ident>;

constexpr Ident HRC_IDENT = Ident{0, 0, 0};

}  // namespace akida::hw