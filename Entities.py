from datetime import datetime

class Device:
    def __init__(self, title, power):
        self.title = title
        self.power = power

# water heater, boiler, fridge, freezer
class InterruptibleDevice(Device):
    def __init__(self, title, power):
        Device.__init__(self, title, power)
        self.off_interval = 30
        self.on_interval = 5

# electric heating, AC
class ThermalDevice(Device):
    def __init__(self, title, power):
        Device.__init__(self, title, power)
        self.off_interval = 60
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

#max_power in kW
class Socket:
    def __init__(self, socket_id, flat):
        self.flat = flat
        self.socket_id = socket_id
        self.current_power = 0
        self.potential_power = 0
        self.is_on = False
        self.last_on_time = None
        self.last_off_time = None
        self.device = None

    def switch_on(self):
        if not self.is_on:
            self.last_on_time = datetime.now()
            self.is_on = True
            self.current_power = self.device.power
            self.flat.notify()

    def switch_off(self):
        if self.is_on:
            self.last_off_time = datetime.now()
            self.is_on = False
            self.current_power = 0
            self.flat.notify()

    def attach_device(self, device):
        self.device = device

    def calculate_potential_power(self):
        pass



# flat_id: house number (1-9) + flat number (1-99)
# approximately five sockets for testing and showing
class Flat:
    def __init__(self, flat_id, house):
        self.house = house
        self.flat_id = flat_id
        self.sockets = [Socket(i, self) for i in range(5)]
        self.current_power = 0
        self.potential_power = 0

    def notify(self):
        pass

    def calculate_current_power(self):
        self.current_power = sum([socket.current_power for socket in self.sockets])

    def calculate_potential_power(self):
        self.potential_power = sum([socket.potential_power for socket in self.sockets])


class House:
    def __init__(self, house_id, village):
        self.village = village
        self.house_id = house_id
        self.flats = [Flat(str(house_id * 100 + i), self) for i in range(1, 100)]
        self.current_power = 0
        self.potential_power = 0

    def notify(self):
        pass

    def calculate_current_power(self):
        self.current_power = sum([flat.current_power for flat in self.flats])

    def calculate_potential_power(self):
        self.potential_power = sum([flat.current_power for flat in self.flats])


class Village:
    def __init__(self):
        self.houses = [House(i, self) for i in range(1, 10)]
        self.current_power = 0
        self.potential_power = 0

    def notify(self):
        pass

    def calculate_current_power(self):
        self.current_power = sum([house.current_power for house in self.houses])

    def calculate_potential_power(self):
        self.potential_power = sum([house.current_power for house in self.houses])


