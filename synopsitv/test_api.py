import unittest
from api import SynopsiTvApi

from mock import Mock, patch


class SynopsiTvTestCase(unittest.TestCase):
    def setUp(self):
        self.api = SynopsiTvApi(token="fake-token")

    def test_identify_name(self):
        with patch('api.requests') as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                '_generated_in': '0:00:00.018855',
                'id': 2208230,
                'name': '2 Broke Girls',
                'relevant_results': [
                    {'id': 2208230, 'name': '2 Broke Girls'}
                ]
            }

            result = self.api.identify_title('2 Broke Girls')

            self.assertEqual(result['name'], '2 Broke Girls')
            self.assertEqual(result['id'], 2208230)

    def test_identify_episode(self):
        with patch('api.requests') as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "seasons": [
                    {
                        "episodes": [
                            {
                                "episode_number": "01",
                                "season_number": "01",
                                "name": "Pilot",
                                "id": 3092812
                            },
                            {
                                "episode_number": "24",
                                "season_number": "01",
                                "name": "And Martha Stewart Have A Ball (2)",
                                "id": 3521164
                            }
                        ],
                        "id": 3092811
                    },
                    {
                        "episodes": [
                            {
                                "episode_number": "12",
                                "season_number": "02",
                                "name": "And the High Holidays",
                                "id": 3538089
                            },
                            {
                                "episode_number": "13",
                                "season_number": "02",
                                "name": "And the Bear Truth",
                                "id": 3539966
                            }
                        ],
                        "id": 3523480
                    },
                ],
                "id": 2208230,
                "_generated_in": "0:00:00.043344",
                "name": "2 Broke Girls"
            }

            result = self.api.episode(2208230, '02', '12')

            self.assertEqual(result['name'], 'And the High Holidays')
            self.assertEqual(result['id'], 3538089)

    def test_check_in(self):
        with patch('api.requests') as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "status": "created",
                "_generated_in": "0:00:00.272651",
                "id": 1952771
            }

            result = self.api.check_in(3567204)

            self.assertEqual(result['status'], 'created')


if __name__ == '__main__':
    unittest.main()