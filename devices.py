
class Device:
    def __init__(self, title, power):
        self.title = title
        self.power = power


# water heater, boiler, fridge, freezer
class InterruptibleDevice(Device):
    def __init__(self, title, power):
        Device.__init__(self, title, power)
        self.off_interval = 10
        self.on_interval = 15


# electric heating, AC
class ThermalDevice(Device):
    def __init__(self, title, power):
        Device.__init__(self, title, power)
        self.off_interval = 25
        self.on_interval = 15


# washing machine, dish washer
class ShiftableDevice(Device):
    def __init__(self, title, power, time_consumption):
        Device.__init__(self, title, power)
        self.time_consumption = time_consumption


# kitchen stove, lighting - could not be interrupted
class NonSwitchableDevice(Device):
    def __init__(self, title, power, time_consumption):
        Device.__init__(self, title, power)
        self.time_consumption = time_consumption
