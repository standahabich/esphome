import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c
from esphome.const import CONF_FREQUENCY, CONF_ID, CONF_EXTERNAL_CLOCK_INPUT

DEPENDENCIES = ["i2c"]
MULTI_CONF = True

pca9685_ns = cg.esphome_ns.namespace("pca9685")
PCA9685Output = pca9685_ns.class_("PCA9685Output", cg.Component, i2c.I2CDevice)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(PCA9685Output),
            cv.Optional(CONF_FREQUENCY, default=1000): cv.All(
                cv.frequency, cv.Range(min=23.84, max=1525.88)
            ),
            cv.Optional(CONF_EXTERNAL_CLOCK_INPUT, default=False): cv.boolean,
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(i2c.i2c_device_schema(0x40))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID], config[CONF_FREQUENCY])
    cg.add(var.set_extclk(config[CONF_EXTERNAL_CLOCK_INPUT]))
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)
