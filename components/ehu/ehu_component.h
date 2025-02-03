#pragma once

#include "esphome/core/component.h"

#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/switch/switch.h"

#ifdef USE_TIME
#include "esphome/components/time/real_time_clock.h"
#endif

#include "../rka_api/rka_component.h"
#include "ehu_api.h"

namespace esphome {
namespace ehu {

using EHUComponentBase = rka_api::RKAComponent<rka_api::rka_dev_type_t::EHU, EHUListener, EHUApi, PollingComponent>;

class EHUComponent : public EHUComponentBase {
  template<uint16_t cmd_v> friend class EHUSwitch;
  friend class EHUWarmMistSwitch;
  friend class EHUUVSwitch;

 public:
  explicit EHUComponent(EHUApi *api) : EHUComponentBase(api) {}
  void on_state(const ehu_state_t &state) override;

  void update() override { this->api_->request_state_ex(); }

#ifdef USE_TIME
  void set_time_id(esphome::time::RealTimeClock *time) { this->time_ = time; }
#endif

  void set_temperature_sensor(sensor::Sensor *temperature) { this->temperature_ = temperature; }
  void set_humidity_sensor(sensor::Sensor *humidity) { this->humidity_ = humidity; }

  void set_warm_mist_switch(switch_::Switch *warm_mist) { this->warm_mist_ = warm_mist; }
  void set_uv_switch(switch_::Switch *uv) { this->uv_ = uv; }
  void set_ionizer_switch(switch_::Switch *ionizer) { this->ionizer_ = ionizer; }
  void set_lock_switch(switch_::Switch *lock) { this->lock_ = lock; }
  void set_mute_switch(switch_::Switch *mute) { this->mute_ = mute; }

  void set_water_binary_sensor(binary_sensor::BinarySensor *water) { this->water_ = water; }

 protected:
#ifdef USE_TIME
  esphome::time::RealTimeClock *time_{};
#endif

  sensor::Sensor *temperature_{};
  sensor::Sensor *humidity_{};

  switch_::Switch *warm_mist_{};
  switch_::Switch *uv_{};
  switch_::Switch *ionizer_{};
  switch_::Switch *lock_{};
  switch_::Switch *mute_{};

  binary_sensor::BinarySensor *water_{};

  template<class T, typename V> inline void publish_state_(T *var, V val) {
    if (var != nullptr && static_cast<V>(var->state) != val) {
      var->publish_state(val);
    }
  }
};

template<uint16_t cmd_v> class EHUSwitch : public switch_::Switch, public Component, public Parented<EHUComponent> {
 public:
  EHUSwitch(EHUComponent *c) : Parented(c) {}
  void write_state(bool state) override { this->write_byte_(state); }

 protected:
  void write_byte_(uint8_t data) {
    if (cmd_v != 0) {
      this->parent_->api_->write_byte(cmd_v, data);
    }
  }
};

template<uint16_t state_flag_first_v, uint16_t state_flag_second_v>
class EHUWaterSwitchBase : public EHUSwitch<ehu_packet_type_t::PACKET_REQ_SET_WARM_MIST_UV> {
 protected:
  EHUWaterSwitchBase(EHUComponent *c, switch_::Switch *second) : EHUSwitch(c) {}

 public:
  void write_state(bool state) override {
    uint8_t data = 0;
    if (state) {
      data |= state_flag_first_v;
    }
    if (this->second_ && this->second_->state) {
      data |= state_flag_second_v;
    }
    this->write_byte_(data);
  }

 protected:
  switch_::Switch *second_{};
};

class EHUWarmMistSwitch : public EHUWaterSwitchBase<ehu_state_t::WATER_WARM_MIST, ehu_state_t::WATER_UV> {
 public:
  EHUWarmMistSwitch(EHUComponent *c) : EHUWaterSwitchBase(c, c->uv_) {}
};

class EHUUVSwitch : public EHUWaterSwitchBase<ehu_state_t::WATER_UV, ehu_state_t::WATER_WARM_MIST> {
 public:
  EHUUVSwitch(EHUComponent *c) : EHUWaterSwitchBase(c, c->warm_mist_) {}
};

}  // namespace ehu
}  // namespace esphome
