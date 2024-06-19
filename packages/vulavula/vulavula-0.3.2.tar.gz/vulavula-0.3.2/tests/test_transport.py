import unittest
from unittest.mock import MagicMock, patch

from vulavula.client.transport import Transport


class TestTransport(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://api.example.com"
        self.client_token = "fake-client-token"
        self.session = MagicMock()
        self.transport = Transport(self.client_token, session=self.session)
        self.transport._handle_response = MagicMock()
        self.transport.base_url = self.base_url

    @patch('vulavula.client.transport.os.path.getsize')
    @patch('vulavula.client.transport.open', new_callable=unittest.mock.mock_open, read_data='file content')
    @patch('vulavula.client.transport.base64.b64encode')
    @patch('vulavula.client.transport.uuid.uuid4', return_value='1234-uuid')
    def test_upload_file(self, mock_uuid, mock_b64encode, mock_open, mock_getsize):
        # Setup mocks
        mock_getsize.return_value = 1024
        mock_b64encode.return_value = b'encoded_file_content'
        mock_response = MagicMock()
        mock_response.json.return_value = {'upload_id': '12345'}
        self.session.post.return_value = mock_response

        # Return Json
        self.transport._handle_response = MagicMock(return_value=mock_response.json.return_value)

        file_path = "./audio/test1.mp3"

        # Call upload file method
        result = self.transport.upload_file(file_path)

        # Assertions
        self.session.post.assert_called_once_with(
            f"{self.base_url}/transport/file-upload",
            headers=self.transport.headers,
            json={
                "file_name": "1234-uuid.mp3",
                "audio_blob": 'encoded_file_content',
                "file_size": 1024,
            }
        )
        self.assertEqual(result, {'upload_id': '12345'})
        self.transport._handle_response.assert_called_once_with(mock_response)
