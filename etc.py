from datetime import datetime, timedelta


# duration of one slot is 5 seconds
class PowerSlot:
    @staticmethod
    def create(from_limit, duration, power, socket):
        root_power_slot = PowerSlot(power, socket)
        root_power_slot.from_limit = from_limit
        root_power_slot.is_root = True
        duration -= 5
        last_slot = root_power_slot
        while duration > 0:
            new_slot = PowerSlot(power, socket)
            last_slot.set_next(new_slot)
            duration -= 5
        return root_power_slot

    def __init__(self, power, socket):
        self.is_root = False
        self.from_limit = None
        self.to_limit = None
        self.next = None
        self.duration = 5
        self.power = power
        self.from_time = None
        self.to_time = None
        self.is_booked = False
        self.socket = socket

    def set_next(self, next_slot: "PowerSlot"):
        self.next = next_slot

    def book(self, from_time):
        if not self.is_root:
            if self.from_time == from_time and not self.is_booked:
                self.is_booked = True
                return True
            else:
                if self.next:
                    return self.next.book(from_time)
                else:
                    return False

        if self.is_root:
            if self.from_limit > from_time:
                return False
            else:
                # not booked
                # book + init_chain
                if not self.from_time:
                    self.from_time = from_time
                    self.to_time = from_time + timedelta(seconds=5)
                    next_slot = self.next
                    next_from_time = from_time + timedelta(seconds=5)
                    while next_slot:
                        next_slot.from_time = next_from_time
                        next_slot.to_time = next_from_time + timedelta(seconds=5)
                        next_from_time = next_slot.to_time
                        next_slot = next_slot.next
                    self.is_booked = True
                    return True
        return False

    def is_possible_to_book(self, from_time):
        if self.from_time == from_time and not self.is_booked:
            return True
        elif self.next:
            return self.next.is_possible_to_book(from_time)
        else:
            return False


class TaskObject:
    def __init__(self, socket, type_of_task, time):
        self.socket = socket
        self.type_of_task = type_of_task
        self.time = time

    def perform(self):
        if self.type_of_task == "on":
            self.socket.switch_on()
        else:
            self.socket.switch_off()

    def is_ready_to_run(self):
        return datetime.now() >= self.time