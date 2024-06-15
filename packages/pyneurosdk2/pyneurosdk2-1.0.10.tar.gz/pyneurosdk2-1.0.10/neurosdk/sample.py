from scanner import Scanner
from cmn_types import *
from brainbit_2_sensor import BrainBit2Sensor

import concurrent.futures
from time import sleep


def sensor_found(scanner, sensors):
    for index in range(len(sensors)):
        print('Sensor found: %s' % sensors[index])


def on_sensor_state_changed(sensor, state):
    print('Sensor {0} is {1}'.format(sensor.name, state))


def on_battery_changed(sensor, battery):
    print('Battery: {0}'.format(battery))


def on_amp_mode_changed(sensor, mode):
    print('Amp mode: {0}'.format(mode))


def on_signal_data_received(sensor, data):
    print(data)


def on_resist_data_received(sensor, data):
    print(data)


def on_electrodes_state_changed(sensor, data):
    print(data)


def on_envelope_received(sensor, data):
    print(data)


def on_respiration_data_received(sensor, data):
    print(data)


try:
    scanner = Scanner([SensorFamily.LEBrainBitBlack, SensorFamily.LEBrainBit,
                       SensorFamily.LEBrainBitFlex, SensorFamily.LEBrainBit2,
                       SensorFamily.LEBrainBitPro, SensorFamily.LECallibri])

    scanner.sensorsChanged = sensor_found
    scanner.start()
    print("Starting search for 5 sec...")
    sleep(5)
    scanner.stop()

    sensorsInfo = scanner.sensors()
    for i in range(len(sensorsInfo)):
        current_sensor_info = sensorsInfo[i]
        print(sensorsInfo[i])

        sensor = scanner.create_sensor(sensorsInfo[i])
        sensor.sensorStateChanged = on_sensor_state_changed
        sensor.batteryChanged = on_battery_changed

        print(sensor.sens_family)
        print(sensor.features)
        print(sensor.commands)
        print(sensor.parameters)
        print(sensor.name)
        print(sensor.state)
        print(sensor.address)
        print(sensor.serial_number)
        print(sensor.batt_power)
        print(sensor.sampling_frequency)
        if sensor.is_supported_parameter(SensorParameter.Gain):
            print(sensor.gain)
        print(sensor.data_offset)
        print(sensor.version)

        if sensor.sens_family == SensorFamily.LECallibri:
            sensor.data_offset = SensorDataOffset.DataOffset3
            sensor.gain = SensorGain.Gain6
            sensor.ext_sw_input = SensorExternalSwitchInput.Electrodes
            sensor.signal_type = CallibriSignalType.ECG

        if sensor.sens_family == SensorFamily.LEBrainBit2 or sensor.sens_family == SensorFamily.LEBrainBitPro or sensor.sens_family == SensorFamily.LEBrainBitFlex:
            amp_param = sensor.amplifier_param
            ch_count = sensor.channels_count
            amp_param.ChGain = [SensorGain.Gain6 for i in range(ch_count)]
            amp_param.ChSignalMode = [BrainBit2ChannelMode.ChModeNormal for i in range(ch_count)]
            amp_param.ChResistUse = [True for i in range(ch_count)]
            amp_param.Current = GenCurrent.GenCurr6nA
            sensor.amplifier_param = amp_param
            print('Amp param: {0}'.format(sensor.amplifier_param))
            s_ch = sensor.supported_channels
            print('Supported channels: {0}'.format(s_ch))

        if sensor.is_supported_parameter(SensorParameter.Amplifier):
            sensor.sensorAmpModeChanged = on_amp_mode_changed

        if sensor.is_supported_parameter(SensorParameter.HardwareFilterState):
            if sensor.is_supported_filter(SensorFilter.BSFBwhLvl2CutoffFreq45_55Hz):
                sensor.hardware_filters = [SensorFilter.BSFBwhLvl2CutoffFreq45_55Hz]

        if sensor.is_supported_feature(SensorFeature.Signal):
            sensor.signalDataReceived = on_signal_data_received

        if sensor.is_supported_parameter(SensorParameter.ElectrodeState):
            print(sensor.electrode_state)
            sensor.electrodeStateChanged = on_electrodes_state_changed

        if sensor.is_supported_feature(SensorFeature.Resist):
            sensor.resistDataReceived = on_resist_data_received

        if sensor.is_supported_feature(SensorFeature.Respiration):
            sensor.respirationDataReceived = on_respiration_data_received

        if sensor.is_supported_feature(SensorFeature.Envelope):
            sensor.envelopeDataReceived = on_envelope_received

        if sensor.is_supported_command(SensorCommand.StartSignal):
            sensor.exec_command(SensorCommand.StartSignal)
            print("Start signal")
            sleep(5)
            sensor.exec_command(SensorCommand.StopSignal)
            print("Stop signal")

        if sensor.is_supported_command(SensorCommand.StartResist):
            sensor.exec_command(SensorCommand.StartResist)
            print("Start resist")
            sleep(5)
            sensor.exec_command(SensorCommand.StopResist)
            print("Stop resist")

        if sensor.is_supported_command(SensorCommand.StartEnvelope):
            sensor.exec_command(SensorCommand.StartEnvelope)
            print("Start envelope")
            sleep(5)
            sensor.exec_command(SensorCommand.StopEnvelope)
            print("Stop envelope")

        if sensor.is_supported_command(SensorCommand.StartRespiration):
            sensor.exec_command(SensorCommand.StartRespiration)
            print("Start respiration")
            sleep(5)
            sensor.exec_command(SensorCommand.StopRespiration)
            print("Stop respiration")

        if sensor.is_supported_command(SensorCommand.StartFPG):
            sensor.exec_command(SensorCommand.StartFPG)
            print("Start FPG")
            sleep(5)
            sensor.exec_command(SensorCommand.StopFPG)
            print("Stop FPG")

        if sensor.is_supported_command(SensorCommand.StartCurrentStimulation):
            sensor.exec_command(SensorCommand.StartCurrentStimulation)
            print("Start CurrentStimulation")
            sleep(5)
            sensor.exec_command(SensorCommand.StopCurrentStimulation)
            print("Stop CurrentStimulation")

        sensor.disconnect()
        print("Disconnect from sensor")
        del sensor

    del scanner
    print('Remove scanner')
except Exception as err:
    print(err)
