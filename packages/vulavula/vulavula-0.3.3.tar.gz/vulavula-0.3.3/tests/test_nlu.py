import unittest
from unittest.mock import MagicMock

from vulavula.client.nlu import NLU


class TestNLU(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://api.example.com"
        self.client_token = "fake-client-token"
        self.session = MagicMock()
        self.nlu = NLU(self.client_token, session=self.session)
        self.nlu._handle_response = MagicMock()
        self.nlu.base_url = self.base_url

    def test_get_entities(self):
        mock_output = [
            {
                "entity": "person",
                "word": "Ramaphosa",
                "start": 10,
                "end": 19
            },
            {
                "entity": "location",
                "word": "Emfuleni Municipality",
                "start": 33,
                "end": 54
            }
        ]

        self.session.post.return_value = MagicMock(status_code=200,
                                                   json=lambda: mock_output)

        # Data for entity recognition
        get_entities_data = {"encoded_text": "President Ramaphosa gaan loop by Emfuleni Municipality"}

        # Return json
        self.nlu._handle_response = lambda x: x.json()

        # Call get entities method test
        result = self.nlu.get_entities(get_entities_data)

        expected_url = f"{self.base_url}/entity_recognition/process"

        # Assertions
        self.session.post.assert_called_once_with(expected_url, headers=self.nlu.headers, json=get_entities_data)
        self.assertEqual(result, mock_output)

    def test_classify(self):
        mock_output = [
            {
                "probabilities": [
                    {
                        "intent": "goodbye",
                        "score": 0.25613666
                    },
                    {
                        "intent": "greeting",
                        "score": 0.74386334
                    }
                ]
            },
            {
                "probabilities": [
                    {
                        "intent": "goodbye",
                        "score": 0.6334656
                    },
                    {
                        "intent": "greeting",
                        "score": 0.36653438
                    }
                ]
            }
        ]
        self.session.post.return_value = MagicMock(status_code=200, json=lambda: mock_output)

        # Data for entity recognition
        classify_data = {
            "examples": [
                {"intent": "greeting", "example": "Hello!"},
                {"intent": "greeting", "example": "Hi there!"},
                {"intent": "goodbye", "example": "Goodbye!"},
                {"intent": "goodbye", "example": "See you later!"}
            ],
            "inputs": [
                "Hey, how are you?",
                "I must be going now."
            ]
        }

        # Return json
        self.nlu._handle_response = lambda x: x.json()

        # Call get entities method test
        result = self.nlu.classify(classify_data)

        expected_url = f"{self.base_url}/classify"

        # Assertions
        self.session.post.assert_called_once_with(expected_url, headers=self.nlu.headers, json=classify_data)
        self.assertEqual(result, mock_output)
