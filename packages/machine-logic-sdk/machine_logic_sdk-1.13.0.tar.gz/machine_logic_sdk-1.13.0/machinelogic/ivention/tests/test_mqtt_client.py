# pylint: disable=missing-function-docstring

import unittest
from unittest.mock import MagicMock, patch

from machinelogic.ivention.mqtt_client import MqttClient


class TestMqttClient(unittest.TestCase):
    def create_mqtt_client(
        self, connection_string: str = "mqtt connection string"
    ) -> MqttClient:
        mqtt_client = MqttClient(connection_string)
        self.addCleanup(mqtt_client.dispose)

        return mqtt_client

    @patch("paho.mqtt.client.Client")
    def test_given_client_and_topic_and_callback_when_subscribe_called_then_client_subscribe_called_with_topic(
        self, mock_client: MagicMock
    ) -> None:
        # Arrange
        client = self.create_mqtt_client()
        topic = "test/topic"
        callback = MagicMock()

        # Act
        client.internal_subscribe(topic, callback)

        # Assert
        mock_client().subscribe.assert_called_with(topic)

    @patch("paho.mqtt.client.Client")
    def test_given_client_and_topic_and_message_when_publish_called_then_client_publish_called_with_topic_and_message(
        self, mock_client: MagicMock
    ) -> None:
        # Arrange
        client = self.create_mqtt_client()
        topic = "test/topic"
        message = "message"

        # Act
        client.publish(topic, message)

        # Assert
        mock_client().publish.assert_called_with(topic, message)

    @patch("paho.mqtt.client.Client")
    def test_given_client_and_single_handle_on_topic_when_unsubscribe_then_client_unsubscribe_called_with_topic(
        self, mock_client: MagicMock
    ) -> None:
        # Arrange
        client = MqttClient("mqtt connection string")
        topic = "test/topic"
        callback = MagicMock()
        handle = client.internal_subscribe(topic, callback)

        # Act
        client.unsubscribe(handle)

        # Assert
        mock_client().unsubscribe.assert_called_with(topic)

        client.dispose()

    @patch("paho.mqtt.client.Client")
    def test_given_client_and_multiple_handles_on_topic_when_unsubscribe_then_client_unsubscribe_not_called(
        self, mock_client: MagicMock
    ) -> None:
        # Arrange
        client = MqttClient("mqtt connection string")
        topic = "test/topic"
        callback = MagicMock()
        handle = client.internal_subscribe(topic, callback)
        client.internal_subscribe(topic, callback)

        # Act
        client.unsubscribe(handle)

        # Assert
        mock_client().unsubscribe.assert_not_called()

        client.dispose()


if __name__ == "__main__":
    unittest.main()
