from ..primitives.packet import Packet


class TestServiceController:
    def __init__(self, parent):
        self.parent = parent

    def process(self, service, subtype, data, node_id):
        case = (service, subtype)

        if case == (17, 2):
            self.received_connection_test_report(node_id)

        elif case == (17, 4):
            apid = int.from_bytes(data)
            self.received_application_connection_test_report(node_id, apid)

    def send_connection_test(self, node_id):
        self.parent.send(Packet([17, 1]), node_id)

    def send_application_connection_test(self, node_id, apid):
        self.parent.send(Packet([17, 3] + [apid]), node_id)

    def received_connection_test_report(self, node_id):
        # to be overwritten
        pass

    def received_application_connection_test_report(self, node_id, apid):
        # to be overwritten
        pass


class TestServiceResponder:
    def __init__(self, parent):
        self.parent = parent

    def process(self, service, subtype, data, node_id):
        case = (service, subtype)

        if case == (17, 1):
            # send success acceptance report
            self.parent.request_verification.send_success_acceptance_report(
                [service, subtype]
            )

            # reply with (17, 2)
            self.send_connection_test_report()

            # send success completion report
            self.parent.request_verification.send_success_completion_report(
                [service, subtype]
            )

        elif case == (17, 3):
            apid = int.from_bytes(data)

            # send success acceptance report
            self.parent.request_verification.send_success_acceptance_report(
                [service, subtype]
            )

            # run the connection test
            result = self.received_application_connection_test(apid)

            if result is True:
                # reply with (17, 4)
                self.send_application_connection_test_report(apid)

                # send success completion report
                self.parent.request_verification.send_success_completion_report(
                    [service, subtype]
                )
            else:
                # send fail completion report
                self.parent.request_verification.send_fail_completion_report(
                    [service, subtype]
                )
        else:
            # send fail acceptance report
            self.parent.request_verification.send_fail_acceptance_report(
                [service, subtype]
            )

    def send_connection_test_report(self):
        self.parent.send(Packet([17, 2]))

    def send_application_connection_test_report(self, apid):
        self.parent.send(Packet([17, 4] + [apid]))

    def received_application_connection_test(self, apid):
        # to be overwritten
        return True
