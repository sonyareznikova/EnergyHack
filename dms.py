from datetime import datetime
from devices import *
from entities import *
from etc import *
import threading


class QueueObject:

    def __init__(self, needed_power, time_consumption, socket):
        self.needed_power = needed_power

        # in seconds
        self.time_consumption = time_consumption
        self.socket = socket
        self.created_at = datetime.now()


class DMS:
    def __init__(self, max_power):
        self.village = None

        # what devices of Shiftable type has to be turned off
        self.queue = []

        # what devices and when should be turned on
        self.tasks_to_run = set([])
        self.current_power = 0
        self.max_power = max_power

    def start(self):
        self.executing_tasks()

    def update_current_power(self):
        self.current_power = self.village.current_power

    def add_task_to_run(self, task: TaskObject):
        print("DMS: adding task...")
        self.tasks_to_run.add(task)
        print(" --- ", task.time, task.type_of_task, task.socket.device.title)

    def release_potential_power(self):
        print("\nDMS: releasing potential power...")
        sockets_and_power = []
        for house in self.village.houses:
            for flat in house.flats:
                for socket in flat.sockets:
                    socket.update_potential_power()
                    if socket.potential_power > 0:
                        sockets_and_power.append((socket, socket.potential_power))
        sum_potential_power = sum([item[1] for item in sockets_and_power])

        released_power = 0

        for socket, power in sockets_and_power:
            task, t_power = socket.release_power()
            self.add_task_to_run(task)
            released_power += t_power
            if released_power >= 0.5 * sum_potential_power:
                break

        return released_power, sum_potential_power

    def check_queue(self):
        print("DMS: checking queue")
        if len(self.queue) > 0:
            print(" --- there are {} devices in the queue".format(len(self.queue)))
            if self.current_power + self.queue[0].needed_power <= self.max_power:
                self.queue[0].socket.switch_on()
                qo = self.queue.pop()
                print(" --- Ok to turn on device {}".format(qo.socket.device.title))
            else:
                released_power, potential_power = self.release_potential_power()
                self.update_current_power()
                print("DMS: trying to run shiftable devices...")
                print(" --- released power {}".format(released_power))
                print(" --- potential power {}".format(potential_power))
                if self.current_power + self.queue[0].needed_power <= self.max_power:
                    qo = self.queue.pop()
                    print(" --- Ok to turn on device {}".format(qo.socket.device.title))
                    qo.socket.switch_on()
                    print(datetime.now() + timedelta(seconds=qo.socket.device.time_consumption))
                    task = TaskObject(qo.socket, 'off', datetime.now() + timedelta(seconds=qo.socket.device.time_consumption))
                    self.add_task_to_run(task)

        else:
            print(" --- no devices in the queue")

    def notify(self):
        self.update_current_power()
        if self.current_power > self.max_power:
            self.process_black_out()
            return

    def process_black_out(self):
        print("\nDMS: !!!! BLACK OUT processing... !!!! \n")
        t_flat = self.village.houses[0].flats[0]
        for house in self.village.houses:
            for flat in house.flats:
                for socket in flat.sockets:
                    socket.switch_off(black_out=True)
        t_flat.notify()
        self.update_current_power()

    def ask_dms(self, socket):
        print("\nDMS: adding object to queue...")
        qo = QueueObject(socket.device.power, socket.device.time_consumption, socket)
        self.queue.append(qo)
        self.notify()

    def executing_tasks(self):
        print("\nDMS: executing tasks and checking queue in another thread...")
        print(' --- there are {} tasks'.format(len(self.tasks_to_run)))
        threading.Timer(5.0, self.executing_tasks).start()

        finished_tasks = set()
        for task in self.tasks_to_run:
            task.perform()
            finished_tasks.add(task)

        self.tasks_to_run = self.tasks_to_run.difference(finished_tasks)
        self.release_potential_power()
        self.check_queue()
