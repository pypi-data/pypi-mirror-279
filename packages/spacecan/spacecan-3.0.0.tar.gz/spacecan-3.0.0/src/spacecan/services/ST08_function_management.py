import struct
import json

from ..primitives.packet import Packet


class Argument:
    def __init__(self, argument_id, argument_name, encoding, **others):
        self.argument_id = argument_id
        self.argument_name = argument_name
        self.encoding = encoding

    def __repr__(self):
        string = (
            f"Argument({self.argument_id}, '{self.argument_name}', '{self.encoding}')"
        )
        return string

    def encode(self, value):
        encoding = (
            self.encoding if self.encoding.startswith("!") else "!" + self.encoding
        )
        return struct.pack(encoding, value)

    def decode(self, data):
        encoding = (
            self.encoding if self.encoding.startswith("!") else "!" + self.encoding
        )
        return struct.unpack(encoding, data)[0]

    def get_encoded_size(self):
        return struct.calcsize(self.encoding)


class Function:
    def __init__(self, function_id, function_name, arguments=None, **others):
        self.function_id = function_id
        self.function_name = function_name
        self.arguments = {}

        if arguments is not None:
            for kwargs in arguments:
                self.add_argument(Argument(**kwargs))

    def __repr__(self):
        string = (
            f"Function({self.function_id}, '{self.function_name}', '{self.arguments}')"
        )
        return string

    def add_argument(self, argument):
        self.arguments[argument.argument_id] = argument

    def get_argument(self, argument_id):
        return self.arguments.get(argument_id)


class FunctionManagementService:
    def __init__(self, parent):
        self.parent = parent
        self.function_pool = {}

    def get_function(self, function_id):
        return self.function_pool.get(function_id)

    def add_function(self, function):
        self.function_pool[function.function_id] = function


class FunctionManagementServiceController(FunctionManagementService):
    def add_functions_from_file(self, filepath, node_id):
        with open(filepath, "r", encoding="utf-8") as f:
            x = json.load(f)
        list_of_dicts = x["functions"]

        # prepend function_id with with node_id
        for y in list_of_dicts:
            y["function_id"] = (node_id, y["function_id"])

        for kwargs in list_of_dicts:
            self.add_function(Function(**kwargs))

    def send_perform_function(self, node_id, function_id, arguments=None):
        function = self.get_function((node_id, function_id))
        if function is None:
            raise ValueError("Requested function is not defined")

        if arguments is None:
            self.parent.send(Packet([8, 1] + [function_id]), node_id)
        else:
            data = bytearray([len(arguments)])
            for i, value in enumerate(arguments):
                argument_id = i + 1
                encoded = function.get_argument(argument_id).encode(value)
                data += bytes([argument_id]) + encoded
            self.parent.send(Packet(bytes([8, 1] + [function_id]) + data), node_id)


class FunctionManagementServiceResponder(FunctionManagementService):
    def add_functions_from_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            x = json.load(f)
        list_of_dicts = x["functions"]

        for kwargs in list_of_dicts:
            self.add_function(Function(**kwargs))

    def process(self, service, subtype, data, node_id):
        case = (service, subtype)

        # request: perform function
        if case == (8, 1):
            function_id = data.pop(0)
            function = self.get_function(function_id)

            if function is None:
                # send fail acceptance report
                self.parent.request_verification.send_fail_acceptance_report(
                    [service, subtype]
                )
                return

            if len(data) > 0:
                n = data.pop(0)

            arguments = []
            for _, argument in sorted(function.arguments.items()):
                size = argument.get_encoded_size()
                try:
                    argument_id = data.pop(0)
                except IndexError:
                    # send fail acceptance report
                    self.parent.request_verification.send_fail_acceptance_report(
                        [service, subtype]
                    )
                    return
                if argument_id != argument.argument_id:
                    # raise ValueError("Arguments order not correct")
                    # send fail acceptance report
                    self.parent.request_verification.send_fail_acceptance_report(
                        [service, subtype]
                    )
                    return
                encoded_value = data[:size]
                data = data[size:]
                value = argument.decode(encoded_value)
                arguments.append(value)

            if len(arguments) > 0 and n != len(arguments):
                # send fail acceptance report
                self.parent.request_verification.send_fail_acceptance_report(
                    [service, subtype]
                )
                return

            # send success acceptance report
            self.parent.request_verification.send_success_acceptance_report(
                [service, subtype]
            )

            if self.perform_function(function_id, arguments) is False:
                # send fail completion report
                self.parent.request_verification.send_fail_completion_report(
                    [service, subtype]
                )
            else:
                # send success completion report
                self.parent.request_verification.send_success_completion_report(
                    [service, subtype]
                )
        else:
            # send fail acceptance report
            self.parent.request_verification.send_fail_acceptance_report(
                [service, subtype]
            )

    def perform_function(self, function_id, arguments):
        # to be overwritten
        return True
