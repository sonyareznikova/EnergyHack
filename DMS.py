from datetime import datetime

class QueueObject:
    def __init__(self, needed_power, time_consumption, socket):
        self.needed_power = needed_power
        self.time_consumption = time_consumption
        self.socket = socket
        self.created_at = datetime.now()

class DMS:
    def __init__(self, village, max_power):
        self.village = village
        self.queue = []
        self.current_power = 0
        self.max_power = max_power

    def update_current_power(self):
        self.current_power = self.village.current_power

    def check_queue(self):
        if len(self.queue) > 0:
            power_level = self.current_power + self.queue[0].needed_power
            if power_level < self.max_power:
                self.queue[0].socket.switch_on()
                self.queue.pop()
            else:
                if power_level - self.village.potential_power <= self.max_power:
                    # TODO: switch some socket off
                    self.queue[0].socket.switch_on()
                    self.queue.pop()



    def notify(self):
        self.update_current_power()
        if self.current_power > self.max_power:
            print("Black oooooout! Bye :(")
            return
        self.check_queue()

        pass