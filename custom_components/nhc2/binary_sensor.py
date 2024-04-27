import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.accesscontrol_action_call_answered import Nhc2AccesscontrolActionCallAnsweredEntity
from .entities.accesscontrol_action_call_pending import Nhc2AccesscontrolActionCallPendingEntity
from .entities.accesscontrol_action_decline_call_applied_on_all_devices import \
    Nhc2AccesscontrolActionDeclineCallAppliedOnAllDevicesEntity
from .entities.alloff_action_active import Nhc2AlloffActionActiveEntity
from .entities.alloff_action_basicstate import Nhc2AlloffActionBasicStateEntity
from .entities.alloff_action_started import Nhc2AlloffActionStartedEntity
from .entities.audiocontrol_action_connected import Nhc2AudiocontrolActionConnectedEntity
from .entities.audiocontrol_action_title_aligned import Nhc2AudiocontrolActionTitleAlignedEntity
from .entities.audiocontrol_action_volume_aligned import Nhc2AudiocontrolActionVolumeAlignedEntity
from .entities.bellbutton_action_decline_call_applied_on_all_devices import \
    Nhc2BellbuttonActionDeclineCallAppliedOnAllDevicesEntity
from .entities.comfort_action_all_started import Nhc2ComfortActionAllStartedEntity
from .entities.comfort_action_basicstate import Nhc2ComfortActionBasicStateEntity
from .entities.comfort_action_mood_active import Nhc2ComfortActionMoodActiveEntity
from .entities.dimmer_action_aligned import Nhc2DimmerActionAlignedEntity
from .entities.electricalheating_action_basicstate import Nhc2ElectricalheatingActionBasicStateEntity
from .entities.electricity_clamp_centralmeter_report_instant_usage import \
    Nhc2ElectricityClampCentralmeterReportInstantUsageEntity
from .entities.garagedoor_action_port_closed import Nhc2GaragedoorActionPortClosedEntity
from .entities.generic_action_all_started import Nhc2GenericActionAllStartedEntity
from .entities.generic_action_start_active import Nhc2GenericActionStartActiveEntity
from .entities.generic_energyhome_electrical_power_production_threshold_exceeded import \
    Nhc2GenericEnergyhomeElectricalPowerProductionThresholdExceededEntity
from .entities.generic_energyhome_report_instant_usage import Nhc2GenericEnergyhomeReportInstantUsageEntity
from .entities.generic_smartplug_report_instant_usage import Nhc2GenericSmartplugReportInstantUsageEntity
from .entities.heatingcooling_action_cooling_mode import Nhc2HeatingcoolingActionCoolingModeEntity
from .entities.heatingcooling_action_heating_mode import Nhc2HeatingcoolingActionHeatingModeEntity
from .entities.hvacthermostat_hvac_hvac_on import Nhc2HvacthermostatHvacHvacOnEntity
from .entities.motor_action_aligned import Nhc2MotorActionAlignedEntity
from .entities.motor_action_moving import Nhc2MotorActionMovingEntity
from .entities.naso_smartplug_feedback_enabled import Nhc2NasoSmartplugFeedbackEnabledEntity
from .entities.naso_smartplug_measuring_only import Nhc2NasoSmartplugMeasuringOnlyEntity
from .entities.naso_smartplug_report_instant_usage import Nhc2NasoSmartplugReportInstantUsageEntity
from .entities.overallcomfort_action_start_active import Nhc2OverallcomfortActionStartActiveEntity
from .entities.overallcomfort_action_all_started import Nhc2OverallcomfortActionAllStartedEntity
from .entities.playerstatus_action_basicstate import Nhc2PlayerstatusActionBasicStateEntity
from .entities.timeschedule_action_active import Nhc2TimeschedulActionActiveEntity
from .nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction
from .nhccoco.devices.alloff_action import CocoAlloffAction
from .nhccoco.devices.audiocontrol_action import CocoAudiocontrolAction
from .nhccoco.devices.bellbutton_action import CocoBellbuttonAction
from .nhccoco.devices.comfort_action import CocoComfortAction
from .nhccoco.devices.dimmer_action import CocoDimmerAction
from .nhccoco.devices.electricalheating_action import CocoElectricalheatingAction
from .nhccoco.devices.electricity_clamp_centralmeter import CocoElectricityClampCentralmeter
from .nhccoco.devices.garagedoor_action import CocoGaragedoorAction
from .nhccoco.devices.gate_action import CocoGateAction
from .nhccoco.devices.generic_action import CocoGenericAction
from .nhccoco.devices.generic_energyhome import CocoGenericEnergyhome
from .nhccoco.devices.generic_smartplug import CocoGenericSmartplug
from .nhccoco.devices.heatingcooling_action import CocoHeatingcoolingAction
from .nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .nhccoco.devices.naso_smartplug import CocoNasoSmartplug
from .nhccoco.devices.overallcomfort_action import CocoOverallcomfortAction
from .nhccoco.devices.playerstatus_action import CocoPlayerstatusAction
from .nhccoco.devices.rolldownshutter_action import CocoRolldownshutterAction
from .nhccoco.devices.sunblind_action import CocoSunblindAction
from .nhccoco.devices.timeschedule_action import CocoTimescheduleAction
from .nhccoco.devices.venetianblind_action import CocoVenetianblindAction

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_binary_sensors'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring binary sensors')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoNasoSmartplug)
    _LOGGER.info('→ Found %s NHC Zigbee Smart plugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2NasoSmartplugReportInstantUsageEntity(device_instance, hub, gateway))
            entities.append(Nhc2NasoSmartplugFeedbackEnabledEntity(device_instance, hub, gateway))
            entities.append(Nhc2NasoSmartplugMeasuringOnlyEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericSmartplug)
    _LOGGER.info('→ Found %s Generic Zigbee Smart plugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericSmartplugReportInstantUsageEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoElectricityClampCentralmeter)
    _LOGGER.info('→ Found %s Electricity Metering modules', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ElectricityClampCentralmeterReportInstantUsageEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericEnergyhome)
    _LOGGER.info('→ Found %s Energy Home\'s', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(
                Nhc2GenericEnergyhomeElectricalPowerProductionThresholdExceededEntity(device_instance, hub, gateway)
            )
            entities.append(Nhc2GenericEnergyhomeReportInstantUsageEntity(device_instance, hub, gateway))

        async_add_entities(entities)
