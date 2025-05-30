import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, fan, number, select, sensor, time
from esphome.components import switch as eh_switch
from esphome.const import (
    CONF_HUMIDITY,
    CONF_ID,
    CONF_NAME,
    CONF_PRESET,
    CONF_SPEED,
    CONF_TEMPERATURE,
    CONF_TIME_ID,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_MOISTURE,
    DEVICE_CLASS_RUNNING,
    DEVICE_CLASS_TEMPERATURE,
    ENTITY_CATEGORY_CONFIG,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_PERCENT,
)

from .. import rka_api  # pylint: disable=relative-beyond-top-level

CODEOWNERS = ["@dentra"]
AUTO_LOAD = [
    "rka_api",
    "switch",
    "binary_sensor",
    "sensor",
    "time",
    "fan",
    "number",
    "select",
]

CONF_EHU_ID = "ehu_id"

ICON_HUMIDIFIER = "mdi:air-humidifier"
ICON_CLOCK = "mdi:clock"

CONF_WARM_MIST = "warm_mist"
CONF_UV = "uv"
CONF_IONIZER = "ionizer"
CONF_LOCK = "lock"
CONF_MUTE = "mute"
CONF_WATER = "water"
CONF_HUMIDIFICATION = "humidification"
CONF_FAN = "fan"
CONF_TARGET_HUMIDITY = "target_humidity"
CONF_LED_BRIGHTNESS = "led_brightness"
CONF_LED_PRESET = "led_preset"
CONF_LED_TOP = "led_top"
CONF_LED_BOTTOM = "led_bottom"

rka_ns = rka_api.rka_ns
ehu_ns = cg.esphome_ns.namespace("ehu")

EHUApi = ehu_ns.class_("EHUApi", cg.Component)
EHUComponent = ehu_ns.class_("EHUComponent", cg.Component)
EHUState = ehu_ns.struct("ehu_state_t")

EHUSwitch = ehu_ns.class_("EHUSwitch", eh_switch.Switch, cg.Component)
EHUDependedSwitch = ehu_ns.class_("EHUDependedSwitch", eh_switch.Switch, cg.Component)
EHUFan = ehu_ns.class_("EHUFan", fan.Fan, cg.Component)
EHUFanPreset = ehu_ns.class_("EHUFanPreset", select.Select, cg.Component)
EHUNumber = ehu_ns.class_("EHUNumber", number.Number, cg.Component)
EHULedPreset = ehu_ns.class_("EHULedPreset", select.Select, cg.Component)
EHUBrightnessNumber = ehu_ns.class_("EHUBrightnessNumber", number.Number, cg.Component)

EHUPacketType = ehu_ns.enum("ehu_packet_type_t", is_class=True)
EHUStateType = ehu_ns.enum("ehu_state_t", is_class=True)

CONFIG_SCHEMA = rka_api.api_schema(
    EHUApi, trigger_class=rka_api.update_trigger(EHUApi, EHUState)
)

