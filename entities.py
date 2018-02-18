from datetime import datetime, timedelta
from devices import *
from etc import *


# max_power in kW
class Socket:
    def __init__(self, socket_id, flat):
        self.flat = flat
        self.socket_id = socket_id
        self.current_power = 0
        self.is_on = False
        self.last_on_time = None
        self.last_off_time = None
        self.device = None
        self.added_to_queue = False
        self.potential_power = 0

    def start_by_user(self):
        if self.added_to_queue:
            print("Task already added to queue")

        if not self.device:
            print("No device to start")
            return

        if isinstance(self.device, ShiftableDevice):
            # go up to ask DMS
            self.flat.ask_dms(self)
            self.added_to_queue = True
        else:
            self.switch_on()

    # used by DMS
    def switch_on(self):
        if not self.is_on:
            print("\n+++++ Device {} has been turned on +++++".format(self.device.title))
            self.last_on_time = datetime.now()
            self.is_on = True
            self.current_power = self.device.power
            self.flat.notify()
            self.added_to_queue = False

    # used by DMS
    def switch_off(self, black_out=False):
        if self.is_on:
            self.last_off_time = datetime.now()
            self.is_on = False
            self.current_power = 0
        if not black_out:
            print("\n+++++ Device '{}' has been turned off +++++".format(self.device.title))
            self.flat.notify()

    def attach_device(self, device: Device):
        self.device = device

    def update_potential_power(self):
        if not self.is_on:
            self.potential_power = 0
            return

        if isinstance(self.device, InterruptibleDevice) or isinstance(self.device, ThermalDevice):
            if datetime.now() - self.last_on_time >= timedelta(seconds=self.device.on_interval):
                self.potential_power = self.current_power

    def release_power(self):
        if self.potential_power > 0:
            self.potential_power = 0
            self.switch_off()
            return TaskObject(self, 'on', datetime.now() + timedelta(self.device.off_interval)), self.device.power


# flat_id: house number (1-9) + flat number (1-99)
# approximately five sockets for testing and showing
class Flat:
    def __init__(self, flat_id, house):
        self.house = house
        self.flat_id = flat_id
        self.sockets = [Socket(i, self) for i in range(5)]
        self.current_power = 0

    def ask_dms(self, socket):
        self.house.ask_dms(socket)

    def release_power(self, task, power):
        self.house.release_power(task, power)

    def notify(self):
        # print("Flat with id = {}: updating information".format(self.flat_id))
        self.calculate_current_power()
        # print("--- Current power = {}".format(self.current_power))
        self.house.notify()

    def calculate_current_power(self):
        self.current_power = sum([socket.current_power for socket in self.sockets])


class House:
    def __init__(self, house_id, village):
        self.village = village
        self.house_id = house_id
        self.flats = [Flat(str(house_id * 100 + i), self) for i in range(1, 100)]
        self.current_power = 0
        self.potential_power = []

    def ask_dms(self, socket):
        self.village.ask_dms(socket)

    def release_power(self, task, power):
        self.village.release_power(task, power)

    def notify(self):
        # print("House with id = {}: updating information".format(self.house_id))
        self.calculate_current_power()
        # print("--- Current power = {}".format(self.current_power))
        self.village.notify()

    def calculate_current_power(self):
        self.current_power = sum([flat.current_power for flat in self.flats])


class Village:
    def __init__(self, dms):
        self.houses = [House(i, self) for i in range(1, 10)]
        self.current_power = 0
        self.dms = dms

    def ask_dms(self, socket):
        self.dms.ask_dms(socket)

    def release_power(self, task, power):
        self.dms.release_power(task, power)

    def notify(self):
        print("Village: updating information")
        self.calculate_current_power()
        print(" --- Current power = {}".format(self.current_power))
        self.dms.notify()

    def calculate_current_power(self):
        self.current_power = sum([house.current_power for house in self.houses])



