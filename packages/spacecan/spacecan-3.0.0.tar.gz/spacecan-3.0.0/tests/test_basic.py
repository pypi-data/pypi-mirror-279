import os
import spacecan


def test_controller():
    controller = spacecan.Controller.from_file(
        os.path.join(os.path.dirname(__file__), "config/controller.json")
    )
    assert controller


def test_responder():
    responder = spacecan.Responder.from_file(
        os.path.join(os.path.dirname(__file__), "config/responder1.json")
    )
    assert responder
