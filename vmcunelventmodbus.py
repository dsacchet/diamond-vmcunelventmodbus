# coding=utf-8

"""
The VmcUnelventModbusCollector class collects metrics from Unelvent VMC using
serial modbus

#### Dependencies

 * /dev/ttyUSB0
 * FTDI USB to RS484 adapter
 * pymodbus python library

"""

import diamond.collector
import diamond.convertor
import os
import re

from pymodbus.client.sync import ModbusSerialClient

try:
    import psutil
except ImportError:
    psutil = None


class VmcUnelventModbusCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(VmcUnelventModbusCollector, self).get_default_config_help()
        config_help.update({
            'port': 'Serial port',
            'method': 'Modbus protocol rtu/ascii/binary',
            'baudrate': 'Speed of the serial communcation',
            'bytesize': 'size of unit of the serial communcation',
            'stopbits': 'number of stop bit of the serial communcation',
            'parity': 'parity of the serial communcation even/odd/none',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(VmcUnelventModbusCollector, self).get_default_config()
        config.update({
            'path':         'vmc',
            'port':         '/dev/ttyUSB0',
            'baudrate':     '19200',
            'bytesize':     '8',
            'stopbits':     '1',
            'parity':       'even',
            'method':       'rtu',
        })
        return config

    def collect(self):
        """
        Collect vmc stats.
        """

        # Initialize results
        results = {}

	if self.config['parity'] == "even":
		parity='E'
	elif self.config['parity'] == "odd":
		parity='O'
	elif self.config['parity'] == "none":
		partiry='N'
	else:
		parity='pas bon'

	client = ModbusSerialClient(method=str(self.config['method']),port=str(self.config['port']),baudrate=int(self.config['baudrate']),bytesize=int(self.config['bytesize']),stopbits=int(self.config['stopbits']),parity=parity)
	client.connect()

	result = client.read_input_registers(address=0x00, count=41, unit=0x01)

	tint=result.registers[21]/10.0)
	tout=result.registers[22]/10.0)
	text=result.registers[23]/10.0)
	timp=result.registers[24]/10.0)

	if tint != 6553:
	        self.publish("tint", tint)
	if tout != 6553:
		self.publish("tout", tout)
	if text != 6553:
		self.publish("text", text)
	if timp != 6553:
		self.publish("timp", timp)

        self.publish("airflow", result.registers[16])
        self.publish("bypass", result.registers[25])
        self.publish("filter_alarm", result.registers[36])
        self.publish("motorspeed_extract", result.registers[19])
        self.publish("motorspeed_input", result.registers[20])
        self.publish("state_of_bypass", result.registers[25])
        self.publish("state_of_pre_heating_battery", result.registers[26])
        self.publish("state_of_post_heating_battery", result.registers[27])
	
	result = client.read_holding_registers(address=0x00, count=34, unit=0x01)

        self.publish("airflow_set", result.registers[15])

        return None
