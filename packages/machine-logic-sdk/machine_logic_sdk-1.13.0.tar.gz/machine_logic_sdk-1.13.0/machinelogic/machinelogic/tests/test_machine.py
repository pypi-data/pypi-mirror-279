import unittest
from unittest.mock import MagicMock, patch


class TestMachine(unittest.TestCase):
    @patch("machinelogic.machinelogic.machine.Machine")
    def test_given_input_when_get_input_then_gets_correct_input(  # pylint: disable=missing-function-docstring
        self, mock_machine: MagicMock
    ) -> None:
        # Arrange
        machine = mock_machine.return_value
        machine_motion_mock = MagicMock()
        input_mock = MagicMock()
        config_mock = MagicMock()

        input_mock.configuration = config_mock
        input_mock.configuration.uuid = "uuid"

        machine.list_machine_motions.return_value = [machine_motion_mock]
        machine._get_input_by_uuid.return_value = (  # pylint: disable=protected-access
            input_mock
        )

        # Act
        found_input = machine._get_input_by_uuid(  # pylint: disable=protected-access
            "uuid"
        )

        # Assert
        self.assertEqual(found_input, input_mock)


if __name__ == "__main__":
    unittest.main()
