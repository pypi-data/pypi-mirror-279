from ..primitives.packet import Packet


class RequestVerificationServiceController:
    def __init__(self, parent):
        self.parent = parent

    def process(self, service, subtype, data, node_id):
        case = (service, subtype)
        source_packet = data[0], data[1]

        self.received_report(node_id, case, source_packet)

        if case == (1, 1):
            self.received_success_acceptance_report(node_id, source_packet)
        elif case == (1, 2):
            self.received_fail_acceptance_report(node_id, source_packet)
        elif case == (1, 7):
            self.received_success_completion_report(node_id, source_packet)
        elif case == (1, 8):
            self.received_fail_completion_report(node_id, source_packet)

    def received_report(self, node_id, case, source_packet):
        # to be overwritten
        pass

    def received_success_acceptance_report(self, node_id, source_packet):
        # to be overwritten
        pass

    def received_fail_acceptance_report(self, node_id, source_packet):
        # to be overwritten
        pass

    def received_success_completion_report(self, node_id, source_packet):
        # to be overwritten
        pass

    def received_fail_completion_report(self, node_id, source_packet):
        # to be overwritten
        pass


class RequestVerificationServiceResponder:
    def __init__(self, parent):
        self.parent = parent

    def process(self, service, subtype, data, node_id):
        pass

    def send_success_acceptance_report(self, source_packet):
        self.parent.send(Packet([1, 1] + source_packet))

    def send_fail_acceptance_report(self, source_packet):
        self.parent.send(Packet([1, 2] + source_packet))

    def send_success_completion_report(self, source_packet):
        self.parent.send(Packet([1, 7] + source_packet))

    def send_fail_completion_report(self, source_packet):
        self.parent.send(Packet([1, 8] + source_packet))
