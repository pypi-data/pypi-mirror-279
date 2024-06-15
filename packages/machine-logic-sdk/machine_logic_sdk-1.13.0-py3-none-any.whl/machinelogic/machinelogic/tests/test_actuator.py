# pylint: disable=missing-function-docstring
import unittest
from unittest.mock import MagicMock

from machinelogic.machinelogic.actuator import Actuator


class TestActuator(unittest.TestCase):
    def test_given_uuid_and_timeout_when_wait_for_move_completion_then_calls_api_with_uuid_and_timeout(
        self,
    ) -> None:
        # Arrange
        api_mock = MagicMock()
        wait_for_motion_completion_spy = MagicMock()
        api_mock.wait_for_motion_completion = wait_for_motion_completion_spy

        uuid = "actuator_uuid"
        config_mock = MagicMock()
        config_mock.uuid = uuid

        actuator = Actuator(config_mock, api_mock)

        # Act
        timeout = 10
        actuator.wait_for_move_completion(timeout)

        # Assert
        wait_for_motion_completion_spy.assert_called_once_with(uuid, timeout=timeout)

    def test_given_uuid_and_speed_when_set_speed_then_calls_api_with_uuid_and_speed(
        self,
    ) -> None:
        # Arrange
        api_mock = MagicMock()
        set_speed_spy = MagicMock()
        api_mock.set_speed = set_speed_spy

        uuid = "actuator_uuid"
        config_mock = MagicMock()
        config_mock.uuid = uuid

        actuator = Actuator(config_mock, api_mock)

        # Act
        speed = 100
        actuator.set_speed(speed)

        # Assert
        set_speed_spy.assert_called_once_with(uuid, speed)

    def test_given_uuid_and_acceleration_when_set_acceleration_then_calls_api_with_uuid_and_acceleration(
        self,
    ) -> None:
        # Arrange
        api_mock = MagicMock()
        set_acceleration_spy = MagicMock()
        api_mock.set_acceleration = set_acceleration_spy

        uuid = "actuator_uuid"
        config_mock = MagicMock()
        config_mock.uuid = uuid

        actuator = Actuator(config_mock, api_mock)

        # Act
        acceleration = 100
        actuator.set_acceleration(acceleration)

        # Assert
        set_acceleration_spy.assert_called_once_with(uuid, acceleration)

    def test_given_uuid_and_distance_when_move_relative_then_calls_api_with_uuid_and_distance_and_wait_for_motion_completion_true_and_timeout_default_timeout(
        self,
    ) -> None:
        # Arrange
        api_mock = MagicMock()
        move_relative_spy = MagicMock()
        api_mock.move_relative = move_relative_spy

        uuid = "actuator_uuid"
        config_mock = MagicMock()
        config_mock.uuid = uuid

        actuator = Actuator(config_mock, api_mock)

        # Act
        distance = 100
        [default_timeout] = actuator.move_relative.__defaults__  # type: ignore

        actuator.move_relative(distance)

        # Assert
        move_relative_spy.assert_called_once_with(uuid, distance, True, default_timeout)

    def test_given_uuid_and_distance_when_move_relative_async_then_calls_api_with_uuid_and_distance_and_wait_for_motion_completion_false(
        self,
    ) -> None:
        # Arrange
        api_mock = MagicMock()
        api_mock.move_relative = MagicMock()

        uuid = "actuator_uuid"
        config_mock = MagicMock()
        config_mock.uuid = uuid

        actuator = Actuator(config_mock, api_mock)

        # Act
        distance = 100
        actuator.move_relative_async(distance)

        # Assert
        api_mock.move_relative.assert_called_once_with(uuid, distance, False)

    def test_given_uuid_and_timeout_when_home_then_calls_api_with_uuid_and_timeout_and_wait_for_motion_completion_true(
        self,
    ) -> None:
        # Arrange
        api_mock = MagicMock()
        api_mock.home = MagicMock()

        uuid = "actuator_uuid"
        config_mock = MagicMock()
        config_mock.uuid = uuid

        actuator = Actuator(config_mock, api_mock)

        # Act
        timeout = 10
        actuator.home(timeout)

        # Assert
        api_mock.home.assert_called_once_with(uuid, True, timeout)

    def test_given_uuid_when_lock_breaks_then_calls_api_with_uuid(
        self,
    ) -> None:
        # Arrange
        api_mock = MagicMock()
        api_mock.lock_brakes = MagicMock()

        uuid = "actuator_uuid"
        config_mock = MagicMock()
        config_mock.uuid = uuid

        actuator = Actuator(config_mock, api_mock)

        # Act
        actuator.lock_brakes()

        # Assert
        api_mock.lock_brakes.assert_called_once_with(uuid)

    def test_given_uuid_when_unlock_breaks_then_calls_api_with_uuid(
        self,
    ) -> None:
        # Arrange
        api_mock = MagicMock()
        api_mock.unlock_brakes = MagicMock()

        uuid = "actuator_uuid"
        config_mock = MagicMock()
        config_mock.uuid = uuid

        actuator = Actuator(config_mock, api_mock)

        # Act
        actuator.unlock_brakes()

        # Assert
        api_mock.unlock_brakes.assert_called_once_with(uuid)

    def test_given_uuid_when_stop_then_calls_api_with_uuid(
        self,
    ) -> None:
        # Arrange
        api_mock = MagicMock()
        api_mock.stop_motion = MagicMock()

        uuid = "actuator_uuid"
        config_mock = MagicMock()
        config_mock.uuid = uuid

        actuator = Actuator(config_mock, api_mock)

        # Act
        actuator.stop()

        # Assert
        api_mock.stop_motion.assert_called_once_with(uuid)


if __name__ == "__main__":
    unittest.main()
