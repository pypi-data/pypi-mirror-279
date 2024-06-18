from typing import Optional


def assert_dataset_message(message: dict, expected: dict):
    expected["dataset"]["startDate"] = message["dataset"]["startDate"]
    expected["dataset"]["endDate"] = message["dataset"]["endDate"]
    expected["dataset"]["parameter"].append(_get_parameter(message, "startDate"))
    expected["dataset"]["parameter"].append(_get_parameter(message, "endDate"))
    expected["dataset"]["parameter"] = sorted(
        expected["dataset"]["parameter"], key=lambda adict: adict["name"]
    )
    message["dataset"]["parameter"] = sorted(
        message["dataset"]["parameter"], key=lambda adict: adict["name"]
    )
    assert message == expected


def assert_investigation_message(message: dict, expected: dict):
    expected["investigation"]["startDate"] = message["investigation"]["startDate"]
    assert message == expected


def _get_parameter(root: dict, parameter_name: str) -> Optional[dict]:
    for parameter in root["dataset"]["parameter"]:
        if parameter["name"] == parameter_name:
            return parameter
