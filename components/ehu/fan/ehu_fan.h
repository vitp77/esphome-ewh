#pragma once

#include "esphome/core/component.h"
#include "esphome/components/fan/fan.h"

#include "esphome/components/sensor/sensor.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/binary_sensor/binary_sensor.h"

#include "../ehu_component.h"

namespace esphome {
namespace ehu {

class EHUFan : public EHUComponent, public fan::Fan {
 public:
  explicit EHUFan(EHUApi *api) : EHUComponent(api) {}

  void dump_config() override;
  fan::FanTraits get_traits() override;
  void control(const fan::FanCall &call) override;

  void on_state(const ehu_state_t &state) override;

  void set_temperature_sensor(sensor::Sensor *temperature) { this->temperature_ = temperature; }
  void set_humidity_sensor(sensor::Sensor *humidity) { this->humidity_ = humidity; }

  void set_warm_mist_switch(switch_::Switch *warm_mist) { this->warm_mist_ = warm_mist; }
  void set_uv_switch(switch_::Switch *uv) { this->uv_ = uv; }
  void set_ionizer_switch(switch_::Switch *ionizer) { this->ionizer_ = ionizer; }
  void set_lock_switch(switch_::Switch *lock) { this->lock_ = lock; }
  void set_sound_switch(switch_::Switch *sound) { this->sound_ = sound; }

  void set_water_binary_sensor(binary_sensor::BinarySensor *water) { this->water_ = water; }

 protected:
  sensor::Sensor *temperature_{};
  sensor::Sensor *humidity_{};

  switch_::Switch *warm_mist_{};
  switch_::Switch *uv_{};
  switch_::Switch *ionizer_{};
  switch_::Switch *lock_{};
  switch_::Switch *sound_{};

  binary_sensor::BinarySensor *water_{};

  template<class T, typename V> inline void publish_state_(T *var, V val) {
    if (var != nullptr && static_cast<V>(var->state) != val) {
      var->publish_state(val);
    }
  }
};
#ifdef USE_SWITCH
class EHUSwitch : public switch_::Switch, public Component {
 public:
  EHUSwitch(EHUApi *api) : api_(api) {}
  void write_state(bool state) override {
    // TODO do api write
  }

 protected:
  EHUApi *api_;
};

#endif
}  // namespace ehu
}  // namespace esphome
