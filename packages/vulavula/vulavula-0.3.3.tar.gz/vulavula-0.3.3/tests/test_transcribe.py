import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from vulavula.client.transcribe import Transcribe


class TestTranscribe(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://api.example.com"
        self.client_token = "fake-client-token"
        self.session = MagicMock()

        # Patch the Config.BASE_URL here
        self.config_patch = patch('vulavula.config.settings.BASE_URL', new=self.base_url)
        self.mock_config = self.config_patch.start()

        self.transcribe = Transcribe(self.client_token, session=self.session)
        self.file_path = "./audio/test1.mp3"
        self.transcribe._handle_response = MagicMock()

    def tearDown(self):
        # Stop the patcher
        self.config_patch.stop()

    @patch('vulavula.client.transcribe.Transport')
    def test_transcribe(self, mock_transport):
        # Mocking the transport class and its upload_file method
        fixed_uuid = uuid4()
        mock_transport_instance = mock_transport.return_value
        mock_upload_response = {'upload_id': str(fixed_uuid)}
        mock_transport_instance.upload_file.return_value = mock_upload_response

        # Instantiate Transcribe after setting up the mock
        self.transcribe = Transcribe(self.client_token, self.session)

        # Mock successful transcription process
        self.transcribe.transcribe_process = MagicMock(return_value={'status': 'success'})

        # Executing the transcribe method
        webhook = "http://example.com/webhook/"
        upload_id, result = self.transcribe.transcribe(self.file_path, webhook)

        # Assertions
        mock_transport_instance.upload_file.assert_called_once_with(self.file_path)
        self.transcribe.transcribe_process.assert_called_once_with(str(fixed_uuid), webhook)
        self.assertEqual(result, {'status': 'success'})
        self.assertEqual(upload_id, str(fixed_uuid))

    def test_transcribe_process(self):
        upload_id = uuid4()
        webhook = "http://example.com/webhook/"
        self.session.post.return_value = MagicMock(status_code=200, json=lambda: {"result": "processed"})

        # Assuming _handle_response just returns the json
        self.transcribe._handle_response = lambda x: x.json()

        result = self.transcribe.transcribe_process(upload_id, webhook)
        self.session.post.assert_called_once_with(
            f"{self.base_url}/transcribe/process/{upload_id}",
            headers=self.transcribe.headers,
            json={'webhook': webhook}
        )
        self.assertEqual(result, {"result": "processed"})

    def test_get_transcribed_text(self):
        self.session.post.return_value = MagicMock(status_code=200,
                                                   json=lambda: {"message": "success",
                                                                 "text": "This is a transcribed text."})

        # Assuming _handle_response just returns the json
        self.transcribe._handle_response = lambda x: x.json()

        # ids and UUID for testing
        test_upload_id = uuid4()
        customer_id = 1
        project_id = 1

        # Call the method under test
        result = self.transcribe.get_transcribed_text(test_upload_id)

        # Assertions
        self.session.post.assert_called_once_with(
            f"{self.base_url}/transcribe/{test_upload_id}/get",
            headers=self.transcribe.headers)
