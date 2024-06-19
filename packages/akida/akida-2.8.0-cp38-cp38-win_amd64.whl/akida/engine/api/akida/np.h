#pragma once

#include <memory>
#include <vector>

#include "hardware_ident.h"
#include "hardware_type.h"

namespace akida::np {

constexpr bool is_cnp(hw::Type type) {
  return type == hw::Type::CNP1 || type == hw::Type::CNP2;
}

constexpr bool is_fnp(hw::Type type) {
  return type == hw::Type::FNP2 || type == hw::Type::FNP3;
}

struct Info {
  hw::Ident ident;
  hw::Types types;
};

struct SkipDmaInfo {
  SkipDmaInfo(const std::vector<hw::Ident>& id, const uint8_t ch_num)
      : idents(id), channels_num(ch_num) {}

  std::vector<hw::Ident> idents;
  uint8_t channels_num;
};

/**
 * The layout of a mesh of Neural Processors
 */
struct Mesh {
  hw::Ident dma_event;                    /**<The DMA event endpoint */
  hw::Ident dma_conf;                     /**<The DMA configuration endpoint */
  std::vector<Info> nps;                  /**<The available Neural Processors */
  std::shared_ptr<SkipDmaInfo> skip_dmas; /**<The available skip dmas */
};

}  // namespace akida::np
