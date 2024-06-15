# pylint: disable=missing-function-docstring
import unittest
from unittest.mock import MagicMock

from machinelogic.machinelogic.bag_gripper import BagGripper


class TestBagGripper(unittest.TestCase):
    def test_given_uuid_when_close_then_calls_api_with_uuid_and_wait_on_motion_completion_true(
        self,
    ) -> None:
        # Arrange
        api_mock = MagicMock()
        mqtt_mock = MagicMock()
        api_mock.close_bag_gripper = MagicMock()

        uuid = "bag_gripper_uuid"
        config_mock = MagicMock()
        config_mock.uuid = uuid

        bag_gripper = BagGripper(config_mock, api_mock, mqtt_mock)

        # Act
        bag_gripper.close_async()

        # Assert
        api_mock.close_bag_gripper.assert_called_once_with(uuid)

    def test_given_uuid_when_open_then_calls_api_with_uuid_and_wait_on_motion_completion_true(
        self,
    ) -> None:
        # Arrange
        api_mock = MagicMock()
        mqtt_mock = MagicMock()
        api_mock.open_bag_gripper = MagicMock()

        uuid = "bag_gripper_uuid"
        config_mock = MagicMock()
        config_mock.uuid = uuid

        bag_gripper = BagGripper(config_mock, api_mock, mqtt_mock)

        # Act
        bag_gripper.open_async()

        # Assert
        api_mock.open_bag_gripper.assert_called_once_with(uuid)