EHU_COMPONENT_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_EHU_ID): cv.use_id(EHUApi),
        cv.GenerateID(CONF_TIME_ID): cv.use_id(time.RealTimeClock),
        cv.Optional(CONF_TEMPERATURE): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_HUMIDITY): cv.maybe_simple_value(
            sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_HUMIDITY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_WARM_MIST): cv.maybe_simple_value(
            eh_switch.switch_schema(
                EHUDependedSwitch.template(
                    EHUPacketType.PACKET_REQ_SET_WARM_MIST_UV,
                    EHUStateType.WATER_WARM_MIST,
                    EHUStateType.WATER_UV,
                ),
                entity_category=ENTITY_CATEGORY_CONFIG,
                block_inverted=True,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_UV): cv.maybe_simple_value(
            eh_switch.switch_schema(
                EHUDependedSwitch.template(
                    EHUPacketType.PACKET_REQ_SET_WARM_MIST_UV,
                    EHUStateType.WATER_UV,
                    EHUStateType.WATER_WARM_MIST,
                ),
                entity_category=ENTITY_CATEGORY_CONFIG,
                block_inverted=True,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_IONIZER): cv.maybe_simple_value(
            eh_switch.switch_schema(
                EHUSwitch.template(EHUPacketType.PACKET_REQ_SET_IONIZER),
                entity_category=ENTITY_CATEGORY_CONFIG,
                block_inverted=True,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_LOCK): cv.maybe_simple_value(
            eh_switch.switch_schema(
                EHUSwitch.template(EHUPacketType.PACKET_REQ_SET_LOCK),
                entity_category=ENTITY_CATEGORY_CONFIG,
                block_inverted=True,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_MUTE): cv.maybe_simple_value(
            eh_switch.switch_schema(
                EHUSwitch.template(EHUPacketType.PACKET_REQ_SET_MUTE),
                entity_category=ENTITY_CATEGORY_CONFIG,
                block_inverted=True,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_WATER): cv.maybe_simple_value(
            binary_sensor.binary_sensor_schema(device_class=DEVICE_CLASS_MOISTURE),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_FAN): cv.maybe_simple_value(
            fan.FAN_SCHEMA.extend({cv.GenerateID(): cv.declare_id(EHUFan)}),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_TARGET_HUMIDITY): cv.maybe_simple_value(
            number.number_schema(
                EHUNumber.template(EHUPacketType.PACKET_REQ_SET_HUMIDITY),
                device_class=DEVICE_CLASS_HUMIDITY,
                unit_of_measurement=UNIT_PERCENT,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_SPEED): cv.maybe_simple_value(
            number.number_schema(
                EHUNumber.template(EHUPacketType.PACKET_REQ_SET_SPEED),
                icon="mdi:fan",
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_PRESET): cv.maybe_simple_value(
            select.select_schema(
                EHUFanPreset,
                icon="mdi:tune",
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_LED_BRIGHTNESS): cv.maybe_simple_value(
            number.number_schema(
                EHUBrightnessNumber  # EHUNumber.template(EHUPacketType.PACKET_REQ_SET_LED_BRIGHTNESS),
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_LED_TOP): cv.maybe_simple_value(
            eh_switch.switch_schema(
                EHUDependedSwitch.template(
                    EHUPacketType.PACKET_REQ_SET_LED_MODE,
                    EHUStateType.LED_MODE_TOP,
                    EHUStateType.LED_MODE_BOTTOM,
                ),
                entity_category=ENTITY_CATEGORY_CONFIG,
                block_inverted=True,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_LED_BOTTOM): cv.maybe_simple_value(
            eh_switch.switch_schema(
                EHUDependedSwitch.template(
                    EHUPacketType.PACKET_REQ_SET_LED_MODE,
                    EHUStateType.LED_MODE_BOTTOM,
                    EHUStateType.LED_MODE_TOP,
                ),
                entity_category=ENTITY_CATEGORY_CONFIG,
                block_inverted=True,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_LED_PRESET): cv.maybe_simple_value(
            select.select_schema(
                EHULedPreset,
            ),
            key=CONF_NAME,
        ),
        cv.Optional(CONF_HUMIDIFICATION): cv.maybe_simple_value(
            binary_sensor.binary_sensor_schema(device_class=DEVICE_CLASS_RUNNING),
            key=CONF_NAME,
        ),
    }
).extend(cv.polling_component_schema("15s"))


async def setup_sensor(config: dict, key: str, fn):
    if conf := config.get(key, None):
        sens = await sensor.new_sensor(conf)
        cg.add(fn(sens))
        return sens


async def setup_switch(config: dict, key: str, fn, *args):
    if key in config:
        parent = await cg.get_variable(config[CONF_ID])
        var = await eh_switch.new_switch(config[key], parent, *args)
        await cg.register_component(var, config[key])
        cg.add(fn(var))
        return var


async def setup_binary_sensor(config: dict, key: str, fn):
    if key in config:
        var = await binary_sensor.new_binary_sensor(config[key])
        cg.add(fn(var))
        return var


async def fan_new_fan(config: dict, *args):
    var = cg.new_Pvariable(config[CONF_ID], *args)
    await fan.register_fan(var, config)
    return var


async def setup_fan(config: dict, key: str, fn):
    if conf := config.get(key, None):
        parent = await cg.get_variable(config[CONF_ID])
        var = await fan_new_fan(conf, parent)
        await cg.register_component(var, conf)
        cg.add(fn(var))
        return var


async def setup_number(config: dict, key: str, fn, min_value, max_value, step=1):
    if conf := config.get(key, None):
        parent = await cg.get_variable(config[CONF_ID])
        var = await number.new_number(
            conf, parent, min_value=min_value, max_value=max_value, step=step
        )
        await cg.register_component(var, conf)
        cg.add(fn(var))
        return var


async def select_new_select(config: dict, *args, options: list[str]):
    # var = await select.new_select(conf, parent, options=options)
    var = cg.new_Pvariable(config[CONF_ID], *args)
    await select.register_select(var, config, options=options)
    return var


async def setup_select(config: dict, key: str, fn, options: list[str]):
    if conf := config.get(key, None):
        parent = await cg.get_variable(config[CONF_ID])
        var = await select_new_select(conf, parent, options=options)
        await cg.register_component(var, conf)
        cg.add(fn(var))
        return var


async def new_ehu(config):
    api = await cg.get_variable(config[CONF_EHU_ID])
    var = cg.new_Pvariable(config[CONF_ID], api)
    await cg.register_component(var, config)

    await setup_sensor(config, CONF_TEMPERATURE, var.set_temperature_sensor)
    await setup_sensor(config, CONF_HUMIDITY, var.set_humidity_sensor)
    await setup_switch(
        config,
        CONF_WARM_MIST,
        var.set_warm_mist_switch,
        cg.RawExpression(f"&{var.st().water_flags}"),
    )
    await setup_switch(
        config,
        CONF_UV,
        var.set_uv_switch,
        cg.RawExpression(f"&{var.st().water_flags}"),
    )
    await setup_switch(config, CONF_IONIZER, var.set_ionizer_switch)
    await setup_switch(config, CONF_LOCK, var.set_lock_switch)
    await setup_switch(config, CONF_MUTE, var.set_mute_switch)
    await setup_binary_sensor(config, CONF_WATER, var.set_water_binary_sensor)
    await setup_binary_sensor(
        config, CONF_HUMIDIFICATION, var.set_humidification_binary_sensor
    )
    await setup_fan(config, CONF_FAN, var.set_fan)
    await setup_number(
        config, CONF_TARGET_HUMIDITY, var.set_target_humidity_number, 30, 85
    )
    await setup_number(config, CONF_SPEED, var.set_fan_speed_number, 1, 3)
    await setup_select(config, CONF_PRESET, var.set_fan_preset_select, [])
    await setup_number(
        config, CONF_LED_BRIGHTNESS, var.set_led_brightness_number, 33, 99
    )
    await setup_switch(
        config,
        CONF_LED_TOP,
        var.set_led_top_switch,
        cg.RawExpression(f"&{var.st().led_mode}"),
    )
    await setup_switch(
        config,
        CONF_LED_BOTTOM,
        var.set_led_bottom_switch,
        cg.RawExpression(f"&{var.st().led_mode}"),
    )
    await setup_select(config, CONF_LED_PRESET, var.set_led_preset_select, [])

    if CONF_TIME_ID in config:
        time_ = await cg.get_variable(config[CONF_TIME_ID])
        cg.add(var.set_time_id(time_))

    return var


async def to_code(config):
    var = await rka_api.new_api(config, EHUState)
