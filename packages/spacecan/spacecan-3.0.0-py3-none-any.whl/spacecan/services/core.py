import threading

from .ST01_request_verification import (
    RequestVerificationServiceController,
    RequestVerificationServiceResponder,
)
from .ST03_housekeeping import (
    HousekeepingServiceController,
    HousekeepingServiceResponder,
)
from .ST08_function_management import (
    FunctionManagementServiceController,
    FunctionManagementServiceResponder,
)
from .ST17_test import TestServiceController, TestServiceResponder
from .ST20_parameter_management import (
    ParameterManagementServiceController,
    ParameterManagementServiceResponder,
)


class PacketUtilizationService:
    def __init__(self):
        self.packet_monitor = None
        self.request_verification = None
        self.housekeeping = None
        self.function_management = None
        self.test = None
        self.parameter_management = None

    def received_packet(self, data, node_id):
        service = data[0]
        subtype = data[1]
        data = data[2:]

        if self.packet_monitor is not None:
            self.packet_monitor(service, subtype, data, node_id)

        # dispatch packet to the individual service handlers
        # run them in threads to not block the main loop

        # request verification service
        if service == 1:
            t = threading.Thread(
                target=self.request_verification.process,
                args=(service, subtype, data, node_id),
            )
            t.start()

        # housekeeping service
        elif service == 3:
            t = threading.Thread(
                target=self.housekeeping.process,
                args=(service, subtype, data, node_id),
            )
            t.start()

        # function management service
        elif service == 8:
            t = threading.Thread(
                target=self.function_management.process,
                args=(service, subtype, data, node_id),
            )
            t.start()

        # test service
        elif service == 17:
            t = threading.Thread(
                target=self.test.process, args=(service, subtype, data, node_id)
            )
            t.start()

        # parameter management service
        elif service == 20:
            t = threading.Thread(
                target=self.parameter_management.process,
                args=(service, subtype, data, node_id),
            )
            t.start()


class PacketUtilizationServiceController(PacketUtilizationService):
    def __init__(self, parent):
        self.parent = parent
        self.parent.received_packet = self.received_packet

        self.request_verification = RequestVerificationServiceController(self)
        self.housekeeping = HousekeepingServiceController(self)
        self.function_management = FunctionManagementServiceController(self)
        self.test = TestServiceController(self)
        self.parameter_management = ParameterManagementServiceController(self)

        self.packet_monitor = None

    def send(self, packet, node_id):
        self.parent.send_packet(packet, node_id)


class PacketUtilizationServiceResponder(PacketUtilizationService):
    def __init__(self, parent):
        self.parent = parent
        self.parent.received_packet = self.received_packet

        self.request_verification = RequestVerificationServiceResponder(self)
        self.housekeeping = HousekeepingServiceResponder(self)
        self.function_management = FunctionManagementServiceResponder(self)
        self.test = TestServiceResponder(self)
        self.parameter_management = ParameterManagementServiceResponder(self)

        self.packet_monitor = None

    def send(self, packet):
        self.parent.send_packet(packet)
