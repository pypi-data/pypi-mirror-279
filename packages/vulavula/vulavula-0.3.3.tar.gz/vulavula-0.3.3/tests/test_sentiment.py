import unittest
from unittest.mock import MagicMock, patch

from vulavula.client.sentiment import Sentiment


class TestTranscribe(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://api.example.com"
        self.client_token = "fake-client-token"
        self.session = MagicMock()
        self.sentiment = Sentiment(self.client_token, session=self.session)
        self.sentiment._handle_response = MagicMock()
        self.sentiment.base_url = self.base_url

    def test_get_sentiments(self):
        mock_output = {"id": 10,
                       "sentiments": [
                           {
                               "text": "I love sunny days",
                               "sentiment": [
                                   {
                                       "label": "positive",
                                       "score": 0.9991829991340637
                                   }
                               ]
                           },
                           {
                               "text": " I hate rain",
                               "sentiment": [
                                   {
                                       "label": "negative",
                                       "score": 0.960746169090271
                                   }
                               ]
                           },
                       ]}
        self.session.post.return_value = MagicMock(status_code=200,
                                                   json=lambda: mock_output)

        # Data for sentiment analysis
        sentiment_data = {"encoded_text": "I love sunny days, but I hate rain."}

        # Assuming _handle_response just returns the json
        self.sentiment._handle_response = lambda x: x.json()

        # Call the method under test
        result = self.sentiment.get_sentiments(sentiment_data)

        expected_url = f"{self.base_url}/sentiment_analysis/process"

        # Assertions
        self.session.post.assert_called_once_with(expected_url, headers=self.sentiment.headers, json=sentiment_data)
        self.assertEqual(result, mock_output)
