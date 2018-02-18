from entities import *
from dms import *
from devices import *
from etc import *
from running_support import *

dms = DMS(30)
village = Village(dms)
dms.village = village
dms.start()
sockets = get_all_sockets(dms)

sockets_for_flat_1 = sockets[0]
sockets_for_flat_2 = sockets[1]


lamp_socket = sockets_for_flat_1[0]
lamp_socket.attach_device(NonSwitchableDevice("Lamp", 1, -1))

wm_socket = sockets_for_flat_1[1]
wm_socket.attach_device(ShiftableDevice("Washing Machine", 4, 60))

kettle_socket_1 = sockets_for_flat_1[2]
kettle_socket_1.attach_device(NonSwitchableDevice("Kettle1", 2, 10))

kettle_socket_2 = sockets_for_flat_1[3]
kettle_socket_2.attach_device(NonSwitchableDevice("Kettle2", 3, 10))

kettle_socket_3 = sockets_for_flat_1[4]
kettle_socket_3.attach_device(NonSwitchableDevice("Kettle3", 2.2, 10))

boiler_socket_1 = sockets_for_flat_2[0]
boiler_socket_1.attach_device(InterruptibleDevice("Boiler1", 2))

boiler_socket_2 = sockets_for_flat_2[1]
boiler_socket_2.attach_device(InterruptibleDevice("Boiler2", 2))

lamp_socket.start_by_user()
kettle_socket_1.start_by_user()
boiler_socket_1.start_by_user()
boiler_socket_2.start_by_user()
wm_socket.start_by_user()
kettle_socket_2.start_by_user()
kettle_socket_3.start_by_user()
lamp_socket.switch_off()


f = 4
