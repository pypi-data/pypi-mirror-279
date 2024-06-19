#pragma once

#include <algorithm>
#include <map>
#include <optional>
#include <vector>

#include "akida/hardware_ident.h"
#include "akida/hardware_type.h"
#include "akida/shape.h"

namespace akida {

struct NpSpace {
  Index x;
  Index y;
  Shape shape;
};

namespace hw {

struct NpMapping {
  NpMapping(const NpSpace& in_int, const NpSpace& in_aug, Index start_n,
            Index neurons, bool single_buf)
      : start_neuron(start_n),
        num_neurons(neurons),
        input_int(in_int),
        input_aug(in_aug),
        single_buffer(single_buf) {}
  NpMapping(const Shape& shape, Index start_n, Index neurons, bool single_buf)
      : start_neuron(start_n),
        num_neurons(neurons),
        input_int{0, 0, shape},
        input_aug{0, 0, shape},
        single_buffer(single_buf) {}

  Index start_neuron;
  Index num_neurons;
  // Internal input box
  NpSpace input_int;
  // Augmented input box
  NpSpace input_aug;
  // Use single buffer or dual ping-pong buffer
  bool single_buffer;
};

struct SkipDmaMapping {
  uint8_t channel_index;
};

struct Component {
  static Component create_np(hw::Type np_type, const NpSpace& in_int,
                             const NpSpace& in_aug, Index start_n,
                             Index neurons, bool single_buf, hw::Ident np_id) {
    Component component(np_type, np_id);
    component.np = NpMapping(in_int, in_aug, start_n, neurons, single_buf);
    return component;
  }

  static Component create_np(hw::Type np_type, const Shape& shape,
                             Index start_n, Index neurons, bool single_buf,
                             hw::Ident np_id) {
    Component component(np_type, np_id);
    component.np = NpMapping(shape, start_n, neurons, single_buf);
    return component;
  }

  static Component create_hrc() { return Component(hw::Type::HRC, HRC_IDENT); }

  static Component create_skip_dma(hw::Ident id) {
    return Component(hw::Type::SKIP_DMA, id);
  }

  static Component create_vit_block(hw::Ident id) {
    return Component(hw::Type::VIT_BLOCK, id);
  }

  static Component create_dma(hw::Ident id) {
    return Component(hw::Type::none, id);
  }

  hw::Type type;
  hw::Ident id;
  std::optional<NpMapping> np = std::nullopt;
  std::optional<SkipDmaMapping> skip_dma = std::nullopt;

 private:
  explicit Component(hw::Type comp_type, hw::Ident comp_id)
      : type(comp_type), id(comp_id) {}
};

}  // namespace hw

// utility function to find the leftmost or rightmost NPs
inline uint8_t find_border_column(const std::vector<hw::Component>& nps,
                                  bool find_left) {
  auto border_np = *std::min_element(
      nps.begin(), nps.end(),
      [find_left](const hw::Component& left, const hw::Component& right) {
        return find_left ? left.id.col < right.id.col
                         : left.id.col > right.id.col;
      });
  return border_np.id.col;
}

}  // namespace akida
