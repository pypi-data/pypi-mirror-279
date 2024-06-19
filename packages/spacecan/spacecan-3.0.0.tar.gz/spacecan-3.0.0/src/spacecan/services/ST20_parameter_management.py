import json
import struct

from ..primitives.packet import Packet


class Parameter:
    def __init__(self, parameter_id, parameter_name, encoding, value, **others):
        self.parameter_id = parameter_id
        self.parameter_name = parameter_name
        self.encoding = encoding
        self.value = value

    def __repr__(self):
        string = f"Parameter({self.parameter_id}, '{self.parameter_name}', '{self.encoding}', "
        if type(self.value) == str:
            string += f"'{self.value}')"
        else:
            string += f"{self.value})"
        return string

    def encode(self):
        encoding = (
            self.encoding if self.encoding.startswith("!") else "!" + self.encoding
        )
        return struct.pack(encoding, self.value)

    def decode(self, data):
        encoding = (
            self.encoding if self.encoding.startswith("!") else "!" + self.encoding
        )
        return struct.unpack(encoding, data)[0]

    def get_encoded_size(self):
        return struct.calcsize(self.encoding)


class ParameterManagementService:
    def __init__(self, parent):
        self.parent = parent
        self.parameter_pool = {}

    def add_parameter(self, parameter):
        self.parameter_pool[parameter.parameter_id] = parameter

    def get_parameter(self, parameter_id):
        return self.parameter_pool.get(parameter_id)

    def set_parameter_value(self, parameter_id, value):
        self.parameter_pool[parameter_id].value = value

    def get_parameter_value(self, parameter_id):
        return self.parameter_pool.get(parameter_id).value

    def get_parameter_encoding(self, parameter_id):
        return self.parameter_pool.get(parameter_id).encoding


class ParameterManagementServiceController(ParameterManagementService):
    def add_parameters_from_file(self, filepath, node_id):
        with open(filepath, "r", encoding="utf-8") as f:
            x = json.load(f)
        list_of_dicts = x["parameters"]

        for y in list_of_dicts:
            y["parameter_id"] = (node_id, y["parameter_id"])

        for kwargs in list_of_dicts:
            self.add_parameter(Parameter(**kwargs))

    def process(self, service, subtype, data, node_id):
        case = (service, subtype)

        # parameter value report
        if case == (20, 2):
            try:
                n = int(data.pop(0))
                report = {}
                while data:
                    parameter_id = (node_id, int(data.pop(0)))
                    parameter = self.get_parameter(parameter_id)
                    size = parameter.get_encoded_size()
                    value = parameter.decode(data[:size])
                    data = data[size:]
                    report[parameter_id] = value
                if n != len(report):
                    raise ValueError
            except ValueError:
                return
            self.received_parameter_value_report(node_id, report)

    def send_report_parameter_values(self, node_id, parameter_ids):
        self.parent.send(
            Packet([20, 1] + [len(parameter_ids)] + parameter_ids), node_id
        )

    def received_parameter_value_report(self, node_id, report):
        # to be overwritten
        pass


class ParameterManagementServiceResponder(ParameterManagementService):
    def add_parameters_from_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            x = json.load(f)
        list_of_dicts = x["parameters"]

        for kwargs in list_of_dicts:
            self.add_parameter(Parameter(**kwargs))

    def process(self, service, subtype, data, node_id):
        case = (service, subtype)

        if case == (20, 1):
            parameter_ids = self._extract_parameter_ids(data)
            if parameter_ids is None:
                # send fail acceptance report
                self.parent.request_verification.send_fail_acceptance_report(
                    [service, subtype]
                )
                return

            # send success acceptance report
            self.parent.request_verification.send_success_acceptance_report(
                [service, subtype]
            )

            # reply with (20, 2)
            self.send_parameter_value_report(parameter_ids)

            # send success completion report
            self.parent.request_verification.send_success_completion_report(
                [service, subtype]
            )
        else:
            # send fail acceptance report
            self.parent.request_verification.send_fail_acceptance_report(
                [service, subtype]
            )

    def _extract_parameter_ids(self, data):
        try:
            n = data.pop(0)
            parameter_ids = list(data)
            if n != len(parameter_ids):
                raise ValueError
            for parameter_id in parameter_ids:
                if parameter_id not in self.parameter_pool:
                    raise ValueError
        except (IndexError, ValueError):
            return None
        return parameter_ids

    def send_parameter_value_report(self, parameter_ids):
        data = bytearray([len(parameter_ids)])
        for parameter_id in parameter_ids:
            parameter = self.get_parameter(parameter_id)
            data += bytes([parameter_id])
            data += parameter.encode()
        self.parent.send(Packet(bytes([20, 2]) + data))
